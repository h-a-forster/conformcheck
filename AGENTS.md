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
- No model or LLM API calls. CPU only. At most 4 worker processes (round 2 used 3).
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
scripts/raps_neff.py   MAPIE RAPS against candidate calibration sizes (hypothesis 6)
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
uv run python scripts/run_study.py --study default --out runs/default     # about 1 h from scratch, 3 workers
uv run conformcheck report runs/default
uv run conformcheck repro runs/default --verify
# Full size (hours, resumable):
uv run python scripts/run_study.py --study full --out runs/full --attempts 5
```

Watch `runs/<name>/progress.log`. A rerun of the same command resumes.

## Status and next steps

Status (2026-10-24): **round 2 done (RAPS, classification bracketing, informative
classifier); not tagged, not pushed.**

- Round 2 run: `runs/default-r2` (gitignored), fingerprint `cbfed0fa569dc01f`. It was
  seeded with the 779 unaffected v0.1 units (unit ids depend only on unit, R, m, seed),
  then 325 LAC/class-conditional/RAPS units (18.0 min, 3 workers) and 308
  `cls_gauss_inf` units (8.6 min). Total 1412 units. The 205 re-run v0.1 units
  reproduced their counts exactly.
- Results in `docs/results/default/` (matrix, summary, cells.csv, units.jsonl.gz,
  repros, `raps_neff.md`). REPORT.md has F1-F10, hypotheses 1-10 and limitations.
- Headline: 18 of 37 rows flagged at n <= 100. New: F9 (MAPIE RAPS ignores
  `size_raps`, holds out ceil(0.1 n), raises at small n), F10 (puncc randomized RAPS set
  rule does not match its score; over-coverage). F1 extended: MAPIE APS `False`
  under-covers on the Bayes classifier too (hypothesis 8 refuted).
- Oracle controls: 0 Holm rejections in 1010 reference statistical cells, 0 non-PASS in
  1329 reference cells; exact mean test rejects 20 of 562 (3.6%, descriptive).
- Bracketing is now a deterministic status for LAC and class-conditional LAC and catches
  every LAC mutant cell at n = 999/1000. v0.1's `bracket_rank` had a lower-end bug that
  hid positive offsets (fixed, CHANGELOG).
- Review of round 2 (2026-10-24): runner/report fixes (records of earlier configs or
  other versions no longer leak into reports; version-aware reuse), `full.toml` now
  includes `cls_gauss_inf`, documented-usage tests for every finding adapter (23 of 37),
  pmf-level simulation tests for the class-conditional and tied laws, REPORT corrections
  (F3 mechanism is float rounding; hypothesis 2 partly confirmed; regenerated Holm
  p-values; MAPIE uniform-reuse and RAPS-branch limitations). No study results changed:
  the report rebuilt from the committed units is byte-identical apart from a new
  `records_dropped` field in matrix.json.

Notes for whoever continues:

- Rank tolerance is `1e-6 * max(1, |q|, scale)`, where scale is the magnitude of the
  endpoints. Float32 libraries need the scale term (`diagnostics.py`).
- Bracketing (`diagnostics.bracket_rank`): with `a` the largest included and `b` the
  smallest excluded test score, consistent order statistics are
  `#{s < a} + 1 .. #{s < b}`. `RankRange(1, 0)` (`"nt"` in records) means the sets are
  not threshold sets; it is FAIL in `testing` and ignored in the report's rank status.
  It runs only for `runner.BRACKET_METHODS` on exact-law, non-smoothed cells.
- APS/RAPS have no rank recovery: deterministic rules differ by convention, randomized
  ones draw uniforms inside the library.
- MAPIE RAPS: `size_raps` is reset to None by `SplitConformalClassifier`, so the hold-out
  is ceil(0.1 n) (`study.mapie_raps_effective_n`). The adapter records MAPIE's
  `n_samples_` per rep as `effective_n`. If MAPIE fixes this, the cell law must change.
- RAPS parameters are fixed at lambda = 0.1, k_reg = 1 (`reference.RAPS_LAMBDA/KREG`).
- The size check counts rejections of the exact two-sided mean test. It is descriptive:
  alphas of a unit and reference rows on a dgp share draws. No binomial/KS p-value.
- Coverage intervals are empirical t intervals; the law's variance is for the MDE only.
- A documented row is excused only for the statuses in `report.DOCUMENTED_STATUSES`.
- `cls_gauss` is anti-informative (top-1 0.118); `cls_gauss_inf` uses the Bayes
  posterior (top-1 0.708). Laws hold for any fixed model; effect sizes do not.
- `conformcheck run` refuses to start when a needed library is missing; use
  `--libraries` or `--allow-missing`. A changed study config needs `--force` (the
  fingerprint guards it; finished units are still reused by id, but only when the
  versions stored in the record match the current ones: `runner.unit_versions`).
  Records without stored versions (round 2 and earlier) take the versions of the
  `run.json` they were written with.
- `report` and `repro` read records through `runner.study_records`, which keeps only the
  units of the study in `run.json` with matching versions; old records stay in
  `units.jsonl` but are counted as left out.
- MAPIE randomized APS/RAPS reuse the calibration uniforms at test time (int
  `random_state`); a test pins this. MAPIE's randomized RAPS denominator differs from
  the authors' rule for L >= k* + 2, a branch the study barely reaches (REPORT section 7).
- `conformcheck plan` probes smallest, middle and largest n; still treat it as a rough
  estimate.
- `conformcheck repro`: raises-type repros try seeds 0-49 and are split by exception
  message. An unexpected crash exits 2, never 1. Hand-written repros are prefixed
  `manual__`.

Open items (not done):

- ACI / EnbPI (time series): not started.
- The `full` study (R = 2000, m = 1000; hours; resumable).
- CV+ `lower` cells with K not dividing n use an extrapolated bound (labelled).
- puncc PASS cells were not re-checked under `numpy<2` (only its findings were).
- First CI run, once the repository is pushed (owner's go-ahead).
- Report the findings upstream (owner's decision).
