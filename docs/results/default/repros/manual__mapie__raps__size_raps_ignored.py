"""MAPIE 1.6.0: SplitConformalClassifier ignores RAPSConformityScore(size_raps=...).

RAPSConformityScore documents ``size_raps`` (default 0.2) as the share of the
conformalization data held out to tune lambda and k_reg. SplitConformalClassifier calls
``set_external_attributes`` without ``size_raps``, which resets it to None, so
scikit-learn's StratifiedShuffleSplit default test share (0.1) is used instead.

Standalone: numpy, scikit-learn and mapie only. Exits 1 while the problem reproduces,
0 if the requested share is honoured.
"""

import math
import sys
from importlib.metadata import version

import numpy as np
from mapie.classification import SplitConformalClassifier
from mapie.conformity_scores import RAPSConformityScore
from sklearn.linear_model import LogisticRegression

print("mapie", version("mapie"), "numpy", np.__version__, "scikit-learn", version("scikit-learn"))
rng = np.random.default_rng(0)
means = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]])
y_fit = rng.integers(0, 4, 400)
model = LogisticRegression().fit(means[y_fit] + rng.normal(size=(400, 2)), y_fit)
n = 100
y_cal = rng.integers(0, 4, n)
x_cal = means[y_cal] + rng.normal(size=(n, 2))

reproduced = False
for requested in (0.2, 0.5):
    score = RAPSConformityScore(size_raps=requested)
    clf = SplitConformalClassifier(
        model, confidence_level=0.9, conformity_score=score, prefit=True, random_state=1
    )
    clf.conformalize(x_cal, y_cal)
    held_out = n - score.n_samples_
    expected = math.ceil(requested * n)
    print(
        f"size_raps={requested}: held out {held_out} of {n} points "
        f"(expected {expected}); size_raps after conformalize: {score.size_raps!r}"
    )
    reproduced |= held_out != expected
print("REPRODUCED" if reproduced else "not reproduced")
sys.exit(1 if reproduced else 0)
