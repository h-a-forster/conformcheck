"""Data-generating processes with known exchangeability (docs/DESIGN.md, section 6).

Every repetition draws fresh calibration and test data from a generator seeded by
``SeedSequence([study seed, crc32(dgp), n, repetition])`` (:func:`rep_seed_sequence`), so
all libraries see identical data in a repetition (common random numbers).

* ``reg_gauss``: ``X ~ U[0,1]^2``, ``Y = 2 X_1 + N(0, 1)``; fixed model ``2 x + 0.3``;
  fixed, deliberately miscalibrated CQR models ``2x - 1.0`` and ``2x + 1.2``.
* ``reg_hetero_t``: ``Y = sin(2 pi X_1) + (0.5 + X_1) t_3``; model ``0.8 sin(2 pi x)``;
  CQR models ``0.8 sin(2 pi x) - 1.5`` and ``+ 1.0``.
* ``reg_tied``: ``Y`` uniform on ``{-3..3}``, constant model 0, so the score ``|Y|`` has
  pmf ``(1, 2, 2, 2) / 7`` on ``{0, 1, 2, 3}`` and the exact discrete law applies.
* ``reg_constant``: data as ``reg_gauss``; the libraries refit ``ConstantRegressor(0)``,
  which makes jackknife+ and CV+ exact split conformal on all ``n`` points.
* ``cls_gauss``: ``Y ~ Uniform{0..3}``, ``X | Y ~ N(mu_Y, I_2)`` with means on a square of
  side 2; fixed linear-softmax classifier at temperature 2. ``per_class=True`` draws
  exactly ``n`` calibration and ``m // 4`` test points per class.
* ``diabetes`` and ``digits`` (bundled with scikit-learn, no download): a fixed training
  subset fits the model once; each repetition is a fresh random split of the remaining
  pool into calibration and test (``m`` is capped at ``pool - n``).
"""

from __future__ import annotations

import functools
import zlib
from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from conformcheck.models import (
    ConstantRegressor,
    FixedClassifier,
    FixedRegressor,
    OffsetRegressor,
)

TaskKind = Literal["regression", "classification"]

TIED_PMF = np.array([1.0, 2.0, 2.0, 2.0]) / 7.0  # pmf of |Y| on {0, 1, 2, 3} for reg_tied
CLS_MEANS = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]])


def rep_seed_sequence(seed: int, dgp: str, n: int, rep: int) -> np.random.SeedSequence:
    """The seed sequence of one repetition: shared by every library (common random numbers)."""
    return np.random.SeedSequence([int(seed), zlib.crc32(dgp.encode()), int(n), int(rep)])


def library_seed(ss: np.random.SeedSequence) -> int:
    """A 31-bit seed for library-internal randomness, spawned from the repetition seed."""
    return int(ss.spawn(1)[0].generate_state(1)[0] & 0x7FFFFFFF)


@dataclass(frozen=True)
class Draw:
    """Calibration and test data of one repetition."""

    x_cal: NDArray[np.float64]
    y_cal: NDArray
    x_test: NDArray[np.float64]
    y_test: NDArray


