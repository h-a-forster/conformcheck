import numpy as np
from statsforecast.models import SklearnModel, HistoricAverage
from statsforecast.utils import ConformalIntervals
from sklearn.dummy import DummyRegressor
ALPHAS = (0.05, 0.1, 0.2)
NS = (2, 5, 9, 10, 19, 20, 49, 50, 99, 100, 999)
REF_N = (5, 9, 19, 49, 99)
_cache = {}
def make(method):
    def fn(xc, yc, xt, a, model):
        r = yc - model.predict(xc); n = len(r)
        key = (method, r.tobytes())
        if key not in _cache:
            _cache.clear()
            # the library sees [pad, r_1..r_n]: first value is the (unused) training window of a fixed 0 forecaster
            y = np.concatenate([[0.0], r])
            m = SklearnModel(DummyRegressor(strategy="constant", constant=0.0), prediction_intervals=ConformalIntervals(n_windows=n, h=1, method=method))
            out = m.forecast(y=y, h=1, X=np.zeros((n + 1, 1)), X_future=np.zeros((1, 1)), level=[80, 90, 95])
            _cache[key] = {lv: (float(out[f"lo-{lv}"][0]), float(out[f"hi-{lv}"][0])) for lv in (80, 90, 95)}
        lo, hi = _cache[key][round(100 * (1 - a))]
        p = model.predict(xt); return np.column_stack([p + lo, p + hi])
    return fn
ROWS = {f"statsforecast/{m}": dict(fn=make(m), n=NS, alpha=ALPHAS) for m in ("conformal_distribution", "conformal_error")}
