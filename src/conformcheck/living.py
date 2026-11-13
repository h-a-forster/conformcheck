"""Living audit: the quick battery against whatever library release is installed.

``scripts/living.py`` builds one fresh environment per target with the newest release,
runs ``python -m conformcheck.living battery <target>`` inside it, then compares the row
verdicts with ``docs/results/living/baseline.json`` (:func:`compare`). The weekly workflow
(``.github/workflows/living.yml``) opens an issue when a verdict changes.

A row's verdict is ``"<worst status at n <= 100>/<worst status at n > 100>"`` (the same
split as the conformance matrix). Seeds are fixed, so a release always gives the same
verdicts; a change means the library's behaviour changed (or the battery did, in which case
the baseline is regenerated in the same commit).
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: Seed of the time-series battery (the study battery's seed is in studies/quick.toml).
SEED = 20261113
TEST_POINTS = 500


@dataclass(frozen=True)
class Target:
    """One environment of the living audit: what to install and which battery to run."""

    name: str
    packages: tuple[str, ...]  # requirement names, newest release unless pinned
    kind: str  # "study" (quick.toml rows of one library) or "ts" (tswrappers rows)


TARGETS: dict[str, Target] = {
    t.name: t
    for t in (
        Target("mapie", ("mapie",), "study"),
        Target("crepes", ("crepes",), "study"),
        Target("puncc", ("puncc",), "study"),
        Target("statsforecast", ("statsforecast", "scikit-learn"), "ts"),
        Target("sktime", ("sktime",), "ts"),
        Target("darts", ("darts",), "ts"),
    )
}

#: Packages whose versions every result records besides the target's own.
CONTEXT_PACKAGES = ("numpy", "scipy", "scikit-learn", "pandas")


def _version(dist: str) -> str | None:
    try:
        return importlib.metadata.version(dist)
    except importlib.metadata.PackageNotFoundError:
        return None


def environment(target: Target) -> dict[str, str | None]:
    names = dict.fromkeys((*target.packages, *CONTEXT_PACKAGES, "conformcheck"))
    out: dict[str, str | None] = {n: _version(n) for n in names}
    out["python"] = platform.python_version()
    return out


def scrub(obj: Any) -> Any:
    """``obj`` with this environment's and the home directory's paths replaced, so results
    (and the committed baseline) never carry a machine's paths."""
    text = json.dumps(obj)
    for path, label in ((sys.prefix, "<env>"), (str(Path.home()), "<home>")):
        for form in {path, path.replace("\\", "/")}:
            text = text.replace(json.dumps(form)[1:-1], label)
    return json.loads(text)


def row_verdict(cells: list[tuple[int, str]]) -> str:
    """``small/large`` worst status of ``(n, status)`` cells; ``-`` where no cell ran."""
    from conformcheck.report import SMALL_N, worst

    small = [s for n, s in cells if n <= SMALL_N]
    large = [s for n, s in cells if n > SMALL_N]
    return f"{worst(small) if small else '-'}/{worst(large) if large else '-'}"


def _study_battery(target: Target, work: Path, workers: int) -> dict[str, Any]:
    from conformcheck.report import write_report
    from conformcheck.runner import run_study
    from conformcheck.study import load_study

    run_dir = work / "run"
    res = run_study(
        load_study("quick"),
        run_dir,
        workers=workers,
        libraries={target.name, "reference"},
        echo=None,
    )
    if res["done"] != res["total"]:
        raise RuntimeError(f"{res['total'] - res['done']} of {res['total']} units did not finish")
    payload = write_report(run_dir, work / "report")
    verdicts, details = {}, {}
    for row in payload["rows"]:
        verdicts[row["row"]] = f"{row['small_n_status']}/{row['large_n_status']}"
        details[row["row"]] = row["non_pass"]
    return {"verdicts": verdicts, "details": details, "units": res["total"]}


def _ts_battery(target: Target, work: Path) -> dict[str, Any]:
    from conformcheck import tswrappers
    from conformcheck.testing import check_split_regressor

    work.mkdir(parents=True, exist_ok=True)
    done_path = work / "rows.jsonl"
    done: dict[str, dict[str, Any]] = {}
    if done_path.exists():
        for line in done_path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            done[rec["row"]] = rec
    rows = tswrappers.library_rows(target.name) + tswrappers.control_rows()
    for row in rows:
        if row.name in done:
            continue
        t0 = time.time()
        try:
            rep = check_split_regressor(
                row.fn,
                n=row.n,
                alpha=row.alpha,
                reps=row.reps,
                test_points=TEST_POINTS,
                seed=SEED,
                score=row.score,  # type: ignore[arg-type]
            )
            cells = [(c.n, c.status) for c in rep.cells]
            rec = {
                "row": row.name,
                "verdict": row_verdict(cells),
                "non_pass": [
                    f"n={c.n} a={c.alpha}: {c.status} (coverage {c.coverage:.4f} vs "
                    f"{c.target:.4f}{', ' + c.detail if c.detail else ''})"
                    for c in rep.cells
                    if c.status != "PASS"
                ],
            }
        except Exception as exc:  # noqa: BLE001 - a library error is a verdict, not a crash
            rec = {
                "row": row.name,
                "verdict": "ERROR",
                "non_pass": [f"{type(exc).__name__}: {str(exc)[:300]}"],
            }
        rec["secs"] = round(time.time() - t0, 1)
        with done_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        done[row.name] = rec
    return {
        "verdicts": {r.name: done[r.name]["verdict"] for r in rows},
        "details": {r.name: done[r.name]["non_pass"] for r in rows},
    }


