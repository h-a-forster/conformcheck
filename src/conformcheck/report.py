"""Turn ``units.jsonl`` into the conformance matrix (docs/DESIGN.md, sections 3.4 and 8).

Outputs in the report directory: ``cells.csv`` (every cell), ``matrix.json``,
``matrix.md`` (row summary, status grid, non-PASS cells) and ``summary.md`` (headline
counts, oracle controls, findings to verify). Statuses are recomputed from
``units.jsonl`` alone.

Statuses, in order of severity: ERROR > FAIL > LAW_MISMATCH > CONSERVATIVE >
OVER_REFUSED > REFUSED > PASS. ``OVER_REFUSED`` means the library raised for a level
where a finite valid set exists (``k <= n``); ``REFUSED`` is a refusal where ``k > n``,
which is valid behaviour. Deterministic diagnostics (rank recovery, trivial-set check,
refusals, errors) do not enter the multiple-testing family; the statistical cells are
adjusted with Holm (decisions) and Benjamini-Yekutieli (reported).
"""

from __future__ import annotations

import csv
import functools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats as sps

from conformcheck import laws, stats
from conformcheck.runner import iter_records
from conformcheck.study import cell_law

SEVERITY = ["ERROR", "FAIL", "LAW_MISMATCH", "CONSERVATIVE", "OVER_REFUSED", "REFUSED", "PASS"]
SYMBOL = {
    "ERROR": "E",
    "FAIL": "F",
    "LAW_MISMATCH": "L",
    "CONSERVATIVE": "C",
    "OVER_REFUSED": "O",
    "REFUSED": "R",
    "PASS": "P",
}
SMALL_N = 100

# Behaviour the library documents; reported, but not counted as a defect in the headline.
DOCUMENTED: dict[str, str] = {
    "mapie/aps/include_last_label=True": (
        "MAPIE documents include_last_label=True as conservative"
    ),
}
# The statuses each documented row is excused for. Any other status of that row (a
# crash, a refused feasible level) still counts towards the headline.
DOCUMENTED_STATUSES: dict[str, frozenset[str]] = {
    "mapie/aps/include_last_label=True": frozenset({"CONSERVATIVE"}),
}


def worst(statuses: list[str]) -> str:
    if not statuses:
        return "PASS"
    return min(statuses, key=SEVERITY.index)


@dataclass
class Cell:
    row: str
    library: str
    method: str
    variant: str
    dgp: str
    grid: str
    n: int
    n_folds: int | None
    alpha: str
    k: int
    m: int
    reps: int
    law_kind: str
    target: float
    n_ok: int
    n_refused: int
    n_error: int
    coverage: float | None = None
    ci_low: float | None = None
    ci_high: float | None = None
    p_mean: float | None = None
    p_gof: float | None = None
    p_cell: float | None = None
    p_holm: float | None = None
    p_by: float | None = None
    holm_threshold: float | None = None
    direction: str = ""
    one_sided: bool = False
    rank_offsets: dict[str, int] = field(default_factory=dict)
    rank_pairs: dict[str, int] = field(default_factory=dict)
    rank_interp: int = 0
    bracket_offsets: dict[str, int] = field(default_factory=dict)
    diff_max: float | None = None
    nontrivial: int = 0
    mde: float | None = None
    det_status: str = "PASS"
    stat_status: str = "PASS"
    by_reject: bool = False
    status: str = "PASS"
    reason: str = ""
    message: str = ""
    warnings: list[str] = field(default_factory=list)

    @property
    def is_control(self) -> bool:
        return self.library == "reference"

    @property
    def statistical(self) -> bool:
        return self.p_cell is not None


@functools.cache
def _cell_law(
    method: str,
    variant: str,
    library: str,
    dgp: str,
    n: int,
    alpha: Fraction,
    m: int,
    n_folds: int | None,
) -> Any:
    """:func:`conformcheck.study.cell_law`, memoised (it is called twice per cell)."""
    return cell_law(
        method=method,
        variant=variant,
        library=library,
        dgp=dgp,
        n=n,
        alpha=alpha,
        m=m,
        n_folds=n_folds,
    )


