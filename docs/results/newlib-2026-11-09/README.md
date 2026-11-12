# Time-series conformal wrappers: statsforecast, sktime, darts (2026-11-09)

A study outside the default grid: `conformcheck.testing.check_split_regressor`, unmodified,
called through small adapters for three libraries the default study does not cover. REPORT
section 4, "Time-series wrappers", has the findings; this folder holds the scripts and the
results they were drawn from.

| Library | Version | Method | Result |
|---|---|---|---|
| statsforecast | 2.1.1 | `ConformalIntervals`, both methods | Under-covers at small n: 32 of 52 library cells rejected (Holm over 76), plus all 14 cells with k > n. With the tutorial's `n_windows=2`, coverage at 90% is 0.637 |
| sktime | 1.3.0 | `ConformalIntervals`, 4 methods | Three known defects confirmed on the release (#10757, #10758, #10766) |
| darts | 0.48.1 | `ConformalNaiveModel` | Exact where k <= n (0 of 34 rejected, 0 of 3,410 rank-scan pairs off). Where k > n it returns a finite interval covering n/(n+1), without an error |

## Design

These libraries wrap forecasters, so the exact law holds only for a fixed forecast. Each
adapter gives the library the calibration residuals as an i.i.d. series and a forecaster
that always returns 0 (statsforecast `SklearnModel(DummyRegressor(0))`, sktime
`ForecastKnownValues(zeros)`, darts `SKLearnModel(DummyRegressor(0))`, all public API). The
scores are then exchangeable and one interval applies to all m test points, so
`BetaBinomial(m, k, n + 1 - k)` holds exactly. This tests the calibration step only; it says
nothing about serial dependence or real forecasters.

R = 200 calibration draws x 500 test points per cell unless `report.txt` shows otherwise
(sktime's non-default methods used R = 50), seed 20261109, Holm FWER 0.05 across every
statistical cell of one library. Reference and `k - 1` mutant rows run through the same
pipeline in every library: 0 of 12 reference cells rejected, 10 of 12 mutant cells rejected
by Holm and all 12 caught by rank recovery, in all three.

## Results

### statsforecast 2.1.1

The tutorial calls these intervals guaranteed and uses `ConformalIntervals(h=24,
n_windows=2)`. `conformal_distribution` against the exact law: n = 9, alpha = 0.1: 0.821
vs 0.900 (Holm p 3.5e-20); n = 19: 0.861 (4.3e-12); n = 99, alpha = 0.05: 0.942 vs 0.950
(1.5e-4); n = 999 passes. Cause: `np.quantile(scores, level)` with linear interpolation and
no (n + 1) correction. PR #1246 (merged 2026-10-14) fixes the quantile on `main`; no release
contains it as of 2026-11-13 (latest is 2.1.1).

The default `n_windows=2` through the public `StatsForecast.forecast` with
`HistoricAverage` on 20,000 i.i.d. series (`repro_sf.py`, independent seed): 0.637
[0.630, 0.643] at 90% and 0.599 [0.592, 0.605] at 80%. No finite interval from two scores
can cover more than 2/3. Filed as statsforecast#1349; the maintainer closed it on
2026-11-12, keeping `n_windows=2` as the default and leaving the check to users
([docs/upstream.md](../../upstream.md)).

### sktime 1.3.0

- `conformal`: 9 of 12 rejected, plus 3 of 3 with k > n (n = 9, alpha = 0.1: 0.829 vs
  0.900). Duplicate of #10758.
- `empirical_residual`: 8 of 8 rejected; `predict_interval(coverage=0.9)` covers 0.056 at
  n = 99. Duplicate of #10757.
- `conformal_bonferroni`: 2 of 3, same cause as `conformal`. `empirical` makes no conformal
  claim, so its 6 of 8 are not a defect.
- Step h calibrated on (h + 1)-step residuals (`repro_sktime.py`, random walk,
  `NaiveForecaster("last")`, 300 series): fh = 1 half-width 2.305, which is 1.645 sqrt(2),
  not 1.645 sqrt(1). Duplicate of #10766.

All three issues were open on 2026-11-13, so nothing was filed.

### darts 0.48.1

Clean where k <= n: 0 of 34 cells rejected, rank offset 0 in every draw, 0 of 3,410
(n, alpha) rank-scan pairs off, asymmetric coverage matches (`darts_extra.py`). darts
merged the finite-sample correction in PR #3227 (2026-10-12), the same fix statsforecast has
only on `main`. Where k > n it uses the largest score, a finite interval with coverage
exactly n/(n + 1) (n = 9, alpha = 0.05: 0.902 at a 0.95 target), with no error or warning.
conformcheck counts MAPIE 1.5.0's finite intervals at k > n as FAIL, so by the same rule this
is a low-severity defect. Not filed: #3227 chose it after review.

## Files

| Path | Contents |
|---|---|
| `scripts/ccrun.py` | Driver: one `check_split_regressor` call per cell, appended to `<lib>/cells.jsonl`, skipped on rerun |
| `scripts/ad_<lib>.py` | The adapters |
| `scripts/ccreport.py` | Holm across a library's statistical cells, then a row table (`<lib>/report.txt`) |
| `scripts/repro_sf.py`, `repro_sktime.py`, `darts_extra.py` | Standalone checks; output in `statsforecast/repro_sf.out`, `sktime/repro.out`, `darts/extra.out` |
| `scripts/mkvenv.sh` | A fresh wheels-only venv per library under the repository's `tmp/newlib/` |
| `<lib>/cells.jsonl` | One record per cell: coverage, exact target, p-values, rank offsets, status |

## Reproducing

```sh
sh docs/results/newlib-2026-11-09/scripts/mkvenv.sh statsforecast 3.12 statsforecast==2.1.1 scikit-learn
tmp/newlib/statsforecast/venv/Scripts/python -I docs/results/newlib-2026-11-09/scripts/ccrun.py statsforecast
uv run python -I docs/results/newlib-2026-11-09/scripts/ccreport.py statsforecast
```

`ccrun.py` writes into this folder and skips cells already in `cells.jsonl`; move the
committed file aside to rerun from scratch. Run times on the original machine: 524 s
(statsforecast), 943 s (sktime), 148 s (darts). `ccreport.py` needs only this repository and
reproduces the committed `report.txt` files from the committed `cells.jsonl`.
