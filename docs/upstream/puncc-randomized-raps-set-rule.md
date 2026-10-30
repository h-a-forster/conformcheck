# puncc: randomized RAPS set rule does not match the RAPS score

**Title:** `raps_set(rand=True)` removes the boundary label with probability
`excess / (p_L + lambd)`, which does not match `raps_score`, so RAPS over-covers

**Template:** Bug report. Module: `api.prediction_sets`, `classification.RAPS`.

---

**Current Behavior**

Split conformal prediction is exact when a label is in the set if and only if its score
is at most the calibration quantile `tau`. puncc's randomized RAPS breaks this link.
`raps_score(rand=True)` randomizes only the probability term:
`E + lambd * reg_term - u * p_at_l`. `raps_set(rand=True)` removes the last candidate
label with probability `proba_excess / (proba_at_l + lambd * 1[L > k_reg])`. Whenever
the boundary label is ranked beyond `k_reg`, the extra `lambd` in the denominator makes
removal less likely than the score implies, so labels enter the set more often than
`score <= tau` allows.

The script below calls the two public functions with one probability vector and
`tau = 0.95`. Label 2 is in `raps_set` 40.1% of the time, while `raps_score(label 2) <=
tau` never holds: its score lies in [0.95, 1.10] and equals 0.95 only at `u = 1`.

In a simulation study (four Gaussian classes, `lambd = 0.1`, `k_reg = 1`, 200
calibration draws per setting) `RAPS(rand=True)` covered 0.990 at a 0.900 target with an
anti-informative classifier (top-1 accuracy 0.12) and 0.917 with the Bayes classifier.
`APS(rand=True)` (`lambd = 0`, where the two rules agree) matched the target in every
setting.

**Expected Behavior**

A label is in the randomized set exactly when its randomized score is at most `tau`.
Dividing by `proba_at_l` alone does this for the current score; it is also what the RAPS
authors' reference code does (github.com/aangelopoulos/conformal_classification,
`conformal.py`, function `gcq`). Alternatively, randomize the regularization term in the
score as well.

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
from deel.puncc.api.nonconformity_scores import raps_score
from deel.puncc.api.prediction_sets import raps_set

LAMBD, K_REG = 0.1, 1
p = np.array([0.45, 0.30, 0.15, 0.10])
tau = 0.95  # between the regularized cumulative masses of ranks 2 (0.85) and 3 (1.10)
reps = 200_000

np.random.seed(0)
probs = np.repeat(p[None, :], reps, axis=0)
in_set = np.zeros(4)
for s in raps_set(probs, tau, lambd=LAMBD, k_reg=K_REG, rand=True)[0]:
    in_set[list(s)] += 1
in_set /= reps

for label in range(4):
    scores = raps_score(probs, np.full(reps, label), lambd=LAMBD, k_reg=K_REG, rand=True)
    print(
        f"label {label} (p={p[label]:.2f}): in raps_set {in_set[label]:.4f}, "
        f"raps_score <= tau {np.mean(np.asarray(scores) <= tau):.4f}"
    )
```

**Relevant log output**

```text
label 0 (p=0.45): in raps_set 1.0000, raps_score <= tau 1.0000
label 1 (p=0.30): in raps_set 1.0000, raps_score <= tau 1.0000
label 2 (p=0.15): in raps_set 0.4013, raps_score <= tau 0.0000
label 3 (p=0.10): in raps_set 0.0000, raps_score <= tau 0.0000
```

Found with conformcheck (https://github.com/h-a-forster/conformcheck); details in its
REPORT.md, finding F10.
