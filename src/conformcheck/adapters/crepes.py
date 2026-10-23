"""crepes (henrikbostrom/crepes, BSD-3-Clause).

Methods: ``WrapRegressor.calibrate`` / ``predict_int`` (split absolute residual) and
``WrapClassifier.calibrate`` / ``predict_set`` with the default hinge score (= LAC),
``smoothing`` False and True, ``class_cond`` False (method ``lac``) and True (method
``class_conditional``). Levels are passed as ``confidence=0.9``. See docs/DESIGN.md,
section 5.2.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck.adapters._common import (
    LibraryAdapter,
    confidence_value,
    guarded,
)
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    MethodSpec,
    RegressionInput,
)


class _Crepes(LibraryAdapter):
    module = "crepes"
    dist = "crepes"


class CrepesSplitAbs(_Crepes):
    spec = MethodSpec("crepes", "split_abs", "default", "regression")

    def run(self, data: RegressionInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        from crepes import WrapRegressor

        holder: dict[str, object] = {}

        def calibrate() -> AlphaOutput:
            w = WrapRegressor(data.model)
            w.calibrate(data.x_cal, data.y_cal)
            holder["w"] = w
            return AlphaOutput()

        cal = guarded(calibrate, data, data.alphas[0])
        out: dict[Fraction, AlphaOutput] = {}
        w = holder.get("w")
        for a in data.alphas:
            if cal.status != "ok":
                out[a] = AlphaOutput(status="error", message=cal.message)
                continue
            out[a] = guarded(
                lambda a=a: AlphaOutput(
                    intervals=np.asarray(
                        w.predict_int(data.x_test, confidence=confidence_value(a)),  # type: ignore[attr-defined]
                        dtype=float,
                    )
                ),
                data,
                a,
            )
        return out


class CrepesClassifier(_Crepes):
    def __init__(self, smoothing: bool, class_cond: bool) -> None:
        self.smoothing = smoothing
        self.class_cond = class_cond
        method = "class_conditional" if class_cond else "lac"
        variant = "smoothed" if smoothing else "unsmoothed"
        law = "smoothed" if smoothing else ("class_conditional" if class_cond else "split")
        self.spec = MethodSpec("crepes", method, variant, "classification", law=law)

    def run(self, data: ClassificationInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        from crepes import WrapClassifier

        holder: dict[str, object] = {}

        def calibrate() -> AlphaOutput:
            w = WrapClassifier(data.model)
            w.calibrate(data.x_cal, data.y_cal, class_cond=self.class_cond)
            holder["w"] = w
            return AlphaOutput()

        cal = guarded(calibrate, data, data.alphas[0])
        out: dict[Fraction, AlphaOutput] = {}
        w = holder.get("w")
        for a in data.alphas:
            if cal.status != "ok":
                out[a] = AlphaOutput(status="error", message=cal.message)
                continue

            def predict(a: Fraction = a) -> AlphaOutput:
                sets = w.predict_set(  # type: ignore[attr-defined]
                    data.x_test,
                    labels=False,
                    confidence=confidence_value(a),
                    smoothing=self.smoothing,
                    seed=data.seed,
                )
                return AlphaOutput(sets=np.asarray(sets).astype(bool))

            out[a] = guarded(predict, data, a)
        return out


def adapters() -> list[LibraryAdapter]:
    return [
        CrepesSplitAbs(),
        CrepesClassifier(smoothing=False, class_cond=False),
        CrepesClassifier(smoothing=True, class_cond=False),
        CrepesClassifier(smoothing=False, class_cond=True),
        CrepesClassifier(smoothing=True, class_cond=True),
    ]
