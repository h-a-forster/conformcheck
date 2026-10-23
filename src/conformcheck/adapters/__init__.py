"""Adapters for the libraries under test, plus the reference and mutant controls.

Each library module imports its library lazily, so ``import conformcheck.adapters``
works without any optional dependency installed. The registry is filled in milestone M3
(see docs/DESIGN.md, section 9).
"""

from __future__ import annotations

from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)

__all__ = [
    "AlphaOutput",
    "ClassificationInput",
    "CrossRegressionInput",
    "MethodSpec",
    "RegressionInput",
]
