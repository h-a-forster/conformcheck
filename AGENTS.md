# AGENTS.md

Guide for anyone (human or agent) continuing work on conformcheck. Read
`docs/DESIGN.md` first: it is the spec (formulas, oracle, study design, milestones).

## What this is

A conformance suite for Python conformal-prediction libraries (MAPIE, crepes, puncc,
TorchCP). It tests each library method against exact finite-sample laws: the order
statistic `k = ceil((n+1)(1-alpha))`, `BetaBinomial(m, k, n+1-k)` covered counts, and
jackknife+/CV+ bounds. The output is a pass / fail / conservative matrix with
standalone repros, plus a pytest plugin.

## Conventions

- uv + hatchling, `src/` layout, Python 3.11 to 3.13, typed code, line length 100.
- `uv sync --all-extras` installs every library under test (CPU torch from the PyTorch
  CPU index). Plain `uv sync` installs only the core; adapter tests then skip.
- Checks: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`.
- Tests: offline, `tmp_path` for files, Windows-safe (`pathlib`), Monte Carlo tests
  over a few seconds are marked `@pytest.mark.slow`, tests needing a library are
  marked `adapter` and use `pytest.importorskip`.
- Exact arithmetic in the oracle: `alpha` is a `Fraction` read from its decimal repr
  (`laws.as_fraction`). Never compute `k` from floats in oracle code.
- Adapters call public APIs only, pass levels as a user would type them, and never
  reimplement the method (`adapters/base.py` docstring).
- No model or LLM API calls. CPU only. At most 4 worker processes.
- Long runs checkpoint each unit to `runs/<name>/units.jsonl` and skip finished units
  on rerun; progress goes to `runs/<name>/progress.log`.
- Scratch work goes in `tmp/` (gitignored). Large or raw outputs stay in `runs/` or
  `data/` (gitignored); only small derived results go in `docs/results/`.
- Do not change `[tool.uv] override-dependencies` without reading DESIGN section 5.
- Commits end with the `Co-Authored-By` trailer used in the history. Do not push or
  create remotes without the owner's go-ahead.
- Statistical honesty: report sizes, seeds and versions; give intervals; use Holm/BY
  across cells. A library "bug" needs a standalone repro and an adapter cross-check
  (DESIGN 8.2) before it is called one.

## Architecture map

```text
src/conformcheck/
  laws.py           exact laws: k, marginal coverage, Beta/BetaBinomial, ties, CV+ bounds   [done]
  stats.py          exact mean test (FFT), chi-square GOF, one-sided test, Holm, BY          [M1]
  reference.py      reference implementations + mutants (oracle self-test)                 [M2]
  data.py           DGPs with known exchangeability; toy datasets                         [M2]
  models.py         fixed-function sklearn models (prefit, deterministic)                  [done]
  adapters/base.py  adapter contract and input/output types                               [done]
  adapters/{mapie,crepes,puncc,torchcp}.py   library adapters                             [M3]
  adapters/_import_stubs.py  placeholder modules for torchcp's unused heavy deps          [done]
  diagnostics.py    rank recovery, bracketing, trivial-set check, differential check       [M3]
  study.py          study TOML -> units                                                    [M4]
  runner.py         checkpointed parallel runner                                           [M4]
  report.py         conformance matrix, summary                                            [M5]
  repro.py          standalone repro scripts + verification                               [M6]
  testing.py        public check_* helpers for library authors                            [M7]
  pytest_plugin.py  pytest11 plugin: options + conformcheck_settings fixture               [skeleton]
  cli.py            conformcheck libraries | plan | run | report | repro                   [skeleton]
  studies/          smoke.toml, default.toml, full.toml
scripts/run_study.py  resume-on-failure wrapper around `conformcheck run`
tests/              test_laws.py (reference values), test_package.py, test_import_stubs.py
docs/DESIGN.md      the spec
```

## How to test

```sh
uv sync --all-extras
uv run pytest                 # everything
uv run pytest -m "not slow"   # what CI runs
uv run ruff check . && uv run ruff format --check .
```

## How to run the study (after M4 to M6)

```sh
uv run conformcheck plan --study default                                  # units + time estimate
uv run python scripts/run_study.py --study default --out runs/default     # about 25 to 40 min, 4 workers
uv run conformcheck report runs/default
uv run conformcheck repro runs/default --verify
# Full size (hours, resumable):
uv run python scripts/run_study.py --study full --out runs/full --attempts 5
```

Watch `runs/<name>/progress.log`. A rerun of the same command resumes.

## Status and next steps

Status (2026-10-23): **M0 done.** Scaffold, lockfile, CI, design, `laws.py` with
reference-value tests, fixed models, the adapter contract, and the verified torchcp
import-stub strategy. All four libraries import and calibrate in this environment.
Scratch calls confirmed: rank used at n=19, alpha=0.1 is 18 for MAPIE, puncc and TorchCP,
and 19 for crepes `WrapRegressor`. That is DESIGN hypothesis 1, not yet a finding.

Next, in order (done-checks in DESIGN section 9):

1. M1 `stats.py`
2. M2 `reference.py` and `data.py`
3. M3 adapters and `diagnostics.py`
4. M4 `study.py`, `runner.py` and CLI `plan`/`run`
5. M5 `report.py`
6. M6 `repro.py`
7. M7 `testing.py` and the plugin fixture
8. M8 default study, `REPORT.md`, README headline

Open questions: none blocking. RAPS (M8) may be cut for time; if so, say so in the
matrix and REPORT.md.
