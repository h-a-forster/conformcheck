"""Checkpointed, resumable, parallel execution of a study (docs/DESIGN.md, section 7.3).

* ``<out>/run.json`` holds the configuration fingerprint, seeds, platform and the
  versions of Python, numpy, scipy, scikit-learn and every library under test; resuming
  with a different fingerprint is refused unless ``force=True``.
* Units run in a ``ProcessPoolExecutor`` with at most 4 workers; BLAS/OpenMP threads
  are pinned to 1 and torch uses one thread.
* The parent process is the only writer: each finished unit is appended as one JSON
  line to ``units.jsonl`` (flushed and fsynced); a rerun skips unit ids already present.
  Each record stores the versions it depends on (:func:`unit_versions`). A record made
  under different versions is never reused: after an upgrade (``force=True``) its unit
  is run again, and the newer record replaces it.
* Progress (done/total, rate, ETA) is appended to ``progress.log`` after every unit.
* Units whose library is not installed are never checkpointed. By default the run is
  refused (:class:`MissingLibraries`); with ``allow_missing=True`` they are left out of
  the run, listed in ``run.json`` and in the report, and run later once installed.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import math
import os
import platform
import sys
import time
from collections import Counter
from collections.abc import Callable, Iterable
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from conformcheck import diagnostics, laws
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    RegressionInput,
)
from conformcheck.data import get_dgp, library_seed, rep_seed_sequence
from conformcheck.study import Study, Unit, cell_law, enumerate_units, fingerprint

MAX_WORKERS = 4
# Set methods whose sets are thresholds of the LAC score 1 - p_y (bracketing applies).
BRACKET_METHODS = ("lac", "class_conditional")
THREAD_ENV = ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS")

# Deterministic library methods and the reference they are compared with (information
# only: conventions may differ, the laws decide).
REFERENCE_FOR: dict[tuple[str, str], str] = {
    ("split_abs", "*"): "reference/split_abs/default",
    ("cqr", "symmetric"): "reference/cqr/symmetric",
    ("cqr", "default"): "reference/cqr/symmetric",
    ("cqr", "asymmetric"): "reference/cqr/asymmetric",
    ("lac", "default"): "reference/lac/default",
    ("lac", "unsmoothed"): "reference/lac/default",
    ("aps", "rand=False"): "reference/aps/deterministic",
    ("aps", "randomized=False"): "reference/aps/deterministic",
    ("raps", "rand=False"): "reference/raps/deterministic",
    ("raps", "randomized=False"): "reference/raps/deterministic",
    ("class_conditional", "default"): "reference/class_conditional/default",
    ("class_conditional", "unsmoothed"): "reference/class_conditional/default",
}


def reference_key(library: str, method: str, variant: str) -> str | None:
    if library == "reference":
        return None
    return REFERENCE_FOR.get((method, variant)) or REFERENCE_FOR.get((method, "*"))


def versions() -> dict[str, str | None]:
    import importlib.metadata as md

    out: dict[str, str | None] = {"python": platform.python_version()}
    for dist in (
        "conformcheck",
        "numpy",
        "scipy",
        "scikit-learn",
        "mapie",
        "crepes",
        "puncc",
        "torchcp",
        "torch",
    ):
        try:
            out[dist] = md.version(dist)
        except md.PackageNotFoundError:
            out[dist] = None
    return out


CORE_DISTS = ("python", "numpy", "scipy", "scikit-learn")
LIBRARY_DISTS: dict[str, tuple[str, ...]] = {
    "mapie": ("mapie",),
    "crepes": ("crepes",),
    "puncc": ("puncc",),
    "torchcp": ("torchcp", "torch"),
    "reference": (),
}


def unit_versions(vers: dict[str, str | None], library: str) -> dict[str, str | None]:
    """The versions a unit's result depends on: Python, the numeric stack and its library."""
    return {d: vers.get(d) for d in (*CORE_DISTS, *LIBRARY_DISTS.get(library, (library,)))}


def record_versions(
    rec: dict[str, Any], fallback: dict[str, str | None] | None
) -> dict[str, str | None] | None:
    """Versions a record was computed under.

    Records written before versions were stored per record carry none; they were
    computed under the versions in the ``run.json`` they were written with (``fallback``).
    """
    v = rec.get("versions")
    if v is not None:
        return dict(v)
    if fallback is None:
        return None
    return unit_versions(fallback, str(rec.get("library", "")))


