"""Exact finite-sample coverage of prediction-powered mean intervals (``ppi_py``).

DESIGN section 15. A binary truth ``Y ~ Bernoulli(pi)`` and a binary judge with sensitivity
= specificity = ``acc`` make the labelled pairs ``(Y, Yhat)`` a 4-cell multinomial with
probabilities ``pi acc, pi (1 - acc), (1 - pi)(1 - acc), (1 - pi) acc`` for the cells
``(1,1), (1,0), (0,1), (0,0)``. The unlabelled judge labels are a fixed array of ``N``
labels with exactly ``N mu`` ones, ``mu = pi acc + (1 - pi)(1 - acc)`` (the judge mean held
at its expectation). The coverage of an interval method is then the sum of the
multinomial probabilities of the outcomes whose interval contains ``pi``, with each
interval computed by the library itself.

Probabilities are exact rationals summed as integers over a common denominator. Outcomes
are evaluated in order of decreasing probability until the unevaluated mass is at most
``tail``; that mass is recorded, so the coverage lies in ``[c, c + unevaluated]``.

The library's d-dimensional mean interval evaluates one outcome per column. For PPI++ it
is called with ``lam_optim_mode="element"``, which for a single column is the default
computation; an outcome whose endpoint lies within ``NEAR`` of ``pi`` is re-evaluated with
a one-dimensional call as a user would make it, so batching cannot change a verdict.
Wald (the library's ``classical_mean_ci``) and Clopper-Pearson (scipy) use the labels
only and are enumerated over ``Binomial(n, pi)`` without pruning.

Commands (run inside a venv holding ``ppi-python``; ``scripts/ppi_study.py`` builds one)::

    python -m conformcheck.ppi run --out runs/ppi       # exact coverage, checkpointed
    python -m conformcheck.ppi mc --out runs/ppi        # Monte Carlo cross-check
    python -m conformcheck.ppi report runs/ppi --to docs/results/ppi   # no ppi_py needed
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import platform
import sys
import time
import tomllib
from collections.abc import Callable, Iterable
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from dataclasses import asdict, dataclass, field
from decimal import Decimal, localcontext
from fractions import Fraction
from importlib import resources
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import numpy as np
from scipy import special, stats

from conformcheck.runner import MAX_WORKERS, THREAD_ENV, _append, _limit_threads, _log, load_done

METHODS: tuple[str, ...] = ("ppi", "ppi++", "wald", "clopper_pearson")
LABELLED_METHODS: tuple[str, ...] = ("ppi", "ppi++")
# endpoints closer than this to pi are recomputed with a one-dimensional library call
NEAR = 1e-9
# a cell is below nominal when its coverage is under 1 - alpha - BELOW
BELOW = Fraction(1, 100)
PACKAGES: tuple[str, ...] = ("ppi-python", "numpy", "scipy", "statsmodels", "numba", "pandas")


# --- study settings ---------------------------------------------------------------------


@dataclass(frozen=True)
class PPIStudy:
    name: str
    n: tuple[int, ...]
    acc: tuple[str, ...]
    pi: tuple[str, ...]
    alphas: tuple[str, ...]
    n_unlabelled: int
    tail: str
    batch: int
    workers: int
    methods: tuple[str, ...]
    mc_seed: int
    mc_draws: int
    mc_cells: tuple[tuple[int, str, str, str], ...]
    source: str = field(default="", compare=False)

    def config(self) -> dict[str, Any]:
        cfg = asdict(self)
        cfg.pop("source")
        return cfg

    def fingerprint(self) -> str:
        blob = json.dumps(self.config(), sort_keys=True).encode()
        return hashlib.sha256(blob).hexdigest()[:16]

    def units(self) -> list[tuple[int, str, str]]:
        return [(n, a, p) for n in self.n for a in self.acc for p in self.pi]


def _frac(text: str, what: str) -> Fraction:
    if not isinstance(text, str):
        raise ValueError(f'{what} must be a decimal string such as "0.1", got {text!r}')
    value = Fraction(text)
    if not 0 < value < 1:
        raise ValueError(f"{what} must lie in (0, 1), got {text!r}")
    return value


def load_ppi_study(name_or_path: str | Path = "ppi") -> PPIStudy:
    """Load the built-in ``ppi`` study or a TOML file of the same form; ValueError if invalid."""
    p = Path(name_or_path)
    if p.suffix == ".toml" and p.exists():
        text, source = p.read_text(encoding="utf-8"), str(p)
    else:
        res = resources.files("conformcheck.studies").joinpath(f"{name_or_path}.toml")
        if not res.is_file():
            raise FileNotFoundError(f"no built-in study {name_or_path!r} and no such file")
        text, source = res.read_text(encoding="utf-8"), f"builtin:{name_or_path}"
    raw = tomllib.loads(text)
    if raw.get("kind") != "ppi":
        raise ValueError(f"{source}: not a ppi study (kind = {raw.get('kind')!r})")
    try:
        ns = tuple(int(v) for v in raw["n"])
        if any(isinstance(v, bool) or v < 2 for v in raw["n"]):
            raise ValueError(f"{source}: every n must be an integer >= 2")
        for key in ("acc", "pi", "alphas"):
            for v in raw[key]:
                _frac(v, f"{source}: {key}")
        methods = tuple(raw["methods"])
        unknown = sorted(set(methods) - set(METHODS))
        if unknown:
            raise ValueError(f"{source}: unknown methods {unknown}; known: {list(METHODS)}")
        tail = Fraction(Decimal(raw["tail"]))
        if not 0 <= tail < 1:
            raise ValueError(f"{source}: tail must lie in [0, 1)")
        n_unl = int(raw["n_unlabelled"])
        mc = raw["mc"]
        cells = tuple((int(c[0]), str(c[1]), str(c[2]), str(c[3])) for c in mc["cells"])
        study = PPIStudy(
            name=str(raw["name"]),
            n=ns,
            acc=tuple(raw["acc"]),
            pi=tuple(raw["pi"]),
            alphas=tuple(raw["alphas"]),
            n_unlabelled=n_unl,
            tail=str(raw["tail"]),
            batch=int(raw["batch"]),
            workers=int(raw["workers"]),
            methods=methods,
            mc_seed=int(mc["seed"]),
            mc_draws=int(mc["draws"]),
            mc_cells=cells,
            source=source,
        )
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{source}: invalid ppi study: {exc!r}") from exc
    for a in study.acc:
        for p in study.pi:
            mu = judge_mean(Fraction(p), Fraction(a))
            if (mu * n_unl).denominator != 1:
                raise ValueError(f"{source}: N * mu is not an integer for acc={a}, pi={p}")
    return study


# --- the exact law ----------------------------------------------------------------------


def cell_probs(pi: Fraction, acc: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """P of (Y, Yhat) = (1,1), (1,0), (0,1), (0,0) for a judge with sens = spec = acc."""
    return (pi * acc, pi * (1 - acc), (1 - pi) * (1 - acc), (1 - pi) * acc)


def judge_mean(pi: Fraction, acc: Fraction) -> Fraction:
    """P(Yhat = 1)."""
    return pi * acc + (1 - pi) * (1 - acc)


def outcomes(n: int) -> np.ndarray:
    """Every count vector (c11, c10, c01, c00) summing to n, shape (C(n + 3, 3), 4)."""
    blocks = []
    for c11 in range(n + 1):
        for c10 in range(n + 1 - c11):
            c01 = np.arange(n + 1 - c11 - c10, dtype=np.int64)
            block = np.empty((c01.size, 4), dtype=np.int64)
            block[:, 0], block[:, 1], block[:, 2], block[:, 3] = c11, c10, c01, n - c11 - c10 - c01
            blocks.append(block)
    return np.concatenate(blocks)


class ExactMass:
    """Exact multinomial probabilities as integers over the common denominator ``den``."""

    def __init__(self, n: int, probs: Iterable[Fraction]) -> None:
        probs = tuple(probs)
        if sum(probs) != 1 or any(p < 0 for p in probs):
            raise ValueError(f"cell probabilities must be >= 0 and sum to 1, got {probs}")
        d = math.lcm(*(p.denominator for p in probs))
        self.n = n
        self.nums = tuple(int(p * d) for p in probs)
        self.den = d**n
        self._fact = [math.factorial(i) for i in range(n + 1)]
        self._pows = [[a**c for c in range(n + 1)] for a in self.nums]

    def weight(self, counts: Iterable[int]) -> int:
        counts = tuple(int(c) for c in counts)
        w = self._fact[self.n]
        for c in counts:
            w //= self._fact[c]
        for pows, c in zip(self._pows, counts, strict=True):
            w *= pows[c]
        return w

    def weights(self, rows: np.ndarray) -> list[int]:
        return [self.weight(r) for r in rows.tolist()]


def log_pmf(rows: np.ndarray, probs: Iterable[Fraction]) -> np.ndarray:
    """Float log multinomial pmf (only to order and select outcomes; -inf for p = 0 cells)."""
    n = int(rows[0].sum())
    lp = special.gammaln(n + 1) - special.gammaln(rows + 1).sum(axis=1)
    with np.errstate(divide="ignore"):
        for j, p in enumerate(probs):
            lp = lp + np.where(rows[:, j] > 0, rows[:, j] * np.log(float(p)), 0.0)
    return lp


@dataclass
class Selection:
    rows: np.ndarray  # evaluated outcomes, most probable first
    weights: list[int]  # exact weights over ``den``
    den: int
    unevaluated: Fraction  # exact probability of the outcomes left out


def select_outcomes(n: int, probs: Iterable[Fraction], tail: Fraction) -> Selection:
    """The most probable outcomes, until the exact unevaluated mass is at most ``tail``."""
    probs = tuple(probs)
    rows = outcomes(n)
    lp = log_pmf(rows, probs)
    order = np.argsort(-lp, kind="stable")
    rows, lp = rows[order], lp[order]
    p = np.exp(lp)
    remaining = np.cumsum(p[::-1])[::-1]  # remaining[k] = mass of rows k..end
    k = int(np.sum(remaining > float(tail) / 4)) if tail > 0 else len(rows)
    k = max(k, 1)
    mass = ExactMass(n, probs)
    weights = mass.weights(rows[:k])
    total = sum(weights)
    while Fraction(mass.den - total, mass.den) > tail and k < len(rows):
        extra = rows[k : min(len(rows), 2 * k)]
        new = mass.weights(extra)
        weights += new
        total += sum(new)
        k += len(extra)
    return Selection(rows[:k], weights, mass.den, Fraction(mass.den - total, mass.den))


def binomial_weights(n: int, pi: Fraction) -> tuple[list[int], int]:
    """Exact Binomial(n, pi) pmf of k = 0..n as integers over the returned denominator."""
    mass = ExactMass(n, (pi, 1 - pi))
    return [mass.weight((k, n - k)) for k in range(n + 1)], mass.den


def columns(rows: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Labelled arrays Y, Yhat of shape (n, d): column j realises the counts rows[j]."""
    r = np.arange(n)[:, None]
    a = rows[:, 0][None, :]
    b = a + rows[:, 1][None, :]
    c = b + rows[:, 2][None, :]
    y = (r < b).astype(float)
    yhat = ((r < a) | ((r >= b) & (r < c))).astype(float)
    return y, yhat


