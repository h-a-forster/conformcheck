"""Command-line interface: ``libraries``, ``plan``, ``run``, ``report`` and ``repro``.

Exit codes: 0 success, 1 failure (or, for ``repro --verify``, at least one verified
repro), 2 usage or configuration error (the resume wrapper does not retry those).
"""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from collections.abc import Sequence
from pathlib import Path

from conformcheck import __version__
from conformcheck.study import load_study

LIBRARIES: dict[str, str] = {
    "mapie": "mapie",
    "crepes": "crepes",
    "puncc": "puncc",
    "torchcp": "torchcp",
}


def library_versions() -> dict[str, str | None]:
    """Installed version of each library under test, or None when it is missing."""
    out: dict[str, str | None] = {}
    for name, dist in LIBRARIES.items():
        try:
            out[name] = importlib.metadata.version(dist)
        except importlib.metadata.PackageNotFoundError:
            out[name] = None
    return out


def _cmd_libraries(_: argparse.Namespace) -> int:
    for name, version in library_versions().items():
        print(f"{name:10s} {version or 'not installed'}")
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    from conformcheck.plan import plan_study

    try:
        study = load_study(args.study, reps=args.reps)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    plan_study(study, workers=min(args.workers, 4), probe=not args.no_probe)
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    from conformcheck.runner import (
        FingerprintMismatch,
        MissingLibraries,
        known_libraries,
        run_study,
    )

    try:
        study = load_study(args.study, reps=args.reps)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    libs = None
    if args.libraries:
        libs = {x.strip() for x in args.libraries.split(",") if x.strip()} | {"reference"}
    if libs is not None:
        unknown = sorted(libs - known_libraries())
        if unknown:
            print(
                f"error: unknown libraries {unknown}; known: {sorted(known_libraries())}",
                file=sys.stderr,
            )
            return 2
    try:
        res = run_study(
            study,
            args.out,
            workers=min(args.workers, 4),
            force=args.force,
            libraries=libs,
            allow_missing=args.allow_missing,
        )
    except (FingerprintMismatch, MissingLibraries) as exc:
        # configuration problems: exit 2 so the resume wrapper does not retry them
        print(f"error: {exc}", file=sys.stderr)
        return 2
    missing = res.get("missing_libraries") or []
    print(
        f"{res['done']}/{res['total']} units done, {res['errors']} unit errors, "
        f"{res['elapsed_s'] / 60:.1f} min"
        + (f"; NOT RUN (not installed): {', '.join(missing)}" if missing else "")
    )
    return 0 if res["done"] == res["total"] else 1


def _cmd_report(args: argparse.Namespace) -> int:
    from conformcheck.report import write_report

    run = Path(args.run_dir)
    if not (run / "run.json").exists():
        print(f"error: {run} has no run.json", file=sys.stderr)
        return 2
    if not any((run / n).exists() for n in ("units.jsonl", "units.jsonl.gz")):
        print(
            f"error: {run} has no units.jsonl (or units.jsonl.gz); nothing to report",
            file=sys.stderr,
        )
        return 2
    payload = write_report(run, args.out)
    h = payload["headline"]
    out = Path(args.out) if args.out else run / "report"
    print(
        f"{payload['units_done']} units, {payload['statistical_cells']} statistical cells; "
        f"{h['rows_small_n_flagged']}/{h['rows']} library rows flagged at n <= 100; "
        f"written to {out}"
    )
    missing = (payload["run"] or {}).get("missing_libraries") or []
    if missing:
        print(f"warning: not run (not installed): {', '.join(missing)}", file=sys.stderr)
    return 0


def _cmd_repro(args: argparse.Namespace) -> int:
    from conformcheck.repro import write_repros

    run = Path(args.run_dir)
    if not (run / "run.json").exists():
        print(f"error: {run} has no run.json", file=sys.stderr)
        return 2
    results = write_repros(run, verify=args.verify, out_dir=args.out)
    for r in results:
        status = "" if r.exit_code is None else f" exit={r.exit_code}"
        print(f"{r.path}{status}  {r.title}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="conformcheck",
        description="Finite-sample coverage certification for conformal-prediction libraries.",
    )
    parser.add_argument("--version", action="version", version=f"conformcheck {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("libraries", help="show which libraries under test are installed")
    p.set_defaults(func=_cmd_libraries)

    p = sub.add_parser("plan", help="enumerate a study's units and estimate its run time")
    p.add_argument("--study", default="default", help="built-in study name or TOML path")
    p.add_argument("--workers", type=int, default=4, help="worker processes (max 4)")
    p.add_argument("--reps", type=int, default=None, help="override repetitions per cell")
    p.add_argument("--no-probe", action="store_true", help="count units without timing")
    p.set_defaults(func=_cmd_plan)

    p = sub.add_parser("run", help="run (or resume) a study with per-unit checkpoints")
    p.add_argument("--study", default="default", help="built-in study name or TOML path")
    p.add_argument("--out", required=True, help="run directory, e.g. runs/default")
    p.add_argument("--workers", type=int, default=4, help="worker processes (max 4)")
    p.add_argument("--reps", type=int, default=None, help="override repetitions per cell")
    p.add_argument("--force", action="store_true", help="resume despite a changed config")
    p.add_argument("--libraries", default=None, help="comma-separated subset, e.g. mapie,puncc")
    p.add_argument(
        "--allow-missing",
        action="store_true",
        help="run without libraries that are not installed (they are listed, not run)",
    )
    p.set_defaults(func=_cmd_run)

    p = sub.add_parser("report", help="build the conformance matrix from a run directory")
    p.add_argument("run_dir")
    p.add_argument("--out", default=None, help="output directory (default <run_dir>/report)")
    p.set_defaults(func=_cmd_report)

    p = sub.add_parser("repro", help="write and verify minimal repro scripts for findings")
    p.add_argument("run_dir")
    p.add_argument("--verify", action="store_true", help="execute each script")
    p.add_argument("--out", default=None, help="output directory (default <run_dir>/repros)")
    p.set_defaults(func=_cmd_repro)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
