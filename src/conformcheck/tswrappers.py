"""Time-series conformal wrappers (statsforecast, sktime, darts) as split regressors.

These libraries wrap forecasters, so the exact split law holds only for a fixed forecast.
Each wrapper hands the library the calibration residuals as an i.i.d. series and a
forecaster that always returns 0 (statsforecast ``SklearnModel(DummyRegressor(0))``, sktime
``ForecastKnownValues(zeros)``, darts ``SKLearnModel(DummyRegressor(0))``, all public API).
The scores are then exchangeable and one interval applies to every test point, so
``BetaBinomial(m, k, n + 1 - k)`` holds exactly. This tests the calibration step only.

Each row is a callable for :func:`conformcheck.testing.check_split_regressor`. The
libraries are imported when a row is built, so importing this module needs none of them.
First used in the 2026-11-09 study (``docs/results/newlib-2026-11-09/``, REPORT section 4).
"""

from __future__ import annotations

import logging
import warnings
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from conformcheck import laws

ALPHAS: tuple[float, ...] = (0.05, 0.1, 0.2)
LIBRARIES: tuple[str, ...] = ("statsforecast", "sktime", "darts")

Interval = tuple[float, float]
Fn = Callable[..., np.ndarray]


@dataclass(frozen=True)
class Row:
    """One library method: the callable, its grid and how ranks are read off its intervals."""

    name: str
    fn: Fn
    n: tuple[int, ...]
    alpha: tuple[float, ...] = ALPHAS
    reps: int = 200
    score: str = "other"


def _cached(compute: Callable[[np.ndarray], dict[float, Interval]]) -> Fn:
    """A regressor fn that asks the library once per residual vector for every alpha.

    ``check_split_regressor`` draws the same calibration set for every alpha of an n, so the
    cache (bounded) saves one library call per extra alpha. ``compute`` maps the residuals
    to ``{alpha: (lower offset, upper offset)}`` around the fixed prediction.
    """
    cache: dict[bytes, dict[float, Interval]] = {}

    def fn(x_cal: Any, y_cal: Any, x_test: Any, alpha: float, model: Any) -> np.ndarray:
        r = np.asarray(y_cal - model.predict(x_cal), dtype=float)
        key = r.tobytes()
        if key not in cache:
            if len(cache) >= 4096:
                cache.clear()
            cache[key] = compute(r)
        lo, hi = cache[key][round(alpha, 6)]
        p = model.predict(x_test)
        return np.column_stack([p + lo, p + hi])

    return fn


def _statsforecast(method: str) -> Fn:
    from sklearn.dummy import DummyRegressor
    from statsforecast.models import SklearnModel
    from statsforecast.utils import ConformalIntervals

    def compute(r: np.ndarray) -> dict[float, Interval]:
        n = len(r)
        # The library sees [pad, r_1..r_n]; the first value is the training window of a
        # fixed 0 forecaster and is never scored.
        y = np.concatenate([[0.0], r])
        model = SklearnModel(
            DummyRegressor(strategy="constant", constant=0.0),
            prediction_intervals=ConformalIntervals(n_windows=n, h=1, method=method),
        )
        levels = [round(100 * (1 - a)) for a in ALPHAS]
        out = model.forecast(
            y=y, h=1, X=np.zeros((n + 1, 1)), X_future=np.zeros((1, 1)), level=levels
        )
        return {
            round(a, 6): (float(out[f"lo-{lv}"][0]), float(out[f"hi-{lv}"][0]))
            for a, lv in zip(ALPHAS, levels, strict=True)
        }

    return _cached(compute)


def _sktime(method: str) -> Fn:
    import pandas as pd
    from sktime.forecasting.conformal import ConformalIntervals
    from sktime.forecasting.dummy import ForecastKnownValues

    window = 3

    def compute(r: np.ndarray) -> dict[float, Interval]:
        n = len(r)
        # y[:window] is the initial window of a fixed 0 forecaster; for fh=1 the library
        # uses the residual-matrix diagonal at offset 1, i.e. y[window + 1:]: the residuals.
        y = pd.Series(np.concatenate([np.zeros(window + 1), r]))
        known = pd.Series(np.zeros(len(y) + 5), index=pd.RangeIndex(len(y) + 5))
        f = ConformalIntervals(ForecastKnownValues(known), method=method, initial_window=window)
        f.fit(y, fh=[1])
        if f.residuals_matrix_.shape[0] != n + 1:
            raise RuntimeError(
                f"sktime residual matrix has {f.residuals_matrix_.shape[0]} rows, expected "
                f"{n + 1}: the wrapper no longer feeds the library what it scores"
            )
        coverages = [round(1 - a, 6) for a in ALPHAS]
        pi = f.predict_interval(coverage=coverages)
        var = pi.columns.levels[0][0]
        return {
            round(a, 6): (
                float(pi.iloc[0][(var, c, "lower")]),
                float(pi.iloc[0][(var, c, "upper")]),
            )
            for a, c in zip(ALPHAS, coverages, strict=True)
        }

    return _cached(compute)


