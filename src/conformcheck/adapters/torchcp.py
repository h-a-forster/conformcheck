"""TorchCP (ml-stat-Sustech/TorchCP, LGPL-3.0; imported, never vendored), CPU only.

Methods: regression ``SplitPredictor`` with the ABS and CQR scores (the fixed model is
wrapped as an identity torch module over precomputed predictions, float32), and
classification ``SplitPredictor`` with LAC and APS (``randomized`` False and True) and
``ClassConditionalPredictor`` with LAC, driven through ``calculate_threshold`` /
``predict_with_logits`` on float32 log-probabilities. ``import torchcp`` pulls in
torchsort, torch_geometric and transformers, which are not installed here: the adapter
installs import stubs for the missing ones (docs/DESIGN.md, section 5.4). RAPS is not
run in v0.1.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from conformcheck.adapters import _import_stubs
from conformcheck.adapters._common import LibraryAdapter, alpha_value, guarded
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    MethodSpec,
    RegressionInput,
)


class _TorchCP(LibraryAdapter):
    module = "torchcp"
    dist = "torchcp"

    def available(self) -> bool:
        if not super().available():
            return False
        try:
            import torch  # noqa: F401
        except ImportError:
            return False
        return True

    def setup(self) -> None:
        _import_stubs.install()


def _identity():
    import torch

    class Identity(torch.nn.Module):
        """Feeds precomputed predictions of the fixed model to TorchCP unchanged."""

        def forward(self, x):  # type: ignore[no-untyped-def]
            return x

    return Identity()


class TorchcpRegression(_TorchCP):
    def __init__(self, score: str) -> None:
        self.score = score
        method = "split_abs" if score == "abs" else "cqr"
        self.spec = MethodSpec("torchcp", method, "default", "regression")

    def _features(self, data: RegressionInput, x: np.ndarray) -> np.ndarray:
        if self.score == "abs":
            return np.asarray(data.model.predict(x), dtype=float)[:, None]  # type: ignore[attr-defined]
        assert data.quantile_models is not None
        lo, hi, _ = data.quantile_models
        return np.column_stack([lo.predict(x), hi.predict(x)])  # type: ignore[attr-defined]

    def run(self, data: RegressionInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        self.setup()
        import torch
        from torch.utils.data import DataLoader, TensorDataset
        from torchcp.regression.predictor import SplitPredictor
        from torchcp.regression.score import ABS, CQR

        torch.manual_seed(data.seed)
        f_cal = torch.tensor(self._features(data, data.x_cal), dtype=torch.float32)
        f_test = torch.tensor(self._features(data, data.x_test), dtype=torch.float32)
        y_cal = torch.tensor(np.asarray(data.y_cal, dtype=float), dtype=torch.float32)
        loader = DataLoader(TensorDataset(f_cal, y_cal), batch_size=max(1, len(data.y_cal)))
        score = ABS() if self.score == "abs" else CQR()

        def one(a: Fraction) -> AlphaOutput:
            pred = SplitPredictor(score_function=score, model=_identity(), device="cpu")
            pred.calibrate(loader, alpha=alpha_value(a))
            iv = pred.predict(f_test).detach().cpu().numpy().astype(float)
            return AlphaOutput(intervals=iv.reshape(iv.shape[0], -1, 2)[:, 0, :])

        return {a: guarded(lambda a=a: one(a), data, a) for a in data.alphas}


class TorchcpClassifier(_TorchCP):
    def __init__(self, score: str, randomized: bool | None = None, class_cond: bool = False):
        self.score = score
        self.randomized = randomized
        self.class_cond = class_cond
        if class_cond:
            self.spec = MethodSpec(
                "torchcp", "class_conditional", "default", "classification", law="class_conditional"
            )
        elif score == "aps":
            self.spec = MethodSpec("torchcp", "aps", f"randomized={randomized}", "classification")
        else:
            self.spec = MethodSpec("torchcp", "lac", "default", "classification")

    def run(self, data: ClassificationInput) -> dict[Fraction, AlphaOutput]:  # type: ignore[override]
        self.setup()
        import torch
        from torchcp.classification.predictor import ClassConditionalPredictor, SplitPredictor
        from torchcp.classification.score import APS, LAC

        torch.manual_seed(data.seed)
        logit_cal = torch.log(torch.tensor(data.proba_cal, dtype=torch.float32))
        logit_test = torch.log(torch.tensor(data.proba_test, dtype=torch.float32))
        labels = torch.tensor(np.asarray(data.y_cal), dtype=torch.long)
        score = LAC() if self.score == "lac" else APS(randomized=bool(self.randomized))
        cls = ClassConditionalPredictor if self.class_cond else SplitPredictor

        def one(a: Fraction) -> AlphaOutput:
            pred = cls(score_function=score, model=None)
            pred.calculate_threshold(logit_cal, labels, alpha_value(a))
            sets = pred.predict_with_logits(logit_test)
            return AlphaOutput(sets=sets.detach().cpu().numpy().astype(bool))

        return {a: guarded(lambda a=a: one(a), data, a) for a in data.alphas}


def adapters() -> list[LibraryAdapter]:
    return [
        TorchcpRegression("abs"),
        TorchcpRegression("cqr"),
        TorchcpClassifier("lac"),
        TorchcpClassifier("aps", randomized=False),
        TorchcpClassifier("aps", randomized=True),
        TorchcpClassifier("lac", class_cond=True),
    ]
