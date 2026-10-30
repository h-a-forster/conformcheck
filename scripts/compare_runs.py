"""Compare two runs of the same study cell by cell (for example one library at two versions).

Usage::

    uv run python scripts/compare_runs.py BEFORE AFTER --library mapie --out compare.md

``BEFORE`` and ``AFTER`` are run directories (``run.json``, ``units.jsonl`` and the
``report/cells.csv`` written by ``conformcheck report``) or a results directory with
``cells.csv`` and ``units.jsonl.gz`` side by side, such as ``docs/results/default``.

Two comparisons are written:

- units: for each unit id in both runs (records of the study in ``run.json`` only, as
  ``conformcheck report`` reads them), whether the raw per-alpha results (covered counts,
  ranks, refusals, errors) are identical. This is exact and does not depend on the rest
  of the run.
- cells: status changes per cell. Statuses depend on the Holm family, so they are only
  comparable when both runs contain the same cells (same study and libraries).
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

from conformcheck.report import SEVERITY
from conformcheck.runner import study_records

KEY = ("row", "dgp", "grid", "n", "n_folds", "alpha")


def read_cells(run: Path, library: str | None) -> dict[tuple[str, ...], dict[str, str]]:
    path = next((p for p in (run / "report" / "cells.csv", run / "cells.csv") if p.exists()), None)
    if path is None:
        raise SystemExit(f"error: no report/cells.csv or cells.csv in {run}")
    with path.open(newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if library is None or r["library"] == library]
    return {tuple(r[k] for k in KEY): r for r in rows}


def read_units(run: Path, library: str | None) -> dict[str, dict]:
    return {
        rec["uid"]: rec
        for rec in study_records(run)[0]
        if library is None or rec.get("library") == library
    }


def _outcome(rec: dict) -> dict:
    """Per-alpha results; a field absent from older records equals its empty value."""
    return {
        a: {k: v for k, v in d.items() if v is not None and v != {}}
        for a, d in rec["alphas_out"].items()
    }


def compare(before: Path, after: Path, library: str | None) -> str:
    ub, ua = read_units(before, library), read_units(after, library)
    shared = sorted(set(ub) & set(ua))
    same = sum(_outcome(ub[u]) == _outcome(ua[u]) for u in shared)
    cb, ca = read_cells(before, library), read_cells(after, library)
    out = [
        f"# {before.as_posix()} vs {after.as_posix()}" + (f" ({library})" if library else ""),
        "",
        "## Units",
        "",
        f"- shared unit ids: {len(shared)}; raw results identical: {same}; "
        f"different: {len(shared) - same}",
        f"- only in before: {len(set(ub) - set(ua))}; only in after: {len(set(ua) - set(ub))}",
        "",
        "## Status counts per row (before -> after)",
        "",
        "| Row | " + " | ".join(SEVERITY) + " | changed cells |",
        "|---|" + "---|" * (len(SEVERITY) + 1),
    ]
    rows = sorted({k[0] for k in cb} | {k[0] for k in ca})
    changed = [k for k in sorted(set(cb) & set(ca)) if cb[k]["status"] != ca[k]["status"]]
    for row in rows:
        sb = Counter(v["status"] for k, v in cb.items() if k[0] == row)
        sa = Counter(v["status"] for k, v in ca.items() if k[0] == row)
        cells = [f"{sb[s]}" if sb[s] == sa[s] else f"{sb[s]} -> {sa[s]}" for s in SEVERITY]
        n_changed = sum(k[0] == row for k in changed)
        out.append(f"| `{row}` | " + " | ".join(cells) + f" | {n_changed} |")
    missing = len(set(cb) ^ set(ca))
    if missing:
        out += ["", f"{missing} cells are in only one of the two runs (not compared)."]
    out += [
        "",
        "## Cells whose status changed",
        "",
        "| Row | dgp | n | K | alpha | status | coverage | target | rank offsets | reason |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for k in changed:
        b, a = cb[k], ca[k]
        out.append(
            f"| `{k[0]}` | {k[1]} | {k[3]} | {k[4] or '-'} | {k[5]} "
            f"| {b['status']} -> {a['status']} | {_num(b['coverage'])} -> {_num(a['coverage'])} "
            f"| {_num(a['target'])} | {b['rank_offsets']} -> {a['rank_offsets']} "
            f"| {(a['reason'] or b['reason']).replace('|', '/')} |"
        )
    if not changed:
        out.append("| (none) | | | | | | | | | |")
    return "\n".join(out) + "\n"


def _num(x: str) -> str:
    return f"{float(x):.4f}" if x not in ("", None) else "-"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--library", default=None, help="only rows of this library")
    parser.add_argument("--out", type=Path, default=None, help="markdown file (default stdout)")
    args = parser.parse_args()
    text = compare(args.before, args.after, args.library)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
