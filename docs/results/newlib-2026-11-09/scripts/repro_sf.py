"""statsforecast standalone: 1-step coverage on iid N(0,1) with the tutorial's n_windows=2, via the public StatsForecast API.
Independent seed from the grid. Run: <venv python> -I repro_sf.py"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy.stats import beta
from statsforecast import StatsForecast
from statsforecast.models import HistoricAverage
from statsforecast.utils import ConformalIntervals
import statsforecast; print("statsforecast", statsforecast.__version__)
S, T = 20000, 200
rng = np.random.default_rng(7)
y = rng.standard_normal((S, T + 1))
df = pd.DataFrame({"unique_id": np.repeat(np.arange(S), T), "ds": np.tile(np.arange(T), S), "y": y[:, :T].ravel()})
def cp(k, n): return beta.ppf(.025, k, n-k+1), beta.ppf(.975, k+1, n-k)
for nw in (2, 5, 10, 20, 50):
    for method in ("conformal_distribution", "conformal_error"):
        sf = StatsForecast(models=[HistoricAverage(prediction_intervals=ConformalIntervals(h=1, n_windows=nw, method=method))], freq=1)
        out = sf.forecast(df=df, h=1, level=[80, 90])
        out = out.sort_values("unique_id")
        row = []
        for lv in (80, 90):
            c = ((out[f"HistoricAverage-lo-{lv}"].values <= y[:, T]) & (y[:, T] <= out[f"HistoricAverage-hi-{lv}"].values)).sum()
            l, u = cp(c, S); row.append(f"{lv}%: {c/S:.4f} [{l:.4f},{u:.4f}]")
        print(f"n_windows={nw:<3} {method:<23}", "  ".join(row), flush=True)
