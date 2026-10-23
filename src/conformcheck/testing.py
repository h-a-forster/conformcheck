"""Public helpers for library authors who want conformance checks in their own CI.

Example::

    from conformcheck.testing import check_split_regressor

    def my_split(x_cal, y_cal, x_test, alpha, model):  # returns (m, 2) intervals
        ...

    report = check_split_regressor(my_split, n=(9, 19, 99), alpha=(0.1, 0.2), reps=200)
    report.assert_valid(allow_conservative=False)

``check_split_classifier`` is the classification analogue: the callable receives
``(x_cal, y_cal, x_test, alpha, model)`` with a fixed 4-class softmax model (it has
``predict_proba``) and returns a boolean ``(m, 4)`` set matrix. With ``score="lac"`` it
also brackets the order statistic between the largest included and smallest excluded
``1 - p`` test score (deterministic, any ``n``).

Each (n, alpha) cell runs ``reps`` independent calibration draws from the built-in
DGPs (``reg_gauss``, ``cls_gauss``). Regression cells can also get rank recovery (the
order statistic used, read off the intervals), which is deterministic; it assumes the
absolute-residual score and is controlled by ``score`` (see :func:`check_split_regressor`).
Statistical cells use the exact BetaBinomial law (mean and goodness-of-fit tests) with
Holm across all cells. A Holm rejection is ``FAIL`` or ``CONSERVATIVE`` when the mean
test alone rejects (by the sign of the deviation) and ``LAW_MISMATCH`` when only the
goodness-of-fit test does (right mean, wrong distribution).
``alpha`` is read as the exact decimal it denotes; the callable receives a float.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

import numpy as np

from conformcheck import diagnostics, laws, stats
from conformcheck.data import get_dgp, rep_seed_sequence

RegressorFn = Callable[..., np.ndarray]
ClassifierFn = Callable[..., np.ndarray]
Score = Literal["auto", "abs", "other"]
SCORES = ("auto", "abs", "other")
SetScore = Literal["lac", "other"]
SET_SCORES = ("lac", "other")


@dataclass
class CheckCell:
    n: int
    alpha: Fraction
    k: int
    coverage: float
    target: float
    p_value: float | None
    rank_offsets: dict[float, int] = field(default_factory=dict)
    p_holm: float | None = None
    p_mean: float | None = None
    p_gof: float | None = None
    rank_skipped: int = 0  # reps where ``score="auto"`` found intervals not of abs form
    status: str = "PASS"
    detail: str = ""


@dataclass
class ConformanceReport:
    """Result of a check; ``assert_valid`` raises ``AssertionError`` with a summary."""

    name: str
    cells: list[CheckCell]
    reps: int
    test_points: int
    fwer: float

    @property
    def ok(self) -> bool:
        return all(c.status == "PASS" for c in self.cells)

    def failures(self, allow_conservative: bool = False) -> list[CheckCell]:
        bad = {"FAIL", "LAW_MISMATCH", "ERROR"}
        if not allow_conservative:
            bad.add("CONSERVATIVE")
        return [c for c in self.cells if c.status in bad]

    def summary(self) -> str:
        lines = [
            f"conformcheck {self.name}: {len(self.cells)} cells, R={self.reps}, "
            f"m={self.test_points}, Holm FWER {self.fwer}"
        ]
        for c in self.cells:
            p = "" if c.p_holm is None else f" Holm p={c.p_holm:.2g}"
            lines.append(
                f"  n={c.n:<5d} alpha={float(c.alpha):<6g} k={c.k:<5d} {c.status:<12s} "
                f"coverage {c.coverage:.4f} (exact {c.target:.4f}){p} {c.detail}".rstrip()
            )
        return "\n".join(lines)

    def assert_valid(self, allow_conservative: bool = False) -> None:
        bad = self.failures(allow_conservative)
        if bad:
            raise AssertionError(
                f"{len(bad)} of {len(self.cells)} conformance cells failed\n" + self.summary()
            )

    def __str__(self) -> str:
        return self.summary()


def _as_tuple(v: int | float | str | Iterable) -> tuple:  # type: ignore[type-arg]
    if isinstance(v, int | float | str | Fraction):
        return (v,)
    return tuple(v)


def _settings(reps: int | None, test_points: int | None, seed: int | None):  # type: ignore[no-untyped-def]
    try:
        from conformcheck.pytest_plugin import current_settings

        s = current_settings()
    except Exception:  # noqa: BLE001 - plugin not active
        s = None
    r = reps if reps is not None else (s.reps if s else 200)
    m = test_points if test_points is not None else (s.test_points if s else 500)
    sd = seed if seed is not None else (s.seed if s else 0)
    return r, m, sd


def _finish(name: str, cells: list[CheckCell], reps: int, m: int, fwer: float):  # type: ignore[no-untyped-def]
    stat = [c for c in cells if c.p_value is not None]
    if stat:
        h = stats.holm([c.p_value for c in stat], fwer)
        for c, adj, rej, thr in zip(stat, h.adjusted, h.reject, h.thresholds, strict=True):
            c.p_holm = float(adj)
            if not rej or c.status != "PASS":
                continue
            # as in report.adjust: the mean test alone (Bonferroni factor 2) decides the
            # direction; a rejection driven only by the goodness-of-fit test is a law
            # mismatch, not under- or over-coverage
            assert c.p_mean is not None
            mean_alone = min(1.0, 2 * c.p_mean) if c.p_gof is not None else c.p_mean
            if mean_alone <= thr:
                c.status = "FAIL" if c.coverage < c.target else "CONSERVATIVE"
            else:
                c.status = "LAW_MISMATCH"
                c.detail = (c.detail + " " if c.detail else "") + "distribution differs from law"
    return ConformanceReport(name, cells, reps, m, fwer)


def check_split_regressor(
    fn: RegressorFn,
    n: int | Iterable[int] = (9, 19, 99),
    alpha: float | str | Iterable = (0.1, 0.2),  # type: ignore[type-arg]
    reps: int | None = None,
    test_points: int | None = None,
    seed: int | None = None,
    fwer: float = 0.05,
    score: Score = "auto",
) -> ConformanceReport:
    """Check a split-conformal regression callable against the exact laws.

    ``fn(x_cal, y_cal, x_test, alpha, model)`` must return ``(m, 2)`` intervals; ``model``
    is a fixed fitted regressor (``predict``).

    ``score`` controls rank recovery, which reads the order statistic off the intervals
    assuming the absolute-residual score ``|y - model.predict(x)|``:

    * ``"abs"``: always use it (the method is declared to use that score);
    * ``"other"``: never use it; only the statistical test applies (any valid score, for
      example a normalised residual, follows the same exact law);
    * ``"auto"`` (default): use it in a repetition only when the intervals have the form
      the absolute-residual score produces (each endpoint at a constant offset from the
      prediction); otherwise skip it for that repetition.
    """
    if score not in SCORES:
        raise ValueError(f"score must be one of {SCORES}, got {score!r}")
    reps, m, seed = _settings(reps, test_points, seed)
    dgp = get_dgp("reg_gauss")
    model = dgp.model()
    cells: list[CheckCell] = []
    for nn in _as_tuple(n):
        for a_raw in _as_tuple(alpha):
            a = laws.as_fraction(a_raw)
            k = laws.split_index(nn, a)
            counts, offsets, nontrivial, skipped = [], {}, 0, 0
            for rep in range(reps):
                d = dgp.draw(
                    np.random.default_rng(rep_seed_sequence(seed, "check", nn, rep)), nn, m
                )
                iv = np.asarray(fn(d.x_cal, d.y_cal, d.x_test, float(a), model), dtype=float)
                if iv.shape != (m, 2):
                    raise ValueError(f"expected intervals of shape {(m, 2)}, got {iv.shape}")
                counts.append(int(np.sum((iv[:, 0] <= d.y_test) & (d.y_test <= iv[:, 1]))))
                nontrivial += k > nn and not diagnostics.is_trivial(iv, None)
                if score == "other":
                    continue
                pred_test = model.predict(d.x_test)
                if score == "auto" and not _abs_form(iv, pred_test):
                    skipped += 1
                    continue
                ranks = diagnostics.regression_ranks(
                    "split_abs", "", iv, d.y_cal, model.predict(d.x_cal), pred_test
                )
                if ranks:
                    off = max((r.offset(k) for r in ranks), key=abs)
                    offsets[off] = offsets.get(off, 0) + 1
            cell = _cell(nn, a, k, np.array(counts), m, offsets, nontrivial)
            cell.rank_skipped = skipped
            cells.append(cell)
    return _finish("check_split_regressor", cells, reps, m, fwer)


def check_split_classifier(
    fn: ClassifierFn,
    n: int | Iterable[int] = (9, 19, 99),
    alpha: float | str | Iterable = (0.1, 0.2),  # type: ignore[type-arg]
    reps: int | None = None,
    test_points: int | None = None,
    seed: int | None = None,
    fwer: float = 0.05,
    score: SetScore = "other",
) -> ConformanceReport:
    """Check a split-conformal classification callable (boolean ``(m, 4)`` sets).

    ``score="lac"`` declares that the sets are ``{y : 1 - p_y <= q}`` (LAC, or any method
    thresholding that score). Each repetition then also brackets the order statistic
    used, which detects a one-step error at any ``n``; a repetition whose sets are not
    threshold sets of ``1 - p_y`` is a ``FAIL`` ("not a threshold set"). The default
    ``"other"`` runs the statistical tests only, which suit any score (APS, RAPS, ...).
    """
    if score not in SET_SCORES:
        raise ValueError(f"score must be one of {SET_SCORES}, got {score!r}")
    reps, m, seed = _settings(reps, test_points, seed)
    dgp = get_dgp("cls_gauss")
    model = dgp.model()
    cells: list[CheckCell] = []
    for nn in _as_tuple(n):
        for a_raw in _as_tuple(alpha):
            a = laws.as_fraction(a_raw)
            k = laws.split_index(nn, a)
            counts, nontrivial, offsets, not_threshold = [], 0, {}, 0
            for rep in range(reps):
                d = dgp.draw(
                    np.random.default_rng(rep_seed_sequence(seed, "check", nn, rep)), nn, m
                )
                sets = np.asarray(fn(d.x_cal, d.y_cal, d.x_test, float(a), model), dtype=bool)
                if sets.shape != (m, dgp.n_classes):
                    raise ValueError(
                        f"expected sets of shape {(m, dgp.n_classes)}, got {sets.shape}"
                    )
                counts.append(int(sets[np.arange(m), d.y_test].sum()))
                nontrivial += k > nn and not diagnostics.is_trivial(None, sets)
                if score != "lac" or k > nn:
                    continue
                p_cal = model.predict_proba(d.x_cal)
                cal_scores = 1.0 - p_cal[np.arange(nn), d.y_cal]
                br = diagnostics.bracket_rank(cal_scores, 1.0 - model.predict_proba(d.x_test), sets)
                if br is None:
                    continue
                off = diagnostics.bracket_offset(br, k)
                if off is None:
                    not_threshold += 1
                else:
                    offsets[off] = offsets.get(off, 0) + 1
            cell = _cell(nn, a, k, np.array(counts), m, offsets, nontrivial)
            if not_threshold:
                cell.status = "FAIL"
                cell.detail = f"not a threshold set of 1 - p in {not_threshold} reps"
            cells.append(cell)
    return _finish("check_split_classifier", cells, reps, m, fwer)


def _abs_form(iv: np.ndarray, pred: np.ndarray) -> bool:
    """True when both endpoints sit at a constant offset from the prediction (the shape
    an absolute-residual split method produces), up to float tolerance."""
    lo, hi = pred - iv[:, 0], iv[:, 1] - pred
    for side in (lo, hi):
        if np.all(np.isinf(side)):
            continue
        if not np.all(np.isfinite(side)):
            return False
        tol = diagnostics.REL_TOL * max(1.0, float(np.max(np.abs(iv[np.isfinite(iv)]))))
        if float(side.max() - side.min()) > tol:
            return False
    return True


def _cell(
    n: int,
    a: Fraction,
    k: int,
    counts: np.ndarray,
    m: int,
    offsets: dict[float, int],
    nontrivial: int,
) -> CheckCell:
    cov = float(counts.mean() / m)
    target = float(laws.marginal_coverage(n, a))
    cell = CheckCell(n, a, k, cov, target, None, offsets)
    if k > n:
        if nontrivial:
            cell.status, cell.detail = "FAIL", f"finite set where k > n in {nontrivial} reps"
        return cell
    below = [o for o in offsets if o < 0]
    above = [o for o in offsets if o > 0]
    if below:
        cell.status, cell.detail = "FAIL", f"order statistic {min(below):+g} (rank recovery)"
    elif above:
        cell.status, cell.detail = "CONSERVATIVE", f"order statistic {max(above):+g}"
    law = laws.split_count_law(n, a, m)
    cell.p_mean = stats.mean_test(counts, law).pvalue
    cell.p_gof = stats.gof_test(counts, law).pvalue
    cell.p_value = stats.cell_pvalue(cell.p_mean, cell.p_gof)
    return cell
