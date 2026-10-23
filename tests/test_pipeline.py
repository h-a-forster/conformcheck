"""Study, runner, report and repro pipeline (milestones M4 to M6), on reference rows only.

The reference rows need no optional library, so these tests run everywhere and fast.
"""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from conformcheck import cli, study
from conformcheck.report import write_report
from conformcheck.repro import write_repros
from conformcheck.runner import FingerprintMismatch, load_done, run_study

TOML = """
name = "tiny"
seed = 3
reps = 60
test_points = 60
workers = 1
fwer = 0.05
fdr = 0.05
alphas = ["0.1", "0.2"]
edge_alphas = true

[grids.split]
n = [9, 19]
dgps = ["reg_gauss", "cls_gauss"]

[grids.cv_plus]
n = [20]
n_folds = [5]
dgps = ["reg_constant"]

[controls]
reference = true
mutants = ["k_plus_1", "k_minus_1"]
"""


@pytest.fixture
def tiny(tmp_path: Path) -> study.Study:
    p = tmp_path / "tiny.toml"
    p.write_text(TOML, encoding="utf-8")
    return study.load_study(p)


def _strip(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if k != "elapsed_s"}


def test_load_builtin_studies() -> None:
    for name in ("smoke", "default", "full"):
        s = study.load_study(name)
        assert s.workers <= 4 and s.reps >= 20
    assert study.load_study("default").reps == 200
    with pytest.raises(FileNotFoundError):
        study.load_study("nope")


def test_grid_alphas_and_units(tiny: study.Study) -> None:
    g = tiny.grids[0]
    assert study.grid_alphas(tiny, g, 19) == (
        Fraction(1, 5),
        Fraction(1, 10),
        Fraction(1, 20),
        Fraction(9, 200),
    )
    units = study.enumerate_units(tiny, libraries={"reference"})
    keys = {u.adapter for u in units}
    assert "reference/split_abs/k_plus_1" in keys
    assert "reference/split_abs/no_correction_linear" not in keys
    assert len({u.uid(tiny) for u in units}) == len(units)


def test_cell_law_mapping() -> None:
    kw = dict(library="x", m=100)
    assert (
        study.cell_law(
            method="split_abs", variant="d", dgp="reg_gauss", n=5, alpha=Fraction(1, 10), **kw
        ).kind
        == "trivial"
    )
    cl = study.cell_law(
        method="cqr", variant="asymmetric", dgp="reg_gauss", n=19, alpha=Fraction(1, 10), **kw
    )
    assert cl.kind == "mean" and cl.target == pytest.approx(0.9) and cl.k == 19
    cl = study.cell_law(
        method="lac", variant="smoothed", dgp="cls_gauss", n=5, alpha=Fraction(1, 10), **kw
    )
    assert cl.kind == "mean" and cl.target == pytest.approx(0.9)
    cl = study.cell_law(
        method="cv_plus",
        variant="K=10",
        dgp="reg_gauss",
        n=100,
        alpha=Fraction(1, 10),
        n_folds=10,
        **kw,
    )
    assert cl.kind == "lower" and cl.target == pytest.approx(0.8 - 9 / 110)
    cl = study.cell_law(
        method="class_conditional",
        variant="default",
        dgp="cls_gauss",
        n=19,
        alpha=Fraction(1, 10),
        **kw,
    )
    assert cl.kind == "exact" and cl.law.m == 100 and cl.target == pytest.approx(0.9)
    cl = study.cell_law(
        method="split_abs", variant="d", dgp="reg_tied", n=19, alpha=Fraction(1, 10), **kw
    )
    assert cl.kind == "exact" and cl.target > 0.9
    cl = study.cell_law(
        method="aps", variant="rand=False", dgp="cls_gauss", n=19, alpha=Fraction(1, 10), **kw
    )
    assert cl.one_sided


