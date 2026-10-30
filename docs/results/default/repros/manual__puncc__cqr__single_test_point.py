"""puncc 0.9.3: CQR raises for a single test point.

``DualPredictor.predict`` stacks the two quantile predictions into an ``(m, 2)`` array and
then squeezes it, so one test point gives shape ``(2,)``. ``cqr_interval`` requires a
2-D array with two columns and raises ``RuntimeError: Each Y_pred must contain lower and
higher quantiles predictions, respectively.`` The same points predicted two or more at a
time work. Found by conformcheck's batch-size invariance check (REPORT.md, F12).

Standalone: numpy, scikit-learn and puncc only. Exits 1 while the problem reproduces,
0 when it does not, 2 on any other error.
"""

import sys
import warnings
from importlib.metadata import version

warnings.filterwarnings("ignore", category=SyntaxWarning)  # puncc docstrings

import numpy as np
from deel.puncc.api.prediction import DualPredictor
from deel.puncc.regression import CQR
from sklearn.linear_model import QuantileRegressor

print("puncc", version("puncc"), "numpy", np.__version__, "scikit-learn", version("scikit-learn"))
rng = np.random.default_rng(0)
x = rng.normal(size=(300, 1))
y = x[:, 0] + rng.normal(size=300)
lo = QuantileRegressor(quantile=0.05, alpha=0.0).fit(x[:100], y[:100])
hi = QuantileRegressor(quantile=0.95, alpha=0.0).fit(x[:100], y[:100])
cp = CQR(DualPredictor([lo, hi], is_trained=[True, True]), train=False)
cp.fit(X_calib=x[100:200], y_calib=y[100:200])

try:
    _, y_lo, y_hi = cp.predict(x[200:202], alpha=0.1)
    print(f"two test points: intervals {np.round(np.c_[y_lo, y_hi], 3).tolist()}")
except Exception as exc:  # noqa: BLE001
    print(f"two test points raised {type(exc).__name__}: {exc}; unexpected")
    sys.exit(2)
try:
    _, y_lo, y_hi = cp.predict(x[200:201], alpha=0.1)
except RuntimeError as exc:
    print(f"one test point raised RuntimeError: {exc}")
    print("REPRODUCED")
    sys.exit(1)
except Exception as exc:  # noqa: BLE001
    print(f"one test point raised {type(exc).__name__}: {exc}; unexpected")
    sys.exit(2)
print(f"one test point: interval {np.round(np.c_[y_lo, y_hi], 3).tolist()}")
print("not reproduced")
sys.exit(0)
