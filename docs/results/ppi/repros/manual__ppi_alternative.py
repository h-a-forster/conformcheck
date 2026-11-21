"""ppi_py: a one-sided PPI++ mean interval comes back two-sided.

``ppi_mean_ci(..., alternative="larger")`` with the default ``lam=None`` tunes lambda and
then calls itself without passing ``alternative`` on, so the result is the two-sided
interval (finite upper bound, lower bound at alpha / 2 instead of alpha). With ``lam``
given, the one-sided interval is correct. ``ppi_mean_pval`` passes ``alternative`` on.

Needs numpy and ppi-python only. Exits 1 while the problem reproduces, 0 when fixed.
"""

import sys
from importlib.metadata import version

import numpy as np
from ppi_py import ppi_mean_ci

print("ppi-python", version("ppi-python"), "numpy", np.__version__)
rng = np.random.default_rng(0)
n, big_n = 200, 10000
y = (rng.random(n) < 0.3).astype(float)
yhat = np.where(rng.random(n) < 0.9, y, 1 - y)
yhat_unlabeled = (rng.random(big_n) < 0.34).astype(float)

two = ppi_mean_ci(y, yhat, yhat_unlabeled, alpha=0.1)
larger = ppi_mean_ci(y, yhat, yhat_unlabeled, alpha=0.1, alternative="larger")
fixed_lam = ppi_mean_ci(y, yhat, yhat_unlabeled, alpha=0.1, lam=1, alternative="larger")
print("lam=None, two-sided:       ", np.ravel(two[0]), np.ravel(two[1]))
print("lam=None, alternative=larger:", np.ravel(larger[0]), np.ravel(larger[1]))
print("lam=1,    alternative=larger:", np.ravel(fixed_lam[0]), np.ravel(fixed_lam[1]))
bug = np.all(np.isfinite(np.ravel(larger[1]))) and np.allclose(
    np.ravel(larger[0]), np.ravel(two[0])
)
print("REPRODUCES: the one-sided request returned the two-sided interval" if bug else "fixed")
sys.exit(1 if bug else 0)
