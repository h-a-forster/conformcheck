"""The adapter contract every library wrapper implements.

An adapter turns one library method (for example MAPIE ``SplitConformalRegressor`` with
the absolute residual score) into a pure function of arrays. The runner supplies the
same data, the same fixed models and the same seeds to every adapter, so results are
comparable across libraries (common random numbers). See docs/DESIGN.md, section 5.

Rules for adapters
------------------
* Call the library the way its documentation tells users to, through its public API.
  Pass levels the way a user would type them: ``alpha=0.1`` or ``confidence_level=0.9``,
  never a recomputed ``1 - 0.1``.
* Do not reimplement any part of the method. Scores may be computed by the adapter only
  when the library's API takes scores as input (and the docstring must say so).
* Fit once per repetition and evaluate every requested ``alpha`` from that fit when the
  library allows it.
* Never swallow an exception silently: a library error becomes ``status="error"`` with
  the message, a deliberate refusal (for example "calibration set too small") becomes
  ``status="refused"``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal, Protocol, runtime_checkable

import numpy as np
from numpy.typing import NDArray

Task = Literal["regression", "classification", "cross_regression"]

Status = Literal["ok", "refused", "error", "unsupported"]


@dataclass(frozen=True)
class MethodSpec:
    """Identity of one library-method-variant triple, the row key of the matrix."""

    library: str
    method: str  # e.g. "split_abs", "cqr", "jackknife_plus", "cv_plus", "lac", "aps", ...
    variant: str = "default"  # e.g. "randomized", "include_last_label=True", "smoothed"
    task: Task = "regression"
    law: str = "split"  # name of the coverage law the method promises (see laws.py)
    notes: str = ""

    @property
    def key(self) -> str:
        return f"{self.library}/{self.method}/{self.variant}"


@dataclass(frozen=True)
class RegressionInput:
    """One repetition of a split regression cell.

    ``model`` is a fitted scikit-learn compatible regressor (a fixed function, see
    :mod:`conformcheck.models`). For CQR, ``quantile_models`` holds fitted
    ``(lower, upper, median)`` regressors.
    """

    x_cal: NDArray[np.float64]
    y_cal: NDArray[np.float64]
    x_test: NDArray[np.float64]
    alphas: Sequence[Fraction]
    model: object
    quantile_models: tuple[object, object, object] | None = None
    seed: int = 0


@dataclass(frozen=True)
class CrossRegressionInput:
    """One repetition of a jackknife+ or CV+ cell: the adapter fits ``estimator_factory()``."""

    x: NDArray[np.float64]
    y: NDArray[np.float64]
    x_test: NDArray[np.float64]
    alphas: Sequence[Fraction]
    estimator_factory: Callable[[], object]
    n_folds: int | None  # None means leave-one-out (jackknife+)
    seed: int = 0


@dataclass(frozen=True)
class ClassificationInput:
    """One repetition of a split classification cell.

    ``model`` is a fitted classifier with ``predict_proba``; ``proba_cal`` and
    ``proba_test`` are its outputs, provided for libraries that take probabilities or
    logits instead of an estimator.
    """

    x_cal: NDArray[np.float64]
    y_cal: NDArray[np.int64]
    x_test: NDArray[np.float64]
    alphas: Sequence[Fraction]
    model: object
    proba_cal: NDArray[np.float64]
    proba_test: NDArray[np.float64]
    n_classes: int
    seed: int = 0


@dataclass
class AlphaOutput:
    """What an adapter returns for one ``alpha``.

    Regression: ``intervals`` of shape ``(m, 2)`` (``-inf``/``inf`` allowed).
    Classification: ``sets`` boolean of shape ``(m, n_classes)``.
    """

    status: Status = "ok"
    intervals: NDArray[np.float64] | None = None
    sets: NDArray[np.bool_] | None = None
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    effective_n: int | None = None  # set when the library uses fewer calibration points


@runtime_checkable
class Adapter(Protocol):
    """A library method under test."""

    spec: MethodSpec

    def available(self) -> bool:
        """True when the library can be imported in this environment."""
        ...

    def library_version(self) -> str: ...

    def run(
        self, data: RegressionInput | CrossRegressionInput | ClassificationInput
    ) -> dict[Fraction, AlphaOutput]:
        """Run one repetition and return one output per requested alpha."""
        ...