def unlabelled(n_unlabelled: int, mu: Fraction) -> np.ndarray:
    ones = mu * n_unlabelled
    if ones.denominator != 1:
        raise ValueError(f"N * mu = {ones} is not an integer")
    u = np.zeros(n_unlabelled)
    u[: int(ones)] = 1.0
    return u


# --- interval methods -------------------------------------------------------------------

Batch = Callable[[np.ndarray, np.ndarray, np.ndarray, float], tuple[np.ndarray, np.ndarray]]
Single = Callable[[np.ndarray, np.ndarray, np.ndarray, float], tuple[float, float]]


@dataclass(frozen=True)
class Impl:
    """Interval functions: ``batch[m]`` takes (n, d) arrays, ``single[m]`` 1-D ones."""

    name: str
    batch: dict[str, Batch]
    single: dict[str, Single]
    wald: Callable[[np.ndarray, float], tuple[float, float]]


def _flat(lo: Any, hi: Any) -> tuple[np.ndarray, np.ndarray]:
    return np.asarray(lo, dtype=float).reshape(-1), np.asarray(hi, dtype=float).reshape(-1)


def library_impl() -> Impl:
    """``ppi_py``'s public functions, called as a user would (imported here, not at load)."""
    from ppi_py import classical_mean_ci, ppi_mean_ci

    def ppi_batch(y, yhat, unl, alpha):
        return _flat(*ppi_mean_ci(y, yhat, unl, alpha=alpha, lam=1))

    def ppipp_batch(y, yhat, unl, alpha):
        return _flat(*ppi_mean_ci(y, yhat, unl, alpha=alpha, lam_optim_mode="element"))

    def ppi_single(y, yhat, unl, alpha):
        lo, hi = _flat(*ppi_mean_ci(y, yhat, unl, alpha=alpha, lam=1))
        return float(lo[0]), float(hi[0])

    def ppipp_single(y, yhat, unl, alpha):
        lo, hi = _flat(*ppi_mean_ci(y, yhat, unl, alpha=alpha))
        return float(lo[0]), float(hi[0])

    def wald(y, alpha):
        lo, hi = classical_mean_ci(y, alpha=alpha)
        return float(lo), float(hi)

    return Impl(
        "library",
        {"ppi": ppi_batch, "ppi++": ppipp_batch},
        {"ppi": ppi_single, "ppi++": ppipp_single},
        wald,
    )


