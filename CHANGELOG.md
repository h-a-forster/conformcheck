# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