@dataclass(frozen=True)
class DGP:
    """A data-generating process plus the fixed models used with it."""

    name: str
    task: TaskKind
    n_classes: int = 0
    pool_size: int | None = None  # finite pool (toy datasets)
    description: str = ""

    # -- data ---------------------------------------------------------------------------
    def draw(self, rng: np.random.Generator, n: int, m: int, per_class: bool = False) -> Draw:
        return _DRAWERS[self.name](rng, n, m, per_class)

    def test_size(self, n: int, m: int, per_class: bool = False) -> int:
        """Number of test points actually drawn."""
        if per_class:
            return self.n_classes * (m // self.n_classes)
        if self.pool_size is not None:
            return min(m, self.pool_size - n)
        return m

    # -- models -------------------------------------------------------------------------
    def model(self) -> object:
        return _model(self.name)

    def quantile_models(self) -> tuple[object, object, object] | None:
        """Fixed ``(lower, upper, median)`` regressors for CQR, or None."""
        return _quantile_models(self.name)

    def estimator_factory(self) -> object:
        """A fresh, unfitted estimator for jackknife+ and CV+ (refit by the library)."""
        if self.name == "reg_constant":
            return ConstantRegressor(0.0)
        if self.name == "reg_gauss":
            from sklearn.linear_model import LinearRegression

            return LinearRegression()
        raise ValueError(f"{self.name} has no estimator factory")

    @property
    def score_pmf(self) -> NDArray[np.float64] | None:
        """Known pmf of the (discrete) absolute residual score, for the exact tie law."""
        return TIED_PMF if self.name == "reg_tied" else None


# --- draws ------------------------------------------------------------------------------


def _reg_gauss(rng: np.random.Generator, n: int, m: int, per_class: bool) -> Draw:
    x = rng.uniform(size=(n + m, 2))
    y = 2.0 * x[:, 0] + rng.normal(size=n + m)
    return Draw(x[:n], y[:n], x[n:], y[n:])


def _reg_hetero_t(rng: np.random.Generator, n: int, m: int, per_class: bool) -> Draw:
    x = rng.uniform(size=(n + m, 2))
    y = np.sin(2 * np.pi * x[:, 0]) + (0.5 + x[:, 0]) * rng.standard_t(3, size=n + m)
    return Draw(x[:n], y[:n], x[n:], y[n:])


def _reg_tied(rng: np.random.Generator, n: int, m: int, per_class: bool) -> Draw:
    x = rng.uniform(size=(n + m, 2))
    y = rng.integers(-3, 4, size=n + m).astype(float)
    return Draw(x[:n], y[:n], x[n:], y[n:])


def _cls_gauss(rng: np.random.Generator, n: int, m: int, per_class: bool) -> Draw:
    k = len(CLS_MEANS)
    if per_class:
        y_cal = np.repeat(np.arange(k), n)
        y_test = np.repeat(np.arange(k), m // k)
        rng.shuffle(y_cal)
        rng.shuffle(y_test)
        y = np.concatenate([y_cal, y_test])
        x = CLS_MEANS[y] + rng.normal(size=(y.size, 2))
        return Draw(x[: y_cal.size], y_cal, x[y_cal.size :], y_test)
    y = rng.integers(0, k, size=n + m)
    x = CLS_MEANS[y] + rng.normal(size=(n + m, 2))
    return Draw(x[:n], y[:n], x[n:], y[n:])


def _toy(name: str):
    def draw(rng: np.random.Generator, n: int, m: int, per_class: bool) -> Draw:
        if per_class:
            raise ValueError(f"{name} does not support per-class draws")
        x_pool, y_pool = _toy_pool(name)
        m_eff = min(m, len(y_pool) - n)
        if m_eff < 1:
            raise ValueError(f"pool of {len(y_pool)} too small for n={n}")
        idx = rng.permutation(len(y_pool))[: n + m_eff]
        cal, test = idx[:n], idx[n:]
        return Draw(x_pool[cal], y_pool[cal], x_pool[test], y_pool[test])

    return draw


_DRAWERS = {
    "reg_gauss": _reg_gauss,
    "reg_constant": _reg_gauss,
    "reg_hetero_t": _reg_hetero_t,
    "reg_tied": _reg_tied,
    "cls_gauss": _cls_gauss,
    "diabetes": _toy("diabetes"),
    "digits": _toy("digits"),
}


# --- toy datasets -----------------------------------------------------------------------

TOY_TRAIN = {"diabetes": 100, "digits": 500}
TOY_SPLIT_SEED = 0


@functools.cache
def _toy_split(name: str) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    """Fixed training rows and the remaining pool for a bundled scikit-learn dataset."""
    from sklearn import datasets

    if name == "diabetes":
        x, y = datasets.load_diabetes(return_X_y=True)
        y = y.astype(float)
    elif name == "digits":
        x, y = datasets.load_digits(return_X_y=True)
        x = x / 16.0
        y = y.astype(np.int64)
    else:  # pragma: no cover - defensive
        raise ValueError(name)
    perm = np.random.default_rng(TOY_SPLIT_SEED).permutation(len(y))
    tr, pool = perm[: TOY_TRAIN[name]], perm[TOY_TRAIN[name] :]
    return x[tr], y[tr], x[pool], y[pool]


def _toy_pool(name: str) -> tuple[NDArray, NDArray]:
    _, _, xp, yp = _toy_split(name)
    return xp, yp


@functools.cache
def _toy_model(name: str) -> object:
    xt, yt, _, _ = _toy_split(name)
    if name == "diabetes":
        from sklearn.linear_model import LinearRegression

        return LinearRegression().fit(xt, yt)
    from sklearn.linear_model import LogisticRegression

    return LogisticRegression(max_iter=5000).fit(xt, yt)


# --- models -----------------------------------------------------------------------------


@functools.cache
def _model(name: str) -> object:
    if name == "reg_gauss":
        return FixedRegressor(slope=2.0, intercept=0.3, n_features=2)
    if name == "reg_hetero_t":
        return FixedRegressor(slope=0.0, amplitude=0.8, n_features=2)
    if name in ("reg_tied", "reg_constant"):
        return ConstantRegressor(0.0).fit(np.zeros((1, 2)))
    if name == "cls_gauss":
        return FixedClassifier(temperature=2.0)
    if name in ("diabetes", "digits"):
        return _toy_model(name)
    raise ValueError(f"unknown dgp {name!r}")


@functools.cache
def _quantile_models(name: str) -> tuple[object, object, object] | None:
    if name == "reg_gauss":
        return (
            FixedRegressor(2.0, -1.0, n_features=2),
            FixedRegressor(2.0, 1.2, n_features=2),
            FixedRegressor(2.0, 0.0, n_features=2),
        )
    if name == "reg_hetero_t":
        return (
            FixedRegressor(0.0, -1.5, 0.8, n_features=2),
            FixedRegressor(0.0, 1.0, 0.8, n_features=2),
            FixedRegressor(0.0, 0.0, 0.8, n_features=2),
        )
    if name == "diabetes":
        base = _toy_model(name)
        xt, yt, _, _ = _toy_split(name)
        resid = yt - base.predict(xt)  # type: ignore[attr-defined]
        lo, hi = np.quantile(resid, [0.1, 0.9])
        return OffsetRegressor(base, float(lo)), OffsetRegressor(base, float(hi)), base
    return None


DGPS: dict[str, DGP] = {
    "reg_gauss": DGP("reg_gauss", "regression", description="Y = 2 X1 + N(0,1)"),
    "reg_hetero_t": DGP("reg_hetero_t", "regression", description="sin + heteroscedastic t3"),
    "reg_tied": DGP("reg_tied", "regression", description="Y uniform on {-3..3}"),
    "reg_constant": DGP("reg_constant", "regression", description="reg_gauss, constant model"),
    "cls_gauss": DGP("cls_gauss", "classification", n_classes=4, description="4 Gaussians"),
    "diabetes": DGP("diabetes", "regression", pool_size=342, description="sklearn diabetes"),
    "digits": DGP(
        "digits", "classification", n_classes=10, pool_size=1297, description="sklearn digits"
    ),
}


def get_dgp(name: str) -> DGP:
    try:
        return DGPS[name]
    except KeyError:
        raise ValueError(f"unknown dgp {name!r}; known: {sorted(DGPS)}") from None