def _record_order(rec: dict[str, Any]) -> tuple[Any, ...]:
    """Deterministic record order (``units.jsonl`` is in completion order)."""
    return (
        str(rec.get("grid", "")),
        str(rec.get("dgp", "")),
        int(rec.get("n", 0)),
        str(rec.get("library", "")),
        str(rec.get("method", "")),
        str(rec.get("variant", "")),
        rec.get("n_folds") or 0,
    )


def _rank_status(offsets: dict[str, int]) -> tuple[str, str]:
    """Deterministic status from the per-repetition order-statistic offsets."""
    below = {float(k): v for k, v in offsets.items() if float(k) < 0}
    above = {float(k): v for k, v in offsets.items() if float(k) > 0}
    if below:
        worst_off = min(below)
        return "FAIL", f"rank {worst_off:+g} in {sum(below.values())} reps"
    if above:
        top = max(above, key=lambda o: above[o])
        return "CONSERVATIVE", f"rank {top:+g} in {sum(above.values())} reps"
    return "PASS", ""


def build_cells(records: list[dict[str, Any]]) -> list[Cell]:
    cells: list[Cell] = []
    for rec in sorted(records, key=_record_order):
        if rec.get("status") != "done":
            continue
        row = f"{rec['library']}/{rec['method']}/{rec['variant']}"
        for a_str, ao in sorted(rec["alphas_out"].items(), key=lambda kv: -Fraction(kv[0])):
            alpha = Fraction(a_str)
            cl = _cell_law(
                rec["method"],
                rec["variant"],
                rec["library"],
                rec["dgp"],
                rec["n"],
                alpha,
                rec["m"],
                rec.get("n_folds"),
            )
            c = Cell(
                row=row,
                library=rec["library"],
                method=rec["method"],
                variant=rec["variant"],
                dgp=rec["dgp"],
                grid=rec["grid"],
                n=rec["n"],
                n_folds=rec.get("n_folds"),
                alpha=a_str,
                k=ao["k"],
                m=rec["m"],
                reps=rec["reps"],
                law_kind=cl.kind,
                target=cl.target,
                n_ok=ao["n_ok"],
                n_refused=ao["n_refused"],
                n_error=ao["n_error"],
                rank_offsets=ao.get("rank_offsets", {}),
                rank_pairs=ao.get("rank_pairs", {}),
                rank_interp=ao.get("rank_interp", 0),
                bracket_offsets=ao.get("bracket_offsets", {}),
                diff_max=ao.get("diff_max"),
                nontrivial=ao.get("nontrivial", 0),
                message=ao.get("message", ""),
                warnings=ao.get("warnings", []),
            )
            counts = np.asarray(ao["counts"], dtype=np.int64)
            # deterministic part
            trivial_needed = c.k > c.n
            if c.n_error:
                c.det_status, c.reason = "ERROR", f"{c.n_error}/{c.reps} reps raised"
            elif c.n_refused == c.reps:
                if trivial_needed or cl.kind == "trivial":
                    c.det_status, c.reason = "REFUSED", "refused (k > n)"
                else:
                    c.det_status, c.reason = "OVER_REFUSED", "refused a feasible level (k <= n)"
            elif c.n_refused:
                c.det_status, c.reason = "ERROR", f"refused in {c.n_refused}/{c.reps} reps only"
            elif cl.kind == "trivial" and c.nontrivial:
                c.det_status, c.reason = "FAIL", f"finite set when k > n in {c.nontrivial} reps"
            else:
                c.det_status, c.reason = _rank_status(c.rank_offsets)
            if counts.size:
                # empirical t interval: the law's variance holds only under the null
                c.coverage, c.ci_low, c.ci_high = stats.coverage_interval(counts, c.m)
            # statistical part
            if counts.size >= 2 and c.n_ok == c.reps and cl.law is not None:
                ties = ao.get("ties_reps", 0) > 0 or cl.one_sided
                c.one_sided = ties
                alt = "less" if ties else "two-sided"
                if cl.kind == "exact":
                    mt = stats.mean_test(counts, cl.law, alternative=alt)
                    c.p_mean, c.direction = mt.pvalue, mt.direction
                    if not ties:
                        c.p_gof = stats.gof_test(counts, cl.law).pvalue
                elif cl.kind == "mean":
                    mt = stats.mean_test(counts, cl.law, alternative=alt)
                    c.p_mean, c.direction = mt.pvalue, mt.direction
                elif cl.kind == "lower":
                    mt = stats.lower_bound_test(counts, c.m, cl.target)
                    c.p_mean, c.direction = mt.pvalue, mt.direction
                if c.p_mean is not None:
                    c.p_cell = stats.cell_pvalue(c.p_mean, c.p_gof)
            cells.append(c)
    return cells


