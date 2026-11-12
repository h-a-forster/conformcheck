import numpy as np, pandas as pd, warnings
from sktime.forecasting.conformal import ConformalIntervals
from sktime.forecasting.dummy import ForecastKnownValues
ALPHAS = (0.05, 0.1, 0.2)
NS = (5, 9, 19, 49, 99)
REF_N = NS
_cache = {}
W = 3
def make(method):
    def fn(xc, yc, xt, a, model):
        r = yc - model.predict(xc); n = len(r); key = (method, r.tobytes())
        if key not in _cache:
            _cache.clear()
            # y[:W] is the initial window of a fixed 0 forecaster; for fh=1 the library uses the
            # diagonal offset=1 of its residual matrix, i.e. y[W+1:]: put the n residuals there.
            y = pd.Series(np.concatenate([np.zeros(W + 1), r]))
            known = pd.Series(np.zeros(len(y) + 5), index=pd.RangeIndex(len(y) + 5))
            f = ConformalIntervals(ForecastKnownValues(known), method=method, initial_window=W)
            f.fit(y, fh=[1])
            assert np.isclose(f.residuals_matrix_.shape[0], n + 1)
            pi = f.predict_interval(coverage=[0.8, 0.9, 0.95])
            d = {}
            for c in (0.8, 0.9, 0.95):
                d[c] = (float(pi.iloc[0][(pi.columns.levels[0][0], c, "lower")]), float(pi.iloc[0][(pi.columns.levels[0][0], c, "upper")]))
            _cache[key] = d
        lo, hi = _cache[key][round(1 - a, 2)]
        p = model.predict(xt); return np.column_stack([p + lo, p + hi])
    return fn
ROWS = {"sktime/conformal": dict(fn=make("conformal"), n=NS, alpha=ALPHAS, reps=200),
        "sktime/conformal_bonferroni": dict(fn=make("conformal_bonferroni"), n=(9, 19, 99), alpha=(0.1,), reps=50),
        "sktime/empirical": dict(fn=make("empirical"), n=(9, 19, 99), alpha=ALPHAS, reps=50),
        "sktime/empirical_residual": dict(fn=make("empirical_residual"), n=(9, 19, 99), alpha=ALPHAS, reps=50)}
