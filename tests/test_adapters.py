"""Adapter contract tests (DESIGN section 5 and the M3 done-check).

For every library: the adapter output equals the library's documented usage pattern
written out by hand on the same data; the order statistic used at n=19, alpha=0.1 is the
value seen in scratch calls before the study (MAPIE 18, puncc 18, TorchCP 18, crepes
19); ``k > n`` behaviour is captured as refused, error or trivial; outputs are
deterministic under a fixed seed.
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


def _reg_input(alphas=(A10,), seed=0) -> tuple[RegressionInput, data.Draw]:
    dgp = data.get_dgp("reg_gauss")
    d = dgp.draw(np.random.default_rng(seed), N, M)
    return (
        RegressionInput(
            d.x_cal, d.y_cal, d.x_test, list(alphas), dgp.model(), dgp.quantile_models(), seed=1
        ),
        d,
    )


def _cls_input(alphas=(A10,), seed=0, per_class=False) -> ClassificationInput:
    dgp = data.get_dgp("cls_gauss")
    d = dgp.draw(np.random.default_rng(seed), N, M, per_class=per_class)
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
    assert sum(a.spec.library != "reference" for a in reg.values()) == 31
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
    ci = _cls_input(alphas=(A10, Fraction(1, 5)), per_class=per_class)
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
