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
  stats.py          exact mean test (FFT), chi-square GOF, one-sided test, Holm, BY          [done]
  reference.py      reference implementations + mutants (oracle self-test)                 [done]
  data.py           DGPs with known exchangeability; toy datasets                         [done]
  models.py         fixed-function sklearn models (prefit, deterministic)                  [done]
  adapters/base.py  adapter contract and input/output types                               [done]
  adapters/{mapie,crepes,puncc,torchcp,reference}.py  library adapters + controls          [done]
  adapters/_import_stubs.py  placeholder modules for torchcp's unused heavy deps          [done]
  diagnostics.py    rank recovery, bracketing, trivial-set check, differential check       [done]
  study.py          study TOML -> units; cell -> law mapping                              [done]
  runner.py         checkpointed parallel runner                                           [done]
  plan.py           unit count + time estimate by probing                                 [done]
  report.py         conformance matrix, summary                                            [done]
  repro.py          standalone repro scripts + verification                               [done]
  testing.py        public check_* helpers for library authors                            [done]
  pytest_plugin.py  pytest11 plugin: options + conformcheck_settings fixture               [done]
  cli.py            conformcheck libraries | plan | run | report | repro                   [done]
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

Status (2026-10-23): **M0 to M7 done.** All modules implemented and tested (stats,
reference + mutants, data, adapters for the four libraries, diagnostics, study, runner,
plan, report, repro, testing API, plugin, CLI). RAPS was cut from v0.1 (DESIGN section
2 allowed this); the matrix has no RAPS rows. The default study is running into
`runs/default` (resumable: rerun the same command).

Next: M8 (finish the default study, `conformcheck report runs/default`,
`conformcheck repro runs/default --verify`, puncc numpy<2 re-check, copy results to
`docs/results/default/`, write REPORT.md, README headline).
