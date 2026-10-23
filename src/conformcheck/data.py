"""Data-generating processes with known exchangeability.

Every repetition draws fresh calibration and test data from a seed derived from
``(study seed, dgp, n, repetition)`` (``numpy.random.SeedSequence``), so all libraries see
identical data (common random numbers). Planned DGPs (milestone M2, docs/DESIGN.md
section 6):

* ``reg_gauss``: ``X ~ U[0,1]^2``, ``Y = 2 X_1 + N(0, 1)``; fixed model biased by +0.3;
  fixed quantile models for CQR deliberately miscalibrated.
* ``reg_hetero_t``: ``Y = sin(2 pi X_1) + (0.5 + X_1) t_3``; fixed model ``0.8 sin(2 pi x)``.
* ``reg_tied``: constant model 0, ``Y`` integer valued with a known pmf, so scores ``|Y|``
  tie and the exact discrete law applies.
* ``cls_gauss``: ``Y ~ Uniform{0..3}``, ``X | Y ~ N(mu_Y, I_2)``; fixed linear-softmax
  classifier at temperature 2 (miscalibrated). Stratified draws give exactly ``n_y``
  calibration points per class for class-conditional cells.
* ``diabetes`` and ``digits`` (bundled with scikit-learn, no download): one fixed
  training subset fits the model once; each repetition is a fresh random split of the
  remaining pool into calibration and test. Score ties are counted and reported.
"""

from __future__ import annotations
