"""pytest plugin, registered through the ``pytest11`` entry point.

It must stay cheap to import: it is loaded by every pytest run in an environment where
conformcheck is installed. It adds command-line options that scale the Monte Carlo
size of conformance checks and a ``conformcheck_settings`` fixture that
:mod:`conformcheck.testing` helpers read. The checking fixture itself arrives in
milestone M7 (docs/DESIGN.md, section 8.4).
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class ConformcheckSettings:
    """Monte Carlo settings for conformance checks run inside pytest."""

    reps: int = 200
    test_points: int = 500
    seed: int = 0
    fwer: float = 0.05


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("conformcheck", "conformal coverage conformance checks")
    group.addoption(
        "--conformcheck-reps",
        type=int,
        default=None,
        help="repetitions per conformance cell (default 200)",
    )
    group.addoption(
        "--conformcheck-seed",
        type=int,
        default=None,
        help="base seed for conformance checks (default 0)",
    )


@pytest.fixture
def conformcheck_settings(request: pytest.FixtureRequest) -> ConformcheckSettings:
    """Settings for conformance checks, taken from the command line when given."""
    reps = request.config.getoption("--conformcheck-reps")
    seed = request.config.getoption("--conformcheck-seed")
    defaults = ConformcheckSettings()
    return ConformcheckSettings(
        reps=defaults.reps if reps is None else reps,
        test_points=defaults.test_points,
        seed=defaults.seed if seed is None else seed,
        fwer=defaults.fwer,
    )
