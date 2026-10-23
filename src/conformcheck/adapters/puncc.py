"""puncc (deel-ai/puncc, MIT).

Methods: SplitCP, CQR, CVPlus (K folds; K = n for jackknife+), LAC, APS (``rand`` False
and True) and ClasswiseLAC. Levels are passed as ``alpha=0.1``. puncc draws its
randomization from the global ``numpy.random`` state, which the adapter seeds per
repetition. puncc 0.9.3 pins numpy<2; this repository runs it under numpy 2 and
re-checks every puncc finding under numpy<2 (docs/DESIGN.md, section 5.3).
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck.adapters._common import (
    LibraryAdapter,
    alpha_value,
    guarded,
    interval,
    labels_to_matrix,
)
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)


class _Puncc(LibraryAdapter):
    module = "deel.puncc"
    dist = "puncc"


def _proba_predictor(model: object):
    from deel.puncc.api.prediction import BasePredictor

    class ProbaPredictor(BasePredictor):
        """puncc's documented pattern for classifiers: ``predict`` returns probabilities."""

        def predict(self, X, **kwargs):  # type: ignore[no-untyped-def]
            return self.model.predict_proba(X)

    return ProbaPredictor(model, is_trained=True)


class _Fitted(_Puncc):
    """Fit once per repetition, then ``predict(X, alpha=...)`` for every alpha."""

    def build(self, data):  # type: ignore[no-untyped-def]  # pragma: no cover
        raise NotImplementedError

    def to_output(self, pred, data) -> AlphaOutput:  # type: ignore[no-untyped-def]
        raise NotImplementedError  # pragma: no cover

    def run(self, data):  # type: ignore[no-untyped-def, override]
        holder: dict[str, object] = {}

        def fit() -> AlphaOutput:
            np.random.seed(data.seed)
            holder["cp"] = self.build(data)
            return AlphaOutput()

        fitted = guarded(fit, data, data.alphas[0])
        out: dict[Fraction, AlphaOutput] = {}
        cp = holder.get("cp")
        for a in data.alphas:
            if fitted.status != "ok":
                out[a] = AlphaOutput(status="error", message=fitted.message)
                continue
            out[a] = guarded(
                lambda a=a: self.to_output(cp.predict(data.x_test, alpha=alpha_value(a)), data),  # type: ignore[attr-defined]
                data,
                a,
            )
        return out


class PunccSplitAbs(_Fitted):
    spec = MethodSpec("puncc", "split_abs", "default", "regression")

    def build(self, data: RegressionInput):  # type: ignore[no-untyped-def]
        from deel.puncc.api.prediction import BasePredictor
        from deel.puncc.regression import SplitCP

        cp = SplitCP(BasePredictor(data.model, is_trained=True), train=False)
        cp.fit(X_calib=data.x_cal, y_calib=data.y_cal)
        return cp

    def to_output(self, pred, data) -> AlphaOutput:  # type: ignore[no-untyped-def]
        _, lo, hi = pred
        return AlphaOutput(intervals=interval(lo, hi))


class PunccCQR(_Fitted):
    spec = MethodSpec("puncc", "cqr", "default", "regression")

    def build(self, data: RegressionInput):  # type: ignore[no-untyped-def]
        from deel.puncc.api.prediction import DualPredictor
        from deel.puncc.regression import CQR

        assert data.quantile_models is not None
        lo, hi, _ = data.quantile_models
        cp = CQR(DualPredictor([lo, hi], is_trained=[True, True]), train=False)
        cp.fit(X_calib=data.x_cal, y_calib=data.y_cal)
        return cp

    def to_output(self, pred, data) -> AlphaOutput:  # type: ignore[no-untyped-def]
        _, lo, hi = pred
        return AlphaOutput(intervals=interval(lo, hi))


class PunccCVPlus(_Fitted):
    """CVPlus with K folds; ``n_folds=None`` means K = n (leave-one-out, jackknife+)."""

    def __init__(self, n_folds: int | None) -> None:
        self.n_folds = n_folds
        if n_folds is None:
            self.spec = MethodSpec(
                "puncc", "jackknife_plus", "K=n", "cross_regression", law="cross"
            )
        else:
            self.spec = MethodSpec(
                "puncc", "cv_plus", f"K={n_folds}", "cross_regression", law="cross"
            )

    def build(self, data: CrossRegressionInput):  # type: ignore[no-untyped-def]
        from deel.puncc.api.prediction import BasePredictor
        from deel.puncc.regression import CVPlus

        k = len(data.y) if self.n_folds is None else self.n_folds
        cp = CVPlus(BasePredictor(data.estimator_factory()), K=k, random_state=data.seed)
        cp.fit(X=data.x, y=data.y)
        return cp

    def to_output(self, pred, data) -> AlphaOutput:  # type: ignore[no-untyped-def]
        _, lo, hi = pred
        return AlphaOutput(intervals=interval(lo, hi))


class PunccClassifier(_Fitted):
    def __init__(self, method: str, rand: bool | None = None) -> None:
        self.method = method
        self.rand = rand
        variant = f"rand={rand}" if method == "aps" else "default"
        name = "class_conditional" if method == "classwise_lac" else method
        law = "class_conditional" if method == "classwise_lac" else "split"
        self.spec = MethodSpec("puncc", name, variant, "classification", law=law)

    def build(self, data: ClassificationInput):  # type: ignore[no-untyped-def]
        from deel.puncc import classification as pc

        predictor = _proba_predictor(data.model)
        if self.method == "lac":
            cp = pc.LAC(predictor, train=False)
        elif self.method == "aps":
            cp = pc.APS(predictor, train=False, rand=bool(self.rand))
        elif self.method == "classwise_lac":
            cp = pc.ClasswiseLAC(predictor, train=False)
        else:  # pragma: no cover - defensive
            raise ValueError(self.method)
        cp.fit(X_calib=data.x_cal, y_calib=data.y_cal)
        return cp

    def to_output(self, pred, data: ClassificationInput) -> AlphaOutput:  # type: ignore[no-untyped-def, override]
        _, sets = pred
        return AlphaOutput(sets=labels_to_matrix(sets, data.n_classes))


def adapters() -> list[LibraryAdapter]:
    return [
        PunccSplitAbs(),
        PunccCQR(),
        PunccCVPlus(None),
        PunccCVPlus(5),
        PunccCVPlus(10),
        PunccClassifier("lac"),
        PunccClassifier("aps", rand=False),
        PunccClassifier("aps", rand=True),
        PunccClassifier("classwise_lac"),
    ]
