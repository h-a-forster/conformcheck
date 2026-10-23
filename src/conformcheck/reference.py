"""Reference implementations of every method under test, and deliberately wrong mutants.

Written directly from the papers in numpy, one short function each. They serve two
purposes:

1. Differential oracle: on identical inputs a non-randomized library method should
   return the same interval or set as its reference (up to documented conventions).
2. Oracle self-test: the reference must PASS every statistical cell and each mutant must
   be detected, which measures the size and power of the test layer.

Conventions: ``alpha`` is an exact :class:`fractions.Fraction` (see
:func:`conformcheck.laws.as_fraction`); the split threshold is the ``k``-th smallest
calibration score with ``k = ceil((n + 1)(1 - alpha))``, ``+inf`` when ``k > n``; sets
and intervals are closed. The order statistic is computed here independently of
:mod:`conformcheck.laws` so that the two can check each other.

References: Vovk et al. (2005); Lei et al. (2018); Romano, Patterson and Candes (2019);
Romano, Sesia and Candes (2020); Vovk (2012); Barber et al. (2021).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction

import numpy as np
from numpy.typing import NDArray

# Fixed RAPS regularisation used by the reference and by every library that takes it as
# a parameter (puncc, TorchCP). MAPIE tunes its own (docs/DESIGN.md, section 5.1).
RAPS_LAMBDA = 0.1
RAPS_KREG = 1

MUTANTS: tuple[str, ...] = (
    "k_minus_1",
    "k_plus_1",
    "no_correction_linear",
    "n_instead_of_n_plus_1",
)


def _kth_smallest(scores: NDArray[np.float64], k: int) -> float:
    """``k``-th smallest (1-based); ``+inf`` for ``k > n`` and ``-inf`` for ``k < 1``."""
    n = scores.size
    if k > n:
        return math.inf
    if k < 1:
        return -math.inf
    return float(np.partition(scores, k - 1)[k - 1])


def conformal_threshold(scores: NDArray[np.float64], alpha: Fraction) -> float:
    """Split conformal threshold: the ``ceil((n + 1)(1 - alpha))``-th smallest score."""
    s = np.asarray(scores, dtype=float)
    k = math.ceil((s.size + 1) * (1 - Fraction(alpha)))
    return _kth_smallest(s, k)


def mutant_threshold(scores: NDArray[np.float64], alpha: Fraction, mutant: str) -> float:
    """Deliberately wrong thresholds used to measure the power of the oracle."""
    s = np.asarray(scores, dtype=float)
    n = s.size
    a = Fraction(alpha)
    k = math.ceil((n + 1) * (1 - a))
    if mutant == "k_minus_1":
        return _kth_smallest(s, min(k, n + 1) - 1)
    if mutant == "k_plus_1":
        return _kth_smallest(s, k + 1)
    if mutant == "no_correction_linear":
        return float(np.quantile(s, float(1 - a), method="linear"))
    if mutant == "n_instead_of_n_plus_1":
        return _kth_smallest(s, math.ceil(n * (1 - a)))
    raise ValueError(f"unknown mutant {mutant!r}")


def _threshold(scores: NDArray[np.float64], alpha: Fraction, mutant: str | None) -> float:
    return (
        conformal_threshold(scores, alpha)
        if mutant is None
        else mutant_threshold(scores, alpha, mutant)
    )


# --- regression -------------------------------------------------------------------------


def split_abs(
    y_cal: NDArray[np.float64],
    y_hat_cal: NDArray[np.float64],
    y_hat_test: NDArray[np.float64],
    alpha: Fraction,
    mutant: str | None = None,
) -> NDArray[np.float64]:
    """Split conformal with the absolute residual score; returns ``(m, 2)`` intervals."""
    scores = np.abs(np.asarray(y_cal, float) - np.asarray(y_hat_cal, float))
    q = _threshold(scores, alpha, mutant)
    yt = np.asarray(y_hat_test, dtype=float)
    return np.column_stack([yt - q, yt + q])


def cqr(
    lo_cal: NDArray[np.float64],
    hi_cal: NDArray[np.float64],
    y_cal: NDArray[np.float64],
    lo_test: NDArray[np.float64],
    hi_test: NDArray[np.float64],
    alpha: Fraction,
    symmetric: bool = True,
) -> NDArray[np.float64]:
    """Conformalized quantile regression (Romano, Patterson and Candes 2019).

    Symmetric: score ``max(lo - y, y - hi)``, interval ``[lo - q, hi + q]``. Asymmetric:
    each side is a one-sided split conformal correction at level ``alpha / 2`` with its
    own scores ``lo - y`` and ``y - hi``.
    """
    y = np.asarray(y_cal, float)
    lo_c, hi_c = np.asarray(lo_cal, float), np.asarray(hi_cal, float)
    lo_t, hi_t = np.asarray(lo_test, float), np.asarray(hi_test, float)
    if symmetric:
        q = conformal_threshold(np.maximum(lo_c - y, y - hi_c), alpha)
        return np.column_stack([lo_t - q, hi_t + q])
    half = Fraction(alpha) / 2
    q_lo = conformal_threshold(lo_c - y, half)
    q_hi = conformal_threshold(y - hi_c, half)
    return np.column_stack([lo_t - q_lo, hi_t + q_hi])


def jackknife_plus(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    x_test: NDArray[np.float64],
    alpha: Fraction,
    factory: Callable[[], object],
) -> NDArray[np.float64]:
    """Jackknife+ (Barber et al. 2021): leave-one-out models, ``n`` folds of size one."""
    return cv_plus(x, y, x_test, alpha, factory, folds=[np.array([i]) for i in range(len(y))])


def kfold_indices(n: int, n_folds: int, rng: np.random.Generator) -> list[NDArray[np.int64]]:
    """A random partition of ``0..n-1`` into ``n_folds`` folds of near-equal size."""
    perm = rng.permutation(n)
    return [np.sort(f) for f in np.array_split(perm, n_folds)]


def cv_plus(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    x_test: NDArray[np.float64],
    alpha: Fraction,
    factory: Callable[[], object],
    folds: list[NDArray[np.int64]],
) -> NDArray[np.float64]:
    """CV+ (Barber et al. 2021, Section 3).

    For each point ``i`` in fold ``f(i)``, ``R_i = |y_i - mu_{-f(i)}(x_i)|``. The upper
    end is the ``ceil((1 - alpha)(n + 1))``-th smallest of ``mu_{-f(i)}(x) + R_i`` and the
    lower end the ``floor(alpha (n + 1))``-th smallest of ``mu_{-f(i)}(x) - R_i``
    (``+inf`` / ``-inf`` when the index is out of range).
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    xt = np.asarray(x_test, float)
    n = y.size
    a = Fraction(alpha)
    upper_idx = math.ceil((1 - a) * (n + 1))
    lower_idx = math.floor(a * (n + 1))
    mu_test = np.empty((n, xt.shape[0]))
    resid = np.empty(n)
    for fold in folds:
        train = np.setdiff1d(np.arange(n), fold)
        model = factory()
        model.fit(x[train], y[train])  # type: ignore[attr-defined]
        resid[fold] = np.abs(y[fold] - model.predict(x[fold]))  # type: ignore[attr-defined]
        mu_test[fold] = model.predict(xt)[None, :]  # type: ignore[attr-defined]
    hi_vals = np.sort(mu_test + resid[:, None], axis=0)
    lo_vals = np.sort(mu_test - resid[:, None], axis=0)
    hi = hi_vals[upper_idx - 1] if upper_idx <= n else np.full(xt.shape[0], np.inf)
    lo = lo_vals[lower_idx - 1] if lower_idx >= 1 else np.full(xt.shape[0], -np.inf)
    return np.column_stack([lo, hi])


