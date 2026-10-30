"""puncc 0.9.3: APS and RAPS prediction sets are capped at the number of test points.

``deel.puncc.api.prediction_sets.raps_set`` (used by ``APS`` and ``RAPS``, with and without
randomization) computes the set size as ``min(#{labels below tau} + 1, pred_len)``, where
``pred_len`` is the number of test points, not the number of classes. Predicting one test
point therefore returns at most the top label (the top label alone without randomization),
and the same point gets a different set depending on how many other points are predicted
with it. Already reported upstream in deel-ai/puncc pull request #97.

Standalone: numpy, scikit-learn and puncc only. Exits 1 while the problem reproduces.
"""

import sys
import warnings
from importlib.metadata import version

warnings.filterwarnings("ignore", category=SyntaxWarning)  # puncc docstrings

import numpy as np
from deel.puncc.api.prediction import BasePredictor
from deel.puncc.classification import APS, RAPS
from sklearn.linear_model import LogisticRegression

print("puncc", version("puncc"), "numpy", np.__version__, "scikit-learn", version("scikit-learn"))
rng = np.random.default_rng(0)
means = np.array([[0.0, 0.0], [1.5, 0.0], [0.0, 1.5], [1.5, 1.5]])


def draw(n):
    y = rng.integers(0, 4, n)
    return means[y] + rng.normal(size=(n, 2)), y


class ProbaPredictor(BasePredictor):
    """puncc's documented pattern for classifiers: ``predict`` returns probabilities."""

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
reproduced = False
for name, cp in methods.items():
    cp.fit(X_calib=x_cal, y_calib=y_cal)
    batch = cp.predict(x_test, alpha=0.1)[1]
    single = [cp.predict(x_test[i : i + 1], alpha=0.1)[1][0] for i in range(len(x_test))]
    same = sum(sorted(map(int, a)) == sorted(map(int, b)) for a, b in zip(batch, single))
    cov_batch = np.mean([y in s for y, s in zip(y_test, batch)])
    cov_single = np.mean([y in s for y, s in zip(y_test, single)])
    print(
        f"{name}: identical sets {same}/{len(x_test)}; set sizes one point at a time "
        f"{sorted({len(s) for s in single})}, in one batch {sorted({len(s) for s in batch})}; "
        f"coverage {cov_single:.3f} one at a time, {cov_batch:.3f} in one batch (target 0.9)"
    )
    reproduced |= same < len(x_test)
print("REPRODUCED" if reproduced else "not reproduced")
sys.exit(1 if reproduced else 0)
