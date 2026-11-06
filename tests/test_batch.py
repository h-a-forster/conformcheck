"""Batch-size invariance check (conformcheck.batch) through the study pipeline.

A fake library caps every set at the number of test points in the call, as puncc 0.9.3
APS and RAPS do (REPORT.md, F11). The reference rows must stay invariant.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from conformcheck import adapters, batch, study
from conformcheck.adapters.base import AlphaOutput, MethodSpec, RegressionInput
from conformcheck.adapters.reference import RefClassifier, RefSplitAbs
from conformcheck.models import FixedRegressor
from conformcheck.report import adjust, build_cells, write_report
from conformcheck.repro import clusters
from conformcheck.runner import run_study, study_records

TOML = """
name = "tiny-batch"
seed = 5
reps = 10
test_points = 10
workers = 1
fwer = 0.05
fdr = 0.05
alphas = ["0.1", "0.2"]
edge_alphas = false
batch_sizes = [1, 5]

[grids.split]
n = [19]
dgps = ["reg_gauss", "cls_gauss"]

[controls]
reference = true
mutants = []
"""


class Capped(RefClassifier):
    """Reference sets cut to the call's top ``m`` labels by probability (F11)."""

    def __init__(self, method: str, variant: str) -> None:
        super().__init__(method, variant)
        self.spec = MethodSpec("capped", method, variant, "classification")

    def run(self, data):  # type: ignore[no-untyped-def]
        outs = super().run(data)
        rank = np.argsort(np.argsort(-data.proba_test, axis=1), axis=1)
        for o in outs.values():
            if o.sets is not None:
                o.sets = o.sets & (rank < len(data.x_test))
        return outs


class Positional(RefSplitAbs):
    """Reference intervals widened by the test point's position in the call."""

    def __init__(self) -> None:
        super().__init__()
        self.spec = MethodSpec("capped", "split_abs", "positional", "regression")

    def run(self, data: RegressionInput):  # type: ignore[no-untyped-def, override]
        outs = super().run(data)
        pos = np.arange(len(data.x_test), dtype=float)[:, None] * [-1e-3, 1e-3]
        for o in outs.values():
            if o.intervals is not None:
                o.intervals = o.intervals + pos
        return outs


class RaisesAlone(RefSplitAbs):
    """Reference intervals, but a call with one test point raises (F12)."""

    def __init__(self) -> None:
        super().__init__()
        self.spec = MethodSpec("capped", "split_abs", "raises_alone", "regression")

    def run(self, data: RegressionInput):  # type: ignore[no-untyped-def, override]
        if len(data.x_test) == 1:
            raise RuntimeError("needs two test points")
        return super().run(data)


class Seeds(RefClassifier):
    """Reference sets; remembers the library seed of every call."""

    def __init__(self) -> None:
        super().__init__("lac")
        self.seen: list[int] = []

    def run(self, data):  # type: ignore[no-untyped-def]
        self.seen.append(data.seed)
        return super().run(data)


FAKES = (
    Capped("aps", "deterministic"),
    Capped("aps", "randomized"),
    Positional(),
    RaisesAlone(),
)


@pytest.fixture
def with_fakes(monkeypatch: pytest.MonkeyPatch) -> None:
    real = adapters.registry
    monkeypatch.setattr(adapters, "registry", lambda: {**real(), **{a.spec.key: a for a in FAKES}})