# --- one unit ---------------------------------------------------------------------------


def _limit_threads() -> None:
    for var in THREAD_ENV:
        os.environ[var] = "1"
    if "torch" in sys.modules:
        sys.modules["torch"].set_num_threads(1)


def _oracle_scores(dgp_name: str, method: str, draw: Any, model: Any, qmodels: Any) -> np.ndarray:
    """True-label scores of calibration and test points (used to detect ties)."""
    x = np.concatenate([draw.x_cal, draw.x_test])
    y = np.concatenate([draw.y_cal, draw.y_test])
    if get_dgp(dgp_name).task == "classification":
        p = model.predict_proba(x)
        return 1.0 - p[np.arange(len(y)), y.astype(int)]
    if method == "cqr" and qmodels is not None:
        return np.maximum(qmodels[0].predict(x) - y, y - qmodels[1].predict(x))
    return np.abs(y - model.predict(x))


def evaluate_unit(unit_key: dict[str, Any], study_cfg: dict[str, Any]) -> dict[str, Any]:
    """Run every repetition of one unit and return its JSON record (picklable in and out)."""
    _limit_threads()
    from conformcheck.adapters import registry

    reg = registry()
    adapter = reg[unit_key["adapter"]]
    spec = adapter.spec
    dgp = get_dgp(unit_key["dgp"])
    n = int(unit_key["n"])
    reps = int(study_cfg["reps"])
    m_req = int(study_cfg["test_points"])
    seed = int(study_cfg["seed"])
    per_class = bool(unit_key["per_class"])
    alphas = [Fraction(a) for a in unit_key["alphas"]]
    m = dgp.test_size(n, m_req, per_class)
    record: dict[str, Any] = {
        **unit_key,
        "library": spec.library,
        "method": spec.method,
        "variant": spec.variant,
        "task": spec.task,
        "m": m,
        "reps": reps,
        "seed": seed,
    }
    if not adapter.available():  # run_study filters these out; never checkpointed
        record.update(status="unavailable", alphas_out={})
        return record

    ref_key = reference_key(spec.library, spec.method, spec.variant)
    ref_adapter = reg.get(ref_key) if ref_key else None
    model = dgp.model()
    qmodels = dgp.quantile_models() if spec.method == "cqr" else None
    laws_by_alpha = {
        a: cell_law(
            method=spec.method,
            variant=spec.variant,
            library=spec.library,
            dgp=dgp.name,
            n=n,
            alpha=a,
            m=m,
            n_folds=unit_key.get("n_folds"),
        )
        for a in alphas
    }

    acc: dict[Fraction, dict[str, Any]] = {
        a: {
            "counts": [],
            "status": Counter(),
            "message": "",
            "error_seen": False,
            "warnings": [],
            "nontrivial": 0,
            "rank_offsets": Counter(),
            "rank_pairs": Counter(),
            "rank_interp": 0,
            "rank_spread": 0.0,
            "bracket_offsets": Counter(),
            "effective_n": Counter(),
            "diff_max": None,
            "ties_reps": 0,
        }
        for a in alphas
    }
    t0 = time.perf_counter()
    for rep in range(reps):
        ss = rep_seed_sequence(seed, dgp.name, n, rep)
        rng = np.random.default_rng(ss)
        lseed = library_seed(ss)
        draw = dgp.draw(rng, n, m_req, per_class)
        inp: RegressionInput | CrossRegressionInput | ClassificationInput
        pred_cal = pred_test = None
        q_cal = q_test = None
        proba_test = None
        if spec.task == "regression":
            inp = RegressionInput(
                draw.x_cal, draw.y_cal, draw.x_test, alphas, model, qmodels, seed=lseed
            )
            pred_cal, pred_test = model.predict(draw.x_cal), model.predict(draw.x_test)
            if qmodels is not None:
                q_cal = (qmodels[0].predict(draw.x_cal), qmodels[1].predict(draw.x_cal))
                q_test = (qmodels[0].predict(draw.x_test), qmodels[1].predict(draw.x_test))
        elif spec.task == "cross_regression":
            inp = CrossRegressionInput(
                draw.x_cal,
                draw.y_cal,
                draw.x_test,
                alphas,
                dgp.estimator_factory,
                unit_key.get("n_folds"),
                seed=lseed,
            )
            if dgp.name == "reg_constant":
                pred_cal, pred_test = np.zeros(n), np.zeros(len(draw.y_test))
        else:
            proba_cal = model.predict_proba(draw.x_cal)
            proba_test = model.predict_proba(draw.x_test)
            inp = ClassificationInput(
                draw.x_cal,
                draw.y_cal,
                draw.x_test,
                alphas,
                model,
                proba_cal,
                proba_test,
                dgp.n_classes,
                seed=lseed,
                per_class=per_class,
            )
        try:
            outs = adapter.run(inp)
        except Exception as exc:  # noqa: BLE001 - recorded, never swallowed silently
            msg = f"{type(exc).__name__}: {exc}"[:500]
            outs = {a: AlphaOutput(status="error", message=msg) for a in alphas}
        ref_outs = ref_adapter.run(inp) if ref_adapter is not None else None
        ties = False
        if dgp.pool_size is not None:
            sc = _oracle_scores(dgp.name, spec.method, draw, model, qmodels)
            ties = np.unique(sc).size < sc.size
        for a in alphas:
            o = outs.get(a) or AlphaOutput(status="error", message="no output for alpha")
            st = acc[a]
            st["status"][o.status] += 1
            for w in o.warnings:
                if w not in st["warnings"] and len(st["warnings"]) < 3:
                    st["warnings"].append(w)
            if o.status != "ok":
                # keep the first error message; a refusal message only if nothing else
                if o.status == "error" and not st["error_seen"]:
                    st["message"], st["error_seen"] = o.message, True
                elif not st["message"]:
                    st["message"] = o.message
                continue
            st["ties_reps"] += int(ties)
            cl = laws_by_alpha[a]
            if o.intervals is not None:
                iv = np.asarray(o.intervals, dtype=float)
                covered = (iv[:, 0] <= draw.y_test) & (draw.y_test <= iv[:, 1])
                trivial = diagnostics.is_trivial(iv, None)
            else:
                sets = np.asarray(o.sets, dtype=bool)
                covered = sets[np.arange(len(draw.y_test)), np.asarray(draw.y_test, dtype=int)]
                trivial = diagnostics.is_trivial(None, sets)
            st["counts"].append(int(covered.sum()))
            if cl.kind == "trivial" and not trivial:
                st["nontrivial"] += 1
            # rank recovery (regression)
            if o.intervals is not None and cl.k is not None:
                ranks = diagnostics.regression_ranks(
                    spec.method,
                    spec.variant,
                    o.intervals,
                    draw.y_cal,
                    pred_cal,
                    pred_test,
                    q_cal,
                    q_test,
                )
                if ranks:
                    worst = max(ranks, key=lambda r: abs(r.offset(cl.k)))  # type: ignore[arg-type]
                    st["rank_offsets"][str(worst.offset(cl.k))] += 1  # type: ignore[arg-type]
                    pair = "|".join(f"{r.offset(cl.k):g}" for r in ranks)  # type: ignore[arg-type]
                    st["rank_pairs"][pair] += 1
                    st["rank_interp"] += int(any(r.interpolated for r in ranks))
                    spread = max(r.spread for r in ranks)
                    if math.isfinite(spread):
                        st["rank_spread"] = max(st["rank_spread"], spread)
            # bracketing: rank recovery for LAC-type set methods with deterministic sets
            if (
                o.sets is not None
                and spec.method in BRACKET_METHODS
                and spec.variant != "smoothed"
                and cl.kind == "exact"
                and proba_test is not None
            ):
                off = _bracket(spec.method, inp, draw, proba_test, o.sets, a)  # type: ignore[arg-type]
                if off is not None:
                    st["bracket_offsets"][off] += 1
            if o.effective_n is not None:
                st["effective_n"][str(o.effective_n)] += 1
            # differential check against the reference implementation
            if ref_outs is not None and ref_outs.get(a) is not None and ref_outs[a].status == "ok":
                r = ref_outs[a]
                if o.intervals is not None:
                    d = diagnostics.compare_to_reference(o.intervals, r.intervals, "intervals")
                else:
                    d = diagnostics.compare_to_reference(o.sets, r.sets, "sets")
                if d is not None:
                    st["diff_max"] = d if st["diff_max"] is None else max(st["diff_max"], d)
    record["elapsed_s"] = round(time.perf_counter() - t0, 3)
    out_alphas: dict[str, Any] = {}
    for a in alphas:
        st = acc[a]
        cl = laws_by_alpha[a]
        out_alphas[f"{a.numerator}/{a.denominator}"] = {
            "k": laws.split_index(n, a),
            "law_kind": cl.kind,
            "counts": st["counts"],
            "n_ok": st["status"]["ok"],
            "n_refused": st["status"]["refused"],
            "n_error": st["status"]["error"],
            "message": st["message"],
            "warnings": st["warnings"],
            "nontrivial": st["nontrivial"],
            "rank_offsets": dict(st["rank_offsets"]),
            "rank_pairs": dict(st["rank_pairs"]),  # "lower|upper" endpoint offsets
            "rank_interp": st["rank_interp"],
            "rank_spread": st["rank_spread"],
            "bracket_offsets": dict(st["bracket_offsets"]),  # "nt": not a threshold set
            "effective_n": dict(st["effective_n"]),  # calibration size the library used
            "diff_max": st["diff_max"],
            "ties_reps": st["ties_reps"],
        }
    record["status"] = "done"
    record["alphas_out"] = out_alphas
    return record


