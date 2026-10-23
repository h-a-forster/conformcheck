"""``conformcheck plan``: enumerate a study's units and estimate its run time.

The estimate probes each (adapter, grid, dgp) group at its smallest and largest ``n``
with two repetitions (after one warm-up call, so import time is excluded), interpolates
the per-repetition cost linearly in ``n``, and divides the total by the worker count.
It is an estimate; ``progress.log`` reports the real rate during the run.
"""

from __future__ import annotations

import time
from collections import Counter, defaultdict

from conformcheck.runner import evaluate_unit
from conformcheck.study import Study, Unit, enumerate_units


def _probe(unit: Unit, seed: int, test_points: int, reps: int = 2) -> float:
    cfg = {"reps": reps, "test_points": test_points, "seed": seed}
    t = time.perf_counter()
    evaluate_unit(unit.key(), cfg)
    return (time.perf_counter() - t) / reps


def estimate_seconds(study: Study, units: list[Unit], echo=print) -> float:  # type: ignore[no-untyped-def]
    groups: dict[tuple[str, str, str], list[Unit]] = defaultdict(list)
    for u in units:
        groups[(u.adapter, u.grid, u.dgp)].append(u)
    warmed: set[str] = set()
    total = 0.0
    for (adapter, grid, dgp), us in sorted(groups.items()):
        us = sorted(us, key=lambda u: u.n)
        lo, hi = us[0], us[-1]
        if adapter.split("/")[0] not in warmed:
            _probe(lo, study.seed, study.test_points, reps=1)
            warmed.add(adapter.split("/")[0])
        c_lo = _probe(lo, study.seed, study.test_points)
        c_hi = c_lo if hi is lo else _probe(hi, study.seed, study.test_points)
        sub = 0.0
        for u in us:
            frac = 0.0 if hi.n == lo.n else (u.n - lo.n) / (hi.n - lo.n)
            sub += study.reps * (c_lo + frac * (c_hi - c_lo))
        total += sub
        echo(f"  {adapter:45s} {grid:17s} {dgp:13s} units={len(us):3d} est={sub / 60:6.1f} CPU-min")
    return total


def plan_study(study: Study, workers: int = 4, probe: bool = True, echo=print) -> dict:  # type: ignore[no-untyped-def]
    units = enumerate_units(study)
    by_lib = Counter(u.adapter.split("/")[0] for u in units)
    by_grid = Counter(u.grid for u in units)
    cells = sum(len(u.alphas) for u in units)
    echo(
        f"study {study.name}: {len(units)} units, {cells} cells, R={study.reps}, "
        f"m={study.test_points}, seed={study.seed}"
    )
    echo("  by library: " + ", ".join(f"{k} {v}" for k, v in sorted(by_lib.items())))
    echo("  by grid:    " + ", ".join(f"{k} {v}" for k, v in sorted(by_grid.items())))
    out = {"units": len(units), "cells": cells}
    if probe:
        cpu = estimate_seconds(study, units, echo)
        wall = cpu / max(1, workers)
        echo(
            f"estimate: {cpu / 3600:.2f} CPU-hours, about {wall / 60:.0f} min on {workers} workers"
        )
        out.update(cpu_s=cpu, wall_s=wall)
    return out
