"""Batch-size invariance: the same test points must get the same sets in any batch.

A conformal method fits on calibration data and then predicts each test point on its
own: the set for ``x`` cannot depend on which other test points share the call. When a
study sets ``batch_sizes``, the runner predicts every repetition's test points again

* in consecutive chunks of each size ``s`` (``size=1`` is one point at a time), and
* in one call in a shuffled order (``shuffled``),

and compares each mode with the single full-batch call (REPORT.md, F11, is a set size
capped at the number of test points in the call).

* Deterministic methods must return identical sets and, up to float tolerance,
  identical intervals. Each chunk call gets the repetition's library seed, so seeded
  fits (CV+ folds) are the same in every call.
* Randomized methods (:data:`RANDOMIZED_VARIANTS`) draw uniforms inside the library, so
  only the distribution of a point's set must be the same. Each chunk call gets its own
  seed (one shared seed would hand every chunk the same first uniform), and the report
  tests, per mode, that the mean over repetitions of the per-repetition difference in
  mean set size and in coverage is zero (:func:`paired_pvalue`, Holm across cells).

A change of status (a chunk raises where the full batch does not, or the reverse)
counts as a difference for both kinds.
"""

from __future__ import annotations

import dataclasses
import math
from collections.abc import Sequence
from fractions import Fraction
from typing import Any

import numpy as np

from conformcheck import diagnostics
from conformcheck.adapters._common import Input, LibraryAdapter
from conformcheck.adapters.base import AlphaOutput, ClassificationInput, MethodSpec

RANDOMIZED_VARIANTS = frozenset(
    {"include_last_label=randomized", "rand=True", "randomized=True", "randomized", "smoothed"}
)
SHUFFLED = "shuffled"


def is_randomized(spec: MethodSpec) -> bool:
    return spec.variant in RANDOMIZED_VARIANTS


def modes(m: int, sizes: Sequence[int], rng: np.random.Generator) -> list[tuple[str, list]]:
    """Each mode's calls as index arrays into the ``m`` test points."""
    idx = np.arange(m)
    out: list[tuple[str, list]] = [
        (f"size={s}", [idx[i : i + s] for i in range(0, m, s)]) for s in sizes
    ]
    out.append((SHUFFLED, [rng.permutation(m)]))
    return out


def subset(inp: Input, idx: np.ndarray, seed: int) -> Input:
    """``inp`` with only the test points ``idx`` (in that order) and library seed ``seed``."""
    changes: dict[str, Any] = {"x_test": inp.x_test[idx], "seed": seed}
    if isinstance(inp, ClassificationInput):
        changes["proba_test"] = inp.proba_test[idx]
    return dataclasses.replace(inp, **changes)


def _chunk_seed(seed: int, mode: int, chunk: int) -> int:
    ss = np.random.SeedSequence([seed, mode, chunk])
    return int(ss.generate_state(1)[0] & 0x7FFFFFFF)


def predict_in_chunks(
    adapter: LibraryAdapter,
    inp: Input,
    chunks: list,
    randomized: bool,
    mode: int,
) -> dict[Fraction, AlphaOutput]:
    """Run ``adapter`` once per chunk and put the outputs back in test-point order.

    An alpha whose chunks are not all ``ok`` gets the status of the first chunk that is
    not, with its message.
    """
    m = len(inp.x_test)
    parts: dict[Fraction, list[tuple[np.ndarray, AlphaOutput]]] = {a: [] for a in inp.alphas}
    for j, idx in enumerate(chunks):
        seed = _chunk_seed(inp.seed, mode, j) if randomized else inp.seed
        try:
            outs = adapter.run(subset(inp, idx, seed))
        except Exception as exc:  # noqa: BLE001 - recorded as a status, as in the runner
            msg = f"{type(exc).__name__}: {exc}"[:500]
            outs = {a: AlphaOutput(status="error", message=msg) for a in inp.alphas}
        for a in inp.alphas:
            o = outs.get(a) or AlphaOutput(status="error", message="no output for alpha")
            parts[a].append((idx, o))
    result: dict[Fraction, AlphaOutput] = {}
    for a, ps in parts.items():
        bad = next((o for _, o in ps if o.status != "ok"), None)
        if bad is not None:
            result[a] = AlphaOutput(status=bad.status, message=bad.message)
            continue
        if ps[0][1].intervals is not None:
            iv = np.full((m, 2), np.nan)
            for idx, o in ps:
                iv[idx] = np.asarray(o.intervals, dtype=float)
            result[a] = AlphaOutput(intervals=iv)
        else:
            k = np.asarray(ps[0][1].sets).shape[1]
            sets = np.zeros((m, k), dtype=bool)
            for idx, o in ps:
                sets[idx] = np.asarray(o.sets, dtype=bool)
            result[a] = AlphaOutput(sets=sets)
    return result


