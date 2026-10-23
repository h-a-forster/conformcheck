"""conformcheck: finite-sample coverage certification for conformal-prediction libraries.

The oracle layer (:mod:`conformcheck.laws`, :mod:`conformcheck.stats`) needs only numpy and
scipy. Adapters for the libraries under test live in :mod:`conformcheck.adapters` and
import their library lazily.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
