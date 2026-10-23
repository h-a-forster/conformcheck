"""crepes (henrikbostrom/crepes, BSD-3-Clause).

Methods: WrapRegressor.calibrate/predict_int (split absolute residual) and
WrapClassifier.calibrate/predict_set with the hinge score (= LAC), smoothing False and
True, class_cond False and True. See docs/DESIGN.md, section 5.2.
"""

from __future__ import annotations
