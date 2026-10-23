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
tests/              laws, stats, reference, adapters, pipeline, testing API, controls
REPORT.md           default study findings; docs/results/default/ holds its outputs
docs/DESIGN.md      the spec
```

## How to test

```sh
uv sync --all-extras
uv run pytest                 # everything
uv run pytest -m "not slow"   # what CI runs
uv run ruff check . && uv run ruff format --check .
```

## How to run the study

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

Status (2026-10-23): **M0 to M8 done; v0.1.0 prepared (not tagged, not pushed).**

- The default study finished: 984 units, 45.2 min with 4 workers, plus 2.4 min
  re-running the 61 TorchCP regression units after the rank-tolerance fix. The plan
  estimated 20 min, so treat `plan` as a lower bound.
- Results are in `docs/results/default/`: the matrix, summary, cells.csv, gzipped
  units and verified repros. `REPORT.md` has the findings, the verdicts on the
  hypotheses and the limitations.
- Every library repro exits 1 under `conformcheck repro --verify`. The puncc repros
  were re-checked under `numpy<2` (`repros/puncc_numpy1_recheck.txt`).
- Oracle controls: the reference rows have 0 Holm rejections and 0 non-PASS cells.
  The exact mean test rejects in 19 of 402 cells (binomial p = 0.63). The mutants are
  caught as shown in REPORT section 3.
- RAPS was cut from v0.1 (DESIGN section 2).

Notes for whoever continues:

- Rank tolerance is `1e-6 * max(1, |q|, scale)`, where scale is the magnitude of the
  endpoints. Float32 libraries need the scale term (`diagnostics.py`).
- The oracle's size check is a binomial test on the exact two-sided mean-test
  p-values. Do not KS-test the combined cell p-values, which are conservative by
  construction.
- `conformcheck repro`: raises-type repros try seeds 0-49 and are split by exception
  message. An unexpected crash in a repro exits 2, never 1.
- `conformcheck report` takes about 1.5 min on the default run (pure Python over
  4330 cells).

Next (not started):

- The `full` study (R = 2000, m = 1000; hours; resumable).
- RAPS rows.
- Rank recovery for classification (currently statistical only, so classifiers have
  low power at n >= 100).
- Probe a mid-range n in `plan`.
- First CI run, once the repository is pushed (needs the owner's go-ahead).
- Report the findings upstream (owner's decision).