def reference_impl() -> Impl:
    """Textbook formulas (numpy, ``ddof = 0`` as in ppi_py), to check the enumeration alone.

    PPI with ``lam = 1`` (Angelopoulos et al. 2023): ``mean(unl) + mean(Y - Yhat)`` plus or
    minus ``z sqrt(var(unl) / N + var(Y - Yhat) / n)``; Wald: ``p +- z sqrt(p (1 - p) / n)``.
    PPI++ has no reference here.
    """

    def ppi_batch(y, yhat, unl, alpha):
        z = stats.norm.ppf(1 - alpha / 2)
        n, big_n = y.shape[0], unl.shape[0]
        r = y - yhat
        est = unl.mean() + r.mean(axis=0)
        se = np.sqrt(unl.var() / big_n + r.var(axis=0) / n)
        return est - z * se, est + z * se

    def ppi_single(y, yhat, unl, alpha):
        lo, hi = ppi_batch(y[:, None], yhat[:, None], unl, alpha)
        return float(lo[0]), float(hi[0])

    def wald(y, alpha):
        z = stats.norm.ppf(1 - alpha / 2)
        p = y.mean()
        h = z * math.sqrt(p * (1 - p) / y.shape[0])
        return p - h, p + h

    return Impl("reference", {"ppi": ppi_batch}, {"ppi": ppi_single}, wald)