def _bracket(
    method: str,
    inp: ClassificationInput,
    draw: Any,
    proba_test: np.ndarray,
    sets: np.ndarray,
    alpha: Fraction,
) -> str | None:
    """Bracket offset of one repetition as a string key (``"nt"``: not a threshold set).

    LAC: one bracket over every label of every test point, against the order statistic
    ``k`` of all ``n`` calibration scores ``1 - p_y``. Mondrian (class-conditional) LAC:
    one bracket per class against that class's own calibration scores and ``k_y``; the
    offset with the largest magnitude is kept.
    """
    sets = np.asarray(sets, dtype=bool)
    y_cal = np.asarray(draw.y_cal, dtype=int)
    p_cal = inp.proba_cal
    cal_scores = 1.0 - p_cal[np.arange(y_cal.size), y_cal]
    test_scores = 1.0 - np.asarray(proba_test, dtype=float)
    if method == "lac":
        groups = [(cal_scores, test_scores, sets, laws.split_index(y_cal.size, alpha))]
    else:
        groups = []
        for c in range(test_scores.shape[1]):
            n_c = int(np.sum(y_cal == c))
            k_c = laws.split_index(n_c, alpha)
            if n_c == 0 or k_c > n_c:
                continue
            groups.append((cal_scores[y_cal == c], test_scores[:, c], sets[:, c], k_c))
    offs: list[int] = []
    for cal, test, st, k in groups:
        br = diagnostics.bracket_rank(cal, test, st)
        if br is None:
            continue
        off = diagnostics.bracket_offset(br, k)
        if off is None:
            return "nt"
        offs.append(off)
    if not offs:
        return None
    return str(max(offs, key=abs))


