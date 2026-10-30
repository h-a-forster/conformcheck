# MAPIE: `RAPSConformityScore(size_raps=...)` is ignored by `SplitConformalClassifier`

**Title:** `SplitConformalClassifier` ignores and resets `RAPSConformityScore.size_raps`

**Template:** Bug report. Labels: bug.

---

**Describe the bug**

`RAPSConformityScore` documents `size_raps` (default 0.2) as the share of the
conformalization data used to choose lambda and k_reg. `SplitConformalClassifier`
ignores it: `_MapieClassifier.fit` calls `cs_estimator.set_external_attributes(...)`
without `size_raps` (`mapie/classification.py`, around line 898), and
`RAPSConformityScore.set_external_attributes` then sets `self.size_raps = None` (its
default argument). `split_data` passes `test_size=None` to `StratifiedShuffleSplit`,
which uses scikit-learn's default share of 0.1. The user's score object is modified too:
`size_raps` reads `None` after `conformalize`.

**To Reproduce**

```python
import math
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

for requested in (0.2, 0.5):
    score = RAPSConformityScore(size_raps=requested)
    clf = SplitConformalClassifier(
        model, confidence_level=0.9, conformity_score=score, prefit=True, random_state=1
    )
    clf.conformalize(x_cal, y_cal)
    print(
        f"size_raps={requested}: held out {n - score.n_samples_} of {n} points "
        f"(expected {math.ceil(requested * n)}); size_raps after conformalize: {score.size_raps!r}"
    )
```

Output:

```text
mapie 1.6.0 numpy 2.5.4 scikit-learn 1.9.1
size_raps=0.2: held out 10 of 100 points (expected 20); size_raps after conformalize: None
size_raps=0.5: held out 10 of 100 points (expected 50); size_raps after conformalize: None
```

MAPIE 1.5.0 gives the same output.

**Expected behavior**

The hold-out share is the `size_raps` the user passed (or the documented default 0.2),
and the user's object keeps it.

**Consequences seen in a simulation study** (4 and 10 classes, 200 calibration draws per
setting)

- In every repetition MAPIE calibrated on exactly `n - ceil(0.1 n)` points. The
  randomized sets match the exact split-conformal coverage at that size, so the sets are
  valid; only the split differs from the documentation.
- With 4 classes, `conformalize` raises at `n <= 20` in every repetition, with
  scikit-learn messages that do not mention RAPS, for example "The test_size = 2 should
  be greater or equal to the number of classes = 4" or "The least populated classes in y
  have only 1 member". With the 10 digits classes it raises at `n <= 50`.
- The level check runs on the hold-out size, so feasible levels are refused: with
  `n = 100` and `confidence_level=0.95`, MAPIE raises "Number of samples of the score is
  too low, 1/confidence_level and 1/(1 - confidence_level) must be lower than the number
  of samples", although 90 calibration points are enough for that level.

**Possible fix**

Pass the score's own `size_raps` through (or have `set_external_attributes` keep the
current value when none is given). A clearer error when the hold-out is smaller than the
number of classes would also help.

**Environment**

- OS: Windows 11
- Python 3.13, numpy 2.5.4, scikit-learn 1.9.1
- MAPIE 1.6.0 and 1.5.0

**Additional context**

Found with conformcheck (https://github.com/h-a-forster/conformcheck); details in its
REPORT.md, finding F9.
