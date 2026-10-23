"""Hypothesis 6 (docs/DESIGN.md, section 12): which calibration size does MAPIE RAPS follow?

For every cell of ``mapie/raps/include_last_label=randomized`` where MAPIE returned sets,
test the covered counts against the exact split law at the nominal ``n`` and at the
effective ``n_eff = n - ceil(0.1 n)`` (the size MAPIE 1.6.0 calibrates on, see
REPORT.md F9) and, for comparison, ``n - ceil(0.2 n)`` (the documented ``size_raps``).
Holm is applied within each column (one family per candidate law). Writes a Markdown
table to stdout or ``--out``.

    uv run python scripts/raps_neff.py runs/default-r2 --out docs/results/default/raps_neff.md
"""

from __future__ import annotations

import argparse
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from conformcheck import laws, stats
from conformcheck.runner import iter_records

ROW = ("mapie", "raps", "include_last_label=randomized")
CANDIDATES = {
    "nominal n": lambda n: n,
    "n - ceil(0.1 n)": lambda n: n - math.ceil(0.1 * n),
    "n - ceil(0.2 n)": lambda n: n - math.ceil(0.2 * n),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dir")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    cells = []
    for rec in iter_records(args.run_dir):
        if (rec["library"], rec["method"], rec["variant"]) != ROW:
            continue
        for a_str, ao in rec["alphas_out"].items():
            if ao["n_ok"] != rec["reps"] or not ao["counts"]:
                continue
            alpha = Fraction(a_str)
            counts = np.asarray(ao["counts"], dtype=np.int64)
            row = {
                "dgp": rec["dgp"],
                "n": rec["n"],
                "alpha": a_str,
                "coverage": counts.mean() / rec["m"],
                "effective_n": ",".join(sorted(ao.get("effective_n", {}))),
            }
            for name, f in CANDIDATES.items():
                ne = f(rec["n"])
                if laws.split_index(ne, alpha) > ne:
                    row[name] = None
                    continue
                law = laws.split_count_law(ne, alpha, rec["m"])
                p = stats.cell_pvalue(
                    stats.mean_test(counts, law).pvalue, stats.gof_test(counts, law).pvalue
                )
                row[name] = (p, law.coverage)
            cells.append(row)
    cells.sort(key=lambda r: (r["dgp"], r["n"], -Fraction(r["alpha"])))
    for name in CANDIDATES:
        idx = [i for i, r in enumerate(cells) if r[name] is not None]
        if not idx:
            continue
        h = stats.holm([cells[i][name][0] for i in idx], 0.05)
        for i, adj, rej in zip(idx, h.adjusted, h.reject, strict=True):
            p, cov = cells[i][name]
            cells[i][name] = (p, cov, float(adj), bool(rej))
    lines = [
        "# MAPIE RAPS: which calibration size does the coverage follow?",
        "",
        "Row `mapie/raps/include_last_label=randomized`, cells where MAPIE returned sets in "
        "every repetition. Each column tests the covered counts against the exact split law "
        "(mean and goodness-of-fit, Bonferroni within the cell) at a candidate calibration "
        "size; Holm at 0.05 within each column. Entry: exact coverage / Holm p "
        "(**rejected** in bold).",
        "",
        "| dgp | n | alpha | n used (adapter) | observed | " + " | ".join(CANDIDATES) + " |",
        "|---|---|---|---|---|" + "---|" * len(CANDIDATES),
    ]
    rejections = dict.fromkeys(CANDIDATES, 0)
    tested = dict.fromkeys(CANDIDATES, 0)
    for r in cells:
        parts = []
        for name in CANDIDATES:
            v = r[name]
            if v is None:
                parts.append("k > n")
                continue
            _, cov, adj, rej = v
            tested[name] += 1
            rejections[name] += rej
            txt = f"{cov:.4f} / {adj:.2g}"
            parts.append(f"**{txt}**" if rej else txt)
        a = float(Fraction(r["alpha"]))
        lines.append(
            f"| {r['dgp']} | {r['n']} | {a:.4g} | {r['effective_n']} | {r['coverage']:.4f} | "
            + " | ".join(parts)
            + " |"
        )
    lines += [
        "",
        "Holm rejections per candidate: "
        + ", ".join(f"{k}: {rejections[k]} of {tested[k]}" for k in CANDIDATES),
        "",
    ]
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
