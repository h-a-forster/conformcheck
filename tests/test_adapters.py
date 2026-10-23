"""Adapter contract tests (DESIGN section 5 and the M3 done-check).

For the adapters listed in REPORT.md section 6 (every adapter behind a finding, plus
the split and LAC adapters of each library): the adapter output equals the library's
documented usage pattern written out by hand on the same data; the order statistic
used at n=19, alpha=0.1 is the value seen in scratch calls before the study (MAPIE 18,
puncc 18, TorchCP 18, crepes 19); ``k > n`` behaviour is captured as refused, error
or trivial; outputs are deterministic under a fixed seed.
"""

from __future__ import annotations

import warnings
from fractions import Fraction

import numpy as np
import pytest

from conformcheck import data, diagnostics, laws
from conformcheck.adapters import get_adapter, registry
from conformcheck.adapters.base import (
    ClassificationInput,
    CrossRegressionInput,
    RegressionInput,
)

pytestmark = pytest.mark.adapter

A10, TRIVIAL = Fraction(1, 10), Fraction(9, 200)  # n=19: k=18 and k=20 > n
N, M = 19, 40


def _reg_input(alphas=(A10,), seed=0, n=N) -> tuple[RegressionInput, data.Draw]:
    dgp = data.get_dgp("reg_gauss")
    d = dgp.draw(np.random.default_rng(seed), n, M)
    return (
        RegressionInput(
            d.x_cal, d.y_cal, d.x_test, list(alphas), dgp.model(), dgp.quantile_models(), seed=1
        ),
        d,
    )


def _cls_input(alphas=(A10,), seed=0, per_class=False, n=N) -> ClassificationInput:
    dgp = data.get_dgp("cls_gauss")
    d = dgp.draw(np.random.default_rng(seed), n, M, per_class=per_class)
    mdl = dgp.model()
    return ClassificationInput(
        d.x_cal,
        d.y_cal,
        d.x_test,
        list(alphas),
        mdl,
        mdl.predict_proba(d.x_cal),
        mdl.predict_proba(d.x_test),
        4,
        seed=1,
        per_class=per_class,
    )


def _rank(key: str, inp: RegressionInput) -> int:
    out = get_adapter(key).run(inp)[A10]
    assert out.status == "ok", out.message
    m = inp.model
    r = diagnostics.regression_ranks(
        "split_abs", "", out.intervals, inp.y_cal, m.predict(inp.x_cal), m.predict(inp.x_test)
    )
    assert r is not None and len(r) == 2
    assert all(not x.interpolated and x.k_lo == x.k_hi for x in r)
    assert r[0].k_hi == r[1].k_hi  # both endpoints use the same order statistic
    return r[0].k_hi


def test_registry_keys_and_specs() -> None:
    reg = registry()
    libs = {a.spec.library for a in reg.values()}
    assert libs == {"mapie", "crepes", "puncc", "torchcp", "reference"}
    assert sum(a.spec.library != "reference" for a in reg.values()) == 37
    for key, a in reg.items():
        assert key == a.spec.key


@pytest.mark.parametrize(
    ("key", "expected_k"),
    [
        ("mapie/split_abs/default", 18),
        ("puncc/split_abs/default", 18),
        ("torchcp/split_abs/default", 18),
        ("crepes/split_abs/default", 19),  # DESIGN hypothesis 1 (float 1 - 0.9)
        ("reference/split_abs/default", 18),
    ],
)
def test_rank_at_n19_alpha01(key: str, expected_k: int) -> None:
    lib = key.split("/")[0]
    if lib != "reference" and not get_adapter(key).available():
        pytest.skip(f"{lib} not installed")
    inp, _ = _reg_input()
    assert _rank(key, inp) == expected_k


