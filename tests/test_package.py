"""Skeleton-level checks: the package, CLI, plugin and fixed models import and behave."""

from __future__ import annotations

import importlib

import numpy as np
import pytest

import conformcheck
from conformcheck import cli
from conformcheck.models import ConstantRegressor, FixedClassifier, FixedRegressor
from conformcheck.pytest_plugin import ConformcheckSettings

MODULES = [
    "conformcheck.laws",
    "conformcheck.stats",
    "conformcheck.reference",
    "conformcheck.data",
    "conformcheck.models",
    "conformcheck.diagnostics",
    "conformcheck.study",
    "conformcheck.runner",
    "conformcheck.report",
    "conformcheck.repro",
    "conformcheck.testing",
    "conformcheck.adapters",
    "conformcheck.adapters.base",
    "conformcheck.adapters.mapie",
    "conformcheck.adapters.crepes",
    "conformcheck.adapters.puncc",
    "conformcheck.adapters.torchcp",
    "conformcheck.adapters._import_stubs",
]


@pytest.mark.parametrize("name", MODULES)
def test_modules_import_without_optional_libraries(name: str) -> None:
    importlib.import_module(name)


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    assert conformcheck.__version__ in capsys.readouterr().out


def test_libraries_command(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["libraries"]) == 0
    out = capsys.readouterr().out
    for name in ("mapie", "crepes", "puncc", "torchcp"):
        assert name in out


def test_plugin_fixture(conformcheck_settings: ConformcheckSettings) -> None:
    assert conformcheck_settings.reps >= 1
    assert 0 < conformcheck_settings.fwer < 1


def test_fixed_models() -> None:
    x = np.array([[0.0, 1.0], [0.5, 0.0], [1.0, 1.0]])
    assert np.allclose(FixedRegressor().predict(x), [0.0, 1.0, 2.0])
    assert np.allclose(ConstantRegressor(1.5).fit(x).predict(x), 1.5)
    proba = FixedClassifier(temperature=2.0).predict_proba(x)
    assert proba.shape == (3, 4)
    assert np.allclose(proba.sum(axis=1), 1.0)
    assert np.all(proba > 0)
