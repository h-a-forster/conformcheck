"""Shared plumbing for adapters: availability, versions, per-alpha error capture."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import warnings
from collections.abc import Callable
from fractions import Fraction

import numpy as np
from numpy.typing import NDArray

from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)

Input = RegressionInput | CrossRegressionInput | ClassificationInput

MAX_WARNINGS = 3
# Library deprecation notices are noise for a coverage audit.
IGNORED_WARNINGS = (DeprecationWarning, SyntaxWarning, PendingDeprecationWarning)


def alpha_value(alpha: Fraction) -> float:
    """The miscoverage level as a user types it: ``0.1`` for 1/10."""
    return float(alpha)


def confidence_value(alpha: Fraction) -> float:
    """The confidence level as a user types it: ``0.9`` for alpha = 1/10.

    This is the double nearest to the exact ``1 - alpha``, i.e. what typing the decimal
    literal gives; it is never computed as ``1 - 0.1`` in floating point.
    """
    return float(1 - alpha)


def calibration_size(data: Input) -> int:
    """Calibration size that decides whether ``k > n``; per class for Mondrian inputs."""
    if isinstance(data, CrossRegressionInput):
        return int(len(data.y))
    if isinstance(data, ClassificationInput) and data.per_class:
        counts = np.bincount(np.asarray(data.y_cal), minlength=data.n_classes)
        return int(counts.min())
    return int(len(data.y_cal))


REFUSAL_HINTS = ("too low", "too small", "alpha", "confidence", "number of samples")


def is_refusal(exc: BaseException) -> bool:
    """A ``ValueError`` whose message is about the level or the sample size."""
    return isinstance(exc, ValueError) and any(h in str(exc).lower() for h in REFUSAL_HINTS)


class LibraryAdapter:
    """Base class: subclasses set ``spec``, ``module``, ``dist`` and implement
    :meth:`run_alpha` (one alpha) or override :meth:`run` (all alphas in one call)."""

    spec: MethodSpec
    module: str = ""
    dist: str = ""
    n_folds: int | None = None  # cross methods: K, or None for leave-one-out

    def available(self) -> bool:
        try:
            return importlib.util.find_spec(self.module) is not None
        except (ImportError, ValueError):
            return False

    def library_version(self) -> str:
        try:
            return importlib.metadata.version(self.dist)
        except importlib.metadata.PackageNotFoundError:
            return "not installed"

    def setup(self) -> None:
        """Import-time preparation (e.g. torchcp import stubs). Called before each run."""

    def run_alpha(self, data: Input, alpha: Fraction) -> AlphaOutput:  # pragma: no cover
        raise NotImplementedError

    def run(self, data: Input) -> dict[Fraction, AlphaOutput]:
        self.setup()
        return {a: guarded(lambda a=a: self.run_alpha(data, a), data, a) for a in data.alphas}

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.spec.key}>"


def guarded(fn: Callable[[], AlphaOutput], data: Input, alpha: Fraction) -> AlphaOutput:
    """Run ``fn`` capturing warnings; turn exceptions into ``refused`` or ``error``.

    A ``ValueError`` about the level or the sample size is a deliberate refusal
    (``refused``); the report separates refusals where ``k > n`` (valid) from refusals of
    feasible levels. Anything else is an ``error``.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            out = fn()
        except Exception as exc:  # noqa: BLE001 - every library error must be recorded
            status = "refused" if is_refusal(exc) else "error"
            out = AlphaOutput(status=status, message=f"{type(exc).__name__}: {exc}"[:500])
    msgs: list[str] = []
    for w in caught:
        if issubclass(w.category, IGNORED_WARNINGS):
            continue
        text = f"{w.category.__name__}: {w.message}"[:200]
        if text not in msgs:
            msgs.append(text)
        if len(msgs) >= MAX_WARNINGS:
            break
    out.warnings = msgs + [m for m in out.warnings if m not in msgs]
    return out


def all_guarded(
    fn: Callable[[], dict[Fraction, AlphaOutput]], data: Input
) -> dict[Fraction, AlphaOutput]:
    """Like :func:`guarded` for adapters that evaluate every alpha in one call."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            outs = fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"[:500]
            status = "refused" if is_refusal(exc) else "error"
            outs = {a: AlphaOutput(status=status, message=msg) for a in data.alphas}
    msgs = list(
        dict.fromkeys(
            f"{w.category.__name__}: {w.message}"[:200]
            for w in caught
            if not issubclass(w.category, IGNORED_WARNINGS)
        )
    )
    for out in outs.values():
        out.warnings = msgs[:MAX_WARNINGS]
    return outs


def labels_to_matrix(sets: list, n_classes: int) -> NDArray[np.bool_]:
    """Convert a list of label lists (puncc) into a boolean ``(m, K)`` matrix."""
    out = np.zeros((len(sets), n_classes), dtype=bool)
    for i, s in enumerate(sets):
        idx = np.asarray(list(s), dtype=np.int64)
        if idx.size:
            out[i, idx] = True
    return out


def interval(lo: object, hi: object) -> NDArray[np.float64]:
    return np.column_stack([np.asarray(lo, dtype=float).ravel(), np.asarray(hi, float).ravel()])