def test_mapie_matches_documented_pattern() -> None:
    pytest.importorskip("mapie")
    from mapie.classification import SplitConformalClassifier
    from mapie.regression import SplitConformalRegressor

    inp, _ = _reg_input()
    r = SplitConformalRegressor(inp.model, confidence_level=0.9, prefit=True)
    r.conformalize(inp.x_cal, inp.y_cal)
    _, pis = r.predict_interval(inp.x_test)
    out = get_adapter("mapie/split_abs/default").run(inp)[A10]
    assert np.array_equal(out.intervals, pis[:, :, 0])
    ci = _cls_input()
    c = SplitConformalClassifier(
        ci.model, confidence_level=0.9, conformity_score="lac", prefit=True
    )
    c.conformalize(ci.x_cal, ci.y_cal)
    _, sets = c.predict_set(ci.x_test)
    assert np.array_equal(get_adapter("mapie/lac/default").run(ci)[A10].sets, sets[:, :, 0])


def test_crepes_matches_documented_pattern() -> None:
    pytest.importorskip("crepes")
    from crepes import WrapClassifier, WrapRegressor

    inp, _ = _reg_input()
    w = WrapRegressor(inp.model)
    w.calibrate(inp.x_cal, inp.y_cal)
    expected = w.predict_int(inp.x_test, confidence=0.9)
    assert np.array_equal(get_adapter("crepes/split_abs/default").run(inp)[A10].intervals, expected)
    ci = _cls_input()
    wc = WrapClassifier(ci.model)
    wc.calibrate(ci.x_cal, ci.y_cal)
    sets = wc.predict_set(ci.x_test, labels=False, confidence=0.9, smoothing=False)
    got = get_adapter("crepes/lac/unsmoothed").run(ci)[A10].sets
    assert np.array_equal(got, np.asarray(sets).astype(bool))


def test_puncc_matches_documented_pattern() -> None:
    pytest.importorskip("deel.puncc")
    from deel.puncc.api.prediction import BasePredictor
    from deel.puncc.regression import SplitCP

    inp, _ = _reg_input()
    cp = SplitCP(BasePredictor(inp.model, is_trained=True), train=False)
    cp.fit(X_calib=inp.x_cal, y_calib=inp.y_cal)
    _, lo, hi = cp.predict(inp.x_test, alpha=0.1)
    out = get_adapter("puncc/split_abs/default").run(inp)[A10]
    assert np.array_equal(out.intervals, np.column_stack([lo, hi]))


def test_torchcp_matches_documented_pattern() -> None:
    pytest.importorskip("torch")
    ad = get_adapter("torchcp/lac/default")
    if not ad.available():
        pytest.skip("torchcp not installed")
    ad.setup()
    import torch
    from torchcp.classification.predictor import SplitPredictor
    from torchcp.classification.score import LAC

    ci = _cls_input()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        p = SplitPredictor(score_function=LAC(), model=None)
        p.calculate_threshold(
            torch.log(torch.tensor(ci.proba_cal, dtype=torch.float32)), torch.tensor(ci.y_cal), 0.1
        )
        sets = p.predict_with_logits(torch.log(torch.tensor(ci.proba_test, dtype=torch.float32)))
    assert np.array_equal(ad.run(ci)[A10].sets, sets.numpy().astype(bool))


def _cross_input(n_folds: int | None, n: int = 20) -> CrossRegressionInput:
    dgp = data.get_dgp("reg_gauss")
    d = dgp.draw(np.random.default_rng(0), n, M)
    return CrossRegressionInput(
        d.x_cal, d.y_cal, d.x_test, [A10], dgp.estimator_factory, n_folds, seed=3
    )


# Documented usage for the adapters behind the findings (REPORT.md, F1, F3-F6, F8-F10).
# Each test writes the library call out by hand, as its documentation shows it, and
# checks the adapter returns the same arrays. This shows the adapter adds nothing (no
# slicing, seeding or label-mapping mistakes); it is not an independent check of the
# library, since a hand-written call follows the same documented pattern.


