# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- RAPS rows: MAPIE (`include_last_label` True and `"randomized"`, tested against the
  effective calibration size MAPIE uses), puncc and TorchCP (fixed `lambda = 0.1`,
  `k_reg = 1`, deterministic and randomized), and reference RAPS implementations.
- Bracketing is now rank recovery for classification: a deterministic status for LAC
  and class-conditional LAC (per class), so one-step errors are detected at any `n`.
- `check_split_classifier(score="lac")` brackets the order statistic.
- DGP `cls_gauss_inf`: the `cls_gauss` Gaussians with the Bayes-posterior classifier.
- `scripts/raps_neff.py`: tests MAPIE RAPS against candidate calibration sizes.
- `conformcheck plan` probes the middle `n` of each group as well.
- Round-2 study results (`docs/results/default/`), REPORT.md findings F9 and F10.

### Fixed

- `diagnostics.bracket_rank` returned a lower end one too low (`#{s <= a}` instead of
  `#{s < a} + 1`), which hid positive offsets. Bracketing was diagnostic only before, so
  no published status depended on it.

- Coverage intervals in reports are t intervals from the empirical spread of the counts.
  They used the variance of the exact (null) law, which is the wrong spread in the
  cells that are reported, and could extend past 1. They are now clipped to [0, 1].
- The headline excuses a documented row only for its documented statuses; the default
  study's headline is 15 of 31 rows (was 14).
- The oracle size check reports the rejection count without a binomial p-value: the
  cells share calibration draws, so they are not independent.
- `check_split_regressor` no longer marks valid methods with a non-absolute-residual
  score as FAIL. A new `score` argument (`"auto"`, `"abs"`, `"other"`) controls rank
  recovery.
- `testing` labels a rejection driven only by the goodness-of-fit test `LAW_MISMATCH`,
  as the report does.
- Study TOML files are validated on load (required keys, positive sizes, known DGPs,
  grids and mutants, `n_folds` for CV+); errors exit with code 2, which the resume
  wrapper does not retry.
- Units of libraries that are not installed are no longer checkpointed as finished.
  `conformcheck run` refuses to start without them unless `--libraries` or the new
  `--allow-missing` is given; unknown names in `--libraries` are rejected.
- The report memoises laws and convolution powers (about 5 times faster on the default
  run) and orders cells deterministically.

### Changed

- REPORT.md: F1 reports the digits cells (over-coverage) beside the synthetic ones
  (under-coverage), discloses that the synthetic classifier is anti-informative, and
  marks hypothesis 3 as partly refuted. The section 2 table and the asymmetric CQR
  over-refusal condition were corrected against the matrix.
- The CV+ bound is flagged as extrapolated where K does not divide n.
- README: the library extras are supported only through `uv sync --all-extras` in a
  clone.

## [0.1.0] - 2026-10-23

First release: the oracle, adapters for four libraries, the study pipeline and the
default study.

### Added

- `conformcheck.laws`: exact split-conformal order statistic, marginal coverage and
  bounds, Beta and BetaBinomial laws, discrete-score (tied) laws, asymmetric CQR
  coverage, jackknife+ and CV+ bounds. `alpha` is read as an exact decimal.
- `conformcheck.stats`: exact mean test of summed counts (FFT convolution), chi-square
  goodness of fit, one-sided bound test, t-tests for mean-only laws, Holm and
  Benjamini-Yekutieli, coverage intervals and minimum detectable effects.
- `conformcheck.reference`: reference implementations (split, CQR symmetric and
  asymmetric, jackknife+, CV+, LAC, APS, class-conditional LAC, smoothed p-values) and
  four mutants used to measure the oracle's size and power.
- `conformcheck.data`: synthetic DGPs with known laws (Gaussian, heteroscedastic t,
  tied scores, constant model, four-class Gaussian) and random splits of the
  scikit-learn diabetes and digits datasets.
- Adapters for MAPIE 1.6, crepes 0.9.1, puncc 0.9.3 and TorchCP 1.2.1 (31
  library-method rows), with import stubs for TorchCP's unused heavy dependencies.
- `conformcheck.diagnostics`: per-endpoint rank recovery, set bracketing, trivial-set
  check and differential comparison with the reference.
- Study pipeline: TOML studies (`smoke`, `default`, `full`), `conformcheck plan`
  (unit count and time estimate), `conformcheck run` (parallel, at most 4 workers,
  per-unit checkpoints, resume, fingerprint guard), `conformcheck report` (matrix,
  summary, cell table) and `conformcheck repro` (standalone repro scripts, optional
  verification); `scripts/run_study.py` retries a run on failure.
- `conformcheck.testing.check_split_regressor` / `check_split_classifier` and the
  pytest plugin options `--conformcheck-reps` and `--conformcheck-seed`.
- `REPORT.md` and `docs/results/default/`: results of the default study.

### Not included

- RAPS rows (cut from v0.1, see `docs/DESIGN.md` section 2), time-series methods,
  weighted conformal prediction, conformal risk control and GPU runs.
