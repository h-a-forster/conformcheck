#!/usr/bin/env bash
# Before/after study: the default study's MAPIE rows (plus reference controls) under
# MAPIE 1.5.0 and MAPIE 1.6.0, each in its own pinned venv built from uv.lock (the two
# requirement sets differ only in the mapie pin).
#
# Resumable: each run checkpoints units in runs/mapie-versions-<study>/<version>/units.jsonl
# and a rerun of this script skips finished units and reuses the venvs in tmp/envs/.
# Each run is wrapped by scripts/run_study.py (3 attempts, exit 2 is not retried).
# Phase log: $LOG (default runs/mapie-versions-<study>/phases.log); per-run progress:
# runs/mapie-versions-<study>/<version>/progress.log.
#
# Usage: bash scripts/mapie_versions.sh            (default study, 4 workers)
#        STUDY=smoke bash scripts/mapie_versions.sh (about 4 minutes)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

STUDY=${STUDY:-default}
WORKERS=${WORKERS:-4}
OUT=runs/mapie-versions-$STUDY
LOG=${LOG:-$OUT/phases.log}
OLD=1.5.0
NEW=1.6.0
mkdir -p "$OUT" tmp/envs

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S') $*" | tee -a "$LOG"; }
die() { log "FAILED: $*"; exit 1; }
envpy() {
    if [ -x "tmp/envs/mapie-$1/Scripts/python.exe" ]; then
        echo "tmp/envs/mapie-$1/Scripts/python.exe"
    else
        echo "tmp/envs/mapie-$1/bin/python"
    fi
}

build_env() {  # $1 = mapie version
    local v=$1 req="tmp/envs/req-mapie-$1.txt" py
    uv export --frozen --no-hashes --no-dev --extra mapie --no-emit-project --no-header \
        | sed "s/^mapie==.*/mapie==$v/" > "$req" || die "uv export"
    grep -q "^mapie==$v\$" "$req" || die "mapie pin missing in $req"
    py=$(envpy "$v")
    if [ ! -x "$py" ]; then
        uv venv -q --python "$(cat .python-version)" "tmp/envs/mapie-$v" || die "venv $v"
        py=$(envpy "$v")
    fi
    uv pip install -q --python "$py" -r "$req" || die "install requirements $v"
    # The project itself, from the current checkout (not editable: the run uses this snapshot).
    uv pip install -q --python "$py" --no-deps --reinstall . || die "install conformcheck $v"
    [ "$("$py" -c 'import importlib.metadata as m; print(m.version("mapie"))')" = "$v" ] \
        || die "env $v does not have mapie $v"
    log "env mapie-$v ready: $("$py" -c 'import platform, numpy, scipy, sklearn; print("python", platform.python_version(), "numpy", numpy.__version__, "scipy", scipy.__version__, "scikit-learn", sklearn.__version__)')"
}

run_one() {  # $1 = mapie version
    local v=$1 py dir="$OUT/$1"
    py=$(envpy "$v")
    log "run mapie $v -> $dir (progress: $dir/progress.log)"
    "$py" scripts/run_study.py --study "$STUDY" --out "$dir" --workers "$WORKERS" \
        --attempts 3 --libraries mapie || die "run mapie $v (see $dir/attempts.log)"
    log "run mapie $v done: $(tail -n 1 "$dir/progress.log")"
    "$py" -m conformcheck report "$dir" 2>&1 | tee -a "$LOG" || die "report mapie $v"
}

log "start study=$STUDY workers=$WORKERS out=$OUT"
build_env "$NEW"
build_env "$OLD"
run_one "$NEW"

# Reference rows do not depend on MAPIE: seed the old run with the new run's reference
# records (they store their versions, so the runner reuses them only if numpy, scipy,
# scikit-learn and Python match). Only before the old run has started.
if [ ! -e "$OUT/$OLD/run.json" ] && [ ! -s "$OUT/$OLD/units.jsonl" ]; then
    mkdir -p "$OUT/$OLD"
    grep '"library": *"reference"' "$OUT/$NEW/units.jsonl" > "$OUT/$OLD/units.jsonl" \
        || { rm -f "$OUT/$OLD/units.jsonl"; die "seed reference records"; }
    log "seeded $(wc -l < "$OUT/$OLD/units.jsonl") reference records into $OUT/$OLD"
fi
run_one "$OLD"

PY=$(envpy "$NEW")
"$PY" scripts/compare_runs.py "$OUT/$OLD" "$OUT/$NEW" --library mapie --out "$OUT/compare.md" \
    || die "compare"
log "comparison written to $OUT/compare.md"
if [ "$STUDY" = default ]; then
    # Reproducibility: the fresh 1.6.0 units against the committed round-2 units.
    "$PY" scripts/compare_runs.py docs/results/default "$OUT/$NEW" --library mapie \
        --out "$OUT/reproduce-committed.md" || die "compare with committed results"
    log "$(grep -m1 'raw results identical' "$OUT/reproduce-committed.md")"
fi
log "done"