@pytest.mark.parametrize("ill", [False, True, "randomized"])
def test_mapie_aps_matches_documented_pattern(ill: bool | str) -> None:
    pytest.importorskip("mapie")
    from mapie.classification import SplitConformalClassifier

    ci = _cls_input(n=50)
    c = SplitConformalClassifier(
        ci.model, confidence_level=0.9, conformity_score="aps", prefit=True, random_state=1
    )
    c.conformalize(ci.x_cal, ci.y_cal)
    _, sets = c.predict_set(ci.x_test, conformity_score_params={"include_last_label": ill})
    got = get_adapter(f"mapie/aps/include_last_label={ill}").run(ci)[A10].sets
    assert np.array_equal(got, sets[:, :, 0])


@pytest.mark.parametrize("ill", [True, "randomized"])
def test_mapie_raps_matches_documented_pattern(ill: bool | str) -> None:
    pytest.importorskip("mapie")
    from mapie.classification import SplitConformalClassifier
    from mapie.conformity_scores import RAPSConformityScore

    ci = _cls_input(n=100)
    c = SplitConformalClassifier(
        ci.model,
        confidence_level=0.9,
        conformity_score=RAPSConformityScore(),
        prefit=True,
        random_state=1,
    )
    c.conformalize(ci.x_cal, ci.y_cal)
    _, sets = c.predict_set(ci.x_test, conformity_score_params={"include_last_label": ill})
    out = get_adapter(f"mapie/raps/include_last_label={ill}").run(ci)[A10]
    assert np.array_equal(out.sets, sets[:, :, 0])
    assert out.effective_n == 90  # n - ceil(0.1 n) (F9)


def test_mapie_split_cqr_and_cv_plus_match_documented_pattern() -> None:
    pytest.importorskip("mapie")
    from mapie.regression import (
        ConformalizedQuantileRegressor,
        CrossConformalRegressor,
        SplitConformalRegressor,
    )
    from sklearn.model_selection import KFold

    inp, _ = _reg_input(n=49)  # asymmetric CQR refuses alpha = 0.1 at n = 19 (F4)
    assert inp.quantile_models is not None
    r = ConformalizedQuantileRegressor(list(inp.quantile_models), confidence_level=0.9, prefit=True)
    r.conformalize(inp.x_cal, inp.y_cal)
    for sym, key in ((False, "mapie/cqr/asymmetric"), (True, "mapie/cqr/symmetric")):
        _, pis = r.predict_interval(inp.x_test, symmetric_correction=sym)
        assert np.array_equal(get_adapter(key).run(inp)[A10].intervals, pis[:, :, 0])
    sr = SplitConformalRegressor(inp.model, confidence_level=0.9, prefit=True)
    sr.conformalize(inp.x_cal, inp.y_cal)
    _, pis = sr.predict_interval(inp.x_test, allow_infinite_bounds=True)
    got = get_adapter("mapie/split_abs/allow_infinite_bounds").run(inp)[A10].intervals
    assert np.array_equal(got, pis[:, :, 0])
    for k in (5, 10):
        ci = _cross_input(k)
        cc = CrossConformalRegressor(
            ci.estimator_factory(),
            confidence_level=0.9,
            method="plus",
            cv=KFold(k, shuffle=True, random_state=ci.seed),
            random_state=ci.seed,
        )
        cc.fit_conformalize(ci.x, ci.y)
        _, pis = cc.predict_interval(ci.x_test, allow_infinite_bounds=True)
        got = get_adapter(f"mapie/cv_plus/K={k}").run(ci)[A10].intervals
        assert np.array_equal(got, pis[:, :, 0])


