"""sktime 1.3.0 ConformalIntervals: confirm three open issues on the release. Run: <venv python> -I repro_sktime.py"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy.stats import beta
from sktime.forecasting.conformal import ConformalIntervals
from sktime.forecasting.naive import NaiveForecaster
def cp(k, n): return beta.ppf(.025, k, n-k+1), beta.ppf(.975, k+1, n-k)
rng = np.random.default_rng(11)
# horizon: random walk, Naive(last) is the optimal forecaster; h-step residual sd is sqrt(h). fh=1 at coverage 0.9
R, T = 300, 80; hit = {1: 0, 3: 0}; wid = {1: [], 3: []}
for rep in range(R):
    y = pd.Series(np.cumsum(rng.standard_normal(T + 3)))
    f = ConformalIntervals(NaiveForecaster(strategy="last"), method="conformal", initial_window=10)
    f.fit(y.iloc[:T], fh=[1, 3])
    pi = f.predict_interval(coverage=0.9)
    for pos, h in enumerate((1, 3)):
        lo, up = float(pi.iloc[pos, 0]), float(pi.iloc[pos, 1]); tv = y.iloc[T + h - 1]
        hit[h] += lo <= tv <= up; wid[h].append((up - lo) / 2)
for h in hit:
    l, u = cp(hit[h], R); print(f"random walk h={h}: coverage {hit[h]/R:.3f} [{l:.3f},{u:.3f}] at 0.90; half-width {np.mean(wid[h]):.3f}; sd ratio check 1.645*sqrt(h)={1.645*h**.5:.3f}, 1.645*sqrt(h+1)={1.645*(h+1)**.5:.3f}")
