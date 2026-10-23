"""Reference implementations, mutants and DGPs (DESIGN sections 4 and 6, milestone M2)."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from conformcheck import data, laws, reference, stats
from conformcheck.models import ConstantRegressor

A10 = Fraction(1, 10)


def test_threshold_hand_values() -> None:
    scores = np.arange(1.0, 20.0)  # 1..19, n = 19
    rng = np.random.default_rng(0)
    rng.shuffle(scores)
    assert reference.conformal_threshold(scores, A10) == 18.0  # k = 18
    assert reference.conformal_threshold(scores, Fraction(1, 5)) == 16.0
    assert reference.conformal_threshold(scores, Fraction(1, 20)) == 19.0
    assert reference.conformal_threshold(scores[:5], A10) == np.inf  # k = 6 > 5
    # n = 4 explicit: k = ceil(5 * 0.8) = 4
    assert reference.conformal_threshold(np.array([0.3, 0.1, 0.4, 0.2]), Fraction(1, 5)) == 0.4


@pytest.mark.parametrize(
    ("mutant", "expected"),
    [
        ("k_minus_1", 17.0),
        ("k_plus_1", 19.0),
        ("n_instead_of_n_plus_1", 18.0),  # ceil(19 * 0.9) = 18: same as k at n = 19
        ("no_correction_linear", float(np.quantile(np.arange(1.0, 20.0), 0.9))),
    ],
)
def test_mutants_n19(mutant: str, expected: float) -> None:
    scores = np.arange(1.0, 20.0)
    assert reference.mutant_threshold(scores, A10, mutant) == pytest.approx(expected)


def test_mutants_shift_k_at_n20() -> None:
    scores = np.arange(1.0, 21.0)  # n = 20: k = ceil(21 * 0.9) = 19
    assert reference.conformal_threshold(scores, A10) == 19.0
    assert reference.mutant_threshold(scores, A10, "n_instead_of_n_plus_1") == 18.0
    assert reference.mutant_threshold(scores, A10, "k_plus_1") == 20.0
    assert reference.mutant_threshold(scores, Fraction(1, 21), "k_plus_1") == np.inf  # k = n
    with pytest.raises(ValueError):
        reference.mutant_threshold(scores, A10, "nope")


def test_k_minus_1_is_finite_when_trivial_set_required() -> None:
    scores = np.arange(1.0, 6.0)  # n = 5, alpha = 0.1: k = 6
    assert reference.mutant_threshold(scores, A10, "k_minus_1") == 5.0


def test_split_abs_and_cqr() -> None:
    y = np.array([0.0, 1.0, -2.0, 3.0])
    yhat = np.zeros(4)
    iv = reference.split_abs(y, yhat, np.array([10.0]), Fraction(1, 5))  # k = 4 -> 3
    assert iv.tolist() == [[7.0, 13.0]]
    lo, hi = np.full(4, -1.0), np.full(4, 1.0)
    sym = reference.cqr(lo, hi, y, np.array([0.0]), np.array([1.0]), Fraction(1, 5))
    # scores max(-1 - y, y - 1) = [-1, 0, 1, 2]; k = 4 -> 2
    assert sym.tolist() == [[-2.0, 3.0]]
    asym = reference.cqr(lo, hi, y, np.array([0.0]), np.array([1.0]), Fraction(2, 5), False)
    # alpha/2 = 1/5: k' = 4; lo scores -1 - y = [-1, -2, 1, -4] -> 1; hi y - 1 -> 2
    assert asym.tolist() == [[-1.0, 3.0]]


def test_jackknife_plus_constant_model_equals_split_on_n() -> None:
    rng = np.random.default_rng(1)
    x, y = rng.uniform(size=(19, 2)), rng.normal(size=19)
    xt = rng.uniform(size=(5, 2))
    jk = reference.jackknife_plus(x, y, xt, A10, lambda: ConstantRegressor(0.0))
    split = reference.split_abs(y, np.zeros(19), np.zeros(5), A10)
    assert np.allclose(jk, split)
    folds = reference.kfold_indices(19, 5, rng)
    cv = reference.cv_plus(x, y, xt, A10, lambda: ConstantRegressor(0.0), folds)
    assert np.allclose(cv, split)
    trivial = reference.jackknife_plus(x, y, xt, Fraction(1, 25), lambda: ConstantRegressor(0.0))
    assert np.all(np.isinf(trivial))


def test_kfold_indices_partition() -> None:
    folds = reference.kfold_indices(23, 5, np.random.default_rng(2))
    assert len(folds) == 5
    assert sorted(np.concatenate(folds).tolist()) == list(range(23))


def test_lac_and_class_conditional() -> None:
    proba_cal = np.array([[0.9, 0.1], [0.6, 0.4], [0.2, 0.8], [0.3, 0.7]])
    y_cal = np.array([0, 0, 1, 1])  # scores 0.1, 0.4, 0.2, 0.3
    pt = np.array([[0.65, 0.35], [0.5, 0.5]])
    # alpha = 0.2: k = 4 -> q = 0.4; include labels with 1 - p <= 0.4
    sets = reference.lac(proba_cal, y_cal, pt, Fraction(1, 5))
    assert sets.tolist() == [[True, False], [False, False]]
    # class-conditional at alpha = 1/3: n_y = 2, k = 2 -> class 0 q = 0.4, class 1 q = 0.3
    cc = reference.class_conditional_lac(proba_cal, y_cal, pt, Fraction(1, 3))
    assert cc.tolist() == [[True, False], [False, False]]


def test_aps_scores_and_sets() -> None:
    p = np.array([[0.5, 0.3, 0.2]])
    det = reference._aps_scores(p, None)
    assert np.allclose(det, [[0.5, 0.8, 1.0]])
    rnd = reference._aps_scores(p, np.array([0.5]))
    assert np.allclose(rnd, [[0.25, 0.65, 0.9]])
    rng = np.random.default_rng(3)
    pc = rng.dirichlet(np.ones(3), size=50)
    yc = rng.integers(0, 3, size=50)
    sets = reference.aps(pc, yc, pc[:10], A10, randomized=True, rng=rng)
    assert sets.shape == (10, 3)
    with pytest.raises(ValueError):
        reference.aps(pc, yc, pc, A10, randomized=True)


def test_smoothed_lac_shape_and_extremes() -> None:
    rng = np.random.default_rng(4)
    pc = rng.dirichlet(np.ones(3), size=30)
    yc = rng.integers(0, 3, size=30)
    sets = reference.smoothed_lac(pc, yc, pc[:7], A10, rng)
    assert sets.shape == (7, 3) and sets.dtype == bool


# --- DGPs -------------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(data.DGPS))
def test_dgp_draw_shapes_and_determinism(name: str) -> None:
    dgp = data.get_dgp(name)
    n, m = 19, 40
    ss = data.rep_seed_sequence(1, name, n, 0)
    d1 = dgp.draw(np.random.default_rng(ss), n, m)
    d2 = dgp.draw(np.random.default_rng(data.rep_seed_sequence(1, name, n, 0)), n, m)
    assert d1.x_cal.shape[0] == n and d1.y_cal.shape == (n,)
    assert d1.x_test.shape[0] == dgp.test_size(n, m)
    assert np.array_equal(d1.y_test, d2.y_test)
    model = dgp.model()
    if dgp.task == "regression":
        assert model.predict(d1.x_cal).shape == (n,)  # type: ignore[attr-defined]
    else:
        proba = model.predict_proba(d1.x_cal)  # type: ignore[attr-defined]
        assert proba.shape == (n, dgp.n_classes)
        assert np.allclose(proba.sum(axis=1), 1.0)


def test_per_class_draw() -> None:
    dgp = data.get_dgp("cls_gauss")
    d = dgp.draw(np.random.default_rng(0), 9, 100, per_class=True)
    assert np.bincount(d.y_cal).tolist() == [9, 9, 9, 9]
    assert np.bincount(d.y_test).tolist() == [25, 25, 25, 25]
    assert dgp.test_size(9, 102, per_class=True) == 100


def test_toy_pool_and_quantile_models() -> None:
    dgp = data.get_dgp("diabetes")
    assert dgp.test_size(99, 500) == 342 - 99
    lo, hi, med = dgp.quantile_models()  # type: ignore[misc]
    x = data._toy_pool("diabetes")[0][:5]
    assert np.all(lo.predict(x) < med.predict(x)) and np.all(med.predict(x) < hi.predict(x))
    assert len(data._toy_pool("digits")[1]) == 1297


def test_tied_score_pmf() -> None:
    dgp = data.get_dgp("reg_tied")
    d = dgp.draw(np.random.default_rng(5), 7000, 1)
    freq = np.bincount(np.abs(d.y_cal).astype(int), minlength=4) / 7000
    assert np.allclose(freq, dgp.score_pmf, atol=0.02)


def test_library_seed_is_deterministic() -> None:
    ss = data.rep_seed_sequence(3, "reg_gauss", 10, 2)
    assert data.library_seed(ss) == data.library_seed(data.rep_seed_sequence(3, "reg_gauss", 10, 2))
    assert 0 <= data.library_seed(ss) < 2**31


# --- reference passes, mutants are detected (M2 done-check) -----------------------------


def _ref_counts(mutant: str | None, n: int, reps: int, m: int) -> np.ndarray:
    dgp = data.get_dgp("reg_gauss")
    model = dgp.model()
    out = []
    for r in range(reps):
        d = dgp.draw(np.random.default_rng(data.rep_seed_sequence(7, "reg_gauss", n, r)), n, m)
        iv = reference.split_abs(
            d.y_cal,
            model.predict(d.x_cal),
            model.predict(d.x_test),
            A10,
            mutant,  # type: ignore[attr-defined]
        )
        out.append(int(np.sum((iv[:, 0] <= d.y_test) & (d.y_test <= iv[:, 1]))))
    return np.array(out)


def test_reference_passes_and_mutants_detected_n19() -> None:
    n, reps, m = 19, 200, 200
    law = laws.split_count_law(n, A10, m)

    def pval(counts: np.ndarray) -> float:
        return stats.cell_pvalue(
            stats.mean_test(counts, law).pvalue, stats.gof_test(counts, law).pvalue
        )

    assert pval(_ref_counts(None, n, reps, m)) > 0.01
    for mutant in ("k_minus_1", "k_plus_1", "no_correction_linear"):
        assert pval(_ref_counts(mutant, n, reps, m)) < 1e-4, mutant
