"""Hand-written repro (conformcheck default study). Needs numpy, scikit-learn and mapie.

MAPIE's SplitConformalRegressor.predict_interval(allow_infinite_bounds=True) is
documented as "If True, allows prediction intervals with infinite bounds". With n = 19
calibration points and confidence 0.96 (alpha = 0.04), k = ceil(20 * 0.96) = 20 > n, so
the only valid interval is (-inf, inf). The call still raises. This is a refusal, not an
invalid interval. Exits 1 while it raises, 0 if infinite bounds are returned.
"""

import sys
import warnings
from importlib.metadata import version

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin

warnings.simplefilter("ignore")


class FixedRegressor(RegressorMixin, BaseEstimator):
    def __init__(self):
        self.n_features_in_ = 2
        self.is_fitted_ = True

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return 2.0 * np.asarray(X, dtype=float)[:, 0]


from mapie.regression import SplitConformalRegressor  # noqa: E402

print(f"mapie {version('mapie')}, numpy {np.__version__}")
rng = np.random.default_rng(0)
x = rng.uniform(size=(22, 2))
y = 2.0 * x[:, 0] + rng.normal(size=22)
r = SplitConformalRegressor(FixedRegressor(), confidence_level=0.96, prefit=True)
try:
    r.conformalize(x[:19], y[:19])
    _, pis = r.predict_interval(x[19:], allow_infinite_bounds=True)
    print("returned", pis[:, :, 0].tolist())
    sys.exit(0)
except Exception as exc:
    print(f"raised {type(exc).__name__}: {exc}")
    print("REPRODUCED")
    sys.exit(1)
