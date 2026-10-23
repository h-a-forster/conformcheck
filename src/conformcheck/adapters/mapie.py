"""MAPIE (scikit-learn-contrib/MAPIE, BSD-3-Clause), v1 API.

Methods: SplitConformalRegressor (absolute; default and ``allow_infinite_bounds=True``),
ConformalizedQuantileRegressor (prefit, ``symmetric_correction`` False (default) and
True), CrossConformalRegressor (``method="plus"``, LeaveOneOut and KFold) and
SplitConformalClassifier (lac; aps with ``include_last_label`` False, True and
"randomized"; raps with ``include_last_label`` True (the default) and "randomized").
See docs/DESIGN.md, section 5.1.

RAPS: MAPIE holds out part of the conformalization data to tune lambda and k_reg
(``RAPSConformityScore.split_data``), so it calibrates on fewer points. The adapter passes
a ``RAPSConformityScore()`` instance (equivalent to ``conformity_score="raps"``) and
reports the calibration size MAPIE used, read from that object, as ``effective_n``.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck.adapters._common import (
    LibraryAdapter,
    all_guarded,
    confidence_value,
)
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)


class _Mapie(LibraryAdapter):
    module = "mapie"
    dist = "mapie"


class MapieSplitAbs(_Mapie):
    def __init__(self, allow_infinite_bounds: bool = False) -> None:
        self.allow_infinite_bounds = allow_infinite_bounds
        variant = "allow_infinite_bounds" if allow_infinite_bounds else "default"
        self.spec = MethodSpec("mapie", "split_abs", variant, "regression")

    def run_alpha(self, data: RegressionInput, alpha: Fraction) -> AlphaOutput:  # type: ignore[override]
        from mapie.regression import SplitConformalRegressor

        reg = SplitConformalRegressor(
            data.model,
            confidence_level=confidence_value(alpha),
            conformity_score="absolute",
            prefit=True,
        )
        reg.conformalize(data.x_cal, data.y_cal)
        _, pis = reg.predict_interval(data.x_test, allow_infinite_bounds=self.allow_infinite_bounds)
        return AlphaOutput(intervals=np.asarray(pis, dtype=float)[:, :, 0])


class MapieCQR(_Mapie):
    def __init__(self, symmetric: bool) -> None:
        self.symmetric = symmetric
        variant = "symmetric" if symmetric else "asymmetric"
        self.spec = MethodSpec(
            "mapie", "cqr", variant, "regression", law="split" if symmetric else "asymmetric_cqr"
        )

    def run_alpha(self, data: RegressionInput, alpha: Fraction) -> AlphaOutput:  # type: ignore[override]
        from mapie.regression import ConformalizedQuantileRegressor

        assert data.quantile_models is not None
        lo, hi, med = data.quantile_models
        reg = ConformalizedQuantileRegressor(
            [lo, hi, med], confidence_level=confidence_value(alpha), prefit=True
        )
        reg.conformalize(data.x_cal, data.y_cal)
        _, pis = reg.predict_interval(data.x_test, symmetric_correction=self.symmetric)
        return AlphaOutput(intervals=np.asarray(pis, dtype=float)[:, :, 0])


class MapieCrossPlus(_Mapie):
    """CrossConformalRegressor(method="plus"); all alphas from one fit."""

    def __init__(self, n_folds: int | None) -> None:
        self.n_folds = n_folds
        if n_folds is None:
            self.spec = MethodSpec(
                "mapie", "jackknife_plus", "default", "cross_regression", law="cross"
            )
        else:
            self.spec = MethodSpec(
                "mapie", "cv_plus", f"K={n_folds}", "cross_regression", law="cross"
            )

    def run(self, data: CrossRegressionInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        def call() -> dict[Fraction, AlphaOutput]:
            from mapie.regression import CrossConformalRegressor
            from sklearn.model_selection import KFold, LeaveOneOut

            cv = (
                LeaveOneOut()
                if self.n_folds is None
                else KFold(self.n_folds, shuffle=True, random_state=data.seed)
            )
            alphas = list(data.alphas)
            reg = CrossConformalRegressor(
                data.estimator_factory(),
                confidence_level=[confidence_value(a) for a in alphas],
                method="plus",
                cv=cv,
                random_state=data.seed,
            )
            reg.fit_conformalize(data.x, data.y)
            _, pis = reg.predict_interval(data.x_test, allow_infinite_bounds=True)
            pis = np.asarray(pis, dtype=float)
            return {a: AlphaOutput(intervals=pis[:, :, j]) for j, a in enumerate(alphas)}

        return all_guarded(call, data)


class MapieClassifier(_Mapie):
    def __init__(self, score: str, include_last_label: bool | str | None = None) -> None:
        self.score = score
        self.include_last_label = include_last_label
        variant = (
            "default"
            if include_last_label is None
            else (f"include_last_label={include_last_label}")
        )
        self.spec = MethodSpec("mapie", score, variant, "classification")

    def run_alpha(self, data: ClassificationInput, alpha: Fraction) -> AlphaOutput:  # type: ignore[override]
        from mapie.classification import SplitConformalClassifier

        score: object = self.score
        if self.score == "raps":
            from mapie.conformity_scores import RAPSConformityScore

            score = RAPSConformityScore()
        clf = SplitConformalClassifier(
            data.model,
            confidence_level=confidence_value(alpha),
            conformity_score=score,
            prefit=True,
            random_state=data.seed,
        )
        clf.conformalize(data.x_cal, data.y_cal)
        params = (
            None
            if self.include_last_label is None
            else {"include_last_label": self.include_last_label}
        )
        _, sets = clf.predict_set(data.x_test, conformity_score_params=params)
        eff = getattr(score, "n_samples_", None) if self.score == "raps" else None
        return AlphaOutput(
            sets=np.asarray(sets, dtype=bool)[:, :, 0],
            effective_n=None if eff is None else int(eff),
        )


def adapters() -> list[LibraryAdapter]:
    return [
        MapieSplitAbs(False),
        MapieSplitAbs(True),
        MapieCQR(symmetric=False),
        MapieCQR(symmetric=True),
        MapieCrossPlus(None),
        MapieCrossPlus(5),
        MapieCrossPlus(10),
        MapieClassifier("lac"),
        MapieClassifier("aps", False),
        MapieClassifier("aps", True),
        MapieClassifier("aps", "randomized"),
        MapieClassifier("raps", True),
        MapieClassifier("raps", "randomized"),
    ]
