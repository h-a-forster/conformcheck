"""Living audit (scripts/living.py, conformcheck.living): battery, comparison and the issue step.

The weekly job is replayed end to end without network: target results already on disk
(as a finished run leaves them) with one verdict changed against a baseline, then the
issue step against a fake ``gh`` that records its calls.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from conformcheck import living, tswrappers

ROOT = Path(__file__).resolve().parents[1]


def _script():  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("living_script", ROOT / "scripts/living.py")
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


FAKE_GH = """
import json, sys
from pathlib import Path
state = Path(sys.argv[1]); args = sys.argv[2:]
calls = json.loads(state.read_text()) if state.exists() else []
calls.append(args); state.write_text(json.dumps(calls))
if args[:2] == ["issue", "list"]:
    opened = [c for c in calls if c[:2] == ["issue", "create"]]
    print(json.dumps([{"number": 7, "title": c[c.index("--title") + 1]} for c in opened]))
"""


def test_committed_baseline_covers_every_target_row() -> None:
    base = json.loads((ROOT / "docs/results/living/baseline.json").read_text("utf-8"))
    assert set(base["targets"]) == set(living.TARGETS)
    for name, t in living.TARGETS.items():
        verdicts = base["targets"][name]["verdicts"]
        # the controls behave in every environment: exact passes, mutants are caught
        if t.kind == "ts":
            assert verdicts["reference/exact"] == "PASS/-"
            assert verdicts["reference/k_minus_1"] == "FAIL/-"
        else:
            assert verdicts["reference/split_abs/default"] == "PASS/PASS"
            assert verdicts["reference/split_abs/k_plus_1"] == "CONSERVATIVE/CONSERVATIVE"


def test_ts_battery_verdicts_and_resume(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    exact = tswrappers.control_rows((9, 19))[0]

    def counted(*a, **k):  # type: ignore[no-untyped-def]
        calls.append(1)
        return exact.fn(*a, **k)

    def boom(*a, **k):  # type: ignore[no-untyped-def]
        raise ValueError("library broke")

    rows = [
        tswrappers.Row("lib/exact", counted, (9, 999), reps=20, score="abs"),
        tswrappers.Row("lib/broken", boom, (9,), reps=20),
    ]
    monkeypatch.setattr(tswrappers, "library_rows", lambda name: rows)
    monkeypatch.setattr(tswrappers, "control_rows", lambda: [])
    res = living.battery("darts", tmp_path)
    assert res["verdicts"] == {"lib/exact": "PASS/PASS", "lib/broken": "ERROR"}
    assert "ValueError: library broke" in res["details"]["lib/broken"][0]
    n_calls = len(calls)
    assert living.battery("darts", tmp_path)["verdicts"] == res["verdicts"]
    assert len(calls) == n_calls  # finished rows are read back, not rerun


def test_ts_library_that_fails_to_import_is_an_error_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(sys.modules, "darts", None)  # import darts raises ImportError
    monkeypatch.setattr(tswrappers, "control_rows", lambda: [])
    res = living.battery("darts", tmp_path)
    assert set(res["verdicts"].values()) == {"ERROR"}
    assert len(res["verdicts"]) == 2
    assert all("ModuleNotFoundError" in d[0] for d in res["details"].values())


def test_living_job_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    script = _script()
    baseline = {
        "targets": {
            "darts": {
                "environment": {"darts": "0.48.1"},
                "verdicts": {"darts/naive_sym_all": "FAIL/-", "reference/exact": "PASS/-"},
                "details": {},
            }
        }
    }
    base_path = tmp_path / "baseline.json"
    base_path.write_text(json.dumps(baseline))
    monkeypatch.setattr(script, "BASELINE", base_path)
    out = tmp_path / "run"

    def finished_run(verdict: str) -> None:
        (out / "results").mkdir(parents=True, exist_ok=True)
        (out / "run.json").write_text(json.dumps({"targets": ["darts"], "pins": []}))
        result = {
            "target": "darts",
            "environment": {"darts": "0.49.0", "numpy": "2.5.4"},
            "verdicts": {"darts/naive_sym_all": verdict, "reference/exact": "PASS/-"},
            "details": {"darts/naive_sym_all": []},
        }
        (out / "results" / "darts.json").write_text(json.dumps(result))

    def no_install(*a, **k):  # type: ignore[no-untyped-def]
        raise AssertionError("a finished target must not be reinstalled")

    monkeypatch.setattr(script, "run_target", no_install)
    gh_state = tmp_path / "gh.json"
    fake = tmp_path / "fake_gh.py"
    fake.write_text(FAKE_GH)
    monkeypatch.setenv("LIVING_GH", json.dumps([sys.executable, str(fake), str(gh_state)]))

    # Same verdicts as the baseline: exit 0 and no issue.
    finished_run("FAIL/-")
    assert script.main(["--out", str(out), "--targets", "darts"]) == 0
    assert script.main(["notify", str(out), "--repo", "o/r"]) == 0
    assert not gh_state.exists()

    # The release fixed the k > n cells: exit 1, an issue, then a comment on it.
    finished_run("PASS/-")
    assert script.main(["--out", str(out), "--targets", "darts"]) == 1
    summary = (out / "summary.md").read_text("utf-8")
    assert "`darts/naive_sym_all`: FAIL/- -> PASS/-" in summary
    assert "| darts | 0.48.1 | 0.49.0 | 2 | 1 |" in summary
    assert "- **darts**: darts 0.48.1 -> 0.49.0, numpy - -> 2.5.4" in summary
    assert script.main(["notify", str(out), "--repo", "o/r", "--run-url", "U"]) == 0
    assert "Run and artifact: U" in (out / "issue.md").read_text("utf-8")
    assert script.main(["notify", str(out), "--repo", "o/r"]) == 0
    calls = json.loads(gh_state.read_text())
    verbs = [c[:2] for c in calls]
    assert verbs == [
        ["issue", "list"],
        ["issue", "create"],
        ["issue", "list"],
        ["issue", "comment"],
    ]
    assert calls[1][calls[1].index("--title") + 1] == script.ISSUE_TITLE
    assert calls[3][2] == "7"


def test_bad_pin_is_refused_before_anything_runs(tmp_path: Path) -> None:
    script = _script()
    out = tmp_path / "run"
    assert script.main(["--out", str(out), "--targets", "darts", "--pin", "mapie==1.5.0"]) == 2
    assert not out.exists()


def test_scrub_removes_machine_paths() -> None:
    home = str(Path.home())
    out = living.scrub({"a": [f"{sys.prefix}/x.py", f"{home}\\y"]})
    assert home not in json.dumps(out) and sys.prefix not in json.dumps(out)
    # an error message is scrubbed before it is cut, so the cut never strands part of a path
    exc = ImportError(f"cannot import name 'X' ({sys.prefix}/lib/site-packages/m.py)")
    cut = len("cannot import name 'X' (") + len(sys.prefix) // 2
    assert living._text(exc, cut) == "cannot import name 'X' (<env>/lib/site-packages/m.py)"[:cut]
