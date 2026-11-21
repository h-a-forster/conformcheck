"""Exact coverage of ppi_py's mean intervals: venv, run, Monte Carlo check, report.

    uv run python scripts/ppi_study.py                   # about 40 min on 4 workers
    uv run python scripts/ppi_study.py --out runs/ppi --attempts 3

Builds a fresh wheels-only venv (``<out>/venv``, Python 3.13.13) holding a wheel of this
checkout plus ``ppi-python`` at the versions in ``docs/results/ppi/constraints.txt``, then
runs ``python -m conformcheck.ppi run`` and ``mc`` inside it. Both checkpoint each unit and
skip finished ones, so a rerun resumes; each is retried up to ``--attempts`` times, with
attempts logged to ``<out>/attempts.log``. The report (``map.md``, ``coverage.csv``,
``mc.md``) is written by this environment into ``--to`` (default ``<out>``). DESIGN
section 15 describes the study.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from conformcheck import ppi

ROOT = Path(__file__).resolve().parents[1]
CONSTRAINTS = ROOT / "docs" / "results" / "ppi" / "constraints.txt"
PYTHON = "3.13.13"


def log(out: Path, msg: str) -> None:
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    with (out / "attempts.log").open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def build_venv(out: Path) -> Path:
    """Wheels only, this repository's uv settings ignored (--no-config), pinned versions."""
    dist, venv = out / "wheel", out / "venv"
    shutil.rmtree(dist, ignore_errors=True)
    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(dist), str(ROOT)],
        check=True,
        capture_output=True,
        text=True,
    )
    (wheel,) = dist.glob("conformcheck-*.whl")
    if venv.exists():
        shutil.rmtree(venv)
    subprocess.run(
        ["uv", "venv", "--no-config", "--python", PYTHON, str(venv), "-q"],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "-q",
            "--no-config",
            "--python",
            str(venv_python(venv)),
            "--only-binary",
            ":all:",
            "--constraint",
            str(CONSTRAINTS),
            str(wheel),
            "ppi-python",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return venv_python(venv)


def attempt(out: Path, python: Path, cmd: str, attempts: int, workers: int | None) -> bool:
    argv = [str(python), "-I", "-m", "conformcheck.ppi", cmd, "--out", str(out)]
    if workers:
        argv += ["--workers", str(workers)]
    for i in range(1, attempts + 1):
        log(out, f"{cmd}: attempt {i}/{attempts}")
        code = subprocess.run(argv).returncode
        log(out, f"{cmd}: attempt {i} exit {code}")
        if code == 0:
            return True
        if code == 2:  # configuration error: retrying cannot help
            return False
    return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--out", default="runs/ppi")
    p.add_argument("--to", help="report directory (default: --out)")
    p.add_argument("--attempts", type=int, default=3)
    p.add_argument("--workers", type=int)
    p.add_argument("--reuse-venv", action="store_true", help="skip the install if it exists")
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    python = venv_python(out / "venv")
    if not (args.reuse_venv and python.exists()):
        log(out, "building venv")
        python = build_venv(out)
    for cmd in ("run", "mc"):
        if not attempt(out, python, cmd, args.attempts, args.workers):
            log(out, f"{cmd} failed; see {out / 'progress.log'}")
            return 1
    summary = ppi.write_report(out, args.to)
    log(out, f"report: {summary}")
    return 0 if summary["units"] == summary["units_expected"] else 1


if __name__ == "__main__":
    sys.exit(main())