def adjust(cells: list[Cell], fwer: float, fdr: float) -> None:
    """Holm and BY across every statistical cell; set statistical and combined statuses."""
    stat_cells = [c for c in cells if c.statistical]
    if stat_cells:
        pv = np.array([c.p_cell for c in stat_cells], dtype=float)
        h = stats.holm(pv, fwer)
        b = stats.benjamini_yekutieli(pv, fdr)
        z_crit = float(sps.norm.isf(fwer / (2 * len(stat_cells))))
        for c, adj, rej, thr, badj, brej in zip(
            stat_cells, h.adjusted, h.reject, h.thresholds, b.adjusted, b.reject, strict=True
        ):
            c.p_holm, c.holm_threshold, c.p_by, c.by_reject = (
                float(adj),
                float(thr),
                float(badj),
                bool(brej),
            )
            if c.law_kind == "exact":
                law = _cell_law(
                    c.method, c.variant, c.library, c.dgp, c.n, Fraction(c.alpha), c.m, c.n_folds
                ).law
                if law is not None:
                    c.mde = stats.min_detectable_effect(law, c.reps, z_crit)
            if not rej:
                continue
            assert c.p_mean is not None
            mean_alone = min(1.0, 2 * c.p_mean) if c.p_gof is not None else c.p_mean
            if mean_alone <= thr or c.p_gof is None:
                c.stat_status = "FAIL" if c.direction == "below" else "CONSERVATIVE"
                if c.law_kind == "lower":
                    c.stat_status = "FAIL"
            else:
                c.stat_status = "LAW_MISMATCH"
    for c in cells:
        c.status = worst([c.det_status, c.stat_status])
        if c.stat_status != "PASS" and c.det_status == "PASS":
            c.reason = (c.reason + "; " if c.reason else "") + (
                f"Holm p={c.p_holm:.2g}, coverage {c.coverage:.4f} vs {c.target:.4f}"
            )


@dataclass
class RowSummary:
    row: str
    library: str
    method: str
    variant: str
    cells: int
    small_n_status: str
    large_n_status: str
    counts: dict[str, int]
    documented: str = ""
    # worst small-n status once the row's documented statuses are set aside
    small_n_undocumented: str = "-"
    non_pass: list[str] = field(default_factory=list)


