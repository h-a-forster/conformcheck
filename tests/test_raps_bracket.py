"""RAPS (reference, laws, adapters) and bracketing as rank recovery for classification."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from conformcheck import laws, reference, stats
from conformcheck.adapters import get_adapter
from conformcheck.adapters.base import ClassificationInput
from conformcheck.data import get_dgp
from conformcheck.runner import evaluate_unit
from conformcheck.study import cell_law, mapie_raps_effective_n
from conformcheck.testing import check_split_classifier

A10 = Fraction(1, 10)


def _proba(rng: np.random.Generator, n: int, k: int = 4) -> np.ndarray:
    return rng.dirichlet(np.ones(k), size=n)


def test_raps_without_penalty_is_aps() -> None:
    rng = np.random.default_rng(0)
    pc, pt = _proba(rng, 50), _proba(rng, 30)
    y = rng.integers(0, 4, 50)
    det = reference.raps(pc, y, pt, A10, randomized=False, lambd=0.0)
    assert np.array_equal(det, reference.aps(pc, y, pt, A10, randomized=False))
    r1 = reference.raps(pc, y, pt, A10, True, np.random.default_rng(5), lambd=0.0)
    r2 = reference.aps(pc, y, pt, A10, True, np.random.default_rng(5))
    assert np.array_equal(r1, r2)


def test_raps_scores_hand_example() -> None:
    p = np.array([[0.1, 0.5, 0.4]])
    # ranks 3, 1, 2; deterministic APS scores 1.0, 0.5, 0.9; penalty 0.1 * (rank - 1)^+
    got = reference._raps_scores(p, None, 0.1, 1)
    assert np.allclose(got, [[1.0 + 0.2, 0.5, 0.9 + 0.1]])
    got = reference._raps_scores(p, np.array([0.5]), 0.1, 2)
    assert np.allclose(got, [[0.95 + 0.1, 0.25, 0.7]])


def test_raps_randomized_reference_follows_exact_law() -> None:
    dgp = get_dgp("cls_gauss")
    model = dgp.model()
    n, m, reps = 19, 100, 300
    counts = []
    for rep in range(reps):
        rng = np.random.default_rng([7, rep])
        d = dgp.draw(rng, n, m)
        sets = reference.raps(
            model.predict_proba(d.x_cal), d.y_cal, model.predict_proba(d.x_test), A10, True, rng
        )
        counts.append(int(sets[np.arange(m), d.y_test].sum()))
    law = laws.split_count_law(n, A10, m)
    assert stats.mean_test(np.array(counts), law).pvalue > 1e-3


def test_mapie_raps_cell_law_uses_effective_n() -> None:
    assert mapie_raps_effective_n(100) == 90
    assert mapie_raps_effective_n(19) == 17  # ceil(1.9) = 2
    assert mapie_raps_effective_n(1000) == 900
    cl = cell_law(
        method="raps",
        variant="include_last_label=randomized",
        library="mapie",
        dgp="cls_gauss",
        n=100,
        alpha=A10,
        m=50,
    )
    assert cl.kind == "exact" and cl.k == laws.split_index(90, A10) == 82
    assert cl.target == pytest.approx(82 / 91)
    other = cell_law(
        method="raps", variant="randomized=True", library="torchcp", dgp="cls_gauss", n=100,
        alpha=A10, m=50,
    )  # fmt: skip
    assert other.k == 91 and not other.one_sided
    det = cell_law(
        method="raps", variant="rand=False", library="puncc", dgp="cls_gauss", n=100,
        alpha=A10, m=50,
    )  # fmt: skip
    assert det.one_sided
    triv = cell_law(
        method="raps", variant="include_last_label=True", library="mapie", dgp="cls_gauss",
        n=100, alpha=Fraction(1, 101), m=50,
    )  # fmt: skip
    assert triv.kind == "trivial"  # k = n for n = 100 but k_eff > n_eff = 90


@pytest.mark.adapter
def test_mapie_raps_reports_effective_n() -> None:
    pytest.importorskip("mapie")
    dgp = get_dgp("cls_gauss")
    model = dgp.model()
    d = dgp.draw(np.random.default_rng(0), 100, 40)
    ci = ClassificationInput(
        d.x_cal, d.y_cal, d.x_test, [A10], model,
        model.predict_proba(d.x_cal), model.predict_proba(d.x_test), 4, seed=1,
    )  # fmt: skip
    out = get_adapter("mapie/raps/include_last_label=randomized").run(ci)[A10]
    assert out.status == "ok", out.message
    assert out.effective_n == mapie_raps_effective_n(100)


def _unit(adapter: str, n: int, alphas: tuple[str, ...], per_class: bool = False) -> dict:
    method = adapter.split("/")[1]
    return {
        "adapter": adapter,
        "dgp": "cls_gauss",
        "n": n,
        "alphas": list(alphas),
        "grid": "class_conditional" if per_class else "split",
        "n_folds": None,
        "per_class": per_class,
        "method": method,
    }


def test_bracketing_catches_one_step_classifier_errors_at_large_n() -> None:
    cfg = {"reps": 6, "test_points": 500, "seed": 3}
    alphas = ("1/10", "1/5")
    ok = evaluate_unit(_unit("reference/lac/default", 999, alphas), cfg)
    for ao in ok["alphas_out"].values():
        assert ao["bracket_offsets"] == {"0": 6}
    for mutant, sign in (("k_plus_1", "1"), ("k_minus_1", "-1")):
        rec = evaluate_unit(_unit(f"reference/lac/{mutant}", 999, alphas), cfg)
        for ao in rec["alphas_out"].values():
            assert ao["bracket_offsets"].get(sign, 0) >= 1, (mutant, ao["bracket_offsets"])
            assert set(ao["bracket_offsets"]) <= {"0", sign}


def test_bracketing_class_conditional_reference() -> None:
    cfg = {"reps": 4, "test_points": 200, "seed": 1}
    rec = evaluate_unit(
        _unit("reference/class_conditional/default", 49, ("1/10",), per_class=True), cfg
    )
    assert rec["alphas_out"]["1/10"]["bracket_offsets"] == {"0": 4}


def test_check_split_classifier_lac_bracketing() -> None:
    def lac(x_cal, y_cal, x_test, alpha, model, mutant=None):  # type: ignore[no-untyped-def]
        a = laws.as_fraction(alpha)
        return reference.lac(
            model.predict_proba(x_cal), y_cal, model.predict_proba(x_test), a, mutant
        )

    good = check_split_classifier(lac, n=999, alpha=0.1, reps=5, test_points=300, score="lac")
    assert good.ok, good.summary()
    bad = check_split_classifier(
        lambda *a: lac(*a, mutant="k_plus_1"),
        n=999, alpha=0.1, reps=5, test_points=300, score="lac",
    )  # fmt: skip
    assert bad.cells[0].status == "CONSERVATIVE", bad.summary()
    with pytest.raises(ValueError):
        check_split_classifier(lac, score="abs")  # type: ignore[arg-type]


def test_plan_probes_smallest_middle_largest_n() -> None:
    from conformcheck.plan import probe_points
    from conformcheck.study import Unit

    us = [Unit("x/y/z", "lac", "cls_gauss", n, ("1/10",), "split") for n in (5, 9, 10, 99, 1000)]
    assert [u.n for u in probe_points(us)] == [5, 10, 1000]
    assert [u.n for u in probe_points(us[:1])] == [5]
    assert [u.n for u in probe_points(us[:2])] == [5, 9]
