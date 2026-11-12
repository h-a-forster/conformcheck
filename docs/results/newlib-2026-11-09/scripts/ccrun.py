"""conformcheck driver for time-series conformal wrappers. Run: <venv python> -I ccrun.py <lib> [reps]
Each cell is one check_split_regressor call (same seed and draws as a batch call), appended to
<lib>/cells.jsonl when finished and skipped on rerun. Holm is applied across the whole library at the end.
Adapter contract: the library sees the calibration residuals as a time series and a forecaster that
returns exactly 0, so its scores are |r_t|, exchangeable, and the same interval applies to all m test points."""
import sys, os, json, time, importlib, warnings
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "..", "..", "..", "src"))  # this repository's conformcheck
sys.path.insert(0, os.path.join(BASE, "scripts"))
warnings.filterwarnings("ignore")
import numpy as np
from conformcheck import testing, stats, laws

lib = sys.argv[1]; reps_arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
ad = importlib.import_module(f"ad_{lib}")
os.makedirs(os.path.join(BASE, lib), exist_ok=True)
OUT = os.path.join(BASE, lib, "cells.jsonl"); LOG = os.path.join(BASE, lib, "progress.log")
done = set()
if os.path.exists(OUT):
    done = {tuple(json.loads(l)["id"]) for l in open(OUT)}
def log(s):
    with open(LOG, "a") as f: f.write(time.strftime("%H:%M:%S ") + s + "\n")

def ref_row(off):
    def fn(xc, yc, xt, a, model):
        r = np.sort(np.abs(yc - model.predict(xc))); n = len(r); k = laws.split_index(n, laws.as_fraction(a)) + off
        q = np.inf if k > n else (r[max(k, 1) - 1])
        p = model.predict(xt); return np.column_stack([p - q, p + q])
    return fn
rows = dict(ad.ROWS)
rows["reference/exact"] = dict(fn=ref_row(0), n=ad.REF_N, alpha=ad.ALPHAS, reps=200, score="abs")
rows["reference/k_minus_1"] = dict(fn=ref_row(-1), n=ad.REF_N, alpha=ad.ALPHAS, reps=200, score="abs")
t0 = time.time()
for name, r in rows.items():
    for n in r["n"]:
        for a in r["alpha"]:
            cid = (name, n, str(a))
            if cid in done: continue
            t1 = time.time()
            reps = reps_arg or r.get("reps", 200)
            rep = testing.check_split_regressor(r["fn"], n=n, alpha=a, reps=reps, test_points=500, seed=20261109, score=r.get("score", "other"))
            c = rep.cells[0]
            rec = dict(id=cid, row=name, n=n, alpha=str(a), k=c.k, reps=reps, coverage=c.coverage, target=c.target, p_value=c.p_value,
                       p_mean=c.p_mean, p_gof=c.p_gof, offsets={str(k): v for k, v in c.rank_offsets.items()}, status=c.status, detail=c.detail,
                       secs=round(time.time() - t1, 2))
            with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
            log(f"{name} n={n} a={a} cov={c.coverage:.4f} target={c.target:.4f} {time.time()-t1:.1f}s")
log(f"done {time.time()-t0:.0f}s")