_DARTS_Q = {0.05: (0.025, 0.975), 0.1: (0.05, 0.95), 0.2: (0.1, 0.9)}


def _darts(cal_length: bool) -> Fn:
    from darts import TimeSeries
    from darts.models import ConformalNaiveModel, SKLearnModel
    from sklearn.dummy import DummyRegressor

    logging.getLogger("darts").setLevel(logging.ERROR)
    base = SKLearnModel(lags=1, model=DummyRegressor(strategy="constant", constant=0.0))
    base.fit(TimeSeries.from_values(np.zeros(10)))
    quantiles = sorted({0.5, *(q for pair in _DARTS_Q.values() for q in pair)})

    def pick(vals: dict[str, float], q: float) -> float:
        hit = [v for c, v in vals.items() if c.endswith((f"_q{q:.3f}", f"_q{q}"))]
        if len(hit) != 1:
            raise RuntimeError(f"darts quantile {q}: components {sorted(vals)}")
        return float(hit[0])

    def compute(r: np.ndarray) -> dict[float, Interval]:
        n = len(r)
        model = ConformalNaiveModel(
            base, quantiles=quantiles, symmetric=True, cal_length=n if cal_length else None
        )
        # One lag precedes the first calibration forecast.
        series = TimeSeries.from_values(np.concatenate([[0.0], r]))
        pred = model.predict(n=1, series=series, predict_likelihood_parameters=True)
        vals = dict(zip(pred.components, pred.values()[0], strict=True))
        return {round(a, 6): (pick(vals, lo), pick(vals, hi)) for a, (lo, hi) in _DARTS_Q.items()}

    return _cached(compute)


def _reference(offset: int) -> Fn:
    """The exact split method (``offset=0``) or a ``k + offset`` mutant, for controls."""

    def fn(x_cal: Any, y_cal: Any, x_test: Any, alpha: float, model: Any) -> np.ndarray:
        r = np.sort(np.abs(y_cal - model.predict(x_cal)))
        n = len(r)
        k = laws.split_index(n, laws.as_fraction(alpha)) + offset
        q = np.inf if k > n else r[max(k, 1) - 1]
        p = model.predict(x_test)
        return np.column_stack([p - q, p + q])

    return fn


def control_rows(n: tuple[int, ...] = (5, 9, 19, 99)) -> list[Row]:
    """Reference and ``k - 1`` mutant rows: the harness must pass one and catch the other."""
    return [
        Row("reference/exact", _reference(0), n, score="abs"),
        Row("reference/k_minus_1", _reference(-1), n, score="abs"),
    ]


def library_rows(library: str) -> list[Row]:
    """The rows of one library. Raises ImportError when the library is not installed."""
    warnings.filterwarnings("ignore")
    if library == "statsforecast":
        ns = (2, 5, 9, 19, 99, 999)
        return [
            Row(f"statsforecast/{m}", _statsforecast(m), ns)
            for m in ("conformal_distribution", "conformal_error")
        ]
    if library == "sktime":
        return [
            Row("sktime/conformal", _sktime("conformal"), (5, 9, 19, 99)),
            Row(
                "sktime/conformal_bonferroni", _sktime("conformal_bonferroni"), (9, 19, 99), reps=50
            ),
            Row("sktime/empirical", _sktime("empirical"), (9, 19, 99), reps=50),
            Row("sktime/empirical_residual", _sktime("empirical_residual"), (9, 19, 99), reps=50),
        ]
    if library == "darts":
        return [
            Row("darts/naive_sym_cal_length", _darts(True), (5, 9, 19, 99, 999), score="abs"),
            Row("darts/naive_sym_all", _darts(False), (9, 19, 99), score="abs"),
        ]
    raise ValueError(f"unknown library {library!r}; known: {', '.join(LIBRARIES)}")