# --- the study --------------------------------------------------------------------------


def load_done(path: Path) -> dict[str, dict[str, Any]]:
    """Records already checkpointed; malformed (e.g. half-written) lines are ignored."""
    done: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return done
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        # "unavailable" records (written by older versions) are not finished units
        if "uid" in rec and rec.get("status") != "unavailable":
            done[rec["uid"]] = rec
    return done


def _append(path: Path, record: dict[str, Any]) -> None:
    data = json.dumps(record, sort_keys=True, separators=(",", ":"))
    needs_nl = path.exists() and path.stat().st_size > 0 and not path.read_bytes().endswith(b"\n")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        if needs_nl:
            fh.write("\n")
        fh.write(data + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def _log(path: Path, msg: str) -> None:
    stamp = dt.datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{stamp} {msg}\n")


def cost_hint(unit: Unit) -> float:
    """Rough relative cost, used only to schedule expensive units first."""
    c = 1.0 + unit.n / 200.0
    if unit.method == "jackknife_plus":
        c *= 3.0 + unit.n / 10.0
    elif unit.method == "cv_plus":
        c *= 3.0 + (unit.n_folds or 5)
    if unit.adapter.startswith("crepes/") and unit.method != "split_abs":
        c *= 8.0
    return c


class FingerprintMismatch(RuntimeError):
    pass


class MissingLibraries(RuntimeError):
    """Requested libraries under test are not installed."""

    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(
            f"not installed: {', '.join(missing)}. Install them (uv sync --all-extras), "
            "restrict the run with --libraries, or pass --allow-missing to run without them"
        )


def known_libraries() -> set[str]:
    from conformcheck.adapters import registry

    return {ad.spec.library for ad in registry().values()}


def run_study(
    study: Study,
    out_dir: str | Path,
    workers: int = 4,
    force: bool = False,
    libraries: set[str] | None = None,
    max_units: int | None = None,
    echo: Callable[[str], None] | None = print,
    allow_missing: bool = False,
) -> dict[str, Any]:
    """Run (or resume) ``study`` into ``out_dir``. Returns a small summary.

    Raises ``ValueError`` for unknown names in ``libraries`` and :class:`MissingLibraries`
    when a library the run needs is not installed, unless ``allow_missing``.
    """
    from conformcheck.adapters import registry

    if libraries is not None:
        unknown = sorted(set(libraries) - known_libraries())
        if unknown:
            raise ValueError(f"unknown libraries {unknown}; known: {sorted(known_libraries())}")
    reg = registry()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    units_path, progress, meta_path = out / "units.jsonl", out / "progress.log", out / "run.json"
    vers = versions()
    fp = fingerprint(study, {"versions": vers, "libraries": sorted(libraries or [])})
    old_versions: dict[str, str | None] | None = None
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        old_versions = old.get("versions")
        if old.get("fingerprint") != fp and not force:
            raise FingerprintMismatch(
                f"{meta_path} has fingerprint {old.get('fingerprint')}, this run {fp}; "
                "use a new --out directory or --force"
            )
    all_units = enumerate_units(study, libraries=libraries)
    available = {key: ad.available() for key, ad in reg.items()}
    missing = sorted({reg[u.adapter].spec.library for u in all_units if not available[u.adapter]})
    if missing and not allow_missing:
        raise MissingLibraries(missing)
    units = [u for u in all_units if available[u.adapter]]
    skipped_units = len(all_units) - len(units)
    uid_of = {u.uid(study): u for u in units}
    done = load_done(units_path)
    stale = {
        uid
        for uid, rec in done.items()
        if uid in uid_of
        and record_versions(rec, old_versions)
        != unit_versions(vers, reg[uid_of[uid].adapter].spec.library)
    }
    done = {uid: rec for uid, rec in done.items() if uid not in stale}
    todo = [u for uid, u in uid_of.items() if uid not in done]
    todo.sort(key=cost_hint, reverse=True)
    if max_units is not None:
        todo = todo[:max_units]
    workers = max(1, min(int(workers), MAX_WORKERS))
    meta = {
        "fingerprint": fp,
        "study": study.config(),
        "source": study.source,
        "versions": vers,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "workers": workers,
        "units_total": len(uid_of),
        "missing_libraries": missing,
        "units_skipped_missing": skipped_units,
        "started": dt.datetime.now().isoformat(timespec="seconds"),
    }
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["first_started"] = old.get("first_started", old.get("started"))
    else:
        meta["first_started"] = meta["started"]
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    total = len(uid_of)
    n_done = total - len([u for u in uid_of if u not in done])
    _log(
        progress,
        f"start fingerprint={fp} total={total} done={n_done} todo={len(todo)} workers={workers}",
    )
    if missing:
        msg = f"warning: {skipped_units} units skipped, not installed: {', '.join(missing)}"
        _log(progress, msg)
        if echo:
            echo(msg)
    if stale:
        msg = f"{len(stale)} finished units were computed under other versions; re-running them"
        _log(progress, msg)
        if echo:
            echo(msg)
    if echo:
        echo(f"{len(todo)} units to run ({n_done}/{total} already done), {workers} workers")
    cfg = {"reps": study.reps, "test_points": study.test_points, "seed": study.seed}
    t0 = time.perf_counter()
    finished = 0
    errors = 0

    def handle(u: Unit, rec: dict[str, Any] | None, exc: BaseException | None) -> None:
        nonlocal finished, errors
        if exc is not None:
            errors += 1
            _log(progress, f"unit-error {u.adapter} {u.dgp} n={u.n}: {type(exc).__name__}: {exc}")
            return
        assert rec is not None
        if rec.get("status") != "done":  # e.g. a library that vanished mid-run
            errors += 1
            _log(progress, f"unit-not-done {u.adapter} {u.dgp} n={u.n}: {rec.get('status')}")
            return
        rec["uid"] = u.uid(study)
        rec["versions"] = unit_versions(vers, reg[u.adapter].spec.library)
        _append(units_path, rec)
        finished += 1
        el = time.perf_counter() - t0
        rate = finished / el if el > 0 else 0.0
        remaining = len(todo) - finished
        eta = remaining / rate if rate > 0 else math.inf
        msg = (
            f"done={n_done + finished}/{total} {u.adapter} {u.dgp} n={u.n} "
            f"{rec.get('elapsed_s', 0):.1f}s rate={rate * 60:.1f}/min eta={eta / 60:.1f}min"
        )
        _log(progress, msg)

    if workers == 1:
        for u in todo:
            try:
                handle(u, evaluate_unit(u.key(), cfg), None)
            except Exception as exc:  # noqa: BLE001
                handle(u, None, exc)
    else:
        for var in THREAD_ENV:
            os.environ[var] = "1"
        with ProcessPoolExecutor(max_workers=workers) as pool:
            pending: dict[Future, Unit] = {}
            queue = list(todo)
            while queue or pending:
                while queue and len(pending) < workers * 2:
                    u = queue.pop(0)
                    pending[pool.submit(evaluate_unit, u.key(), cfg)] = u
                ready, _ = wait(list(pending), return_when=FIRST_COMPLETED)
                for f in ready:
                    u = pending.pop(f)
                    exc = f.exception()
                    handle(u, None if exc else f.result(), exc)
    elapsed = time.perf_counter() - t0
    all_done = len(
        {
            uid
            for uid, rec in load_done(units_path).items()
            if uid in uid_of
            and record_versions(rec, old_versions)
            == unit_versions(vers, reg[uid_of[uid].adapter].spec.library)
        }
    )
    _log(
        progress,
        f"end finished={finished} errors={errors} done={all_done}/{total} "
        f"elapsed={elapsed / 60:.1f}min",
    )
    meta["ended"] = dt.datetime.now().isoformat(timespec="seconds")
    meta["elapsed_s_last_session"] = round(elapsed, 1)
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "total": total,
        "done": all_done,
        "finished": finished,
        "errors": errors,
        "elapsed_s": elapsed,
        "missing_libraries": missing,
        "units_skipped_missing": skipped_units,
    }


