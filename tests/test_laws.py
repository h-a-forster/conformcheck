"""Reference values for the exact laws. Hand-derived values are listed in docs/DESIGN.md."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest

from conformcheck import laws


@pytest.mark.parametrize(
    ("n", "alpha", "k"),
    [
        (5, 0.1, 6),  # k > n: trivial set required
        (5, 0.2, 5),
        (9, 0.1, 9),  # (n+1) alpha = 1, integer boundary
        (10, 0.1, 10),
        (19, 0.05, 19),
        (19, 0.1, 18),
        (19, 0.2, 16),
        (20, 0.1, 19),
        (99, 0.1, 90),
        (100, 0.1, 91),
        (999, 0.1, 900),
        (1000, 0.05, 951),
    ],
)
def test_split_index(n: int, alpha: float, k: int) -> None:
    assert laws.split_index(n, alpha) == k
    assert laws.split_index(n, alpha) == n + 1 - laws.floor_index(n, alpha)


def test_alpha_is_read_as_decimal() -> None:
    assert laws.as_fraction(0.1) == Fraction(1, 10)
    assert laws.as_fraction("1/20") == Fraction(1, 20)
    # The binary double nearest 0.3 is below 3/10; the decimal reading must win.
    assert laws.split_index(9, 0.3) == 7
    with pytest.raises(ValueError):
        laws.as_fraction(1.0)


def test_integer_boundary() -> None:
    assert laws.is_integer_boundary(19, 0.1)
    assert laws.is_integer_boundary(99, 0.2)
    assert not laws.is_integer_boundary(20, 0.1)


def test_marginal_coverage_and_bounds() -> None:
    assert laws.marginal_coverage(19, 0.1) == Fraction(18, 20)
    assert laws.marginal_coverage(10, 0.1) == Fraction(10, 11)
    assert laws.marginal_coverage(5, 0.1) == 1
    assert laws.requires_trivial_set(5, 0.1)
    assert not laws.requires_trivial_set(5, 0.2)
    for n in (5, 9, 10, 19, 20, 49, 50, 99, 100, 999, 1000):
        for alpha in (0.05, 0.1, 0.2):
            if laws.requires_trivial_set(n, alpha):
                continue
            lo, hi = laws.marginal_bounds(n, alpha)
            assert lo <= laws.marginal_coverage(n, alpha) < hi


def test_beta_binomial_moments() -> None:
    k, b = laws.conditional_beta_params(19, 0.1)
    assert (k, b) == (18, 2)
    mean, var = laws.beta_binomial_moments(10, k, b)
    assert mean == pytest.approx(9.0)
    assert var == pytest.approx(10800 / 8400)
    law = laws.split_count_law(19, 0.1, 10)
    assert law.pmf is not None
    assert law.pmf.sum() == pytest.approx(1.0)
    assert law.mean == pytest.approx(9.0)
    assert law.variance == pytest.approx(10800 / 8400)


def test_trivial_count_law() -> None:
    law = laws.split_count_law(5, 0.1, 7)
    assert law.coverage == 1.0
    assert law.pmf is not None and law.pmf[7] == 1.0


def test_jackknife_and_cv_plus_bounds() -> None:
    assert laws.jackknife_plus_bound(0.1) == Fraction(4, 5)
    # n=100, K=10, alpha=0.1: min(2*0.9/11, 0.9/11) = 0.9/11
    assert laws.cv_plus_bound(100, 10, 0.1) == Fraction(4, 5) - Fraction(9, 110)
    # K = n reduces to the jackknife+ bound
    assert laws.cv_plus_bound(50, 50, 0.1) == laws.jackknife_plus_bound(0.1)
    assert float(laws.cv_plus_bound(100, 5, 0.1)) >= 0.8 - math.sqrt(2 / 100)


def test_asymmetric_cqr_coverage() -> None:
    # n=19, alpha=0.1: k' = ceil(20 * 0.95) = 19 -> (38 - 20) / 20
    assert laws.asymmetric_cqr_coverage(19, 0.1) == Fraction(18, 20)
    # n=10, alpha=0.1: k' = ceil(11 * 0.95) = 11 > 10 -> trivial
    assert laws.asymmetric_cqr_coverage(10, 0.1) == 1


def test_discrete_coverage_matches_simulation() -> None:
    rng = np.random.default_rng(0)
    pmf = np.array([0.2, 0.3, 0.1, 0.25, 0.15])
    n, alpha, reps = 9, 0.2, 40_000
    exact = laws.discrete_split_coverage(n, alpha, pmf)
    k = laws.split_index(n, alpha)
    cal = rng.choice(5, size=(reps, n), p=pmf)
    test = rng.choice(5, size=reps, p=pmf)
    q = np.sort(cal, axis=1)[:, k - 1]
    sim = float(np.mean(test <= q))
    assert abs(sim - exact) < 4 * math.sqrt(exact * (1 - exact) / reps)
    # Ties can only add coverage relative to the continuous case.
    assert exact >= float(laws.marginal_coverage(n, alpha))


def test_discrete_count_law_reduces_to_coverage() -> None:
    pmf = np.array([0.5, 0.25, 0.25])
    law = laws.discrete_count_law(9, 0.2, 20, pmf)
    assert law.pmf is not None and law.pmf.sum() == pytest.approx(1.0)
    assert law.mean / 20 == pytest.approx(laws.discrete_split_coverage(9, 0.2, pmf))


def test_split_count_law_matches_simulation() -> None:
    """A correct split conformal implementation reproduces BetaBinomial(m, k, n+1-k)."""
    rng = np.random.default_rng(1)
    n, alpha, m, reps = 19, 0.1, 25, 20_000
    law = laws.split_count_law(n, alpha, m)
    k = laws.split_index(n, alpha)
    cal = np.sort(rng.normal(size=(reps, n)), axis=1)[:, k - 1]
    counts = np.sum(rng.normal(size=(reps, m)) <= cal[:, None], axis=1)
    assert law.pmf is not None
    observed = np.bincount(counts, minlength=m + 1) / reps
    # Total variation distance between empirical and exact pmf is small.
    assert 0.5 * np.abs(observed - law.pmf).sum() < 0.03
    assert counts.mean() == pytest.approx(law.mean, abs=4 * math.sqrt(law.variance / reps))