def test_run_resume_is_identical_and_report(tiny: study.Study, tmp_path: Path) -> None:
    libs = {"reference"}
    full = tmp_path / "full"
    run_study(tiny, full, workers=1, libraries=libs, echo=None)
    part = tmp_path / "part"
    res = run_study(tiny, part, workers=1, libraries=libs, max_units=5, echo=None)
    assert res["done"] == 5
    # simulate a crash mid-write: a truncated last line must be ignored on resume
    with (part / "units.jsonl").open("a", encoding="utf-8") as fh:
        fh.write('{"uid": "trunc')
    res = run_study(tiny, part, workers=1, libraries=libs, echo=None)
    assert res["done"] == res["total"]
    a = {k: _strip(v) for k, v in load_done(full / "units.jsonl").items()}
    b = {k: _strip(v) for k, v in load_done(part / "units.jsonl").items()}
    assert a == b
    assert "done=" in (part / "progress.log").read_text(encoding="utf-8")

    payload = write_report(full)
    rows = {r["row"]: r for r in payload["rows"]}
    assert rows["reference/split_abs/default"]["small_n_status"] == "PASS"
    assert rows["reference/lac/default"]["small_n_status"] == "PASS"
    assert rows["reference/cv_plus/K=5"]["small_n_status"] == "PASS"
    assert rows["reference/split_abs/k_plus_1"]["small_n_status"] == "CONSERVATIVE"
    assert rows["reference/split_abs/k_minus_1"]["small_n_status"] == "FAIL"
    assert rows["reference/lac/k_minus_1"]["small_n_status"] == "FAIL"
    assert payload["controls"]["size"]["reference_holm_rejections"] == 0
    for f in ("cells.csv", "matrix.json", "matrix.md", "summary.md"):
        assert (full / "report" / f).stat().st_size > 0
    # statuses are reproducible from units.jsonl alone
    again = write_report(full, tmp_path / "again")
    assert again["rows"] == payload["rows"]

    # M6: repros run standalone; a mutant reproduces (exit 1)
    repros = write_repros(full, verify=True)
    by_row = {(r.row, r.kind): r for r in repros}
    r = by_row[("reference/split_abs/k_plus_1", "rank")]
    assert r.exit_code == 1, r.path.with_suffix(".out.txt").read_text(encoding="utf-8")
    assert "conformcheck" not in r.path.read_text(encoding="utf-8").split('"""', 2)[2]


def test_reference_repro_exits_zero(tiny: study.Study, tmp_path: Path) -> None:
    from conformcheck.repro import MODELS, PRELUDE, RANK_HARNESS, REFERENCE_SNIPPET

    src = (
        PRELUDE.format(lib="numpy")
        + MODELS
        + REFERENCE_SNIPPET.format(mutant="default")
        + RANK_HARNESS.format(n=19, alpha="1/10")
    )
    p = tmp_path / "ref.py"
    p.write_text(src, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "expected 18" in proc.stdout


def test_fingerprint_guard(tiny: study.Study, tmp_path: Path) -> None:
    out = tmp_path / "run"
    run_study(tiny, out, workers=1, libraries={"reference"}, max_units=1, echo=None)
    other = study.Study(**{**tiny.__dict__, "reps": 61})
    with pytest.raises(FingerprintMismatch):
        run_study(other, out, workers=1, libraries={"reference"}, max_units=1, echo=None)
    run_study(other, out, workers=1, libraries={"reference"}, max_units=1, force=True, echo=None)


def test_worker_cap(tiny: study.Study, tmp_path: Path) -> None:
    out = tmp_path / "run"
    run_study(tiny, out, workers=64, libraries={"reference"}, max_units=0, echo=None)
    assert json.loads((out / "run.json").read_text())["workers"] == 4
    assert study.Study(**{**tiny.__dict__}).workers <= 4


def test_cli_plan_and_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["plan", "--study", "smoke", "--no-probe"]) == 0
    assert "units" in capsys.readouterr().out
    assert cli.main(["plan", "--study", "missing-study", "--no-probe"]) == 2
    assert cli.main(["report", str(tmp_path)]) == 2
    assert cli.main(["repro", str(tmp_path)]) == 2


def _write(tmp_path: Path, text: str, name: str = "s.toml") -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


@pytest.mark.parametrize(
    ("old", "new", "match"),
    [
        ('dgps = ["reg_gauss", "cls_gauss"]', 'dgps = ["reg_gaus"]', "unknown dgp"),
        ("reps = 60\n", "", "missing required key"),
        ("reps = 60", "reps = 0", "reps must be a positive integer"),
        ("test_points = 60", "test_points = 0", "test_points"),
        ("n = [9, 19]", "n = [0, 19]", "n must be a positive integer"),
        ('mutants = ["k_plus_1", "k_minus_1"]', 'mutants = ["k_plus_2"]', "unknown mutant"),
        ("n_folds = [5]\n", "", "n_folds"),
        ('alphas = ["0.1", "0.2"]', 'alphas = ["1.5"]', "alpha must lie in"),
        ('dgps = ["reg_constant"]', 'dgps = ["cls_gauss"]', "has no methods on grid"),
    ],
)
def test_load_study_validates(tmp_path: Path, old: str, new: str, match: str) -> None:
    # Invalid configs must fail at load time (exit 2, not retried), never run 0 cells.
    assert old in TOML
    p = _write(tmp_path, TOML.replace(old, new, 1))
    with pytest.raises(ValueError, match=match):
        study.load_study(p)
    assert cli.main(["run", "--study", str(p), "--out", str(tmp_path / "o")]) == 2
    assert cli.main(["plan", "--study", str(p), "--no-probe"]) == 2