def summarize_rows(cells: list[Cell]) -> list[RowSummary]:
    by_row: dict[str, list[Cell]] = defaultdict(list)
    for c in cells:
        by_row[c.row].append(c)
    out = []
    for row, cs in by_row.items():
        small = [c.status for c in cs if c.n <= SMALL_N]
        large = [c.status for c in cs if c.n > SMALL_N]
        excused = DOCUMENTED_STATUSES.get(row, frozenset())
        small_undoc = [st for st in small if st not in excused]
        out.append(
            RowSummary(
                row=row,
                library=cs[0].library,
                method=cs[0].method,
                variant=cs[0].variant,
                cells=len(cs),
                small_n_status=worst(small) if small else "-",
                large_n_status=worst(large) if large else "-",
                counts=dict(Counter(c.status for c in cs)),
                documented=DOCUMENTED.get(row, ""),
                small_n_undocumented=(
                    worst(small_undoc) if small_undoc else ("PASS" if small else "-")
                ),
                non_pass=[
                    f"{c.dgp} n={c.n} a={c.alpha}: {c.status} ({c.reason})"
                    for c in cs
                    if c.status != "PASS"
                ],
            )
        )
    order = {"mapie": 0, "crepes": 1, "puncc": 2, "torchcp": 3, "reference": 4}
    out.sort(key=lambda r: (order.get(r.library, 9), r.method, r.variant))
    return out


def _fmt(x: float | None, digits: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{digits}f}"


def _alpha_label(a: str) -> str:
    f = Fraction(a)
    dec = float(f)
    return f"{dec:g}" if Fraction(repr(dec)) == f else a


def mutant_is_identical(n: int, alpha: Fraction, mutant: str) -> bool:
    """True when a mutant uses the same order statistic as the correct method at
    ``(n, alpha)``, so it cannot be detected and is left out of the power counts."""
    k = laws.split_index(n, alpha)
    if mutant == "n_instead_of_n_plus_1":
        return math.ceil(n * (1 - alpha)) == k
    if mutant == "no_correction_linear":
        h = (n - 1) * (1 - alpha)  # 0-based position of numpy's linear quantile
        return h.denominator == 1 and int(h) + 1 == k
    return False