# --- classification ---------------------------------------------------------------------


def lac(
    proba_cal: NDArray[np.float64],
    y_cal: NDArray[np.int64],
    proba_test: NDArray[np.float64],
    alpha: Fraction,
    mutant: str | None = None,
) -> NDArray[np.bool_]:
    """Least ambiguous set-valued classifier: score ``1 - p_y``; set ``{y : 1 - p_y <= q}``."""
    p = np.asarray(proba_cal, float)
    scores = 1.0 - p[np.arange(p.shape[0]), np.asarray(y_cal)]
    q = _threshold(scores, alpha, mutant)
    return (1.0 - np.asarray(proba_test, float)) <= q


def class_conditional_lac(
    proba_cal: NDArray[np.float64],
    y_cal: NDArray[np.int64],
    proba_test: NDArray[np.float64],
    alpha: Fraction,
) -> NDArray[np.bool_]:
    """Mondrian (label-conditional) LAC (Vovk 2012): one threshold per class from its own
    calibration scores; a class with too few points is always included."""
    p = np.asarray(proba_cal, float)
    y = np.asarray(y_cal)
    pt = np.asarray(proba_test, float)
    out = np.zeros(pt.shape, dtype=bool)
    for c in range(pt.shape[1]):
        scores = 1.0 - p[y == c, c]
        out[:, c] = (1.0 - pt[:, c]) <= conformal_threshold(scores, alpha)
    return out


