"""Fixed-function models with a scikit-learn interface.

The study conditions on the model: every repetition uses the same deterministic
function, so calibration and test scores are exchangeable by construction and no
training noise enters the oracle. The models are "fitted" from the start (they set the
attributes scikit-learn and the libraries check) and ``fit`` is a no-op.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin


class FixedRegressor(RegressorMixin, BaseEstimator):
    """``predict(x) = slope * x[:, 0] + intercept + amplitude * sin(2 pi x[:, 0])``."""

    def __init__(
        self,
        slope: float = 2.0,
        intercept: float = 0.0,
        amplitude: float = 0.0,
        n_features: int = 1,
    ) -> None:
        self.slope = slope
        self.intercept = intercept
        self.amplitude = amplitude
        self.n_features = n_features
        self.n_features_in_ = n_features
        self.is_fitted_ = True

    def fit(self, X: ArrayLike, y: ArrayLike | None = None, **_: object) -> FixedRegressor:
        return self

    def predict(self, X: ArrayLike) -> NDArray[np.float64]:
        x0 = np.asarray(X, dtype=float)[:, 0]
        return self.slope * x0 + self.intercept + self.amplitude * np.sin(2 * np.pi * x0)


class ConstantRegressor(RegressorMixin, BaseEstimator):
    """Always predicts ``value``.

    With this model every leave-one-out or out-of-fold model is identical, so jackknife+
    and CV+ reduce to split conformal on all ``n`` points and inherit its exact law.
    ``fit`` is a genuine (trivial) fit so the libraries can refit it.
    """

    def __init__(self, value: float = 0.0) -> None:
        self.value = value

    def fit(self, X: ArrayLike, y: ArrayLike | None = None, **_: object) -> ConstantRegressor:
        self.n_features_in_ = np.asarray(X).shape[1]
        self.is_fitted_ = True
        return self

    def predict(self, X: ArrayLike) -> NDArray[np.float64]:
        return np.full(np.asarray(X).shape[0], float(self.value))


class FixedClassifier(ClassifierMixin, BaseEstimator):
    """Softmax of fixed linear logits ``x @ weights + bias`` divided by ``temperature``.

    ``weights`` has shape ``(n_features, n_classes)``. A temperature other than 1 makes
    the probabilities deliberately miscalibrated, which the guarantee must survive.
    """

    def __init__(
        self,
        weights: NDArray[np.float64] | None = None,
        bias: NDArray[np.float64] | None = None,
        temperature: float = 1.0,
    ) -> None:
        self.weights = weights
        self.bias = bias
        self.temperature = temperature
        w = self._weights()
        self.classes_ = np.arange(w.shape[1])
        self.n_features_in_ = w.shape[0]
        self.is_fitted_ = True

    def _weights(self) -> NDArray[np.float64]:
        if self.weights is None:
            return np.array([[2.0, -1.0, 0.5, -1.5], [-1.0, 2.0, 0.5, -0.5]])
        return np.asarray(self.weights, dtype=float)

    def fit(self, X: ArrayLike, y: ArrayLike | None = None, **_: object) -> FixedClassifier:
        return self

    def decision_function(self, X: ArrayLike) -> NDArray[np.float64]:
        w = self._weights()
        b = np.zeros(w.shape[1]) if self.bias is None else np.asarray(self.bias, dtype=float)
        return (np.asarray(X, dtype=float) @ w + b) / self.temperature

    def predict_proba(self, X: ArrayLike) -> NDArray[np.float64]:
        z = self.decision_function(X)
        z = z - z.max(axis=1, keepdims=True)
        e = np.exp(z)
        return e / e.sum(axis=1, keepdims=True)

    def predict(self, X: ArrayLike) -> NDArray[np.int64]:
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]