def controls_summary(cells: list[Cell]) -> dict[str, Any]:
    """Size (reference rows) and power (mutant rows) of the oracle, per n.

    Size: the cell p-value is conservative by construction (``2 min`` of two tests, both
    discrete), so its distribution is not uniform under the null and a uniformity test
    on it is meaningless. The calibration check counts how often the exact two-sided mean
    test alone rejects at 0.05 (under the null ``P(p_mean <= 0.05) <= 0.05``). The count
    is descriptive: the alphas of one unit and the reference rows on one dgp share their
    calibration draws (common random numbers), so the cells are dependent and a binomial
    test on the count would not give a valid p-value.
    """
    ref = [c for c in cells if c.library == "reference"]
    from conformcheck.reference import MUTANTS

    ref_main = [c for c in ref if c.variant not in MUTANTS]
    stat_main = [c for c in ref_main if c.statistical]
    exact_p = [
        c.p_mean
        for c in stat_main
        if c.law_kind == "exact" and not c.one_sided and c.p_mean is not None
    ]
    raw = sum(p <= 0.05 for p in exact_p)
    size = {
        "reference_cells": len(ref_main),
        "reference_statistical_cells": len(stat_main),
        "reference_holm_rejections": sum(c.stat_status != "PASS" for c in stat_main),
        "reference_nonpass_cells": sum(c.status != "PASS" for c in ref_main),
        "reference_raw_rejections_at_0.05": sum((c.p_cell or 1) <= 0.05 for c in stat_main),
        "reference_exact_mean_tests": len(exact_p),
        "reference_exact_mean_rejections_at_0.05": raw,
        "reference_exact_mean_rejection_rate": (raw / len(exact_p)) if exact_p else None,
    }
    power: dict[str, dict[str, Any]] = {}
    for mut in MUTANTS:
        cs = [c for c in ref if c.variant == mut and c.law_kind != "trivial"]
        if not cs:
            continue
        per_n: dict[int, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
        for c in cs:
            v = per_n[c.n]
            if c.k > c.n or mutant_is_identical(c.n, Fraction(c.alpha), mut):
                v[3] += 1
                continue
            v[0] += 1
            v[1] += c.stat_status != "PASS"
            v[2] += c.status != "PASS"
        power[mut] = {
            str(n): {
                "cells": v[0],
                "stat_detected": v[1],
                "any_detected": v[2],
                "identical_excluded": v[3],
            }
            for n, v in sorted(per_n.items())
        }
    return {"size": size, "power": power}


def write_report(run_dir: str | Path, out_dir: str | Path | None = None) -> dict[str, Any]:
    run = Path(run_dir)
    out = Path(out_dir) if out_dir else run / "report"
    out.mkdir(parents=True, exist_ok=True)
    meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
    study = meta["study"]
    records = list(iter_records(run))
    cells = build_cells(records)
    adjust(cells, float(study["fwer"]), float(study["fdr"]))
    rows = summarize_rows(cells)
    controls = controls_summary(cells)

    # cells.csv
    fields = [f for f in asdict(cells[0])] if cells else []
    with (out / "cells.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for c in cells:
            d = asdict(c)
            d["rank_offsets"] = json.dumps(d["rank_offsets"], sort_keys=True)
            d["rank_pairs"] = json.dumps(d["rank_pairs"], sort_keys=True)
            d["bracket_offsets"] = json.dumps(d["bracket_offsets"], sort_keys=True)
            d["warnings"] = " | ".join(d["warnings"])
            w.writerow(d)
    lib_rows = [r for r in rows if r.library != "reference"]
    headline = headline_counts(lib_rows)
    payload = {
        "run": {
            k: meta.get(k)
            for k in (
                "fingerprint",
                "versions",
                "platform",
                "workers",
                "units_total",
                "first_started",
                "ended",
                "source",
                "missing_libraries",
            )
        },
        "study": study,
        "units_done": len(records),
        "statistical_cells": sum(c.statistical for c in cells),
        "headline": headline,
        "controls": controls,
        "rows": [asdict(r) for r in rows],
    }
    (out / "matrix.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    (out / "matrix.md").write_text(render_matrix_md(cells, rows, payload), encoding="utf-8")
    (out / "summary.md").write_text(render_summary_md(cells, rows, payload), encoding="utf-8")
    _cell_law.cache_clear()
    return payload


def headline_counts(lib_rows: list[RowSummary]) -> dict[str, Any]:
    """Rows flagged at small n. A documented row is excused only for its documented
    statuses (``DOCUMENTED_STATUSES``); its other non-PASS statuses still count."""
    bad = {"FAIL", "CONSERVATIVE", "LAW_MISMATCH", "ERROR", "OVER_REFUSED"}
    flagged = [r.row for r in lib_rows if r.small_n_undocumented in bad]
    return {
        "rows": len(lib_rows),
        "rows_small_n_flagged": len(flagged),
        "flagged_rows": flagged,
        "by_small_n_status": dict(Counter(r.small_n_status for r in lib_rows)),
    }


def render_matrix_md(cells: list[Cell], rows: list[RowSummary], payload: dict[str, Any]) -> str:
    study = payload["study"]
    lines = [
        f"# Conformance matrix: study `{study['name']}`",
        "",
        f"R = {study['reps']} repetitions, m = {study['test_points']} test points (capped "
        f"by the pool on toy data), seed {study['seed']}. Holm FWER {study['fwer']} over "
        f"{payload['statistical_cells']} statistical cells; BY FDR {study['fdr']} reported.",
        "",
        "Status per row: worst over cells with n <= 100 (small n) and n > 100 (large n).",
        "",
        "| row | small n | large n | cells | status counts | note |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        counts = ", ".join(
            f"{k} {v}" for k, v in sorted(r.counts.items(), key=lambda kv: SEVERITY.index(kv[0]))
        )
        lines.append(
            f"| `{r.row}` | {r.small_n_status} | {r.large_n_status} | {r.cells} | "
            f"{counts} | {r.documented} |"
        )
    ns = sorted({c.n for c in cells})
    lines += [
        "",
        "## Status grid (worst over dgps and alphas at each n)",
        "",
        "P pass, C conservative, F fail, L law mismatch, O refused a feasible level, "
        "R refused with k > n, E error, . not run.",
        "",
        "| row | " + " | ".join(str(n) for n in ns) + " |",
        "|---|" + "---|" * len(ns),
    ]
    by_row_n: dict[tuple[str, int], list[str]] = defaultdict(list)
    for c in cells:
        by_row_n[(c.row, c.n)].append(c.status)
    for r in rows:
        syms = [SYMBOL[worst(by_row_n[(r.row, n)])] if (r.row, n) in by_row_n else "." for n in ns]
        lines.append(f"| `{r.row}` | " + " | ".join(syms) + " |")
    lines += [
        "",
        "## Non-PASS cells (libraries)",
        "",
        "| row | dgp | n | alpha | k | status | coverage [95% CI] | target | "
        "rank offsets lower|upper (reps) | "
        "Holm p | reason |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in sorted(
        (c for c in cells if c.status != "PASS" and not c.is_control),
        key=lambda c: (c.row, c.dgp, c.n, -Fraction(c.alpha)),
    ):
        cov = f"{_fmt(c.coverage)} [{_fmt(c.ci_low)}, {_fmt(c.ci_high)}]" if c.coverage else ""
        lines.append(
            f"| `{c.row}` | {c.dgp} | {c.n} | {_alpha_label(c.alpha)} | {c.k} | {c.status} | "
            f"{cov} | {c.target:.4f} | {json.dumps(c.rank_pairs) if c.rank_pairs else ''} | "
            f"{'' if c.p_holm is None else f'{c.p_holm:.2g}'} | "
            f"{(c.reason + ' ' + c.message[:80]).strip()} |"
        )
    return "\n".join(lines) + "\n"


def render_summary_md(cells: list[Cell], rows: list[RowSummary], payload: dict[str, Any]) -> str:
    h = payload["headline"]
    ctl = payload["controls"]
    v = payload["run"]["versions"] or {}
    lines = [
        f"# Summary: study `{payload['study']['name']}`",
        "",
        "Versions: " + ", ".join(f"{k} {val}" for k, val in v.items() if val),
        "",
        f"**Headline.** {h['rows_small_n_flagged']} of {h['rows']} library-method rows are "
        "flagged (FAIL, CONSERVATIVE, LAW_MISMATCH, OVER_REFUSED or ERROR) in at least one "
        "cell with n <= 100. A documented row is excused only for its documented status.",
        "",
        *(
            [
                "**Not run (library not installed):** "
                + ", ".join(payload["run"]["missing_libraries"]),
                "",
            ]
            if payload["run"].get("missing_libraries")
            else []
        ),
        "Small-n status counts: "
        + ", ".join(f"{k} {val}" for k, val in sorted(h["by_small_n_status"].items())),
        "",
        "## Oracle controls",
        "",
        "Size (reference implementations through the same pipeline): "
        + ", ".join(
            f"{k} = {val if not isinstance(val, float) else f'{val:.3g}'}"
            for k, val in ctl["size"].items()
        ),
        "",
        "Power (mutants; statistical detections / cells per n, deterministic included in "
        "'any'; cells where the mutant uses the correct order statistic are excluded):",
        "",
    ]
    for mut, per_n in ctl["power"].items():
        parts = [
            f"n={n}: {d['stat_detected']}/{d['cells']} (any {d['any_detected']})"
            for n, d in per_n.items()
            if d["cells"]
        ]
        lines.append(f"- `{mut}`: " + "; ".join(parts))
    lines += ["", "## Flagged rows", ""]
    for r in rows:
        if r.library == "reference" or not r.non_pass:
            continue
        note = f" ({r.documented})" if r.documented else ""
        lines.append(f"### `{r.row}`{note}")
        lines.append("")
        for item in r.non_pass[:25]:
            lines.append(f"- {item}")
        if len(r.non_pass) > 25:
            lines.append(f"- ... {len(r.non_pass) - 25} more in cells.csv")
        lines.append("")
    return "\n".join(lines) + "\n"
