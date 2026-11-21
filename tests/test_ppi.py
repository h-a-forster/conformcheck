"""Exact law and pipeline of the prediction-powered inference study (DESIGN section 15)."""

from __future__ import annotations

import dataclasses
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
from scipy import stats

from conformcheck import ppi, study


def _study(**kw: object) -> ppi.PPIStudy:
    return dataclasses.replace(ppi.load_ppi_study(), **kw)


def test_builtin_study_loads_and_conformal_loader_refuses_it() -> None:
    s = ppi.load_ppi_study()
    assert s.n == (20, 50, 100, 200) and s.n_unlabelled == 10000 and s.workers <= 4
    assert len(s.units()) == 64
    with pytest.raises(ValueError, match="conformcheck.ppi"):
        study.load_study("ppi")
    with pytest.raises(ValueError, match="not a ppi study"):
        ppi.load_ppi_study("default")


def test_cell_probabilities_outcomes_and_exact_mass() -> None:
    pi, acc = Fraction("0.02"), Fraction("0.95")
    probs = ppi.cell_probs(pi, acc)
    assert sum(probs) == 1
    assert ppi.judge_mean(pi, acc) == probs[0] + probs[2] == Fraction("0.068")
    rows = ppi.outcomes(9)
    assert len(rows) == math.comb(12, 3) and (rows.sum(axis=1) == 9).all()
    assert len({tuple(r) for r in rows.tolist()}) == len(rows)
    mass = ppi.ExactMass(9, probs)
    assert sum(mass.weights(rows)) == mass.den  # the pmf sums to exactly 1
    w, den = ppi.binomial_weights(9, pi)
    assert sum(w) == den
    assert Fraction(w[1], den) == 9 * pi * (1 - pi) ** 8


def test_selection_leaves_at_most_tail_and_tail_zero_is_complete() -> None:
    probs = ppi.cell_probs(Fraction("0.3"), Fraction("0.8"))
    tail = Fraction(1, 10**10)
    sel = ppi.select_outcomes(60, probs, tail)
    assert 0 <= sel.unevaluated <= tail
    assert sel.unevaluated == 1 - Fraction(sum(sel.weights), sel.den)
    assert len(sel.rows) < math.comb(63, 3)
    full = ppi.select_outcomes(12, probs, Fraction(0))
    assert len(full.rows) == math.comb(15, 3) and full.unevaluated == 0


def test_columns_realise_the_counts() -> None:
    rows = ppi.outcomes(7)
    y, yhat = ppi.columns(rows, 7)
    got = np.stack(
        [
            (y * yhat).sum(0),
            (y * (1 - yhat)).sum(0),
            ((1 - y) * yhat).sum(0),
            ((1 - y) * (1 - yhat)).sum(0),
        ],
        axis=1,
    )
    assert (got == rows).all()


def test_ppi_coverage_equals_brute_force_over_sequences() -> None:
    """Counts, weights and columns against all 4^n labelled sequences, independently."""
    n, pi, acc = 6, Fraction("0.1"), Fraction("0.7")
    s = _study(n_unlabelled=100, tail="0", methods=("ppi",), alphas=("0.1",))
    impl = ppi.reference_impl()
    rec = ppi.evaluate_unit(n, str(acc), str(pi), s, impl)
    unl = ppi.unlabelled(100, ppi.judge_mean(pi, acc))
    cells = [(1, 1), (1, 0), (0, 1), (0, 0)]
    probs = ppi.cell_probs(pi, acc)
    cov = Fraction(0)
    for seq in itertools.product(range(4), repeat=n):
        y = np.array([cells[i][0] for i in seq], float)
        yhat = np.array([cells[i][1] for i in seq], float)
        lo, hi = impl.single["ppi"](y, yhat, unl, 0.1)
        if lo <= float(pi) <= hi:
            cov += math.prod(probs[i] for i in seq)
    assert rec["results"]["ppi|0.1"]["coverage"] == pytest.approx(float(cov), abs=1e-15)


