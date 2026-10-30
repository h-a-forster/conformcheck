# puncc: APS and RAPS set size is capped at the number of test points

**Do not file: already reported in
[deel-ai/puncc#97](https://github.com/deel-ai/puncc/pull/97)** ("fix: cap raps set size
at the number of classes, not the number of samples", a pull request by another
contributor, opened 2026-10-07 and open on 2026-10-30). It covers the same
`L = b.minimum(..., pred_len)` line in `raps_set`, the same fix (cap at `n_classes`) and
the `IndexError`, with a test. conformcheck found the bug independently on 2026-10-30.
Below is an optional supporting comment for #97; it adds the effect through the public
`APS`/`RAPS` API.

---

**Comment for #97**

Independent confirmation on puncc 0.9.3 through the public `deel.puncc.classification`
API: predicting one point at a time, `APS(rand=False)` and `RAPS(rand=False)` return the
top label alone, and coverage falls to 0.610 against a 0.9 target (1.000 and 0.985 for
the same points predicted in one batch). With `rand=True` a single point gets at most the
top label. Reproduced on Windows 11 with Python 3.13 and numpy 2.5.4, and with Python
3.12 and numpy 1.26.4 (puncc's declared `numpy<2`).

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

Found with conformcheck (https://github.com/h-a-forster/conformcheck); details in its
REPORT.md, finding F11.
