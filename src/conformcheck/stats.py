"""Statistical tests of observed covered counts against an exact law.

Per cell the runner records ``S_1..S_R``, the covered counts in ``R`` independent
repetitions with ``m`` test points each. Planned functions (milestone M1,
docs/DESIGN.md section 3.4):

* ``mean_test(counts, law)``: exact two-sided p-value of ``T = sum S_r`` against the
  ``R``-fold convolution of the law's pmf (FFT), with a normal approximation using the
  exact variance as a cross-check. ``kind="mean"`` laws use the exact mean and the
  empirical variance (t-test).
* ``gof_test(counts, law)``: Pearson chi-square of the histogram of ``S_r`` against the
  pmf, bins merged from both tails until every expected count is at least 5.
* ``lower_bound_test(counts, m, bound)``: one-sided t-test of mean coverage against a
  guaranteed lower bound (jackknife+ and CV+ with non-degenerate models).
* ``cell_pvalue = min(1, 2 min(p_mean, p_gof))`` (Bonferroni within the cell).
* ``holm(pvalues)`` and ``benjamini_yekutieli(pvalues)`` across cells.
"""

from __future__ import annotations
