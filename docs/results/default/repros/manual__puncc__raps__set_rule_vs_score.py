"""puncc 0.9.3: randomized RAPS prediction sets do not match puncc's own RAPS score.

Split conformal is exact when a label is in the set if and only if its score is at most
the calibration quantile tau. This script takes one probability vector and one tau and
compares, over many uniforms, how often each label is in ``raps_set(...)`` with how often
``raps_score(...)`` of that label is at most tau. Both are public functions of
``deel.puncc.api``; ``RAPS(rand=True)`` uses them for calibration and prediction.

Standalone: numpy and puncc only. Exits 1 while the problem reproduces.
"""

import sys
import warnings
from importlib.metadata import version

warnings.filterwarnings("ignore", category=SyntaxWarning)  # puncc docstrings

import numpy as np
from deel.puncc.api.nonconformity_scores import raps_score
from deel.puncc.api.prediction_sets import raps_set

print("puncc", version("puncc"), "numpy", np.__version__)
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

score_rule = np.zeros(4)
for label in range(4):
    scores = raps_score(probs, np.full(reps, label), lambd=LAMBD, k_reg=K_REG, rand=True)
    score_rule[label] = np.mean(np.asarray(scores) <= tau)

se = np.sqrt(0.25 / reps)
print(f"tau = {tau}, lambda = {LAMBD}, k_reg = {K_REG}, p = {p.tolist()}")
for label in range(4):
    print(
        f"label {label} (p={p[label]:.2f}): in raps_set {in_set[label]:.4f}, "
        f"raps_score <= tau {score_rule[label]:.4f}"
    )
gap = np.max(np.abs(in_set - score_rule))
reproduced = gap > 10 * se
print(f"largest gap {gap:.4f} (Monte Carlo SE about {se:.4f})")
print("REPRODUCED" if reproduced else "not reproduced")
sys.exit(1 if reproduced else 0)
