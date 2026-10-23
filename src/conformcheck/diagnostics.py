"""Deterministic checks that need no hypothesis test (docs/DESIGN.md, section 3.3).

* :func:`rank_range`: the order statistic a library used, read off its threshold. For a
  threshold ``q`` and calibration scores ``s`` the result is the range
  ``[#{s < q - tol} + 1, #{s <= q + tol}]``. A correct split method has ``k`` in that
  range. When the range is empty (``k_lo = k_hi + 1``) the threshold lies strictly
  between two order statistics: the library interpolates.
* :func:`regression_ranks`: per method, how the threshold is read off the returned
  intervals and which calibration scores it is compared with (split absolute residual,
  symmetric and asymmetric CQR, jackknife+ / CV+ with the constant model).
* :func:`bracket_rank`: for LAC the largest included and smallest excluded test score
  bracket the threshold, which gives a range for the order statistic (diagnostic only).
* :func:`is_trivial`: when ``k > n`` every interval must be infinite and every set full.
* :func:`compare_to_reference`: maximum endpoint difference or set disagreement rate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

REL_TOL = 1e-6  # covers float32 libraries (TorchCP); scores are continuous elsewhere


@dataclass(frozen=True)
class RankRange:
    """Range of order statistics consistent with a threshold."""

    k_lo: int
    k_hi: int
    spread: float = 0.0  # max - min of the per-test-point threshold estimates

    @property
    def interpolated(self) -> bool:
        return self.k_lo > self.k_hi

    def offset(self, k: int) -> float:
        """0 when ``k`` is consistent; ``-j`` when the threshold is ``j`` order statistics
        too low (under-coverage) and ``+j`` when too high (over-coverage). An interpolated
        threshold strictly between ``s_(j)`` and ``s_(j+1)`` has offset ``j + 0.5 - k``."""
        if self.interpolated:
            return self.k_hi + 0.5 - k
        if k < self.k_lo:
            return self.k_lo - k
        if k > self.k_hi:
            return self.k_hi - k
        return 0


def rank_range(scores: NDArray[np.float64], q: float, rel_tol: float = REL_TOL) -> RankRange:
    """Order statistics ``j`` with ``s_(j)`` equal to ``q`` within tolerance (see module doc).

    ``q = +inf`` maps to ``n + 1`` (trivial set) and ``q = -inf`` to ``0``.
    """
    s = np.asarray(scores, dtype=float)
    n = s.size
    if math.isinf(q):
        j = n + 1 if q > 0 else 0
        return RankRange(j, j)
    if math.isnan(q):
        return RankRange(0, -1)
    tol = rel_tol * max(1.0, abs(q))
    k_lo = int(np.sum(s < q - tol)) + 1
    k_hi = int(np.sum(s <= q + tol))
    return RankRange(k_lo, k_hi)


def _threshold(estimates: NDArray[np.float64]) -> tuple[float, float]:
    e = np.asarray(estimates, dtype=float)
    if np.all(np.isposinf(e)):
        return math.inf, 0.0
    if np.all(np.isneginf(e)):
        return -math.inf, 0.0
    finite = e[np.isfinite(e)]
    if finite.size != e.size:
        return math.nan, math.inf
    return float(np.median(finite)), float(finite.max() - finite.min())


def _with_spread(r: RankRange, spread: float) -> RankRange:
    return RankRange(r.k_lo, r.k_hi, spread)


def regression_ranks(
    method: str,
    variant: str,
    intervals: NDArray[np.float64],
    y_cal: NDArray[np.float64],
    pred_cal: NDArray[np.float64] | None = None,
    pred_test: NDArray[np.float64] | None = None,
    q_cal: tuple[NDArray[np.float64], NDArray[np.float64]] | None = None,
    q_test: tuple[NDArray[np.float64], NDArray[np.float64]] | None = None,
) -> list[RankRange] | None:
    """Rank recovery for one repetition and alpha; None when the method has none.

    * ``split_abs``: ``q = f(x) - lo`` and ``q = hi - f(x)`` (one range per endpoint);
      scores ``|y - f(x)|``.
    * ``cqr`` symmetric: ``q = q_lo(x) - lo`` (and ``hi - q_hi(x)``); scores
      ``max(q_lo - y, y - q_hi)``. Asymmetric: the two sides separately, scores
      ``q_lo - y`` and ``y - q_hi``. Two ranges (lower, upper endpoint) are returned.
    * ``jackknife_plus`` / ``cv_plus`` with the constant model: ``q = -lo`` and
      ``q = hi``; scores ``|y|`` (pass ``pred_cal`` and ``pred_test`` = zeros).
    """
    iv = np.asarray(intervals, dtype=float)
    lo, hi = iv[:, 0], iv[:, 1]
    y = np.asarray(y_cal, dtype=float)
    if method in ("split_abs", "jackknife_plus", "cv_plus"):
        if pred_cal is None or pred_test is None:
            return None
        pt = np.asarray(pred_test, dtype=float)
        scores = np.abs(y - np.asarray(pred_cal, dtype=float))
        with np.errstate(invalid="ignore"):
            q_lo, s_lo = _threshold(pt - lo)
            q_hi, s_hi = _threshold(hi - pt)
        # each endpoint separately: an asymmetric off-by-one shows up on one side only
        return [
            _with_spread(rank_range(scores, q_lo), s_lo),
            _with_spread(rank_range(scores, q_hi), s_hi),
        ]
    if method == "cqr":
        if q_cal is None or q_test is None:
            return None
        lo_c, hi_c = q_cal
        lo_t, hi_t = q_test
        with np.errstate(invalid="ignore"):
            q_lo, s_lo = _threshold(lo_t - lo)
            q_hi, s_hi = _threshold(hi - hi_t)
        if variant == "asymmetric":
            return [
                _with_spread(rank_range(lo_c - y, q_lo), s_lo),
                _with_spread(rank_range(y - hi_c, q_hi), s_hi),
            ]
        scores = np.maximum(lo_c - y, y - hi_c)
        return [
            _with_spread(rank_range(scores, q_lo), s_lo),
            _with_spread(rank_range(scores, q_hi), s_hi),
        ]
    return None


def bracket_rank(
    cal_scores: NDArray[np.float64],
    test_scores: NDArray[np.float64],
    sets: NDArray[np.bool_],
) -> RankRange | None:
    """Range of order statistics consistent with a set-valued output (LAC-type scores).

    The threshold ``q`` satisfies ``max included <= q < min excluded``. A correct method
    uses ``s_(k)``, so ``#{s <= a} <= k <= #{s < b}`` with ``a`` the largest included and
    ``b`` the smallest excluded test score. Returns None when every set is full or empty.
    """
    ts = np.asarray(test_scores, dtype=float)
    st = np.asarray(sets, dtype=bool)
    s = np.asarray(cal_scores, dtype=float)
    inc = ts[st]
    exc = ts[~st]
    if inc.size == 0 and exc.size == 0:  # pragma: no cover - defensive
        return None
    a = float(inc.max()) if inc.size else -math.inf
    b = float(exc.min()) if exc.size else math.inf
    tol = REL_TOL * max(1.0, abs(a) if math.isfinite(a) else 1.0)
    k_lo = int(np.sum(s <= a - tol)) if math.isfinite(a) else 0
    k_hi = int(np.sum(s < b + tol)) if math.isfinite(b) else s.size + 1
    if not math.isfinite(b):
        return RankRange(max(k_lo, 1), s.size + 1)
    return RankRange(k_lo, k_hi)


def is_trivial(intervals: NDArray[np.float64] | None, sets: NDArray[np.bool_] | None) -> bool:
    """True when every interval is ``(-inf, inf)`` or every set holds all labels."""
    if intervals is not None:
        iv = np.asarray(intervals, dtype=float)
        return bool(np.all(np.isneginf(iv[:, 0])) and np.all(np.isposinf(iv[:, 1])))
    if sets is not None:
        return bool(np.all(np.asarray(sets, dtype=bool)))
    return False


def compare_to_reference(out: NDArray | None, ref: NDArray | None, kind: str) -> float | None:
    """Max absolute endpoint difference (intervals) or set disagreement rate (sets)."""
    if out is None or ref is None:
        return None
    a = np.asarray(out)
    b = np.asarray(ref)
    if a.shape != b.shape:
        return math.inf
    if kind == "intervals":
        a = a.astype(float)
        b = b.astype(float)
        same_inf = np.isinf(a) & np.isinf(b) & (np.sign(a) == np.sign(b))
        with np.errstate(invalid="ignore"):
            diff = np.where(same_inf, 0.0, np.abs(a - b))
        return float(np.nanmax(diff)) if diff.size else 0.0
    return float(np.mean(a.astype(bool) != b.astype(bool)))
