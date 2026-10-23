"""Public testing API (milestone M7) and deterministic diagnostics."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest

from conformcheck import diagnostics, reference
from conformcheck.testing import check_split_classifier, check_split_regressor


def good_split(x_cal, y_cal, x_test, alpha, model):  # type: ignore[no-untyped-def]
    return reference.split_abs(
        y_cal, model.predict(x_cal), model.predict(x_test), Fraction(repr(alpha))
    )


def off_by_one(x_cal, y_cal, x_test, alpha, model):  # type: ignore[no-untyped-def]
    return reference.split_abs(
        y_cal, model.predict(x_cal), model.predict(x_test), Fraction(repr(alpha)), "k_minus_1"
    )


def test_check_split_regressor_reference_passes() -> None:
    rep = check_split_regressor(good_split, n=(9, 19), alpha=(0.1, 0.2), reps=60, test_points=50)
    rep.assert_valid()
    assert rep.ok and len(rep.cells) == 4


def test_check_split_regressor_mutant_fails_readably() -> None:
    rep = check_split_regressor(off_by_one, n=19, alpha=0.1, reps=30, test_points=50)
    with pytest.raises(AssertionError) as exc:
        rep.assert_valid()
    msg = str(exc.value)
    assert "1 of 1 conformance cells failed" in msg
    assert "FAIL" in msg and "order statistic -1" in msg


def test_check_split_regressor_trivial_cell() -> None:
    rep = check_split_regressor(off_by_one, n=5, alpha=0.1, reps=5, test_points=20)
    assert rep.cells[0].status == "FAIL"  # k = 6 > n requires an infinite interval
    rep = check_split_regressor(good_split, n=5, alpha=0.1, reps=5, test_points=20)
    assert rep.ok


def test_check_split_classifier() -> None:
    def lac(x_cal, y_cal, x_test, alpha, model):  # type: ignore[no-untyped-def]
        return reference.lac(
            model.predict_proba(x_cal), y_cal, model.predict_proba(x_test), Fraction(repr(alpha))
        )

    def lac_kp1(x_cal, y_cal, x_test, alpha, model):  # type: ignore[no-untyped-def]
        return reference.lac(
            model.predict_proba(x_cal),
            y_cal,
            model.predict_proba(x_test),
            Fraction(repr(alpha)),
            "k_plus_1",
        )

    check_split_classifier(lac, n=19, alpha=0.1, reps=150, test_points=100).assert_valid()
    rep = check_split_classifier(lac_kp1, n=9, alpha=0.2, reps=150, test_points=100)
    assert rep.cells[0].status == "CONSERVATIVE"
    rep.assert_valid(allow_conservative=True)
    with pytest.raises(AssertionError):
        rep.assert_valid()


def test_shape_errors() -> None:
    with pytest.raises(ValueError):
        check_split_regressor(lambda *a: np.zeros((3, 2)), n=9, alpha=0.1, reps=1)


def test_plugin_settings_drive_defaults(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        from conformcheck.pytest_plugin import current_settings
        def test_it(conformcheck_settings):
            assert conformcheck_settings.reps == 7
            assert current_settings().seed == 3
        """
    )
    res = pytester.runpytest("--conformcheck-reps", "7", "--conformcheck-seed", "3")
    res.assert_outcomes(passed=1)


# --- diagnostics ------------------------------------------------------------------------


def test_rank_range() -> None:
    s = np.array([0.1, 0.5, 0.2, 0.9])
    assert diagnostics.rank_range(s, 0.5) == diagnostics.RankRange(3, 3)
    r = diagnostics.rank_range(s, 0.3)
    assert r.interpolated and r.offset(3) == -0.5 and r.offset(2) == 0.5
    assert diagnostics.rank_range(s, math.inf) == diagnostics.RankRange(5, 5)
    tied = diagnostics.rank_range(np.array([1.0, 1.0, 2.0]), 1.0)
    assert (tied.k_lo, tied.k_hi) == (1, 2) and tied.offset(2) == 0 and tied.offset(3) == -1
    assert diagnostics.RankRange(4, 4).offset(3) == 1


def test_regression_ranks_cqr_and_bracket() -> None:
    y = np.array([0.0, 1.0, -2.0, 3.0])
    lo_c, hi_c = np.full(4, -1.0), np.full(4, 1.0)
    iv = reference.cqr(lo_c, hi_c, y, np.array([0.0]), np.array([1.0]), Fraction(1, 5))
    r = diagnostics.regression_ranks(
        "cqr", "symmetric", iv, y, q_cal=(lo_c, hi_c), q_test=(np.array([0.0]), np.array([1.0]))
    )
    assert r is not None and all(x.offset(4) == 0 for x in r)
    assert diagnostics.regression_ranks("lac", "", iv, y) is None
    cal = np.array([0.1, 0.2, 0.3, 0.4])
    br = diagnostics.bracket_rank(cal, np.array([[0.15, 0.35]]), np.array([[True, False]]))
    assert br is not None and br.k_lo <= 1 <= br.k_hi


def test_is_trivial_and_compare() -> None:
    assert diagnostics.is_trivial(np.array([[-np.inf, np.inf]]), None)
    assert not diagnostics.is_trivial(np.array([[-1.0, np.inf]]), None)
    assert diagnostics.is_trivial(None, np.ones((2, 3), bool))
    a = np.array([[0.0, 1.0], [-np.inf, np.inf]])
    assert diagnostics.compare_to_reference(a, a + 0.0, "intervals") == 0.0
    assert (
        diagnostics.compare_to_reference(np.ones((2, 2), bool), np.eye(2, dtype=bool), "sets")
        == 0.5
    )
