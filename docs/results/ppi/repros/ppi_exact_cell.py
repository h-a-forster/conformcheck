"""Exact coverage of ppi_py's mean intervals in one cell, by full enumeration.

n = 20 human labels, base rate pi = 0.02, a judge with sensitivity = specificity = 0.9,
alpha = 0.1, and N = 10,000 judge labels whose mean is exactly the judge's expected rate
mu = pi acc + (1 - pi)(1 - acc). Every one of the C(23, 3) = 1771 labelled count vectors
is passed to the library one at a time, as a user would call it, and the multinomial
probabilities of the covering outcomes are summed exactly (fractions). Independent of
conformcheck: it checks the study's batched, pruned evaluation (DESIGN section 15).

Needs numpy and ppi-python only; about 15 s. Prints the coverage of PPI (lam=1), PPI++
(default lam=None) and the label-only Wald interval (classical_mean_ci). Exits 1 while a
PPI interval is below nominal by more than one point.
"""

import math
import sys
from fractions import Fraction
from importlib.metadata import version

import numpy as np
from ppi_py import classical_mean_ci, ppi_mean_ci

print("ppi-python", version("ppi-python"), "numpy", np.__version__)
n, big_n, alpha = 20, 10000, 0.1
pi, acc = Fraction("0.02"), Fraction("0.9")
probs = [pi * acc, pi * (1 - acc), (1 - pi) * (1 - acc), (1 - pi) * acc]  # (1,1) (1,0) (0,1) (0,0)
mu = pi * acc + (1 - pi) * (1 - acc)
unl = np.zeros(big_n)
unl[: int(mu * big_n)] = 1.0
cov = {"ppi": Fraction(0), "ppi++": Fraction(0), "wald": Fraction(0)}
total = Fraction(0)
for c11 in range(n + 1):
    for c10 in range(n + 1 - c11):
        for c01 in range(n + 1 - c11 - c10):
            c = (c11, c10, c01, n - c11 - c10 - c01)
            p = Fraction(math.factorial(n))
            for k, q in zip(c, probs):
                p = p / math.factorial(k) * q**k
            total += p
            y = np.array([1.0] * (c[0] + c[1]) + [0.0] * (c[2] + c[3]))
            yhat = np.array([1.0] * c[0] + [0.0] * c[1] + [1.0] * c[2] + [0.0] * c[3])
            for name, kw in (("ppi", {"lam": 1}), ("ppi++", {})):
                lo, hi = ppi_mean_ci(y, yhat, unl, alpha=alpha, **kw)
                if np.ravel(lo)[0] <= float(pi) <= np.ravel(hi)[0]:
                    cov[name] += p
            lo, hi = classical_mean_ci(y, alpha=alpha)
            if lo <= float(pi) <= hi:
                cov["wald"] += p
assert total == 1
for name, c in cov.items():
    print(f"{name:6s} exact coverage {float(c):.6f}  (nominal {1 - alpha})")
below = any(float(cov[m]) < 1 - alpha - 0.01 for m in ("ppi", "ppi++"))
print("REPRODUCES: below nominal by more than one point" if below else "not below nominal")
sys.exit(1 if below else 0)
