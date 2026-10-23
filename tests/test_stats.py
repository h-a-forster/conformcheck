"""Known-answer, size and power tests for the statistical layer (DESIGN section 3.4)."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats as sps

from conformcheck import laws, stats
from conformcheck.laws import CoverageLaw


def test_convolution_power_matches_binomial() -> None:
    # Sum of r Bernoulli(p) is Binomial(r, p).
    pmf = np.array([0.7, 0.3])
    for r in (1, 2, 3, 7, 64, 200):
        out = stats.convolution_power(pmf, r)
        assert out.shape == (r + 1,)
        assert np.allclose(out, sps.binom.pmf(np.arange(r + 1), r, 0.3), atol=1e-12)


def test_convolution_power_of_betabinomial_moments() -> None:
    law = laws.split_count_law(19, 0.1, 50)
    r = 37
    out = stats.convolution_power(law.pmf, r)
    support = np.arange(out.size)
    mean = float(support @ out)
    var = float(((support - mean) ** 2) @ out)
    assert mean == pytest.approx(r * law.mean, rel=1e-10)
    assert var == pytest.approx(r * law.variance, rel=1e-8)


def test_mean_test_exact_matches_normal_for_moderate_t() -> None:
    law = laws.split_count_law(49, 0.1, 500)
    r = 200
    sd = np.sqrt(r * law.variance)
    for z in (-2.5, -1.0, 0.3, 1.7, 2.2):
        t = int(round(r * law.mean + z * sd))
        counts = np.full(r, t // r)
        counts[: t - counts.sum()] += 1
        assert counts.sum() == t
        res = stats.mean_test(counts, law)
        assert res.p_normal is not None
        assert abs(res.pvalue - res.p_normal) < 0.01
        assert res.direction == ("below" if z < 0 else "above")


def test_mean_test_point_mass() -> None:
    law = laws.split_count_law(5, 0.1, 20)  # k > n: S = m surely
    assert stats.mean_test(np.full(10, 20), law).pvalue == 1.0
    res = stats.mean_test(np.array([20] * 9 + [19]), law)
    assert res.pvalue == 0.0
    assert res.direction == "below"


def test_mean_test_one_sided() -> None:
    law = laws.split_count_law(19, 0.1, 100)
    high = np.full(100, 95)  # coverage 0.95 against 0.9: over-coverage only
    assert stats.mean_test(high, law, alternative="less").pvalue > 0.99
    assert stats.mean_test(high, law).pvalue < 1e-6


def test_t_test_for_mean_law() -> None:
    law = CoverageLaw("mean", 100, 0.9)
    rng = np.random.default_rng(0)
    ok = rng.binomial(100, 0.9, size=300)
    assert stats.mean_test(ok, law).pvalue > 0.001
    bad = rng.binomial(100, 0.85, size=300)
    res = stats.mean_test(bad, law)
    assert res.pvalue < 1e-6 and res.direction == "below"
    assert stats.mean_test(np.full(5, 90), law).pvalue == 1.0


def test_merge_bins() -> None:
    e = np.array([0.1, 1.0, 4.0, 10.0, 6.0, 2.0, 1.0, 0.5])
    bins = stats.merge_bins(e, 5.0)
    sums = [e[b].sum() for b in bins]
    assert all(s >= 5.0 for s in sums)
    assert bins[0].start == 0 and bins[-1].stop == len(e)
    assert sum(b.stop - b.start for b in bins) == len(e)


def test_gof_detects_wrong_effective_n() -> None:
    rng = np.random.default_rng(1)
    m, r = 200, 400
    # Same mean (0.9) but different conditional law: n=19 vs n=199.
    law = laws.split_count_law(19, 0.1, m)
    wide = sps.betabinom.rvs(m, 18, 2, size=r, random_state=rng)
    narrow = sps.betabinom.rvs(m, 180, 20, size=r, random_state=rng)
    assert stats.gof_test(wide, law).pvalue > 0.001
    assert stats.gof_test(narrow, law).pvalue < 1e-6


def test_lower_bound_test() -> None:
    rng = np.random.default_rng(2)
    above = rng.binomial(100, 0.85, size=200)
    assert stats.lower_bound_test(above, 100, 0.8).pvalue > 0.5
    below = rng.binomial(100, 0.75, size=200)
    assert stats.lower_bound_test(below, 100, 0.8).pvalue < 1e-6


def test_cell_pvalue() -> None:
    assert stats.cell_pvalue(0.01, 0.2) == pytest.approx(0.02)
    assert stats.cell_pvalue(0.7, 0.9) == 1.0
    assert stats.cell_pvalue(0.3, None) == 0.3


def test_holm_hand_example() -> None:
    p = [0.01, 0.04, 0.03, 0.005]
    res = stats.holm(p, 0.05)
    # sorted: 0.005*4=0.02, 0.01*3=0.03, 0.03*2=0.06, 0.04*1=0.04 -> max-accumulate 0.06
    assert np.allclose(res.adjusted, [0.03, 0.06, 0.06, 0.02])
    assert res.reject.tolist() == [True, False, False, True]
    assert np.allclose(res.thresholds, [0.05 / 3, 0.05 / 1, 0.05 / 2, 0.05 / 4])


def test_by_matches_scipy() -> None:
    rng = np.random.default_rng(3)
    p = np.concatenate([rng.uniform(size=50), rng.uniform(0, 1e-4, size=5)])
    res = stats.benjamini_yekutieli(p, 0.05)
    ref = sps.false_discovery_control(p, method="by")
    assert np.allclose(res.adjusted, ref)
    assert res.reject.sum() >= 1


def test_holm_and_by_empty() -> None:
    assert stats.holm([]).adjusted.size == 0
    assert stats.benjamini_yekutieli([]).reject.size == 0


def test_coverage_interval_contains_truth_for_exact_law() -> None:
    law = laws.split_count_law(19, 0.1, 100)
    rng = np.random.default_rng(4)
    hits = 0
    for _ in range(200):
        s = sps.betabinom.rvs(100, 18, 2, size=50, random_state=rng)
        _, lo, hi = stats.coverage_interval(s, 100, law)
        hits += lo <= 0.9 <= hi
    assert 180 <= hits <= 200


def test_min_detectable_effect_matches_design_table() -> None:
    # DESIGN 3.5: about 0.012 at n=99 and 0.006 at n=999 in the default study.
    z = 4.21
    assert stats.min_detectable_effect(laws.split_count_law(99, 0.1, 500), 200, z) == (
        pytest.approx(0.012, abs=0.002)
    )
    assert stats.min_detectable_effect(laws.split_count_law(999, 0.1, 500), 200, z) == (
        pytest.approx(0.006, abs=0.001)
    )


def _null_rejections(n_cells: int, r: int, m: int, seed: int) -> int:
    rng = np.random.default_rng(seed)
    rejections = 0
    for i in range(n_cells):
        n = [9, 19, 49, 99][i % 4]
        law = laws.split_count_law(n, 0.1, m)
        a, b = laws.conditional_beta_params(n, 0.1)
        s = sps.betabinom.rvs(m, a, b, size=r, random_state=rng)
        p = stats.cell_pvalue(stats.mean_test(s, law).pvalue, stats.gof_test(s, law).pvalue)
        rejections += p <= 0.05
    return rejections


def test_null_rejection_rate_small() -> None:
    n_cells = 200
    rej = _null_rejections(n_cells, r=50, m=50, seed=5)
    lo, hi = sps.binom.ppf([0.005, 0.995], n_cells, 0.05)
    # The Bonferroni cell p-value is conservative, so allow anything up to the upper limit.
    assert rej <= hi, (rej, lo, hi)


@pytest.mark.slow
def test_null_rejection_rate_design_size() -> None:
    # M1 done-check: correct split, R=200, 500 cells, rate within a binomial 99% interval
    # (upper side; the within-cell Bonferroni combination is conservative).
    n_cells = 500
    rej = _null_rejections(n_cells, r=200, m=500, seed=6)
    _, hi = sps.binom.ppf([0.005, 0.995], n_cells, 0.05)
    assert rej <= hi
    assert rej >= 5  # not degenerate


def test_power_against_off_by_one() -> None:
    rng = np.random.default_rng(7)
    n, m, r = 19, 200, 400
    law = laws.split_count_law(n, 0.1, m)
    k = laws.split_index(n, 0.1)
    s_plus = sps.betabinom.rvs(m, k + 1, n - k, size=r, random_state=rng)
    s_minus = sps.betabinom.rvs(m, k - 1, n + 2 - k, size=r, random_state=rng)
    up = stats.mean_test(s_plus, law)
    down = stats.mean_test(s_minus, law)
    assert up.pvalue < 1e-6 and up.direction == "above"
    assert down.pvalue < 1e-6 and down.direction == "below"


def test_t_tests_with_zero_variance() -> None:
    # Every repetition fully covered: above a lower bound, so no violation.
    assert stats.lower_bound_test(np.full(20, 50), 50, 0.8).pvalue == 1.0
    assert stats.lower_bound_test(np.full(20, 30), 50, 0.8).pvalue == 0.0
    law = CoverageLaw("mean", 50, 0.9)
    assert stats.mean_test(np.full(20, 45), law).pvalue == 1.0
    assert stats.mean_test(np.full(20, 50), law).pvalue == 0.0
