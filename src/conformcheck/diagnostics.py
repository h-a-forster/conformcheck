"""Deterministic checks that need no hypothesis test.

Planned functions (milestone M3, docs/DESIGN.md section 3.3):

* ``recover_rank(cal_scores, threshold)``: for split regression and CQR the threshold is
  read off the returned interval (``(hi - lo) / 2`` for the absolute score), and the
  order statistic the library used is ``#{s_i <= threshold}`` (exact for distinct
  scores, with a relative tolerance of 1e-9, or float32 resolution for TorchCP). A value
  strictly between order statistics is reported as interpolation.
* ``bracket_rank(cal_scores, test_scores_all_labels, sets)``: for LAC and non-randomized
  APS the largest included and smallest excluded test score bracket the threshold.
* ``check_trivial(outputs)``: when ``k > n`` every interval must be infinite and every
  set full, unless the library refused with an error or warning.
* ``compare_to_reference(outputs, reference_outputs)``: maximum endpoint difference or
  set disagreement rate.
"""

from __future__ import annotations
