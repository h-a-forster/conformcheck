# puncc: APS and RAPS set size is capped at the number of test points

**Title:** `raps_set` caps the set size at the number of test points instead of the
number of classes (one test point always gets a singleton set)

**Template:** Bug report. Module: `api.prediction_sets`, `classification.APS`,
`classification.RAPS`.

---

**Current Behavior**

In `deel/puncc/api/prediction_sets.py`, `raps_set` computes

```python
L = b.minimum(b.sum(below_tau, axis=-1) + 1, pred_len)
```

where `pred_len = shape[0]` is the number of test points in the call. The cap should be
the number of classes (`n_classes = shape[-1]`). `APS` and `RAPS` predict through this
function, with and without randomization, so:

- predicting a single point always returns the top label alone, whatever `alpha`;
  predicting fewer points than classes caps every set at that number of points;
- the same point gets a different set depending on how many other points are predicted
  with it;
- when every label is below `tau` and more points than classes are predicted,
  `L - 1 == n_classes` and the randomized branch raises
  `IndexError: index 4 is out of bounds for axis 1 with size 4`.

**Expected Behavior**

The set of a point does not depend on the batch it is predicted in, and sets can hold up
to all classes: `L = b.minimum(b.sum(below_tau, axis=-1) + 1, n_classes)`.

**Version**

puncc 0.9.3 (latest release on 2026-10-30)

**Environment**

Windows 11, Python 3.13 with numpy 2.5.4; also reproduced with Python 3.12 and numpy
1.26.4 (puncc's declared `numpy<2`).

**To Reproduce**

```python
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

import numpy as np
from deel.puncc.api.prediction import BasePredictor
from deel.puncc.classification import APS, RAPS
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(0)
means = np.array([[0.0, 0.0], [1.5, 0.0], [0.0, 1.5], [1.5, 1.5]])


def draw(n):
    y = rng.integers(0, 4, n)
    return means[y] + rng.normal(size=(n, 2)), y


class ProbaPredictor(BasePredictor):
    def predict(self, X, **kwargs):
        return self.model.predict_proba(X)


model = LogisticRegression().fit(*draw(5000))
x_cal, y_cal = draw(1000)
x_test, y_test = draw(200)
methods = {
    "APS(rand=False)": APS(ProbaPredictor(model, is_trained=True), train=False, rand=False),
    "RAPS(lambd=0.1, k_reg=1, rand=False)": RAPS(
        ProbaPredictor(model, is_trained=True), train=False, lambd=0.1, k_reg=1, rand=False
    ),
}
for name, cp in methods.items():
    cp.fit(X_calib=x_cal, y_calib=y_cal)
    batch = cp.predict(x_test, alpha=0.1)[1]
    single = [cp.predict(x_test[i : i + 1], alpha=0.1)[1][0] for i in range(len(x_test))]
    print(
        f"{name}: set sizes one point at a time {sorted({len(s) for s in single})}, "
        f"in one batch {sorted({len(s) for s in batch})}; coverage "
        f"{np.mean([y in s for y, s in zip(y_test, single)]):.3f} one at a time, "
        f"{np.mean([y in s for y, s in zip(y_test, batch)]):.3f} in one batch (target 0.9)"
    )
```

**Relevant log output**

```text
APS(rand=False): set sizes one point at a time [1], in one batch [2, 3, 4]; coverage 0.610 one at a time, 1.000 in one batch (target 0.9)
RAPS(lambd=0.1, k_reg=1, rand=False): set sizes one point at a time [1], in one batch [3, 4]; coverage 0.610 one at a time, 0.985 in one batch (target 0.9)
```

The `IndexError`: `raps_set(np.repeat([[0.45, 0.30, 0.15, 0.10]], 10, axis=0), 5.0,
lambd=0.1, k_reg=1, rand=True)`.

Found with conformcheck (https://github.com/h-a-forster/conformcheck); details in its
REPORT.md, finding F11.
