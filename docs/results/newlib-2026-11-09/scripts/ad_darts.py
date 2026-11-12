import numpy as np, logging
logging.disable(logging.WARNING)
from darts import TimeSeries
from darts.models import ConformalNaiveModel, SKLearnModel
from sklearn.dummy import DummyRegressor
ALPHAS = (0.05, 0.1, 0.2)
NS = (5, 9, 10, 19, 20, 49, 50, 99, 100, 999)
REF_N = (5, 9, 19, 49, 99)
_cache = {}
_fit = SKLearnModel(lags=1, model=DummyRegressor(strategy="constant", constant=0.0)).fit(TimeSeries.from_values(np.zeros(10)))
QS = {0.05: (0.025, 0.975), 0.1: (0.05, 0.95), 0.2: (0.1, 0.9)}
def make(symmetric, cal_length_mode):
    def fn(xc, yc, xt, a, model):
        r = yc - model.predict(xc); n = len(r); key = (symmetric, cal_length_mode, r.tobytes())
        if key not in _cache:
            _cache.clear()
            q = sorted({0.5, *[x for v in QS.values() for x in v]})
            m = ConformalNaiveModel(_fit, quantiles=q, symmetric=symmetric, cal_length=(n if cal_length_mode else None))
            # one lag precedes the first calibration forecast
            s = TimeSeries.from_values(np.concatenate([[0.0], r]))
            pr = m.predict(n=1, series=s, predict_likelihood_parameters=True)
            vals = dict(zip(pr.components, pr.values()[0]))
            d = {}
            for al, (ql, qh) in QS.items():
                lo = [v for c, v in vals.items() if c.endswith(f"_q{ql:.3f}") or c.endswith(f"_q{ql}")]
                hi = [v for c, v in vals.items() if c.endswith(f"_q{qh:.3f}") or c.endswith(f"_q{qh}")]
                assert len(lo) == 1 and len(hi) == 1, (list(vals), ql, qh)
                d[al] = (float(lo[0]), float(hi[0]))
            _cache[key] = d
        lo, hi = _cache[key][a]
        p = model.predict(xt); return np.column_stack([p + lo, p + hi])
    return fn
ROWS = {"darts/naive_sym_cal_length": dict(fn=make(True, True), n=NS, alpha=ALPHAS, score="abs"),
        "darts/naive_sym_all": dict(fn=make(True, False), n=(9, 19, 99), alpha=ALPHAS, score="abs")}
