"""Reference implementations of every method under test, and deliberately wrong mutants.

Written directly from the papers in numpy, one short function each, with no shared
"clever" code. They serve two purposes:

1. Differential oracle: on identical inputs a non-randomized library method should
   return the same interval or set as its reference (up to documented conventions).
2. Oracle self-test: the reference must PASS every statistical cell, and each mutant must
   be detected, which measures the size and power of the test layer.

Planned functions (milestone M2, docs/DESIGN.md section 4):

* ``split_abs(cal_scores, y_hat_test, alpha) -> (m, 2)``: threshold is the k-th smallest
  score, ``k = ceil((n+1)(1-alpha))``; ``inf`` when ``k > n``.
* ``cqr(lo_cal, hi_cal, y_cal, lo_test, hi_test, alpha, symmetric=True)``: score
  ``max(lo - y, y - hi)``; the asymmetric variant uses ``alpha/2`` per side.
* ``lac(proba_cal, y_cal, proba_test, alpha)``: score ``1 - p_y``.
* ``aps(proba_cal, y_cal, proba_test, alpha, randomized, rng)``: score is the cumulative
  mass of labels ranked at or above ``y`` (minus ``U * p_y`` when randomized), Romano,
  Sesia and Candes (2020).
* ``raps(..., lam, k_reg)``: APS plus ``lam * max(0, rank - k_reg)``, Angelopoulos et al.
  (2021).
* ``class_conditional_lac(...)``: per-class thresholds with per-class ``n_y``.
* ``smoothed_lac(...)``: smoothed p-values ``(#{s_i > s} + U (#{s_i = s} + 1)) / (n + 1)``,
  set ``{y : p_y > alpha}`` (Vovk et al. 2005).
* ``jackknife_plus`` and ``cv_plus``: Barber et al. (2021), with ``q^+`` the
  ``ceil((1-alpha)(n+1))``-th and ``q^-`` the ``floor(alpha(n+1))``-th smallest value
  (``-inf`` when that index is 0, ``+inf`` when the upper index exceeds n).

Mutants: ``k - 1``, ``k + 1``, ``np.quantile(scores, 1 - alpha)`` (no finite-sample
correction, linear interpolation), and ``ceil(n (1 - alpha))``.
"""

from __future__ import annotations
