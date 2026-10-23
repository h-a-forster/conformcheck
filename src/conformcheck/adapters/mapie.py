"""MAPIE (scikit-learn-contrib/MAPIE, BSD-3-Clause), v1 API.

Methods: SplitConformalRegressor (absolute), ConformalizedQuantileRegressor (prefit,
symmetric_correction False and True), CrossConformalRegressor (method="plus",
LeaveOneOut and KFold), SplitConformalClassifier (lac; aps with include_last_label
False, True and "randomized"; raps, which tunes lambda on an internal 20% split, so the
effective calibration size is reported). See docs/DESIGN.md, section 5.1.
"""

from __future__ import annotations
