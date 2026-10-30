# MAPIE: APS with `include_last_label=False` can under-cover

**Title:** APS with `include_last_label=False` under-covers: the calibration score is
randomized but the prediction rule is not

**Template:** Bug report. Labels: bug.

---

**Describe the bug**

With `SplitConformalClassifier(conformity_score="aps")` and
`predict_set(..., conformity_score_params={"include_last_label": False})`, the coverage
can fall well below `confidence_level`. With an ordinary fitted `LogisticRegression` on
four Gaussian classes and 1000 calibration points, a 0.9 target gives 0.783 coverage.
The docstring of `include_last_label` says that `True` and `False` "may result in
a coverage higher than `1 - alpha`", so users would expect the opposite.

`include_last_label=True` is conservative, as documented, and `"randomized"` matches the
target.

**To Reproduce**

```python
from importlib.metadata import version

import numpy as np
from mapie.classification import SplitConformalClassifier
from sklearn.linear_model import LogisticRegression

print("mapie", version("mapie"), "scikit-learn", version("scikit-learn"), "numpy", np.__version__)
rng = np.random.default_rng(0)
means = np.array([[0.0, 0.0], [1.5, 0.0], [0.0, 1.5], [1.5, 1.5]])


def draw(n):
    y = rng.integers(0, 4, n)
    return means[y] + rng.normal(size=(n, 2)), y


model = LogisticRegression().fit(*draw(5000))
x_test, y_test = draw(20_000)
print(f"top-1 accuracy {np.mean(model.predict(x_test) == y_test):.3f}")
for confidence in (0.8, 0.9, 0.95):
    cov = {False: [], True: [], "randomized": []}
    for rep in range(50):
        x_cal, y_cal = draw(1000)
        clf = SplitConformalClassifier(
            model,
            confidence_level=confidence,
            conformity_score="aps",
            prefit=True,
            random_state=rep,
        ).conformalize(x_cal, y_cal)
        for ill in cov:
            _, sets = clf.predict_set(x_test, conformity_score_params={"include_last_label": ill})
            cov[ill].append(sets[np.arange(len(y_test)), y_test, 0].mean())
    print(
        f"confidence_level={confidence}: "
        + ", ".join(f"include_last_label={k!r}: {np.mean(v):.3f}" for k, v in cov.items())
    )
```

Output (mean coverage over 50 calibration sets of 1000 points, 20,000 test points):

```text
mapie 1.6.0 scikit-learn 1.9.1 numpy 2.5.4
top-1 accuracy 0.598
confidence_level=0.8: include_last_label=False: 0.682, include_last_label=True: 0.897, include_last_label='randomized': 0.805
confidence_level=0.9: include_last_label=False: 0.783, include_last_label=True: 0.955, include_last_label='randomized': 0.901
confidence_level=0.95: include_last_label=False: 0.868, include_last_label=True: 0.984, include_last_label='randomized': 0.952
```

MAPIE 1.5.0 gives the same numbers.

**Expected behavior**

Coverage of at least `confidence_level` for `include_last_label=False`, or documentation
that says it can be lower.

**Cause**

The APS conformity score is always randomized at calibration
(`conformity_scores/sets/aps.py`, `get_conformity_scores`:
`conformity_scores -= u * y_proba_true`), whatever `include_last_label` is used later.
With `False`, the prediction rule is deterministic: it keeps the labels whose cumulative
probability is at most the quantile, plus the top label
(`conformity_scores/sets/utils.py`, `get_last_index_included`, `max_threshold`). The
randomized scores are smaller than the cumulative probability up to and including the
true label, so the quantile is too low for that rule, and the true label is dropped more
often than alpha allows. Always keeping the top label adds coverage back, so the net
effect depends on the model: we measured under-coverage on two synthetic models (0.55
and 0.79 at a 0.9 target) and over-coverage on the scikit-learn digits data (about 0.97),
where most sets are the top label alone.

**Possible fixes**

- For `include_last_label=False`, use the quantile of the non-randomized score (the
  cumulative probability up to and including the true label). A label is then in the set
  whenever its score is at most that quantile, which gives coverage of at least
  `1 - alpha`. Since `include_last_label` is chosen at prediction time, both quantiles
  would be computed in `conformalize`.
- Or document that `False` can give coverage below `1 - alpha`.

**Environment**

- OS: Windows 11
- Python 3.13, numpy 2.5.4, scikit-learn 1.9.1
- MAPIE 1.6.0 and 1.5.0

**Additional context**

#236 discussed the same setting and concluded that `True` and `False` over-cover, which
led to the current docstring. The example above shows that `False` can also under-cover.
Found with conformcheck (https://github.com/h-a-forster/conformcheck), which tests
conformal libraries against the exact finite-sample laws; details in its REPORT.md,
finding F1.
