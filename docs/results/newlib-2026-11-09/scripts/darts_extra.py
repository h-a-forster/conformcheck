"""darts ConformalNaiveModel: deterministic rank scan on (n, alpha); asymmetric mode; two-step horizon. Fixed 0 forecaster. Run: <venv python> -I darts_extra.py"""
import sys, math, logging, warnings, time, json, os
from fractions import Fraction
warnings.filterwarnings("ignore"); logging.disable(logging.WARNING)
import numpy as np
from scipy.stats import beta
from darts import TimeSeries
from darts.models import ConformalNaiveModel, SKLearnModel
from sklearn.dummy import DummyRegressor
fit = SKLearnModel(lags=1, model=DummyRegressor(strategy="constant", constant=0.0)).fit(TimeSeries.from_values(np.zeros(10)))
def cp(k, n): return beta.ppf(.025, k, n-k+1), beta.ppf(.975, k+1, n-k)
def bounds(r, a, sym, cal=True, h=1):
    ql, qh = a / 2, 1 - a / 2
    m = ConformalNaiveModel(fit, quantiles=[ql, 0.5, qh], symmetric=sym, cal_length=len(r) if cal else None)
    pr = m.predict(n=h, series=TimeSeries.from_values(np.concatenate([[0.0], r])), predict_likelihood_parameters=True).values()
    return pr
rng = np.random.default_rng(20261109)
# 1. rank scan: symmetric. Exact k from exact decimal alpha; capped at n when k > n
bad = 0; tot = 0; offs = {}
alphas = ["0.01", "0.02", "0.025", "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.4", "0.5"]
t0 = time.time()
for n in list(range(1, 201)) + [249, 250, 299, 399, 499, 999, 1999]:
    for s in alphas:
        a = float(s); fa = Fraction(s); k = math.ceil((n + 1) * (1 - fa))
        r = rng.standard_normal(n); pr = bounds(r, a, True)
        q = pr[0, 2]; rs = np.sort(np.abs(r)); idx = int(np.argmin(np.abs(rs - q))) + 1
        assert abs(rs[idx - 1] - q) < 1e-9
        kk = min(k, n); tot += 1
        if idx != kk: bad += 1; offs[(n, s)] = (idx, kk)
print(f"rank scan symmetric: {tot} pairs, {bad} off from min(k,n), {time.time()-t0:.0f}s", dict(list(offs.items())[:20]))
# 2. rank scan asymmetric: per side k' = ceil((n+1)(1-a/2))
bad = 0; tot = 0; offs = {}
for n in list(range(1, 101)) + [199, 399, 999]:
    for s in alphas:
        a = float(s); fa = Fraction(s); k = math.ceil((n + 1) * (1 - fa / 2))
        r = rng.standard_normal(n); pr = bounds(r, a, False); lo, hi = pr[0, 0], pr[0, 2]
        up = np.sort(r); dn = np.sort(-r); iu = int(np.argmin(np.abs(up - hi))) + 1; il = int(np.argmin(np.abs(dn + lo))) + 1
        tot += 1
        if iu != min(k, n) or il != min(k, n): bad += 1; offs[(n, s)] = (il, iu, min(k, n))
print(f"rank scan asymmetric: {tot} pairs, {bad} off", dict(list(offs.items())[:20]))
# 3. asymmetric coverage, exact target 1 - 2 (n+1-k')/(n+1) for k' <= n
R, m = 200, 500
print("asymmetric coverage, 200 draws x 500 test points")
for n, s in ((19, "0.2"), (39, "0.1"), (99, "0.1"), (199, "0.05")):
    a = float(s); k = math.ceil((n + 1) * (1 - Fraction(s) / 2)); ex = 1 - 2 * (n + 1 - k) / (n + 1); c = []
    for rep in range(R):
        g = np.random.default_rng([20261109, n, rep]); r = g.standard_normal(n); t = g.standard_normal(m); pr = bounds(r, a, False)
        c.append(np.mean((pr[0, 0] <= t) & (t <= pr[0, 2])))
    c = np.array(c); se = c.std(ddof=1) / np.sqrt(R); print(f" n={n} a={s} k'={k} cov {c.mean():.4f} +- {1.96*se:.4f} exact {ex:.4f}")
# 4. k > n cap: exact coverage is n/(n+1)
print("k>n cap (symmetric), 2000 draws x 200 test points")
for n, s in ((4, "0.1"), (9, "0.05"), (18, "0.05")):
    c = []
    for rep in range(2000):
        g = np.random.default_rng([7, n, rep]); r = g.standard_normal(n); t = g.standard_normal(200); pr = bounds(r, float(s), True)
        c.append(np.mean((pr[0, 0] <= t) & (t <= pr[0, 2])))
    c = np.array(c); print(f" n={n} a={s} target {1-float(s):.2f} cov {c.mean():.4f} +- {1.96*c.std(ddof=1)/np.sqrt(2000):.4f}, n/(n+1)={n/(n+1):.4f}, finite interval returned, warnings none checked")