def battery(name: str, work: str | Path, workers: int = 4) -> dict[str, Any]:
    """Run one target's battery in this environment; resumable through ``work``."""
    target = TARGETS[name]
    work = Path(work)
    t0 = time.time()
    if target.kind == "study":
        out = _study_battery(target, work, workers)
    else:
        out = _ts_battery(target, work)
    return scrub(
        {
            "target": name,
            "environment": environment(target),
            **out,
            "elapsed_s": round(time.time() - t0, 1),
        }
    )


# --- comparison -------------------------------------------------------------------------


@dataclass(frozen=True)
class Change:
    target: str
    row: str
    old: str | None  # None: the row is new
    new: str | None  # None: the row is gone, or the target did not run


def compare(results: dict[str, dict[str, Any]], baseline: dict[str, Any]) -> list[Change]:
    """Every row whose verdict differs from the baseline, over the targets in ``results``."""
    changes: list[Change] = []
    base_targets = baseline.get("targets", {})
    for target in sorted(results):
        new = results[target]["verdicts"]
        old = base_targets.get(target, {}).get("verdicts", {})
        for row in sorted(set(old) | set(new)):
            if old.get(row) != new.get(row):
                changes.append(Change(target, row, old.get(row), new.get(row)))
    return changes


def make_baseline(results: dict[str, dict[str, Any]], note: str = "") -> dict[str, Any]:
    return {
        "note": note,
        "targets": {
            t: {k: r[k] for k in ("environment", "verdicts", "details")}
            for t, r in sorted(results.items())
        },
    }


def summary_markdown(
    results: dict[str, dict[str, Any]],
    baseline: dict[str, Any],
    changes: list[Change],
    failed: dict[str, str] | None = None,
) -> str:
    """The run summary; it is also the issue body when a verdict changed."""
    failed = failed or {}
    base_targets = baseline.get("targets", {})
    lines = [
        "# conformcheck living audit",
        "",
        f"{len(changes)} verdict change(s) against `docs/results/living/baseline.json`"
        + (f"; {len(failed)} target(s) could not run" if failed else "")
        + ".",
        "",
        "| Target | Baseline | Now | Rows | Changed |",
        "|---|---|---|---|---|",
    ]
    for target in sorted(set(results) | set(failed)):
        t = TARGETS.get(target)
        pkg = t.packages[0] if t else target
        old_v = base_targets.get(target, {}).get("environment", {}).get(pkg, "-")
        if target in failed:
            lines.append(f"| {target} | {old_v} | not run | - | - |")
            continue
        r = results[target]
        n_changed = sum(c.target == target for c in changes)
        lines.append(
            f"| {target} | {old_v} | {r['environment'].get(pkg)} | {len(r['verdicts'])} | "
            f"{n_changed} |"
        )
    if changes:
        lines += ["", "## Changed verdicts", "", "Verdict: worst status at n <= 100 / n > 100.", ""]
        for c in changes:
            lines.append(f"- **{c.target}** `{c.row}`: {c.old or 'new row'} -> {c.new or 'gone'}")
            for d in (results.get(c.target, {}).get("details", {}).get(c.row) or [])[:8]:
                lines.append(f"  - now: {d}")
    if failed:
        lines += ["", "## Not run", ""]
        lines += [f"- **{t}**: {msg}" for t, msg in sorted(failed.items())]
    lines += [
        "",
        "A change means the newest release behaves differently from the audited one. Check",
        "it against the full study before updating REPORT.md, then regenerate the baseline",
        "(`uv run python scripts/living.py --update-baseline`).",
    ]
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m conformcheck.living")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("battery", help="run one target's battery in this environment")
    b.add_argument("target", choices=sorted(TARGETS))
    b.add_argument("--work", required=True, help="checkpoint directory")
    b.add_argument("--result", required=True, help="JSON file to write")
    b.add_argument("--workers", type=int, default=4)
    args = p.parse_args(argv)
    res = battery(args.target, args.work, workers=min(args.workers, 4))
    Path(args.result).parent.mkdir(parents=True, exist_ok=True)
    Path(args.result).write_text(json.dumps(res, indent=1, sort_keys=True) + "\n", "utf-8")
    clean = {"PASS/PASS", "PASS/-", "-/PASS"}
    flagged = sum(v not in clean for v in res["verdicts"].values())
    print(f"{args.target}: {len(res['verdicts'])} rows, {flagged} not PASS, {res['elapsed_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
