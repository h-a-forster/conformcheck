"""Rank tolerance for float32 endpoints, and the oracle-control bookkeeping."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck import diagnostics, laws
from conformcheck.report import mutant_is_identical


def test_rank_range_scale_absorbs_float32_rounding() -> None:
    rng = np.random.default_rng(0)
    n, k = 19, 18
    y = rng.normal(size=n) + 150.0  # endpoints far from 0, as on the diabetes data
    pred = np.full(n, 150.0)
    scores = np.abs(y - pred)
    q = np.sort(scores)[k - 1]
    # a float32 endpoint near 150 is off by up to half an ulp (7.6e-6): simulate 5e-6
    assert np.spacing(np.float32(150.0)) / 2 > 5e-6
    hi32 = 150.0 + q + 5e-6
    q_read = hi32 - 150.0
    assert abs(q_read - q) > 1e-6  # outside the old tolerance of 1e-6 * max(1, |q|)
    r = diagnostics.regression_ranks(
        "split_abs",
        "",
        np.array([[150.0 - q_read, hi32]]),
        y,
        pred,
        np.array([150.0]),
    )
    assert r is not None
    assert all(x.offset(k) == 0 for x in r)


def test_rank_range_scale_default_unchanged() -> None:
    s = np.array([0.1, 0.2, 0.3])
    assert diagnostics.rank_range(s, 0.2) == diagnostics.RankRange(2, 2)
    assert diagnostics.rank_range(s, 0.25).interpolated


def test_mutant_identical_cells() -> None:
    # n * (1 - alpha) and (n + 1)(1 - alpha) round up to the same integer
    assert mutant_is_identical(9, Fraction(1, 10), "n_instead_of_n_plus_1")  # 8.1, 9 -> 9, 9
    assert not mutant_is_identical(10, Fraction(1, 10), "n_instead_of_n_plus_1")  # 9 vs 10
    for n in (5, 9, 10, 19, 20, 99, 100, 1000):
        for a in (Fraction(1, 10), Fraction(1, 5), Fraction(1, 20)):
            k = laws.split_index(n, a)
            same = -(-(n * (1 - a)) // 1) == k
            assert mutant_is_identical(n, a, "n_instead_of_n_plus_1") == same
            assert not mutant_is_identical(n, a, "k_minus_1")
            assert not mutant_is_identical(n, a, "k_plus_1")
    # numpy's linear quantile sits at 0-based position h = (n - 1)(1 - alpha); it equals
    # s_(k) only when h is an integer and h + 1 = k, which needs alpha >= 1/2
    assert not mutant_is_identical(11, Fraction(1, 5), "no_correction_linear")
    assert mutant_is_identical(3, Fraction(1, 2), "no_correction_linear")  # h = 1, k = 2
