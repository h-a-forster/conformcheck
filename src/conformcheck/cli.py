"""Command-line interface.

``conformcheck --version`` and ``conformcheck libraries`` work now; the study commands
(``plan``, ``run``, ``report``, ``repro``) arrive in milestones M4 to M6 (docs/DESIGN.md,
section 9).
"""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from collections.abc import Sequence

from conformcheck import __version__

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


def _not_yet(milestone: str):
    def run(_: argparse.Namespace) -> int:
        print(f"not implemented yet (milestone {milestone}, see docs/DESIGN.md)", file=sys.stderr)
        return 2

    return run


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
    p.set_defaults(func=_not_yet("M4"))

    p = sub.add_parser("run", help="run (or resume) a study with per-unit checkpoints")
    p.add_argument("--study", default="default", help="built-in study name or TOML path")
    p.add_argument("--out", required=True, help="run directory, e.g. runs/default")
    p.add_argument("--workers", type=int, default=4, help="worker processes (max 4)")
    p.add_argument("--reps", type=int, default=None, help="override repetitions per cell")
    p.add_argument("--force", action="store_true", help="resume despite a changed config")
    p.set_defaults(func=_not_yet("M4"))

    p = sub.add_parser("report", help="build the conformance matrix from a run directory")
    p.add_argument("run_dir")
    p.set_defaults(func=_not_yet("M5"))

    p = sub.add_parser("repro", help="write and verify minimal repro scripts for findings")
    p.add_argument("run_dir")
    p.add_argument("--verify", action="store_true", help="execute each script")
    p.set_defaults(func=_not_yet("M6"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
