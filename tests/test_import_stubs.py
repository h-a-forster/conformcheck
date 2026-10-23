"""The TorchCP dependency strategy: torchcp imports with its heavy extras stubbed."""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from conformcheck.adapters import _import_stubs

pytestmark = pytest.mark.adapter


def test_torchcp_imports_and_calibrates_with_stubs() -> None:
    pytest.importorskip("torch")
    _import_stubs.install()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        torchcp_cls = pytest.importorskip("torchcp.classification.predictor")
        from torchcp.classification.score import LAC

    import torch

    rng = np.random.default_rng(0)
    n, alpha = 19, 0.1
    proba = rng.dirichlet(np.ones(3), size=n)
    labels = rng.integers(0, 3, size=n)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        predictor = torchcp_cls.SplitPredictor(score_function=LAC(), model=None)
        predictor.calculate_threshold(
            torch.log(torch.tensor(proba, dtype=torch.float32)), torch.tensor(labels), alpha
        )
    scores = np.sort(1 - proba[np.arange(n), labels]).astype(np.float32)
    # k = ceil(20 * 0.9) = 18: TorchCP returns the 18th smallest score.
    assert float(predictor.q_hat) == pytest.approx(float(scores[17]), rel=1e-6)


def test_install_does_not_shadow_real_packages() -> None:
    stubbed = _import_stubs.install(("numpy",))
    assert "numpy" not in stubbed
    assert not getattr(np, "__conformcheck_stub__", False)