def test_mapie_aps_reuses_calibration_uniforms_at_test_time() -> None:
    """Known MAPIE 1.6.0 behaviour (REPORT.md, section 7).

    With an int ``random_state``, the test-time tie-break uniforms repeat the calibration
    uniforms, so test point i shares U with calibration point i. If this test fails,
    MAPIE changed the behaviour and the caveat in REPORT.md should be revisited.
    """
    pytest.importorskip("mapie")
    from unittest import mock

    import mapie.conformity_scores.sets.aps as aps_mod
    from mapie.classification import SplitConformalClassifier
    from sklearn.utils import check_random_state

    draws: list[np.ndarray] = []

    class Recorder:
        def __init__(self, rs: np.random.RandomState) -> None:
            self.rs = rs

        def uniform(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            out = self.rs.uniform(*args, **kwargs)
            draws.append(np.asarray(out).ravel().copy())
            return out

    ci = _cls_input(n=30)
    with mock.patch.object(
        aps_mod, "check_random_state", lambda s: Recorder(check_random_state(s))
    ):
        c = SplitConformalClassifier(
            ci.model, confidence_level=0.9, conformity_score="aps", prefit=True, random_state=7
        )
        c.conformalize(ci.x_cal, ci.y_cal)
        c.predict_set(ci.x_test, conformity_score_params={"include_last_label": "randomized"})
    assert [len(d) for d in draws] == [30, M]
    assert np.array_equal(draws[0], draws[1][:30])


def test_crepes_class_conditional_matches_documented_pattern() -> None:
    pytest.importorskip("crepes")
    from crepes import WrapClassifier

    ci = _cls_input(per_class=True)
    wc = WrapClassifier(ci.model)
    wc.calibrate(ci.x_cal, ci.y_cal, class_cond=True)
    sets = wc.predict_set(ci.x_test, labels=False, confidence=0.9, smoothing=False)
    got = get_adapter("crepes/class_conditional/unsmoothed").run(ci)[A10].sets
    assert np.array_equal(got, np.asarray(sets).astype(bool))


def test_puncc_cv_plus_and_raps_match_documented_pattern() -> None:
    pytest.importorskip("deel.puncc")
    from deel.puncc.api.prediction import BasePredictor
    from deel.puncc.classification import RAPS
    from deel.puncc.regression import CVPlus

    from conformcheck.adapters.puncc import _proba_predictor

    for k in (5, 10):
        ci = _cross_input(k)
        cp = CVPlus(BasePredictor(ci.estimator_factory()), K=k, random_state=ci.seed)
        cp.fit(X=ci.x, y=ci.y)
        _, lo, hi = cp.predict(ci.x_test, alpha=0.1)
        got = get_adapter(f"puncc/cv_plus/K={k}").run(ci)[A10].intervals
        assert np.array_equal(got, np.column_stack([lo, hi]))
    # jackknife+ is CVPlus with K = n; the documented call crashes as the adapter does (F6)
    ci = _cross_input(None)
    out = get_adapter("puncc/jackknife_plus/K=n").run(ci)[A10]
    assert out.status == "error"
    cp = CVPlus(BasePredictor(ci.estimator_factory()), K=len(ci.y), random_state=ci.seed)
    with pytest.raises(TypeError, match="has no len"):
        cp.fit(X=ci.x, y=ci.y)
        cp.predict(ci.x_test, alpha=0.1)
    assert "has no len" in out.message

    cl = _cls_input()
    np.random.seed(cl.seed)  # puncc randomizes through the global numpy state
    rc = RAPS(_proba_predictor(cl.model), train=False, lambd=0.1, k_reg=1, rand=True)
    rc.fit(X_calib=cl.x_cal, y_calib=cl.y_cal)
    _, sets = rc.predict(cl.x_test, alpha=0.1)
    expected = np.zeros((len(sets), 4), dtype=bool)
    for i, s in enumerate(sets):
        expected[i, list(s)] = True
    assert np.array_equal(get_adapter("puncc/raps/rand=True").run(cl)[A10].sets, expected)


@pytest.mark.parametrize("score", ["abs", "cqr"])
def test_torchcp_regression_matches_documented_pattern(score: str) -> None:
    pytest.importorskip("torch")
    ad = get_adapter("torchcp/split_abs/default" if score == "abs" else "torchcp/cqr/default")
    if not ad.available():
        pytest.skip("torchcp not installed")
    ad.setup()
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    from torchcp.regression.predictor import SplitPredictor
    from torchcp.regression.score import ABS, CQR

    class Identity(torch.nn.Module):
        def forward(self, x):  # type: ignore[no-untyped-def]
            return x

    inp, _ = _reg_input()
    if score == "abs":
        models = [inp.model]
    else:
        assert inp.quantile_models is not None
        models = list(inp.quantile_models[:2])

    def feats(x: np.ndarray):  # type: ignore[no-untyped-def]
        cols = np.column_stack([mdl.predict(x) for mdl in models])  # type: ignore[attr-defined]
        return torch.tensor(cols, dtype=torch.float32)

    f_cal, f_test = feats(inp.x_cal), feats(inp.x_test)
    y_cal = torch.tensor(inp.y_cal, dtype=torch.float32)
    sf = ABS() if score == "abs" else CQR()
    p = SplitPredictor(score_function=sf, model=Identity(), device="cpu")
    p.calibrate(DataLoader(TensorDataset(f_cal, y_cal), batch_size=N), alpha=0.1)
    iv = p.predict(f_test).detach().numpy().astype(float).reshape(M, -1, 2)[:, 0, :]
    assert np.array_equal(ad.run(inp)[A10].intervals, iv)


@pytest.mark.parametrize(
    ("key", "statuses"),
    [
        ("mapie/split_abs/default", {"refused"}),
        ("mapie/split_abs/allow_infinite_bounds", {"refused"}),  # option ignored (finding)
        ("puncc/split_abs/default", {"refused"}),
        ("crepes/split_abs/default", {"ok"}),
        ("torchcp/split_abs/default", {"error"}),  # crashes (finding)
        ("reference/split_abs/default", {"ok"}),
    ],
)
def test_k_greater_than_n_behaviour(key: str, statuses: set[str]) -> None:
    ad = get_adapter(key)
    if not ad.available():
        pytest.skip("library not installed")
    inp, _ = _reg_input(alphas=(TRIVIAL,))
    out = ad.run(inp)[TRIVIAL]
    assert out.status in statuses, (out.status, out.message)
    if out.status == "ok":
        assert diagnostics.is_trivial(out.intervals, None)


@pytest.mark.parametrize(
    "key",
    [
        k
        for k, a in registry().items()
        if a.spec.task == "classification" and a.spec.library != "reference"
    ],
)
def test_classification_shapes_and_determinism(key: str) -> None:
    ad = get_adapter(key)
    if not ad.available():
        pytest.skip("library not installed")
    per_class = ad.spec.method == "class_conditional"
    # MAPIE RAPS holds out ceil(0.1 n) points, stratified: it needs n >= 31 with 4 classes
    n = 100 if key.startswith("mapie/raps/") else N
    ci = _cls_input(alphas=(A10, Fraction(1, 5)), per_class=per_class, n=n)
    o1 = ad.run(ci)
    o2 = ad.run(ci)
    for a in ci.alphas:
        assert o1[a].status == "ok", o1[a].message
        assert o1[a].sets.shape == (len(ci.x_test), 4) and o1[a].sets.dtype == bool
        assert np.array_equal(o1[a].sets, o2[a].sets)


@pytest.mark.parametrize(
    "key", [k for k, a in registry().items() if a.spec.task == "cross_regression"]
)
def test_cross_constant_model_rank(key: str) -> None:
    ad = get_adapter(key)
    if not ad.available():
        pytest.skip("library not installed")
    dgp = data.get_dgp("reg_constant")
    d = dgp.draw(np.random.default_rng(0), 20, M)  # n=20: every K in {5, 10} divides n
    inp = CrossRegressionInput(
        d.x_cal, d.y_cal, d.x_test, [A10], dgp.estimator_factory, ad.n_folds, seed=3
    )
    out = ad.run(inp)[A10]
    if key == "puncc/jackknife_plus/K=n":
        assert out.status == "error"  # CVPlus crashes on folds of size one (finding)
        return
    assert out.status == "ok", out.message
    r = diagnostics.regression_ranks(
        "cv_plus", "", out.intervals, d.y_cal, np.zeros(20), np.zeros(M)
    )
    k = laws.split_index(20, A10)
    # both endpoints: an off-by-one on the upper endpoint alone must fail this test
    assert r is not None and len(r) == 2
    assert all(x.offset(k) == 0 for x in r), [x.offset(k) for x in r]