def test_label_only_baselines_against_an_independent_sum() -> None:
    s = _study(methods=("wald", "clopper_pearson"))
    for n, pi in ((30, "0.1"), (200, "0.02"), (57, "0.5")):
        rec = ppi.evaluate_unit(n, "0.9", pi, s, ppi.reference_impl())
        p = float(pi)
        k = np.arange(n + 1)
        pmf = stats.binom.pmf(k, n, p)
        for alpha in ("0.1", "0.05"):
            z = stats.norm.ppf(1 - float(alpha) / 2)
            ph = k / n
            h = z * np.sqrt(ph * (1 - ph) / n)
            wald = pmf[(ph - h <= p) & (p <= ph + h)].sum()
            assert rec["results"][f"wald|{alpha}"]["coverage"] == pytest.approx(wald, abs=1e-12)
            cp = rec["results"][f"clopper_pearson|{alpha}"]["coverage"]
            assert cp >= 1 - float(alpha)  # Clopper-Pearson is exact-conservative


def test_runner_resumes_and_report_flags_below_nominal(tmp_path: Path) -> None:
    toml = tmp_path / "t.toml"
    toml.write_text(
        'kind = "ppi"\nname = "t"\nn = [10, 12]\nacc = ["0.9"]\npi = ["0.02"]\n'
        'alphas = ["0.1"]\nn_unlabelled = 250\ntail = "1e-12"\nbatch = 7\nworkers = 2\n'
        'methods = ["ppi", "wald", "clopper_pearson"]\n'
        '[mc]\nseed = 1\ndraws = 10\ncells = [[10, "0.9", "0.02", "0.1"]]\n',
        encoding="utf-8",
    )
    s = ppi.load_ppi_study(toml)
    out = tmp_path / "run"
    assert ppi.run(s, out, impl="reference", echo=None) == 0
    first = (out / "units.jsonl").read_text(encoding="utf-8")
    assert len(first.splitlines()) == 2
    assert ppi.run(s, out, impl="reference", echo=None) == 0
    assert (out / "units.jsonl").read_text(encoding="utf-8") == first
    with pytest.raises(ValueError, match="fingerprint"):
        ppi.run(dataclasses.replace(s, tail="1e-11"), out, impl="reference", echo=None)
    summary = ppi.write_report(out, tmp_path / "rep")
    assert summary == {"units": 2, "units_expected": 2}
    rows = (tmp_path / "rep" / "coverage.csv").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1 + 2 * 3
    md = (tmp_path / "rep" / "map.md").read_text(encoding="utf-8")
    assert "| wald | 0.1 | 2 / 2 |" in md  # Wald at pi = 0.02, n <= 12 is far below 0.9
    assert "| clopper_pearson | 0.1 | 0 / 2 |" in md
    meta = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert meta["study"]["n"] == [10, 12]


@pytest.mark.adapter
def test_library_batched_calls_match_single_calls_and_reference() -> None:
    pytest.importorskip("ppi_py")
    impl, ref = ppi.library_impl(), ppi.reference_impl()
    rng = np.random.default_rng(0)
    for n, acc, pi in ((20, "0.9", "0.02"), (50, "0.7", "0.3")):
        sel = ppi.select_outcomes(
            n, ppi.cell_probs(Fraction(pi), Fraction(acc)), Fraction(1, 10**6)
        )
        rows = sel.rows[rng.choice(len(sel.rows), 40, replace=False)]
        unl = ppi.unlabelled(1000, ppi.judge_mean(Fraction(pi), Fraction(acc)))
        y, yhat = ppi.columns(rows, n)
        for m in ("ppi", "ppi++"):
            lo, hi = impl.batch[m](y, yhat, unl, 0.1)
            for j in range(len(rows)):
                l1, h1 = impl.single[m](y[:, j], yhat[:, j], unl, 0.1)
                assert lo[j] == pytest.approx(l1, abs=1e-12)
                assert hi[j] == pytest.approx(h1, abs=1e-12)
        lo, hi = impl.batch["ppi"](y, yhat, unl, 0.1)
        rlo, rhi = ref.batch["ppi"](y, yhat, unl, 0.1)
        np.testing.assert_allclose(lo, rlo, atol=1e-12)
        np.testing.assert_allclose(hi, rhi, atol=1e-12)
        for j in range(5):
            assert impl.wald(y[:, j], 0.05) == pytest.approx(ref.wald(y[:, j], 0.05), abs=1e-12)
