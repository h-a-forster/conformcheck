"""puncc (deel-ai/puncc, MIT).

Methods: SplitCP, CQR, CVPlus (K folds; K = n for jackknife+), LAC, APS (rand False and
True), RAPS, ClasswiseLAC. puncc 0.9.3 pins numpy<2; this repository runs it under
numpy 2 and re-checks every puncc finding under numpy<2 (docs/DESIGN.md, section 5.3).
"""

from __future__ import annotations