def iter_records(run_dir: str | Path) -> Iterable[dict[str, Any]]:
    """All checkpointed records of a run directory, including ones from earlier configs.

    Reads ``units.jsonl`` or, failing that, ``units.jsonl.gz``. Use :func:`study_records`
    for the records that belong to the study in ``run.json``.
    """
    run = Path(run_dir)
    plain, gz = run / "units.jsonl", run / "units.jsonl.gz"
    yield from load_done(gz if not plain.exists() and gz.exists() else plain).values()


def study_records(run_dir: str | Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Records of the study described by ``run.json``, and counts of those left out.

    A run directory reused with ``--force`` can hold records of an earlier configuration
    (other R, m, seed or grid) and records computed under other library versions. Only
    records whose unit id belongs to the current study and whose versions match
    ``run.json`` are returned; the second value counts the rest by reason
    (``other_config``, ``other_versions``).
    """
    run = Path(run_dir)
    meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
    study = Study.from_config(meta["study"], meta.get("source", ""))
    lib_of = {u.uid(study): u.adapter.split("/")[0] for u in enumerate_units(study)}
    vers = meta.get("versions") or {}
    kept: list[dict[str, Any]] = []
    dropped = {"other_config": 0, "other_versions": 0}
    for rec in iter_records(run):
        uid = rec.get("uid")
        if uid not in lib_of:
            dropped["other_config"] += 1
        elif record_versions(rec, vers) != unit_versions(vers, lib_of[uid]):
            dropped["other_versions"] += 1
        else:
            kept.append(rec)
    return kept, dropped
