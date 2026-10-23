# Contributing

Bug reports, new adapters, new methods and corrections to the oracle are welcome. Read
[docs/DESIGN.md](docs/DESIGN.md) first; it defines the laws and conventions every
change must respect.

## Setup

You need [uv](https://docs.astral.sh/uv/) and git.

```sh
uv sync --all-extras
uv run conformcheck libraries
```

## Checks

```sh
uv run pytest -m "not slow"
uv run ruff check .
uv run ruff format --check .
```

CI runs these on Ubuntu (Python 3.11 and 3.13) and Windows (Python 3.13) for pull
requests.

Test rules:

- No network. Use synthetic data or datasets bundled with scikit-learn.
- Use `tmp_path` for every file.
- Must pass on Windows: `pathlib`, no shell assumptions.
- Mark anything over a few seconds with `@pytest.mark.slow`, and tests that need a
  library under test with `@pytest.mark.adapter` plus `pytest.importorskip`.

## Adding an adapter

1. Implement the `Adapter` protocol in `src/conformcheck/adapters/base.py`, in a new
   module that imports the library lazily.
2. Call only the library's public API, the way its documentation tells users to. Pass
   levels as a user would type them. Do not reimplement any part of the method.
3. Fit once per repetition and evaluate every requested alpha from that fit.
4. Map deliberate refusals to `status="refused"` and other exceptions to
   `status="error"`, with the message. Never swallow an exception.
5. Add a test that reproduces a value from the library's own documentation or tests.
   This is what separates adapter mistakes from library behaviour.
6. Add the library as an optional extra in `pyproject.toml`.

## Reporting a finding upstream

A matrix entry is not a bug report. Before contacting a library's maintainers, the
finding must pass the checks in DESIGN section 8.2: a passing documented-example test
for the adapter, a standalone repro that does not import conformcheck, and any extra
environment check listed for that library.

## Guidelines

- Do not change `laws.py` or `stats.py` without an issue first. They change every
  verdict.
- Oracle code uses exact rational arithmetic for indices (`fractions.Fraction`).
- Runtime dependencies of the core: numpy, scipy, scikit-learn. Discuss new ones in an
  issue first.
- Match the surrounding style; ruff enforces the rest (line length 100).

## Pull requests

One change per pull request, with tests and docs. Add a line under "Unreleased" in
[CHANGELOG.md](CHANGELOG.md) for user-visible changes.

Security issues: see [SECURITY.md](SECURITY.md).
