"""Run a study with automatic resume on failure.

Usage::

    uv run python scripts/run_study.py --study default --out runs/default
    uv run python scripts/run_study.py --study full --out runs/full --attempts 5

Each attempt calls ``conformcheck run``, which skips units already checkpointed in
``<out>/units.jsonl``. Attempts and exit codes are appended to ``<out>/attempts.log``.
Progress is in ``<out>/progress.log``; watch that file, not only the exit code.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--study", default="default")
    parser.add_argument("--out", required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--attempts", type=int, default=3)
    args, extra = parser.parse_known_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    log = out / "attempts.log"
    cmd = [
        sys.executable, "-m", "conformcheck", "run",
        "--study", args.study, "--out", str(out), "--workers", str(min(args.workers, 4)),
        *extra,
    ]  # fmt: skip
    code = 1
    for attempt in range(1, args.attempts + 1):
        start = dt.datetime.now().isoformat(timespec="seconds")
        code = subprocess.call(cmd)
        with log.open("a", encoding="utf-8") as fh:
            fh.write(f"{start} attempt={attempt} exit={code}\n")
        if code == 0:
            return 0
        if code == 2:  # usage or configuration error: retrying will not help
            return code
    return code


if __name__ == "__main__":
    raise SystemExit(main())
