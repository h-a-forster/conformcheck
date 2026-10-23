"""The reference implementations and mutants exposed as adapters (library ``reference``).

They go through the same runner, tests and report as the libraries, which measures the
size (reference rows) and power (mutant rows) of the oracle (docs/DESIGN.md, section 4).
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck import reference as ref
from conformcheck.adapters._common import LibraryAdapter, all_guarded, guarded
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)


class _Reference(LibraryAdapter):
    module = "conformcheck"
    dist = "conformcheck"


class RefSplitAbs(_Reference):
    def __init__(self, mutant: str | None = None) -> None:
        self.mutant = mutant
        self.spec = MethodSpec("reference", "split_abs", mutant or "default", "regression")

    def run_alpha(self, data: RegressionInput, alpha: Fraction) -> AlphaOutput:  # type: ignore[override]
        m = data.model
        iv = ref.split_abs(
            data.y_cal,
            m.predict(data.x_cal),
            m.predict(data.x_test),
            alpha,
            self.mutant,  # type: ignore[attr-defined]
        )
        return AlphaOutput(intervals=iv)


class RefCQR(_Reference):
    def __init__(self, symmetric: bool) -> None:
        self.symmetric = symmetric
        variant = "symmetric" if symmetric else "asymmetric"
        law = "split" if symmetric else "asymmetric_cqr"
        self.spec = MethodSpec("reference", "cqr", variant, "regression", law=law)

    def run_alpha(self, data: RegressionInput, alpha: Fraction) -> AlphaOutput:  # type: ignore[override]
        assert data.quantile_models is not None
        lo, hi, _ = data.quantile_models
        iv = ref.cqr(
            lo.predict(data.x_cal),  # type: ignore[attr-defined]
            hi.predict(data.x_cal),  # type: ignore[attr-defined]
            data.y_cal,
            lo.predict(data.x_test),  # type: ignore[attr-defined]
            hi.predict(data.x_test),  # type: ignore[attr-defined]
            alpha,
            self.symmetric,
        )
        return AlphaOutput(intervals=iv)


class RefCrossPlus(_Reference):
    def __init__(self, n_folds: int | None) -> None:
        self.n_folds = n_folds
        if n_folds is None:
            self.spec = MethodSpec(
                "reference", "jackknife_plus", "default", "cross_regression", law="cross"
            )
        else:
            self.spec = MethodSpec(
                "reference", "cv_plus", f"K={n_folds}", "cross_regression", law="cross"
            )

    def run(self, data: CrossRegressionInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        def call() -> dict[Fraction, AlphaOutput]:
            n = len(data.y)
            if self.n_folds is None:
                folds = [np.array([i]) for i in range(n)]
            else:
                folds = ref.kfold_indices(n, self.n_folds, np.random.default_rng(data.seed))
            return {
                a: AlphaOutput(
                    intervals=ref.cv_plus(
                        data.x, data.y, data.x_test, a, data.estimator_factory, folds
                    )
                )
                for a in data.alphas
            }

        return all_guarded(call, data)


class RefClassifier(_Reference):
    def __init__(self, method: str, variant: str = "default") -> None:
        self.method = method
        self.variant = variant
        law = {"class_conditional": "class_conditional"}.get(method, "split")
        if variant == "smoothed":
            law = "smoothed"
        self.spec = MethodSpec("reference", method, variant, "classification", law=law)

    def run(self, data: ClassificationInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        out: dict[Fraction, AlphaOutput] = {}
        for i, a in enumerate(data.alphas):
            rng = np.random.default_rng([data.seed, i])
            out[a] = guarded(lambda a=a, rng=rng: self._one(data, a, rng), data, a)
        return out

    def _one(self, data: ClassificationInput, a: Fraction, rng: np.random.Generator) -> AlphaOutput:
        pc, yc, pt = data.proba_cal, data.y_cal, data.proba_test
        if self.method == "lac" and self.variant == "smoothed":
            sets = ref.smoothed_lac(pc, yc, pt, a, rng)
        elif self.method == "lac":
            mutant = None if self.variant == "default" else self.variant
            sets = ref.lac(pc, yc, pt, a, mutant)
        elif self.method == "aps":
            sets = ref.aps(pc, yc, pt, a, randomized=self.variant == "randomized", rng=rng)
        elif self.method == "raps":
            sets = ref.raps(pc, yc, pt, a, randomized=self.variant == "randomized", rng=rng)
        elif self.method == "class_conditional":
            sets = ref.class_conditional_lac(pc, yc, pt, a)
        else:  # pragma: no cover - defensive
            raise ValueError(self.method)
        return AlphaOutput(sets=sets)


def adapters(mutants: tuple[str, ...] = ref.MUTANTS) -> list[LibraryAdapter]:
    out: list[LibraryAdapter] = [
        RefSplitAbs(),
        RefCQR(symmetric=True),
        RefCQR(symmetric=False),
        RefCrossPlus(None),
        RefCrossPlus(5),
        RefCrossPlus(10),
        RefClassifier("lac"),
        RefClassifier("lac", "smoothed"),
        RefClassifier("aps", "deterministic"),
        RefClassifier("aps", "randomized"),
        RefClassifier("raps", "deterministic"),
        RefClassifier("raps", "randomized"),
        RefClassifier("class_conditional"),
    ]
    out += [RefSplitAbs(m) for m in mutants]
    out += [RefClassifier("lac", m) for m in mutants]
    return out