def clopper_pearson(k: int, n: int, alpha: float) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(stats.beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


# --- one unit ---------------------------------------------------------------------------


def _decimal(x: Fraction, digits: int = 20) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def _summary(
    covered: np.ndarray,
    lo: np.ndarray,
    hi: np.ndarray,
    weights: list[int],
    den: int,
    unevaluated: Fraction,
    w: np.ndarray,
) -> dict[str, Any]:
    finite = np.isfinite(lo) & np.isfinite(hi)
    cov = Fraction(sum(x for x, c in zip(weights, covered.tolist(), strict=True) if c), den)
    width = hi - lo
    return {
        "coverage": float(cov),
        "coverage_decimal": _decimal(cov),
        "unevaluated": float(unevaluated),
        "mean_width": float(np.sum(w[finite] * width[finite])),
        "zero_width_mass": float(np.sum(w[finite & (width == 0)])),
        "nan_mass": float(np.sum(w[~finite])),
    }


def evaluate_unit(
    n: int, acc: str, pi: str, study: PPIStudy, impl: Impl | None = None
) -> dict[str, Any]:
    """Exact coverage of every method and alpha at one (n, acc, pi)."""
    impl = impl or library_impl()
    t0 = time.perf_counter()
    pi_q, acc_q = Fraction(pi), Fraction(acc)
    pi_f = float(pi_q)
    rec: dict[str, Any] = {"uid": unit_id(n, acc, pi), "n": n, "acc": acc, "pi": pi}
    results: dict[str, dict[str, Any]] = {}
    labelled = [m for m in study.methods if m in LABELLED_METHODS]
    if labelled:
        sel = select_outcomes(n, cell_probs(pi_q, acc_q), Fraction(Decimal(study.tail)))
        rec["outcomes_evaluated"] = int(len(sel.rows))
        rec["outcomes_total"] = math.comb(n + 3, 3)
        unl = unlabelled(study.n_unlabelled, judge_mean(pi_q, acc_q))
        pw = np.array([x / sel.den for x in sel.weights])
        for alpha in study.alphas:
            a = float(alpha)
            for m in labelled:
                if m not in impl.batch:
                    raise ValueError(f"{impl.name} has no method {m!r}")
                lo = np.empty(len(sel.rows))
                hi = np.empty(len(sel.rows))
                for s in range(0, len(sel.rows), study.batch):
                    y, yhat = columns(sel.rows[s : s + study.batch], n)
                    lo[s : s + study.batch], hi[s : s + study.batch] = impl.batch[m](
                        y, yhat, unl, a
                    )
                near = np.flatnonzero(np.minimum(np.abs(lo - pi_f), np.abs(hi - pi_f)) <= NEAR)
                flips = 0
                for j in near.tolist():
                    y, yhat = columns(sel.rows[j : j + 1], n)
                    l1, h1 = impl.single[m](y[:, 0], yhat[:, 0], unl, a)
                    flips += (lo[j] <= pi_f <= hi[j]) != (l1 <= pi_f <= h1)
                    lo[j], hi[j] = l1, h1
                covered = (lo <= pi_f) & (pi_f <= hi)
                res = _summary(covered, lo, hi, sel.weights, sel.den, sel.unevaluated, pw)
                res["near_endpoint"] = int(near.size)
                res["batch_flips"] = int(flips)
                results[f"{m}|{alpha}"] = res
    label_only = [m for m in study.methods if m not in LABELLED_METHODS]
    if label_only:
        weights, den = binomial_weights(n, pi_q)
        bw = np.array([x / den for x in weights])
        for alpha in study.alphas:
            a = float(alpha)
            for m in label_only:
                bounds = []
                for k in range(n + 1):
                    if m == "wald":
                        y = np.zeros(n)
                        y[:k] = 1.0
                        bounds.append(impl.wald(y, a))
                    else:
                        bounds.append(clopper_pearson(k, n, a))
                lo = np.array([b[0] for b in bounds])
                hi = np.array([b[1] for b in bounds])
                covered = (lo <= pi_f) & (pi_f <= hi)
                results[f"{m}|{alpha}"] = _summary(covered, lo, hi, weights, den, Fraction(0), bw)
    rec["results"] = results
    rec["impl"] = impl.name
    rec["elapsed_s"] = round(time.perf_counter() - t0, 3)
    return rec


def unit_id(n: int, acc: str, pi: str) -> str:
    return f"n{n}-acc{acc}-pi{pi}"


# --- runner -----------------------------------------------------------------------------


def versions() -> dict[str, str | None]:
    out: dict[str, str | None] = {"python": platform.python_version()}
    for pkg in PACKAGES:
        try:
            out[pkg] = version(pkg)
        except PackageNotFoundError:
            out[pkg] = None
    return out


def _worker_init() -> None:
    _limit_threads()


def _unit_job(args: tuple[int, str, str, PPIStudy, str]) -> dict[str, Any]:
    n, acc, pi, study, impl_name = args
    impl = library_impl() if impl_name == "library" else reference_impl()
    return evaluate_unit(n, acc, pi, study, impl)


def _mc_job(args: tuple[tuple[int, str, str, str], str, PPIStudy]) -> dict[str, Any]:
    cell, variant, study = args
    return monte_carlo_cell(cell, variant, study)


def _start_meta(out: Path, study: PPIStudy, kind: str, workers: int, force: bool) -> str:
    """Write ``<kind>.json``; refuse a changed configuration unless ``force``."""
    meta_path = out / f"{kind}.json"
    vers = versions()
    fp = hashlib.sha256(
        json.dumps({"study": study.config(), "versions": vers}, sort_keys=True).encode()
    ).hexdigest()[:16]
    first = None
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if old.get("fingerprint") != fp and not force:
            raise ValueError(
                f"{meta_path} has fingerprint {old.get('fingerprint')}, this run {fp}; "
                "use a new --out directory or --force"
            )
        first = old.get("first_started")
    now = dt.datetime.now().isoformat(timespec="seconds")
    meta = {
        "fingerprint": fp,
        "study": study.config(),
        "source": study.source,
        "versions": vers,
        "platform": platform.platform(),
        "workers": workers,
        "started": now,
        "first_started": first or now,
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    return fp


def _run_jobs(
    jobs: dict[str, Any],
    fn: Callable[[Any], dict[str, Any]],
    out_path: Path,
    progress: Path,
    workers: int,
    echo: Callable[[str], None] | None,
) -> int:
    done = load_done(out_path)
    todo = {uid: job for uid, job in jobs.items() if uid not in done}
    total = len(jobs)
    n_done = total - len(todo)
    _log(progress, f"start total={total} done={n_done} todo={len(todo)} workers={workers}")
    if echo:
        echo(f"{len(todo)} units to run ({n_done}/{total} done), {workers} workers")
    if not todo:
        return 0
    # BLAS reads its thread count when numpy loads, which in a spawned worker happens
    # before any initializer runs; multithreaded OpenBLAS made np.cov here about 6x slower.
    for var in THREAD_ENV:
        os.environ[var] = "1"
    t0 = time.time()
    finished = 0
    errors = 0
    with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init) as pool:
        pending: dict[Future[dict[str, Any]], str] = {
            pool.submit(fn, job): uid for uid, job in todo.items()
        }
        while pending:
            ready, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in ready:
                uid = pending.pop(fut)
                exc = fut.exception()
                if exc is not None:
                    errors += 1
                    _log(progress, f"unit-error {uid}: {type(exc).__name__}: {exc}")
                    continue
                _append(out_path, fut.result())
                finished += 1
                rate = finished / max(time.time() - t0, 1e-9)
                left = len(todo) - finished - errors
                msg = (
                    f"done {n_done + finished}/{total} {uid} rate={rate * 60:.2f}/min "
                    f"eta={left / rate / 60 if rate else float('nan'):.1f} min"
                )
                _log(progress, msg)
                if echo:
                    echo(msg)
    if errors:
        _log(progress, f"{errors} units failed")
    return 1 if errors else 0


def run(
    study: PPIStudy,
    out_dir: str | Path,
    workers: int | None = None,
    impl: str = "library",
    force: bool = False,
    echo: Callable[[str], None] | None = print,
) -> int:
    """Exact coverage of every unit into ``<out>/units.jsonl``; reruns skip finished units."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if impl == "library":
        library_impl()  # fail before any work when ppi_py is missing
    w = max(1, min(int(workers or study.workers), MAX_WORKERS))
    _start_meta(out, study, "run", w, force)
    units = sorted(study.units(), key=lambda u: -u[0])
    jobs = {unit_id(*u): (*u, study, impl) for u in units}
    return _run_jobs(jobs, _unit_job, out / "units.jsonl", out / "progress.log", w, echo)


# --- Monte Carlo cross-check ------------------------------------------------------------

MC_VARIANTS: tuple[str, ...] = ("fixed", "binomial")


def mc_id(cell: tuple[int, str, str, str], variant: str) -> str:
    n, acc, pi, alpha = cell
    return f"mc-n{n}-acc{acc}-pi{pi}-alpha{alpha}-{variant}"


def monte_carlo_cell(
    cell: tuple[int, str, str, str], variant: str, study: PPIStudy
) -> dict[str, Any]:
    """Raw draws passed one at a time to the library; counts of covering intervals.

    ``fixed`` uses the study's unlabelled array; ``binomial`` draws the unlabelled count
    from Binomial(N, mu) per sample. Both variants see the same labelled draws.
    """
    from ppi_py import classical_mean_ci, ppi_mean_ci

    t0 = time.perf_counter()
    n, acc, pi, alpha = cell
    pi_q, acc_q = Fraction(pi), Fraction(acc)
    pi_f, acc_f, a = float(pi_q), float(acc_q), float(alpha)
    mu = judge_mean(pi_q, acc_q)
    big_n = study.n_unlabelled
    key = [study.mc_seed, n, int(acc_q * 1000), int(pi_q * 1000), int(Fraction(alpha) * 1000)]
    lab = np.random.default_rng(np.random.SeedSequence(key))
    unl_rng = np.random.default_rng(np.random.SeedSequence([*key, 1]))
    fixed = unlabelled(big_n, mu)
    counts = {"ppi": 0, "ppi++": 0, "wald": 0}
    for _ in range(study.mc_draws):
        y = (lab.random(n) < pi_f).astype(float)
        yhat = np.where(lab.random(n) < acc_f, y, 1.0 - y)
        if variant == "fixed":
            unl = fixed
        else:
            unl = np.zeros(big_n)
            unl[: int(unl_rng.binomial(big_n, float(mu)))] = 1.0
        lo, hi = _flat(*ppi_mean_ci(y, yhat, unl, alpha=a, lam=1))
        counts["ppi"] += bool(lo[0] <= pi_f <= hi[0])
        lo, hi = _flat(*ppi_mean_ci(y, yhat, unl, alpha=a))
        counts["ppi++"] += bool(lo[0] <= pi_f <= hi[0])
        if variant == "fixed":
            lo_w, hi_w = classical_mean_ci(y, alpha=a)
            counts["wald"] += bool(lo_w <= pi_f <= hi_w)
    if variant != "fixed":
        counts.pop("wald")
    return {
        "uid": mc_id(cell, variant),
        "cell": list(cell),
        "variant": variant,
        "draws": study.mc_draws,
        "covered": counts,
        "elapsed_s": round(time.perf_counter() - t0, 3),
    }


def run_mc(
    study: PPIStudy,
    out_dir: str | Path,
    workers: int | None = None,
    force: bool = False,
    echo: Callable[[str], None] | None = print,
) -> int:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    library_impl()
    w = max(1, min(int(workers or study.workers), MAX_WORKERS))
    _start_meta(out, study, "mc", w, force)
    jobs = {mc_id(c, v): (c, v, study) for c in study.mc_cells for v in MC_VARIANTS}
    return _run_jobs(jobs, _mc_job, out / "mc.jsonl", out / "progress.log", w, echo)


# --- report -----------------------------------------------------------------------------


def _records(path: Path) -> list[dict[str, Any]]:
    return list(load_done(path).values())


def coverage_table(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """One row per (method, alpha, n, acc, pi), with the below-nominal flag."""
    rows = []
    for rec in records:
        for key, res in rec["results"].items():
            method, alpha = key.split("|")
            nominal = 1 - Fraction(alpha)
            rows.append(
                {
                    "method": method,
                    "alpha": alpha,
                    "n": rec["n"],
                    "acc": rec["acc"],
                    "pi": rec["pi"],
                    "coverage": res["coverage"],
                    "coverage_decimal": res["coverage_decimal"],
                    "nominal": float(nominal),
                    "below_nominal": res["coverage"] < float(nominal - BELOW),
                    "shortfall": float(nominal) - res["coverage"],
                    "unevaluated": res["unevaluated"],
                    "mean_width": res["mean_width"],
                    "zero_width_mass": res["zero_width_mass"],
                    "nan_mass": res["nan_mass"],
                    "near_endpoint": res.get("near_endpoint", 0),
                    "batch_flips": res.get("batch_flips", 0),
                }
            )
    order = {m: i for i, m in enumerate(METHODS)}
    rows.sort(
        key=lambda r: (order[r["method"]], -float(r["alpha"]), r["n"], r["acc"], float(r["pi"]))
    )
    return rows


def _cp_interval(k: int, n: int, level: float) -> tuple[float, float]:
    return clopper_pearson(k, n, 1 - level)


def hypothesis_checks(rows: list[dict[str, Any]]) -> list[str]:
    """Mechanical verdict inputs for DESIGN 15.3 hypotheses 11-14."""
    by = {(r["method"], r["alpha"], r["n"], r["acc"], r["pi"]): r for r in rows}
    cells = {(r["alpha"], r["n"], r["acc"], r["pi"]) for r in rows}
    out = []

    def tally(name: str, keys: list[tuple[str, str, int, str, str]], want_below: bool) -> None:
        keys = [k for k in keys if k in by]
        hits = [k for k in keys if by[k]["below_nominal"] == want_below]
        miss = [k for k in keys if by[k]["below_nominal"] != want_below]
        word = "below nominal" if want_below else "not below nominal"
        line = f"- {name}: {len(hits)} of {len(keys)} cells {word}"
        if miss:
            shown = ", ".join(
                f"{m} a={a} n={n} acc={c} pi={p} ({by[(m, a, n, c, p)]['coverage']:.4f})"
                for m, a, n, c, p in miss[:12]
            )
            line += f"; exceptions: {shown}" + (" ..." if len(miss) > 12 else "")
        out.append(line)

    h11 = [
        ("ppi", a, n, c, p)
        for a, n, c, p in sorted(cells)
        if p != "0.5" and Fraction(c) ** n >= Fraction(a)
    ]
    tally("H11 PPI, pi != 0.5 and acc^n >= alpha", h11, True)
    tally(
        "H11 PPI, pi = 0.5",
        [("ppi", a, n, c, p) for a, n, c, p in sorted(cells) if p == "0.5"],
        False,
    )
    h12 = [("ppi++", a, n, c, p) for a, n, c, p in sorted(cells) if p == "0.02" and n <= 100]
    tally("H12 PPI++, pi = 0.02 and n <= 100", h12, True)
    bound_ok = sum(
        by[("ppi++", a, n, c, p)]["coverage"] <= 1 - (1 - float(Fraction(p))) ** n + 1e-12
        for a, n, c, p in cells
        if ("ppi++", a, n, c, p) in by
    )
    out.append(
        f"- H12 bound coverage <= 1 - (1 - pi)^n holds in {bound_ok} of "
        f"{sum(('ppi++', *k) in by for k in cells)} PPI++ cells"
    )
    low = [(a, n, c, p) for a, n, c, p in cells if p in ("0.02", "0.1")]
    lower = sum(
        by[("ppi++", *k)]["coverage"] < by[("ppi", *k)]["coverage"]
        for k in low
        if ("ppi++", *k) in by and ("ppi", *k) in by
    )
    out.append(f"- H12 PPI++ below PPI in {lower} of {len(low)} cells with pi <= 0.1")
    tally(
        "H13 Wald, pi = 0.02",
        [("wald", a, n, c, p) for a, n, c, p in sorted(cells) if p == "0.02"],
        True,
    )
    tally(
        "H13 Wald, pi = 0.1 and n <= 50",
        [("wald", a, n, c, p) for a, n, c, p in sorted(cells) if p == "0.1" and n <= 50],
        True,
    )
    cp = [r for r in rows if r["method"] == "clopper_pearson"]
    if cp:
        worst = min(cp, key=lambda r: r["coverage"] - r["nominal"])
        out.append(
            f"- H13 Clopper-Pearson: minimum coverage minus nominal "
            f"{worst['coverage'] - worst['nominal']:+.4f} (n={worst['n']}, pi={worst['pi']}, "
            f"alpha={worst['alpha']}); below 1 - alpha in "
            f"{sum(r['coverage'] < r['nominal'] for r in cp)} of {len(cp)} cells"
        )
    for m in ("ppi", "ppi++"):
        tally(
            f"H14 {m}, pi in (0.3, 0.5) and n >= 100",
            [(m, a, n, c, p) for a, n, c, p in sorted(cells) if p in ("0.3", "0.5") and n >= 100],
            False,
        )
    return out


def _fmt_cov(r: dict[str, Any]) -> str:
    s = f"{r['coverage']:.3f}"
    return f"**{s}**" if r["below_nominal"] else s


def map_markdown(rows: list[dict[str, Any]], meta: dict[str, Any]) -> str:
    """The coverage map: one table per method and alpha, flags for below-nominal cells."""
    by = {(r["method"], r["alpha"], r["n"], r["acc"], r["pi"]): r for r in rows}
    cfg = meta["study"]
    ns, accs, pis = cfg["n"], cfg["acc"], cfg["pi"]
    lines = ["# Exact coverage of prediction-powered mean intervals", ""]
    vers = meta.get("versions", {})
    lines += [
        "Generated by `python -m conformcheck.ppi report` from `units.jsonl` and `run.json`.",
        "",
        f"ppi-python {vers.get('ppi-python')}, numpy {vers.get('numpy')}, scipy "
        f"{vers.get('scipy')}, statsmodels {vers.get('statsmodels')}, Python "
        f"{vers.get('python')}. Unlabelled judge labels: N = {cfg['n_unlabelled']} with mean "
        f"exactly mu = pi acc + (1 - pi)(1 - acc). Outcomes left unevaluated: at most "
        f"{max(r['unevaluated'] for r in rows):.1e} of probability per cell.",
        "",
        "Coverage in **bold** is below nominal by more than one point "
        "(under 1 - alpha - 0.01). Exact values, no sampling error.",
        "",
    ]
    counts = []
    for m in METHODS:
        for a in cfg["alphas"]:
            sub = [r for r in rows if r["method"] == m and r["alpha"] == a]
            if sub:
                counts.append(
                    f"| {m} | {a} | {sum(r['below_nominal'] for r in sub)} / {len(sub)} | "
                    f"{min(r['coverage'] for r in sub):.4f} |"
                )
    lines += [
        "## Cells below nominal",
        "",
        "| method | alpha | below nominal | lowest coverage |",
        "|---|---|---|---|",
        *counts,
        "",
        "## Largest n below nominal",
        "",
        "Largest n in the grid that is below nominal (`-`: none), per judge accuracy and "
        "base rate. Coverage is not monotone in n, so a smaller n can pass.",
        "",
    ]
    for a in cfg["alphas"]:
        lines += [
            f"### alpha = {a}",
            "",
            "| acc | pi | " + " | ".join(m for m in METHODS) + " |",
            "|---|---|" + "---|" * len(METHODS),
        ]
        for c in accs:
            for p in pis:
                cells = []
                for m in METHODS:
                    below = [
                        n
                        for n in ns
                        if (m, a, n, c, p) in by and by[(m, a, n, c, p)]["below_nominal"]
                    ]
                    cells.append(str(max(below)) if below else "-")
                lines.append(f"| {c} | {p} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## Coverage", ""]
    for m in METHODS:
        for a in cfg["alphas"]:
            if not any((m, a, n, c, p) in by for n in ns for c in accs for p in pis):
                continue
            lines += [
                f"### {m}, alpha = {a} (nominal {1 - Fraction(a)})",
                "",
                "| acc | pi | " + " | ".join(f"n={n}" for n in ns) + " |",
                "|---|---|" + "---|" * len(ns),
            ]
            rows_seen = set()
            for c in accs:
                for p in pis:
                    if m in ("wald", "clopper_pearson"):
                        if p in rows_seen:
                            continue
                        rows_seen.add(p)
                        label = "any"
                    else:
                        label = c
                    vals = [
                        _fmt_cov(by[(m, a, n, c, p)]) if (m, a, n, c, p) in by else "" for n in ns
                    ]
                    lines.append(f"| {label} | {p} | " + " | ".join(vals) + " |")
            lines.append("")
    lines += ["## Hypothesis checks (DESIGN 15.3)", "", *hypothesis_checks(rows), ""]
    flips = sum(r["batch_flips"] for r in rows)
    near = sum(r["near_endpoint"] for r in rows)
    lines += [
        "## Evaluation checks",
        "",
        f"- Outcomes with an endpoint within {NEAR:g} of pi, re-evaluated one at a time: "
        f"{near}; verdicts changed by the re-evaluation: {flips}.",
        f"- Mass of outcomes with a NaN or infinite endpoint: "
        f"{max(r['nan_mass'] for r in rows):.3g} at most per cell.",
        "",
    ]
    return "\n".join(lines)


def mc_markdown(
    mc: list[dict[str, Any]], rows: list[dict[str, Any]], level: float = 0.99
) -> tuple[str, int]:
    """Monte Carlo against exact; returns the markdown and the number of disagreements."""
    by = {(r["method"], r["alpha"], r["n"], r["acc"], r["pi"]): r for r in rows}
    lines = [
        "# Monte Carlo cross-check",
        "",
        "Generated by `python -m conformcheck.ppi report`. Raw labelled draws passed one at a",
        "time to `ppi_mean_ci` / `classical_mean_ci`. `fixed`: the exact study's unlabelled",
        "array (must agree with the exact coverage); `binomial`: an unlabelled count drawn",
        f"from Binomial(N, mu) per sample (the unconditional coverage). Intervals: "
        f"{level:.0%} Clopper-Pearson.",
        "",
        "| n | acc | pi | alpha | method | variant | draws | MC coverage | interval | exact | "
        "agrees |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    bad = 0
    for rec in sorted(mc, key=lambda r: (r["cell"][0], r["cell"][1], r["cell"][2], r["variant"])):
        n, acc, pi, alpha = rec["cell"]
        for m, k in rec["covered"].items():
            lo, hi = _cp_interval(k, rec["draws"], level)
            ex = by.get((m, alpha, n, acc, pi))
            exact = ex["coverage"] if ex else float("nan")
            if rec["variant"] == "fixed":
                ok = lo <= exact <= hi
                bad += not ok
                verdict = "yes" if ok else "**no**"
            else:
                verdict = "(not compared)"
            lines.append(
                f"| {n} | {acc} | {pi} | {alpha} | {m} | {rec['variant']} | {rec['draws']} | "
                f"{k / rec['draws']:.4f} | [{lo:.4f}, {hi:.4f}] | {exact:.4f} | {verdict} |"
            )
    lines += ["", f"Fixed-variant comparisons outside the interval: {bad}.", ""]
    return "\n".join(lines), bad


def write_report(run_dir: str | Path, to: str | Path | None = None) -> dict[str, Any]:
    """``coverage.csv``, ``map.md`` and (when ``mc.jsonl`` exists) ``mc.md`` into ``to``."""
    run_dir = Path(run_dir)
    dest = Path(to) if to else run_dir
    dest.mkdir(parents=True, exist_ok=True)
    meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    records = _records(run_dir / "units.jsonl")
    expected = len(meta["study"]["n"]) * len(meta["study"]["acc"]) * len(meta["study"]["pi"])
    rows = coverage_table(records)
    cols = list(rows[0])
    csv = [",".join(cols)] + [",".join(str(r[c]) for c in cols) for r in rows]
    (dest / "coverage.csv").write_text("\n".join(csv) + "\n", encoding="utf-8")
    (dest / "map.md").write_text(map_markdown(rows, meta), encoding="utf-8")
    summary: dict[str, Any] = {"units": len(records), "units_expected": expected}
    mc_path = run_dir / "mc.jsonl"
    if mc_path.exists():
        text, bad = mc_markdown(_records(mc_path), rows)
        (dest / "mc.md").write_text(text, encoding="utf-8")
        summary["mc_disagreements"] = bad
    return summary


# --- command line -----------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m conformcheck.ppi", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("run", "mc"):
        p = sub.add_parser(name)
        p.add_argument("--study", default="ppi")
        p.add_argument("--out", required=True)
        p.add_argument("--workers", type=int)
        p.add_argument("--force", action="store_true")
        if name == "run":
            p.add_argument("--impl", choices=("library", "reference"), default="library")
    p = sub.add_parser("report")
    p.add_argument("run_dir")
    p.add_argument("--to")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "run":
            return run(load_ppi_study(args.study), args.out, args.workers, args.impl, args.force)
        if args.cmd == "mc":
            return run_mc(load_ppi_study(args.study), args.out, args.workers, args.force)
        summary = write_report(args.run_dir, args.to)
        print(json.dumps(summary))
        if summary["units"] != summary["units_expected"]:
            print("error: the run is incomplete", file=sys.stderr)
            return 1
        return 1 if summary.get("mc_disagreements") else 0
    except (ValueError, FileNotFoundError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