def compare(full: AlphaOutput, mode: AlphaOutput, y_test: np.ndarray) -> dict[str, Any] | None:
    """One repetition of one mode against the full batch; None when neither is ``ok``.

    ``points``: test points whose output differs (sets exactly, intervals beyond the
    tolerance of :mod:`conformcheck.diagnostics`); ``size_diff`` and ``cover_diff``:
    mean set size (sets only) and coverage of the mode minus those of the full batch.
    """
    if full.status != "ok" and mode.status != "ok":
        return None
    if full.status != mode.status:
        return {"status_mismatch": 1, "message": (mode.message or full.message)[:200]}
    y = np.asarray(y_test)
    if full.intervals is not None:
        a = np.asarray(full.intervals, dtype=float)
        b = np.asarray(mode.intervals, dtype=float)
        same_inf = np.isinf(a) & np.isinf(b) & (np.sign(a) == np.sign(b))
        with np.errstate(invalid="ignore"):
            diff = np.where(same_inf, 0.0, np.abs(a - b))
        fin = np.abs(a[np.isfinite(a)])
        tol = diagnostics.REL_TOL * max(1.0, float(fin.max()) if fin.size else 1.0)
        bad = ~(diff <= tol)  # NaN (one side infinite) counts as a difference
        cov_a = (a[:, 0] <= y) & (y <= a[:, 1])
        cov_b = (b[:, 0] <= y) & (y <= b[:, 1])
        return {
            "points": int(np.any(bad, axis=1).sum()),
            "max_diff": float(np.nanmax(np.where(np.isnan(diff), np.inf, diff))),
            "cover_diff": float(cov_b.mean() - cov_a.mean()),
        }
    sa = np.asarray(full.sets, dtype=bool)
    sb = np.asarray(mode.sets, dtype=bool)
    rows = np.arange(len(y))
    yi = y.astype(int)
    return {
        "points": int(np.any(sa != sb, axis=1).sum()),
        "size_diff": float(sb.sum(axis=1).mean() - sa.sum(axis=1).mean()),
        "cover_diff": float(sb[rows, yi].mean() - sa[rows, yi].mean()),
    }


def check_repetition(
    adapter: LibraryAdapter,
    inp: Input,
    full: dict[Fraction, AlphaOutput],
    y_test: np.ndarray,
    sizes: Sequence[int],
    rng: np.random.Generator,
) -> dict[Fraction, dict[str, dict[str, Any]]]:
    """Every mode of one repetition: ``{alpha: {mode: comparison}}`` (see :func:`compare`)."""
    randomized = is_randomized(adapter.spec)
    out: dict[Fraction, dict[str, dict[str, Any]]] = {a: {} for a in inp.alphas}
    for i, (name, chunks) in enumerate(modes(len(inp.x_test), sizes, rng)):
        outs = predict_in_chunks(adapter, inp, chunks, randomized, i + 1)
        for a in inp.alphas:
            f = full.get(a) or AlphaOutput(status="error", message="no output for alpha")
            c = compare(f, outs[a], y_test)
            if c is not None:
                out[a][name] = c
    return out


def new_accumulator() -> dict[str, Any]:
    return {
        "reps": 0,
        "differ": 0,
        "points": 0,
        "max_diff": 0.0,
        "status_mismatch": 0,
        "message": "",
        "size_diff": [],
        "cover_diff": [],
    }


def accumulate(acc: dict[str, dict[str, Any]], rep: dict[str, dict[str, Any]]) -> None:
    """Add one repetition's comparisons to the per-mode record of one alpha."""
    for name, c in rep.items():
        st = acc.setdefault(name, new_accumulator())
        st["reps"] += 1
        if c.get("status_mismatch"):
            st["status_mismatch"] += 1
            st["message"] = st["message"] or c["message"]
            continue
        st["differ"] += int(c["points"] > 0)
        st["points"] += c["points"]
        if "max_diff" in c:
            st["max_diff"] = max(st["max_diff"], c["max_diff"])
        if "size_diff" in c:
            st["size_diff"].append(round(c["size_diff"], 6))
        st["cover_diff"].append(round(c["cover_diff"], 6))


def _zero_mean_pvalue(x: Sequence[float]) -> float:
    """Two-sided one-sample t-test of mean zero; a constant sample gives 1 or 0."""
    v = np.asarray(x, dtype=float)
    if v.size < 2:
        return 1.0
    if float(np.ptp(v)) == 0.0:  # np.std of equal floats can be 1e-16, not 0
        return 1.0 if np.all(v == 0) else 0.0
    from scipy import stats as sps

    return float(sps.ttest_1samp(v, 0.0).pvalue)


def paired_pvalue(batch: dict[str, dict[str, Any]]) -> float | None:
    """p-value that every mode has the full batch's mean set size and coverage.

    Per mode, a t-test on the per-repetition differences of mean set size and of
    coverage; Bonferroni over the two tests and over the modes. None without data.
    """
    ps = []
    for st in batch.values():
        for key in ("size_diff", "cover_diff"):
            if st.get(key):
                ps.append(_zero_mean_pvalue(st[key]))
    if not ps:
        return None
    return min(1.0, len(ps) * min(ps))


def deterministic_reason(batch: dict[str, dict[str, Any]], randomized: bool) -> str:
    """Differences that need no test: a changed status in any row, and differing
    outputs in a deterministic row. Empty when there are none."""
    parts = []
    for name, st in batch.items():
        if st["status_mismatch"]:
            parts.append(
                f"{name}: status differs in {st['status_mismatch']}/{st['reps']} reps "
                f"({st['message'][:60]})"
            )
        elif st["differ"] and not randomized:
            parts.append(f"{name}: {describe(st)}")
    return "; ".join(parts)


def describe(st: dict[str, Any], randomized: bool = False) -> str:
    """Differences of one mode in words: reps and points differing (deterministic rows;
    randomized outputs differ by design) and the mean change in set size and coverage."""
    bits = []
    if not randomized:
        bits.append(f"differs in {st['differ']}/{st['reps']} reps ({st['points']} points)")
    for key, label in (("size_diff", "set size"), ("cover_diff", "coverage")):
        if st.get(key):
            bits.append(f"{label} {float(np.mean(st[key])):+.3f}")
    if st.get("max_diff") and math.isfinite(st["max_diff"]) and st["max_diff"] > 0:
        bits.append(f"max endpoint diff {st['max_diff']:.3g}")
    return ", ".join(bits)