def _aps_scores(proba: NDArray[np.float64], u: NDArray[np.float64] | None) -> NDArray[np.float64]:
    """APS score of every label: mass of labels ranked strictly above it, plus ``u p_y``
    (randomized) or ``p_y`` (deterministic). Ties in probability are broken by label index."""
    p = np.asarray(proba, float)
    order = np.argsort(-p, axis=1, kind="stable")
    sorted_p = np.take_along_axis(p, order, axis=1)
    before = np.cumsum(sorted_p, axis=1) - sorted_p
    own = sorted_p if u is None else u[:, None] * sorted_p
    out = np.empty_like(p)
    np.put_along_axis(out, order, before + own, axis=1)
    return out


def aps(
    proba_cal: NDArray[np.float64],
    y_cal: NDArray[np.int64],
    proba_test: NDArray[np.float64],
    alpha: Fraction,
    randomized: bool,
    rng: np.random.Generator | None = None,
) -> NDArray[np.bool_]:
    """Adaptive prediction sets (Romano, Sesia and Candes 2020).

    Randomized: one uniform ``U`` per calibration and per test point; the set is every
    label whose randomized score is at most the threshold, so calibration and test scores
    are exchangeable and the exact split law holds.
    """
    if randomized and rng is None:
        raise ValueError("randomized APS needs an rng")
    pc = np.asarray(proba_cal, float)
    pt = np.asarray(proba_test, float)
    u_cal = rng.uniform(size=pc.shape[0]) if randomized else None  # type: ignore[union-attr]
    u_test = rng.uniform(size=pt.shape[0]) if randomized else None  # type: ignore[union-attr]
    cal_all = _aps_scores(pc, u_cal)
    scores = cal_all[np.arange(pc.shape[0]), np.asarray(y_cal)]
    q = conformal_threshold(scores, alpha)
    return _aps_scores(pt, u_test) <= q


def _raps_scores(
    proba: NDArray[np.float64], u: NDArray[np.float64] | None, lambd: float, k_reg: int
) -> NDArray[np.float64]:
    """RAPS score of every label: the APS score plus ``lambd * max(0, o - k_reg)``, with
    ``o`` the 1-based rank of the label by decreasing probability (ties by label index)."""
    p = np.asarray(proba, float)
    order = np.argsort(-p, axis=1, kind="stable")
    rank = np.empty_like(order)
    np.put_along_axis(rank, order, np.broadcast_to(np.arange(1, p.shape[1] + 1), p.shape), axis=1)
    return _aps_scores(p, u) + lambd * np.maximum(0, rank - k_reg)


def raps(
    proba_cal: NDArray[np.float64],
    y_cal: NDArray[np.int64],
    proba_test: NDArray[np.float64],
    alpha: Fraction,
    randomized: bool,
    rng: np.random.Generator | None = None,
    lambd: float = RAPS_LAMBDA,
    k_reg: int = RAPS_KREG,
) -> NDArray[np.bool_]:
    """Regularized adaptive prediction sets (Angelopoulos, Bates, Malik and Jordan 2021)
    with fixed ``lambd`` and ``k_reg``. Same structure as :func:`aps`: one uniform per
    calibration and per test point when randomized; the set is every label whose score
    is at most the ``k``-th smallest calibration score."""
    if randomized and rng is None:
        raise ValueError("randomized RAPS needs an rng")
    pc = np.asarray(proba_cal, float)
    pt = np.asarray(proba_test, float)
    u_cal = rng.uniform(size=pc.shape[0]) if randomized else None  # type: ignore[union-attr]
    u_test = rng.uniform(size=pt.shape[0]) if randomized else None  # type: ignore[union-attr]
    cal_all = _raps_scores(pc, u_cal, lambd, k_reg)
    scores = cal_all[np.arange(pc.shape[0]), np.asarray(y_cal)]
    q = conformal_threshold(scores, alpha)
    return _raps_scores(pt, u_test, lambd, k_reg) <= q


def smoothed_lac(
    proba_cal: NDArray[np.float64],
    y_cal: NDArray[np.int64],
    proba_test: NDArray[np.float64],
    alpha: Fraction,
    rng: np.random.Generator,
) -> NDArray[np.bool_]:
    """Smoothed conformal p-values (Vovk et al. 2005) with the LAC score.

    ``p_y = (#{s_i > s} + U (#{s_i = s} + 1)) / (n + 1)``; the set is ``{y : p_y > alpha}``
    and its coverage is exactly ``1 - alpha`` for every ``n``.
    """
    pc = np.asarray(proba_cal, float)
    cal = np.sort(1.0 - pc[np.arange(pc.shape[0]), np.asarray(y_cal)])
    test = 1.0 - np.asarray(proba_test, float)
    n = cal.size
    greater = n - np.searchsorted(cal, test, side="right")
    equal = np.searchsorted(cal, test, side="right") - np.searchsorted(cal, test, side="left")
    u = rng.uniform(size=test.shape)
    pvals = (greater + u * (equal + 1)) / (n + 1)
    return pvals > float(alpha)
