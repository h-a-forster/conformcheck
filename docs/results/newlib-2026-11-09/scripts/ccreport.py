"""Holm across all statistical cells of a library, then a row table. Run: python -I ccreport.py <lib>"""
import sys, os, json
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "..", "..", "..", "src"))  # this repository's conformcheck
import numpy as np
from conformcheck import stats
lib = sys.argv[1]
recs = [json.loads(l) for l in open(os.path.join(BASE, lib, "cells.jsonl"))]
st = [r for r in recs if r["p_value"] is not None]
h = stats.holm([r["p_value"] for r in st], 0.05)
for r, adj, rej in zip(st, h.adjusted, h.reject): r["holm"] = float(adj); r["rej"] = bool(rej)
print(f"{lib}: {len(recs)} cells, {len(st)} statistical, Holm over {len(st)}")
for row in dict.fromkeys(r["row"] for r in recs):
    rr = [r for r in recs if r["row"] == row]
    print(f"--- {row}: rejected {sum(r.get('rej',False) for r in rr)}/{sum(r['p_value'] is not None for r in rr)}; k>n cells flagged {sum(r['p_value'] is None and r['status']!='PASS' for r in rr)}/{sum(r['p_value'] is None for r in rr)}")
    for r in rr:
        se = ""
        print(f"  n={r['n']:<5} a={r['alpha']:<5} k={r['k']:<5} R={r['reps']} cov {r['coverage']:.4f} exact {r['target']:.4f} diff {r['coverage']-r['target']:+.4f} holm {r.get('holm',float('nan')):.2g} {'REJ' if r.get('rej') else ''} {r['status']} {r['detail']} off={r['offsets']}")
