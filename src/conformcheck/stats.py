"""Statistical tests of observed covered counts against an exact law.

Per cell the runner records ``S_1..S_R``, the covered counts in ``R`` independent
repetitions with ``m`` test points each (docs/DESIGN.md, section 3.4).

* :func:`mean_test`: exact two-sided p-value of ``T = sum S_r`` against the ``R``-fold
  convolution of the law's pmf (FFT, by repeated squaring), with a normal
  approximation that uses the exact variance as a cross-check. Laws with only an exact
  mean (``kind="mean"``) use a t-test with the empirical variance.
* :func:`gof_test`: Pearson chi-square of the histogram of ``S_r`` against the pmf, bins
  merged until every expected count is at least 5.
* :func:`lower_bound_test`: one-sided t-test of mean coverage against a guaranteed
  lower bound (jackknife+ and CV+ with non-degenerate models).
* :func:`cell_pvalue`: ``min(1, 2 min(p_mean, p_gof))`` (Bonferroni within a cell).
* :func:`holm` and :func:`benjamini_yekutieli` across cells.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import signal, stats

from conformcheck.laws import CoverageLaw

Direction = Literal["below", "above", "equal"]


def convolution_power(pmf: ArrayLike, r: int) -> NDArray[np.float64]:
    """pmf of the sum of ``r`` i.i.d. copies of a variable with pmf ``pmf`` on ``0..len-1``.

    Uses FFT convolution with binary exponentiation. Negative round-off is clipped and
    the result renormalised; tail probabilities below about 1e-14 are not resolved, which
    is far below any threshold used here.
    """
    if r < 1:
        raise ValueError(f"r must be >= 1, got {r}")
    base = np.clip(np.asarray(pmf, dtype=float), 0.0, None)
    base = base / base.sum()
    result: NDArray[np.float64] | None = None
    while True:
        if r & 1:
            result = base.copy() if result is None else _conv(result, base)
        r >>= 1
        if not r:
            break
        base = _conv(base, base)
    assert result is not None
    return result


def _conv(a: NDArray[np.float64], b: NDArray[np.float64]) -> NDArray[np.float64]:
    out = signal.fftconvolve(a, b)
    out = np.clip(out, 0.0, None)
    return out / out.sum()


@dataclass(frozen=True)
class MeanTest:
    """Result of a test on ``T = sum_r S_r``."""

    pvalue: float
    statistic: float  # observed T
    expected: float  # E T under the law
    z: float  # standardised difference (exact or empirical variance)
    direction: Direction
    p_normal: float | None = None  # normal approximation, exact laws only


def _direction(t: float, expected: float) -> Direction:
    if math.isclose(t, expected, rel_tol=0.0, abs_tol=1e-9):
        return "equal"
    return "below" if t < expected else "above"


def mean_test(
    counts: ArrayLike,
    law: CoverageLaw,
    alternative: Literal["two-sided", "less"] = "two-sided",
) -> MeanTest:
    """Test the mean of the covered counts against ``law``.

    ``alternative="less"`` gives a one-sided p-value for under-coverage only; it is used
    when ties are observed on finite pools, where ties can only add coverage.
    """
    s = np.asarray(counts, dtype=np.int64)
    r = s.size
    if r == 0:
        raise ValueError("no counts")
    t = float(s.sum())
    expected = r * law.mean
    if law.kind == "exact":
        assert law.pmf is not None
        var = law.variance
        assert var is not None
        if var <= 1e-15:  # point mass, e.g. a required trivial set
            p = 1.0 if math.isclose(t, expected, abs_tol=1e-9) else 0.0
            return MeanTest(p, t, expected, 0.0 if p else math.inf, _direction(t, expected), p)
        conv = convolution_power(law.pmf, r)
        ti = int(round(t))
        cdf = float(conv[: ti + 1].sum())
        sf = float(conv[ti:].sum())
        sd = math.sqrt(r * var)
        z = (t - expected) / sd
        if alternative == "less":
            p = min(1.0, cdf)
            p_norm = float(stats.norm.cdf((t + 0.5 - expected) / sd))
        else:
            p = min(1.0, 2.0 * min(cdf, sf))
            p_norm = float(min(1.0, 2.0 * stats.norm.sf(max(abs(t - expected) - 0.5, 0.0) / sd)))
        return MeanTest(p, t, expected, z, _direction(t, expected), p_norm)
    if law.kind == "mean":
        return _t_test(s, law.m, law.coverage, alternative)
    raise ValueError(f"mean_test does not apply to a law of kind {law.kind!r}")


def _t_test(
    s: NDArray[np.int64], m: int, coverage: float, alternative: Literal["two-sided", "less"]
) -> MeanTest:
    r = s.size
    expected = r * m * coverage
    t = float(s.sum())
    if r < 2:
        return MeanTest(1.0, t, expected, 0.0, _direction(t, expected))
    sd = float(np.std(s, ddof=1))
    if sd == 0.0:  # every repetition gave the same count
        direction = _direction(t, expected)
        if alternative == "less":
            p = 0.0 if direction == "below" else 1.0
        else:
            p = 1.0 if direction == "equal" else 0.0
        return MeanTest(p, t, expected, 0.0, direction)
    z = (t / r - m * coverage) / (sd / math.sqrt(r))
    if alternative == "less":
        p = float(stats.t.cdf(z, df=r - 1))
    else:
        p = float(min(1.0, 2.0 * stats.t.sf(abs(z), df=r - 1)))
    return MeanTest(p, t, expected, z, _direction(t, expected))


@dataclass(frozen=True)
class GofTest:
    """Pearson chi-square goodness of fit of the histogram of ``S_r``."""

    pvalue: float
    statistic: float
    df: int


def merge_bins(expected: NDArray[np.float64], minimum: float = 5.0) -> list[slice]:
    """Contiguous bins over the support, merged left to right until each has
    ``expected >= minimum``; an underfilled last bin is merged into its neighbour."""
    bins: list[slice] = []
    start = 0
    acc = 0.0
    for i, e in enumerate(expected):
        acc += e
        if acc >= minimum:
            bins.append(slice(start, i + 1))
            start, acc = i + 1, 0.0
    if start < len(expected):
        if bins:
            bins[-1] = slice(bins[-1].start, len(expected))
        else:
            bins.append(slice(0, len(expected)))
    return bins


def gof_test(counts: ArrayLike, law: CoverageLaw, minimum_expected: float = 5.0) -> GofTest:
    """Chi-square test of the empirical distribution of counts against the exact pmf."""
    if law.kind != "exact" or law.pmf is None:
        raise ValueError("gof_test needs an exact law")
    s = np.asarray(counts, dtype=np.int64)
    r = s.size
    observed = np.bincount(s, minlength=law.m + 1)[: law.m + 1].astype(float)
    if observed.sum() != r:
        raise ValueError("counts outside 0..m")
    expected = r * np.asarray(law.pmf, dtype=float)
    bins = merge_bins(expected, minimum_expected)
    if len(bins) < 2:
        return GofTest(1.0, 0.0, 0)
    o = np.array([observed[b].sum() for b in bins])
    e = np.array([expected[b].sum() for b in bins])
    stat = float(np.sum((o - e) ** 2 / e))
    df = len(bins) - 1
    return GofTest(float(stats.chi2.sf(stat, df)), stat, df)


def lower_bound_test(counts: ArrayLike, m: int, bound: float) -> MeanTest:
    """One-sided t-test of ``H0: E[S/m] >= bound``; small p-values mean a violation."""
    s = np.asarray(counts, dtype=np.int64)
    return _t_test(s, m, float(bound), "less")


def cell_pvalue(p_mean: float, p_gof: float | None) -> float:
    """Bonferroni combination within a cell: ``min(1, 2 min(p_mean, p_gof))``."""
    if p_gof is None:
        return float(p_mean)
    return float(min(1.0, 2.0 * min(p_mean, p_gof)))


@dataclass(frozen=True)
class Adjusted:
    """Adjusted p-values and decisions for a family of hypotheses."""

    adjusted: NDArray[np.float64]
    reject: NDArray[np.bool_]
    thresholds: NDArray[np.float64]  # per-hypothesis critical value of the raw p-value


def holm(pvalues: ArrayLike, level: float = 0.05) -> Adjusted:
    """Holm (1979) step-down procedure; controls the FWER at ``level``.

    ``thresholds[i]`` is the step-down critical value ``level / (N - rank_i)`` attached
    to hypothesis ``i`` (rank from 0 in increasing p-value order).
    """
    p = np.asarray(pvalues, dtype=float)
    n = p.size
    if n == 0:
        empty = np.zeros(0)
        return Adjusted(empty, empty.astype(bool), empty)
    order = np.argsort(p, kind="stable")
    ranked = p[order]
    factors = n - np.arange(n)
    adj_sorted = np.minimum(1.0, np.maximum.accumulate(ranked * factors))
    adjusted = np.empty(n)
    adjusted[order] = adj_sorted
    thresholds = np.empty(n)
    thresholds[order] = level / factors
    return Adjusted(adjusted, adjusted <= level, thresholds)


def benjamini_yekutieli(pvalues: ArrayLike, level: float = 0.05) -> Adjusted:
    """Benjamini and Yekutieli (2001) step-up procedure; FDR control under dependence."""
    p = np.asarray(pvalues, dtype=float)
    n = p.size
    if n == 0:
        empty = np.zeros(0)
        return Adjusted(empty, empty.astype(bool), empty)
    c_n = float(np.sum(1.0 / np.arange(1, n + 1)))
    order = np.argsort(p, kind="stable")
    ranked = p[order]
    raw = ranked * n * c_n / np.arange(1, n + 1)
    adj_sorted = np.minimum(1.0, np.minimum.accumulate(raw[::-1])[::-1])
    adjusted = np.empty(n)
    adjusted[order] = adj_sorted
    thresholds = np.empty(n)
    thresholds[order] = level * np.arange(1, n + 1) / (n * c_n)
    return Adjusted(adjusted, adjusted <= level, thresholds)


def coverage_interval(
    counts: ArrayLike, m: int, law: CoverageLaw | None = None, level: float = 0.95
) -> tuple[float, float, float]:
    """Observed mean coverage and a ``level`` interval for it.

    With an exact law the interval uses the exact variance of ``S`` (a normal interval
    around the observed mean); otherwise a t interval with the empirical variance.
    """
    s = np.asarray(counts, dtype=float)
    r = s.size
    mean = float(s.mean() / m)
    if law is not None and law.kind == "exact" and law.variance is not None:
        se = math.sqrt(law.variance / r) / m
        z = float(stats.norm.ppf(0.5 + level / 2))
    else:
        if r < 2:
            return mean, mean, mean
        se = float(np.std(s, ddof=1)) / math.sqrt(r) / m
        z = float(stats.t.ppf(0.5 + level / 2, df=r - 1))
    return mean, mean - z * se, mean + z * se


def min_detectable_effect(law: CoverageLaw, reps: int, z_crit: float) -> float | None:
    """Smallest coverage shift the mean test detects with 80% power at critical ``z_crit``.

    ``(z_crit + 0.84) sd(S/m) / sqrt(R)`` (docs/DESIGN.md, section 3.5).
    """
    var = law.variance
    if var is None or var <= 0:
        return None
    return (z_crit + 0.8416) * math.sqrt(var) / law.m / math.sqrt(reps)
