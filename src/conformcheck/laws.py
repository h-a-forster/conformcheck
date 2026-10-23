"""Exact finite-sample laws of conformal coverage.

Everything here is distribution-free: it depends only on the calibration size ``n``,
the miscoverage level ``alpha`` and (for the per-repetition count laws) the number of
test points ``m`` that share one calibration set. See docs/DESIGN.md, section 3.

Conventions
-----------
* ``alpha`` is interpreted as the exact rational the user meant. A float is converted
  through its shortest decimal representation (``0.1`` means 1/10, not the binary double
  0.1000000000000000055...). Pass a :class:`fractions.Fraction` or a string such as
  ``"1/20"`` to be explicit.
* Split conformal with ``n`` calibration scores uses the ``k``-th smallest score,
  ``k = ceil((n + 1) * (1 - alpha))``. When ``k > n`` the only valid set is the trivial
  one (infinite interval, all labels).
* Prediction sets are closed: a test point is covered when its score is ``<=`` the
  threshold.

References
----------
Vovk, Gammerman and Shafer (2005), *Algorithmic Learning in a Random World*.
Vovk (2012), "Conditional validity of inductive conformal predictors", ACML.
Lei, G'Sell, Rinaldo, Tibshirani and Wasserman (2018), "Distribution-free predictive
inference for regression", JASA, Theorem 2.2.
Barber, Candes, Ramdas and Tibshirani (2021), "Predictive inference with the jackknife+",
Annals of Statistics, Theorems 1 and 4.
Angelopoulos and Bates (2023), "Conformal prediction: a gentle introduction",
Foundations and Trends in ML, Section 3.2 (Beta law of conditional coverage).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from scipy import stats

AlphaLike = float | str | Fraction


def as_fraction(alpha: AlphaLike) -> Fraction:
    """Return ``alpha`` as the exact rational it denotes (see module docstring)."""
    if isinstance(alpha, Fraction):
        value = alpha
    elif isinstance(alpha, str):
        value = Fraction(alpha)
    elif isinstance(alpha, float | int):
        value = Fraction(repr(float(alpha)))
    else:  # pragma: no cover - defensive
        raise TypeError(f"alpha must be a float, str or Fraction, not {type(alpha).__name__}")
    if not 0 < value < 1:
        raise ValueError(f"alpha must lie in (0, 1), got {value}")
    return value


def _check_n(n: int) -> None:
    if not isinstance(n, int | np.integer) or n < 1:
        raise ValueError(f"n must be a positive integer, got {n!r}")


def split_index(n: int, alpha: AlphaLike) -> int:
    """``k = ceil((n + 1)(1 - alpha))``, the order statistic split conformal must use.

    The result can be ``n + 1``, which means the prediction set must be trivial.
    """
    _check_n(n)
    return math.ceil((n + 1) * (1 - as_fraction(alpha)))


def floor_index(n: int, alpha: AlphaLike) -> int:
    """``l = floor((n + 1) alpha)``; always ``split_index(n, alpha) == n + 1 - l``."""
    _check_n(n)
    return math.floor((n + 1) * as_fraction(alpha))


def is_integer_boundary(n: int, alpha: AlphaLike) -> bool:
    """True when ``(n + 1) * alpha`` is an integer.

    At these points the order statistic is most sensitive to rounding: an implementation
    that evaluates ``(n + 1) * (1 - alpha)`` in floating point can land on ``k + 1``.
    """
    _check_n(n)
    return ((n + 1) * as_fraction(alpha)).denominator == 1


def requires_trivial_set(n: int, alpha: AlphaLike) -> bool:
    """True when ``alpha < 1 / (n + 1)``, i.e. ``k > n``: no finite set is valid."""
    return split_index(n, alpha) > n


def marginal_coverage(n: int, alpha: AlphaLike) -> Fraction:
    """Exact marginal coverage ``k / (n + 1)`` of split conformal with continuous scores.

    Returns 1 when the set must be trivial.
    """
    k = split_index(n, alpha)
    return Fraction(1) if k > n else Fraction(k, n + 1)


def marginal_bounds(n: int, alpha: AlphaLike) -> tuple[Fraction, Fraction]:
    """The classical bounds ``[1 - alpha, 1 - alpha + 1/(n + 1))`` (Lei et al. 2018)."""
    a = as_fraction(alpha)
    return 1 - a, 1 - a + Fraction(1, n + 1)


def conditional_beta_params(n: int, alpha: AlphaLike) -> tuple[int, int]:
    """Parameters ``(k, n + 1 - k)`` of the Beta law of coverage given the calibration set.

    Equivalently ``Beta(n + 1 - l, l)`` with ``l = floor((n + 1) alpha)``.
    """
    k = split_index(n, alpha)
    if k > n:
        raise ValueError(f"alpha={alpha} < 1/(n+1) for n={n}: coverage is identically 1")
    return k, n + 1 - k


def beta_binomial_moments(m: int, a: int, b: int) -> tuple[float, float]:
    """Mean and variance of ``BetaBinomial(m, a, b)``."""
    s = a + b
    mean = m * a / s
    var = m * a * b * (s + m) / (s * s * (s + 1))
    return mean, var


def jackknife_plus_bound(alpha: AlphaLike) -> Fraction:
    """Worst-case coverage ``1 - 2 alpha`` of jackknife+ (Barber et al. 2021, Thm 1)."""
    return 1 - 2 * as_fraction(alpha)


def cv_plus_bound(n: int, n_folds: int, alpha: AlphaLike) -> Fraction:
    """Worst-case coverage of K-fold CV+ (Barber et al. 2021, Thm 4).

    ``1 - 2 alpha - min{2(1 - 1/K) / (n/K + 1), (1 - K/n) / (K + 1)}``. With ``K = n``
    this is the jackknife+ bound.

    The theorem assumes folds of equal size ``m = n/K`` (an integer). For ``K`` not
    dividing ``n`` the formula is applied with ``n/K`` as a rational, which is an
    extrapolation, not a proven bound; :func:`cv_plus_bound_proven` says which case
    applies.
    """
    _check_n(n)
    if not 2 <= n_folds <= n:
        raise ValueError(f"need 2 <= K <= n, got K={n_folds}, n={n}")
    k = Fraction(n_folds)
    slack = min(2 * (1 - 1 / k) / (n / k + 1), (1 - k / n) / (k + 1))
    return 1 - 2 * as_fraction(alpha) - slack


def cv_plus_bound_proven(n: int, n_folds: int) -> bool:
    """True when Barber et al. (2021, Thm 4) covers ``(n, K)``: ``K`` divides ``n``."""
    return n % n_folds == 0


def asymmetric_cqr_coverage(n: int, alpha: AlphaLike) -> Fraction:
    """Exact marginal coverage of CQR with separate lower and upper corrections.

    Each side is a one-sided split conformal bound at level ``alpha / 2`` using the
    ``k' = ceil((n + 1)(1 - alpha/2))``-th order statistic of its own scores. The two
    miscoverage events are disjoint, so coverage is ``(2 k' - (n + 1)) / (n + 1)``, or 1
    when ``k' > n``.
    """
    k = split_index(n, as_fraction(alpha) / 2)
    return Fraction(1) if k > n else Fraction(2 * k - (n + 1), n + 1)


def discrete_order_stat_cdf(n: int, k: int, cdf_values: NDArray[np.float64]) -> NDArray:
    """``P(S_(k) <= v)`` for each support point ``v`` with ``F(v) = cdf_values``.

    ``S_(k)`` is the ``k``-th smallest of ``n`` i.i.d. scores. Uses
    ``P(S_(k) <= v) = P(Binomial(n, F(v)) >= k)``.
    """
    return stats.binom.sf(k - 1, n, np.asarray(cdf_values, dtype=float))


def discrete_split_coverage(n: int, alpha: AlphaLike, pmf: NDArray[np.float64]) -> float:
    """Exact marginal coverage of split conformal when scores are discrete.

    ``pmf`` gives the score distribution on an increasing support. Ties make split
    conformal conservative; this is the exact value a correct implementation attains with
    closed sets and the ``k``-th order statistic.
    """
    p = np.asarray(pmf, dtype=float)
    if np.any(p < 0) or not math.isclose(p.sum(), 1.0, abs_tol=1e-12):
        raise ValueError("pmf must be non-negative and sum to 1")
    k = split_index(n, alpha)
    if k > n:
        return 1.0
    cdf = np.cumsum(p)
    q_cdf = discrete_order_stat_cdf(n, k, cdf)
    q_pmf = np.diff(np.concatenate([[0.0], q_cdf]))
    return float(np.dot(q_pmf, cdf))


@dataclass(frozen=True)
class CoverageLaw:
    """Law of ``S``, the number of covered test points among ``m`` sharing a calibration set.

    ``kind`` is ``"exact"`` when ``pmf`` is the exact distribution of ``S``,
    ``"mean"`` when only the exact mean is known, and ``"lower"`` when only a lower bound
    on coverage is guaranteed.
    """

    kind: Literal["exact", "mean", "lower"]
    m: int
    coverage: float
    pmf: NDArray[np.float64] | None = None
    description: str = ""

    @property
    def mean(self) -> float:
        return self.m * self.coverage

    @property
    def variance(self) -> float | None:
        if self.pmf is None:
            return None
        s = np.arange(self.m + 1)
        mu = float(np.dot(s, self.pmf))
        return float(np.dot((s - mu) ** 2, self.pmf))


def split_count_law(n: int, alpha: AlphaLike, m: int) -> CoverageLaw:
    """Exact law of the covered count for split conformal with distinct scores.

    ``S ~ BetaBinomial(m, k, n + 1 - k)``. This holds for i.i.d. continuous data and for
    random splits of a finite pool with distinct scores, since it depends only on the
    random relative order of the ``n + m`` scores. When ``k > n``, ``S = m`` surely.
    """
    k = split_index(n, alpha)
    if k > n:
        pmf = np.zeros(m + 1)
        pmf[m] = 1.0
        return CoverageLaw("exact", m, 1.0, pmf, f"trivial set (k={k} > n={n})")
    a, b = k, n + 1 - k
    pmf = stats.betabinom.pmf(np.arange(m + 1), m, a, b)
    return CoverageLaw("exact", m, k / (n + 1), pmf, f"BetaBinomial(m={m}, {a}, {b})")


def discrete_count_law(n: int, alpha: AlphaLike, m: int, pmf: NDArray[np.float64]) -> CoverageLaw:
    """Exact law of the covered count when scores are discrete with known ``pmf``.

    Given the threshold ``q = S_(k)``, each test point is covered independently with
    probability ``F(q)``, so ``S`` is a mixture of ``Binomial(m, F(v))`` weighted by
    ``P(S_(k) = v)``.
    """
    p = np.asarray(pmf, dtype=float)
    k = split_index(n, alpha)
    if k > n:
        out = np.zeros(m + 1)
        out[m] = 1.0
        return CoverageLaw("exact", m, 1.0, out, f"trivial set (k={k} > n={n})")
    cdf = np.minimum(np.cumsum(p), 1.0)
    q_pmf = np.diff(np.concatenate([[0.0], discrete_order_stat_cdf(n, k, cdf)]))
    counts = np.arange(m + 1)
    mix = stats.binom.pmf(counts[None, :], m, cdf[:, None])
    out = q_pmf @ mix
    out = out / out.sum()
    return CoverageLaw(
        "exact", m, float(np.dot(q_pmf, cdf)), out, f"discrete mixture (k={k}, support={len(p)})"
    )