def test_batch_check_flags_batch_dependent_rows(with_fakes: None, tmp_path: Path) -> None:
    p = tmp_path / "s.toml"
    p.write_text(TOML, encoding="utf-8")
    s = study.load_study(p)
    out = tmp_path / "run"
    run_study(s, out, workers=1, libraries={"reference", "capped"}, echo=None)
    payload = write_report(out)
    cells = build_cells(study_records(out)[0])
    adjust(cells, s.fwer, s.fdr)
    by_row: dict[str, list] = {}
    for c in cells:
        by_row.setdefault(c.row, []).append(c)

    for row, cs in by_row.items():
        assert all(c.batch for c in cs), row
        if row.startswith("reference/"):
            assert all(c.batch_status == "PASS" for c in cs), (row, [c.reason for c in cs])
    # one point at a time caps the set at one label; two chunks of 5 do not (4 classes)
    for c in by_row["capped/aps/deterministic"]:
        assert c.batch_status == "FAIL" and c.status == "FAIL"
        assert "size=1" in c.batch_reason and "size=5" not in c.batch_reason
        assert c.batch["size=1"]["differ"] == s.reps and c.batch["size=5"]["differ"] == 0
        assert np.mean(c.batch["size=1"]["size_diff"]) < -0.5
    # randomized: outputs always differ, only the paired test decides
    for c in by_row["capped/aps/randomized"]:
        assert c.batch_status == "FAIL" and c.batch_p_holm is not None
        assert c.batch_p_holm < 1e-6
    ref_rand = by_row["reference/aps/randomized"]
    assert all(c.batch_p is not None and c.batch["size=1"]["differ"] for c in ref_rand)
    # a shuffled call exposes position dependence that consecutive chunks of 1 also show
    for c in by_row["capped/split_abs/positional"]:
        assert "shuffled" in c.batch_reason and "size=1" in c.batch_reason
    # a crash of the one-point calls alone is a difference, chunks of 5 still match
    for c in by_row["capped/split_abs/raises_alone"]:
        assert c.batch_status == "FAIL" and c.batch["size=1"]["status_mismatch"] == s.reps
        assert "needs two test points" in c.batch_reason and "size=5" not in c.batch_reason
    # coverage of the full batch is untouched, so the row passes everything else and gets
    # no (misleading) generated coverage repro
    assert all(c.det_status == "PASS" for c in by_row["capped/aps/deterministic"])
    assert not [c for c, _ in clusters(cells) if c.row.startswith("capped/aps/")]
    assert payload["batch"]["sizes"] == [1, 5]
    md = (out / "report" / "matrix.md").read_text(encoding="utf-8")
    assert "## Batch-size invariance" in md and "capped/aps/deterministic" in md
    header = (out / "report" / "cells.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "batch_status" in header


def test_studies_without_batch_sizes_keep_fingerprints_and_columns(tmp_path: Path) -> None:
    # the committed default run must still resume and rebuild without --force
    run_json = Path(__file__).parents[1] / "docs/results/default/run.json"
    meta = json.loads(run_json.read_text(encoding="utf-8"))
    s = study.Study.from_config(meta["study"], meta["source"])
    assert s.batch_sizes == ()
    fp = study.fingerprint(s, {"versions": meta["versions"], "libraries": []})
    assert fp == meta["fingerprint"]
    tiny = study.load_study("smoke")
    out = tmp_path / "run"
    run_study(tiny, out, workers=1, libraries={"reference"}, max_units=2, echo=None)
    payload = write_report(out)
    assert "batch" not in payload
    header = (out / "report" / "cells.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "batch" not in header


def test_chunks_reassemble_in_test_point_order() -> None:
    rng = np.random.default_rng(0)
    m = 11
    ms = batch.modes(m, (1, 4), rng)
    assert [name for name, _ in ms] == ["size=1", "size=4", "shuffled"]
    for _, chunks in ms:
        assert sorted(np.concatenate(chunks).tolist()) == list(range(m))
    ad = RefClassifier("lac")
    x = rng.normal(size=(m, 2))
    p = rng.dirichlet(np.ones(4), size=20 + m)
    y = rng.integers(0, 4, size=20)
    from conformcheck.adapters.base import ClassificationInput

    inp = ClassificationInput(x[:0], y, x, [Fraction(1, 10)], None, p[:20], p[20:], 4, seed=1)
    full = ad.run(inp)[Fraction(1, 10)]
    for i, (_, chunks) in enumerate(ms):
        got = batch.predict_in_chunks(ad, inp, chunks, randomized=False, mode=i + 1)
        np.testing.assert_array_equal(got[Fraction(1, 10)].sets, full.sets)

    # a deterministic row keeps the repetition's seed (same CV+ folds in every chunk); a
    # randomized row gets a new seed per chunk and per mode (no shared first uniform)
    spy = Seeds()
    chunks = ms[0][1]
    batch.predict_in_chunks(spy, inp, chunks, randomized=False, mode=1)
    assert set(spy.seen) == {inp.seed}
    spy.seen.clear()
    batch.predict_in_chunks(spy, inp, chunks, randomized=True, mode=1)
    batch.predict_in_chunks(spy, inp, chunks, randomized=True, mode=2)
    assert len(set(spy.seen)) == 2 * m and inp.seed not in spy.seen


def test_a_failing_later_chunk_decides_the_status() -> None:
    class FailsOnShortChunk(RefSplitAbs):
        def run(self, data: RegressionInput):  # type: ignore[no-untyped-def, override]
            if len(data.x_test) < 2:
                return {a: AlphaOutput(status="refused", message="short") for a in data.alphas}
            return super().run(data)

    rng = np.random.default_rng(0)
    x = rng.normal(size=(3, 2))
    a = Fraction(1, 5)
    inp = RegressionInput(x, rng.normal(size=3), x, [a], FixedRegressor())
    chunks = [np.arange(2), np.arange(2, 3)]
    got = batch.predict_in_chunks(FailsOnShortChunk(), inp, chunks, randomized=False, mode=1)
    assert got[a].status == "refused" and got[a].message == "short"


def test_infinite_endpoints_compare_equal_only_with_the_same_sign() -> None:
    y = np.array([0.5, 0.5])
    full = AlphaOutput(intervals=np.array([[-np.inf, np.inf], [0.0, 1.0]]))
    same = batch.compare(full, AlphaOutput(intervals=full.intervals.copy()), y)
    assert same is not None and same["points"] == 0 and same["max_diff"] == 0.0
    finite = np.array([[-1.0, 1.0], [0.0, 1.0]])
    other = batch.compare(full, AlphaOutput(intervals=finite), y)
    assert other is not None and other["points"] == 1 and other["max_diff"] == np.inf


def test_constant_differences_give_exact_pvalues() -> None:
    assert batch._zero_mean_pvalue([-1.1] * 20) == 0.0  # np.std of these is 2e-16
    assert batch._zero_mean_pvalue([0.0] * 20) == 1.0


def test_paired_pvalue_corrects_for_every_test_of_every_mode() -> None:
    v = [0.1, -0.05, 0.2, 0.15, 0.05, 0.1, -0.1, 0.25, 0.1, 0.0]
    one = batch._zero_mean_pvalue(v)
    assert 0 < one < 0.25
    rec = {"size=1": {"size_diff": v, "cover_diff": [0.0] * 10}, "shuffled": {"cover_diff": [0.0]}}
    assert batch.paired_pvalue(rec) == pytest.approx(3 * one)
