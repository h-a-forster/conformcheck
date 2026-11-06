# puncc: CQR raises for a single test point

**Title:** `CQR.predict` raises `RuntimeError` when `X_test` holds one point, because
`DualPredictor.predict` squeezes `(1, 2)` to `(2,)`

**Template:** Bug report. Module: `api.prediction`, `api.prediction_sets`,
`regression.CQR`.

---

**Current Behavior**

`CQR.predict` works for two or more test points and raises for one:
`RuntimeError: Each Y_pred must contain lower and higher quantiles predictions,
respectively.` `DualPredictor.predict` stacks the two quantile predictions into an
`(m, 2)` array and returns `b.squeeze(Y_pred)` (`deel/puncc/api/prediction.py`), so
`m = 1` gives shape `(2,)`. `cqr_interval` (`deel/puncc/api/prediction_sets.py`) requires
a 2-D array with two columns. A model served one point at a time cannot use CQR.

**Expected Behavior**

One test point gets one interval, as it does with `SplitCP`. Squeezing only a trailing
singleton axis, or not squeezing in `DualPredictor`, keeps the `(1, 2)` shape.

**To Reproduce**

```python
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

import numpy as np
from deel.puncc.api.prediction import DualPredictor
from deel.puncc.regression import CQR
from sklearn.linear_model import QuantileRegressor

rng = np.random.default_rng(0)
x = rng.normal(size=(300, 1))
y = x[:, 0] + rng.normal(size=300)
lo = QuantileRegressor(quantile=0.05, alpha=0.0).fit(x[:100], y[:100])
hi = QuantileRegressor(quantile=0.95, alpha=0.0).fit(x[:100], y[:100])
cp = CQR(DualPredictor([lo, hi], is_trained=[True, True]), train=False)
cp.fit(X_calib=x[100:200], y_calib=y[100:200])
print(cp.predict(x[200:202], alpha=0.1)[1:])  # works
print(cp.predict(x[200:201], alpha=0.1)[1:])  # RuntimeError
```

**Version**

puncc 0.9.3 (latest release on 2026-11-06)

**Environment**

Windows 11, Python 3.13 with numpy 2.5.4; also reproduced with Python 3.12 and numpy
1.26.4 (puncc's declared `numpy<2`).

**Relevant log output**

```text
two test points: intervals [[-2.196, 0.97], [-2.154, 1.02]]
one test point raised RuntimeError: Each Y_pred must contain lower and higher quantiles predictions, respectively.
```

Found with conformcheck (https://github.com/h-a-forster/conformcheck); details in its
REPORT.md, finding F12.