def test_cli_rejects_unknown_library(tmp_path: Path) -> None:
    p = _write(tmp_path, TOML)
    out = tmp_path / "o"
    assert cli.main(["run", "--study", str(p), "--out", str(out), "--libraries", "mapei"]) == 2
    assert not (out / "units.jsonl").exists()


def test_missing_libraries_are_not_checkpointed(
    tiny: study.Study, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Units of libraries that are not installed must not be checkpointed as finished, so
    # a core-only run does not look complete and the units still run once installed.
    from conformcheck.adapters._common import LibraryAdapter
    from conformcheck.runner import MissingLibraries

    real = LibraryAdapter.available
    monkeypatch.setattr(
        LibraryAdapter, "available", lambda self: self.spec.library != "mapie" and real(self)
    )
    out = tmp_path / "run"
    with pytest.raises(MissingLibraries, match="mapie"):
        run_study(tiny, out, workers=1, libraries={"reference", "mapie"}, echo=None)
    p = _write(tmp_path, TOML)
    args = ["run", "--study", str(p), "--out", str(out), "--libraries", "mapie"]
    assert cli.main(args) == 2
    res = run_study(
        tiny, out, workers=1, libraries={"reference", "mapie"}, allow_missing=True, echo=None
    )
    assert res["missing_libraries"] == ["mapie"] and res["units_skipped_missing"] > 0
    assert res["done"] == res["total"]
    recs = load_done(out / "units.jsonl")
    assert recs and all(r["library"] == "reference" for r in recs.values())
    meta = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert meta["missing_libraries"] == ["mapie"]
    assert "mapie" in (write_report(out)["run"]["missing_libraries"])
    # legacy "unavailable" records do not count as finished units
    with (out / "units.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"uid": "legacy", "status": "unavailable"}) + "\n")
    assert "legacy" not in load_done(out / "units.jsonl")


def test_headline_excuses_only_documented_statuses() -> None:
    # A documented row is excused from the headline only for its documented statuses.
    from conformcheck.report import RowSummary, headline_counts

    row = "mapie/aps/include_last_label=True"

    def rs(small: str, undoc: str) -> RowSummary:
        return RowSummary(
            row, "mapie", "aps", "x", 1, small, "-", {}, documented="doc",
            small_n_undocumented=undoc,
        )  # fmt: skip

    assert headline_counts([rs("CONSERVATIVE", "PASS")])["rows_small_n_flagged"] == 0
    assert headline_counts([rs("ERROR", "ERROR")])["flagged_rows"] == [row]


def test_summarize_rows_documented_status() -> None:
    from conformcheck.report import Cell, summarize_rows

    def cell(status: str, n: int = 9) -> Cell:
        c = Cell(
            "mapie/aps/include_last_label=True", "mapie", "aps", "include_last_label=True",
            "cls_gauss", "split", n, None, "1/10", 9, 50, 10, "exact", 0.9, 10, 0, 0,
        )  # fmt: skip
        c.status = status
        return c

    (r,) = summarize_rows([cell("CONSERVATIVE"), cell("PASS")])
    assert r.small_n_status == "CONSERVATIVE" and r.small_n_undocumented == "PASS"
    (r,) = summarize_rows([cell("CONSERVATIVE"), cell("OVER_REFUSED"), cell("ERROR", 1000)])
    assert r.small_n_undocumented == "OVER_REFUSED"


def test_report_requires_units_and_reads_gzip(tmp_path: Path) -> None:
    import gzip
    import shutil

    # a run directory without any units file is an error, not an empty "0 units" report
    (tmp_path / "run.json").write_text("{}", encoding="utf-8")
    assert cli.main(["report", str(tmp_path)]) == 2
    assert not (tmp_path / "report").exists()

    # a gzip-compressed units file is read transparently
    p = _write(tmp_path, TOML)
    src, dst = tmp_path / "src", tmp_path / "gz"
    assert cli.main(["run", "--study", str(p), "--out", str(src), "--libraries", "reference"]) == 0
    dst.mkdir()
    shutil.copy(src / "run.json", dst / "run.json")
    with (src / "units.jsonl").open("rb") as fi, gzip.open(dst / "units.jsonl.gz", "wb") as fo:
        shutil.copyfileobj(fi, fo)
    assert cli.main(["report", str(dst)]) == 0
    assert cli.main(["report", str(src)]) == 0
    assert (dst / "report" / "cells.csv").read_bytes() == (
        src / "report" / "cells.csv"
    ).read_bytes()


def test_cli_run_runtime_errors_are_not_config_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Only config problems exit 2 (the resume wrapper stops); a runtime ValueError propagates.
    from conformcheck import runner

    def boom(*a: object, **k: object) -> None:
        raise ValueError("runtime failure")

    monkeypatch.setattr(runner, "run_study", boom)
    p = _write(tmp_path, TOML)
    with pytest.raises(ValueError, match="runtime failure"):
        cli.main(["run", "--study", str(p), "--out", str(tmp_path / "o")])


SMALL = TOML.replace("reps = 60", "reps = 20").replace("n = [9, 19]", "n = [9]")


def test_study_from_config_round_trips_unit_ids(tiny: study.Study) -> None:
    again = study.Study.from_config(json.loads(json.dumps(tiny.config())), tiny.source)
    assert again == tiny
    assert [u.uid(again) for u in study.enumerate_units(again)] == [
        u.uid(tiny) for u in study.enumerate_units(tiny)
    ]


def test_full_study_is_default_grid_at_full_size() -> None:
    d, f = study.load_study("default"), study.load_study("full")
    assert (f.reps, f.test_points) == (2000, 1000)
    assert f.grids == d.grids and f.alphas == d.alphas and f.mutants == d.mutants
    assert f.seed == d.seed and f.edge_alphas == d.edge_alphas


def test_report_uses_only_records_of_the_current_study(tmp_path: Path) -> None:
    # A directory reused with --force after a config change keeps the old records in
    # units.jsonl; the report and the repros must use only the current study's units.
    from conformcheck.report import build_cells
    from conformcheck.runner import study_records

    libs = {"reference"}
    first = study.load_study(_write(tmp_path, SMALL))
    out = tmp_path / "run"
    run_study(first, out, workers=1, libraries=libs, echo=None)
    second = study.Study(**{**first.__dict__, "reps": 21})
    res = run_study(second, out, workers=1, libraries=libs, force=True, echo=None)
    assert res["done"] == res["total"] == res["finished"]
    records, dropped = study_records(out)
    assert len(records) == res["total"] and dropped["other_config"] == res["total"]
    assert {r["reps"] for r in records} == {21}
    payload = write_report(out)
    assert payload["units_done"] == res["total"]
    assert payload["records_dropped"]["other_config"] == res["total"]
    cells = build_cells(records)
    keys = [(c.row, c.dgp, c.n, c.alpha) for c in cells]
    assert len(keys) == len(set(keys))
    assert "Records left out" in (out / "report" / "summary.md").read_text(encoding="utf-8")


def test_units_from_other_versions_are_rerun(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from conformcheck import runner

    libs = {"reference"}
    s = study.load_study(_write(tmp_path, SMALL))
    out = tmp_path / "run"
    total = run_study(s, out, workers=1, libraries=libs, echo=None)["total"]
    recs = load_done(out / "units.jsonl")
    assert all(r["versions"]["numpy"] for r in recs.values())
    # Records written before versions were stored per record are reused when run.json
    # says they were made under the current versions.
    legacy = [{k: v for k, v in r.items() if k != "versions"} for r in recs.values()]
    (out / "units.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in legacy), encoding="utf-8"
    )
    assert run_study(s, out, workers=1, libraries=libs, echo=None)["finished"] == 0
    # After an upgrade (here: a different numpy), nothing is reused under --force.
    real = runner.versions
    monkeypatch.setattr(runner, "versions", lambda: {**real(), "numpy": "0.0.1"})
    with pytest.raises(FingerprintMismatch):
        run_study(s, out, workers=1, libraries=libs, echo=None)
    res = run_study(s, out, workers=1, libraries=libs, force=True, echo=None)
    assert res["finished"] == total and res["done"] == total
    assert "other versions" in (out / "progress.log").read_text(encoding="utf-8")
    assert {r["versions"]["numpy"] for r in load_done(out / "units.jsonl").values()} == {"0.0.1"}
    # A library-only upgrade re-runs only that library's units (none here).
    monkeypatch.setattr(runner, "versions", lambda: {**real(), "numpy": "0.0.1", "mapie": "9"})
    res = run_study(s, out, workers=1, libraries=libs, force=True, echo=None)
    assert res["finished"] == 0 and res["done"] == total
    payload = write_report(out)
    assert payload["units_done"] == total and payload["records_dropped"]["other_versions"] == 0


def test_matrix_shows_zero_coverage(tmp_path: Path) -> None:
    import dataclasses

    from conformcheck.report import build_cells, render_matrix_md, summarize_rows
    from conformcheck.runner import study_records

    s = study.load_study(_write(tmp_path, SMALL))
    out = tmp_path / "run"
    run_study(s, out, workers=1, libraries={"reference"}, max_units=1, echo=None)
    payload = write_report(out)
    cell = build_cells(study_records(out)[0])[0]
    bad = dataclasses.replace(
        cell, row="lib/x/y", library="lib", status="FAIL", coverage=0.0, ci_low=0.0, ci_high=0.0
    )
    text = render_matrix_md([bad], summarize_rows([bad]), payload)
    assert "0.0000 [0.0000, 0.0000]" in text
