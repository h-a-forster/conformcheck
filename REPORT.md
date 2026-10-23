# conformcheck default study: report

This report covers one run of the `default` study, made on 2026-10-23. It ran four Python
conformal-prediction libraries (31 library-method rows) and a set of reference and mutant
rows through the exact finite-sample laws of split conformal prediction. All numbers
below come from [docs/results/default](docs/results/default). Each finding has a
standalone repro script in [docs/results/default/repros](docs/results/default/repros).
The scripts depend only on numpy, scikit-learn and the library concerned, and exit 1
while the problem reproduces.

The design, the formulas and the pre-registered hypotheses are in
[docs/DESIGN.md](docs/DESIGN.md).

## 1. What ran

| | |
|---|---|
| Study | `default` (`src/conformcheck/studies/default.toml`), fingerprint `bc040613bb12ec08` |
| Repetitions | R = 200 calibration draws per cell, m = 500 test points per draw (capped by the pool on the toy datasets) |
| Seed | 20261023; common random numbers across libraries (`SeedSequence([seed, crc32(dgp), n, rep])`) |
| n | 5, 9, 10, 19, 20, 49, 50, 99, 100, 999, 1000 (split); 9 to 99 (jackknife+); 19 to 1000 (CV+, K = 5, 10); 5 to 99 per class (class-conditional); 10, 19, 50, 99 (toy data) |
| alpha | 0.05, 0.1, 0.2, plus the edge levels 1/(n+1) (k = n) and 0.9/(n+1) (k = n + 1, trivial set required) |
| DGPs | Gaussian and heteroscedastic-t regression, tied scores, constant model (jackknife+/CV+), four-class Gaussian classification, random splits of scikit-learn's diabetes and digits |
| Size | 984 units, 4330 cells (2569 library cells), 3058 statistical cells |
| Multiple testing | Holm at FWER 0.05 over all 3058 statistical cells; Benjamini-Yekutieli at FDR 0.05 reported alongside |
| Versions | Python 3.13.1, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, MAPIE 1.6.0, crepes 0.9.1, puncc 0.9.3, TorchCP 1.2.1, torch 2.14.1+cpu, conformcheck 0.1.0.dev0 |
| Hardware | Windows 11, AMD64, 4 worker processes, CPU only |
| Wall time | 45.2 min for the full run, plus 2.4 min to re-run the 61 TorchCP regression units after a diagnostics fix (section 6). `conformcheck plan` had estimated 20 min. |

The plan estimate was low by about a factor of 2.3. It probes only the smallest and
largest `n` of each unit type, and the APS and CV+ units at `n = 999-1000` cost more
than that extrapolation predicts. The run stayed inside the 25-40 min budget in the
design plus about 15%.

### Statuses

Each cell gets one of the following statuses. When several apply, the most severe wins
(listed from most to least severe):

- **ERROR**: the library crashed.
- **FAIL**: under-coverage (statistical rejection or rank deficit).
- **LAW_MISMATCH**: the distribution of covered counts differs from the law although
  the mean is right.
- **CONSERVATIVE**: over-coverage (statistical rejection, or rank surplus found by rank
  recovery).
- **OVER_REFUSED**: the library raised at a level where a finite valid set exists
  (`k <= n`).
- **REFUSED**: the library raised where `k > n`, which is a valid choice.
- **PASS**: none of the above.

## 2. Headline

At n <= 100, **15 of the 31 library-method rows are flagged** in at least one cell.
Flagged means FAIL, CONSERVATIVE, LAW_MISMATCH, OVER_REFUSED or ERROR. Behaviour the
library documents is excused, and only that behaviour: MAPIE documents
`include_last_label=True` as conservative, so that row's CONSERVATIVE cells do not count.
The same row still counts, because it also crashes (F7) and refuses feasible levels
(F4), and MAPIE documents neither.

Of the 2569 library cells:

| Status | Cells |
|---|---|
| PASS | 1765 |
| REFUSED | 380 |
| ERROR | 198 |
| CONSERVATIVE | 105 |
| OVER_REFUSED | 96 |
| FAIL | 25 |

Only one row under-covers: MAPIE APS with `include_last_label=False`, which accounts for
all 25 FAIL cells. They are all on the synthetic `cls_gauss` data. On the digits data
the same row over-covers by a wide margin in all 8 cells (F1). Its coverage follows
the model, not the law. The other flags are of these kinds:

- over-coverage by exactly one order statistic, from floating-point arithmetic on
  `alpha` or from a non-randomized p-value;
- the documented conservatism of `include_last_label=True`;
- a refusal of a feasible level;
- a crash.

The status columns are the worst status over the row's cells with n <= 100 and n > 100,
copied from [matrix.md](docs/results/default/matrix.md).

| Row | Small n | Large n | What |
|---|---|---|---|
| `mapie/aps/include_last_label=False` | ERROR | FAIL | model-dependent coverage: 0.53-0.57 on `cls_gauss` at every n and alpha (FAIL), 0.96-0.97 on digits (CONSERVATIVE) (F1); also F4 and F7 |
| `mapie/aps/include_last_label=True` | ERROR | CONSERVATIVE | conservative, as documented (0.971 vs 0.900 at n = 1000); also crashes (F7) and refuses feasible levels (F4), which are not documented |
| `mapie/aps/include_last_label=randomized` | ERROR | OVER_REFUSED | exact where it runs; crashes when a class is missing from a small calibration set (F7); F4 |
| `mapie/split_abs/default`, `mapie/lac/default`, `mapie/cqr/symmetric` | OVER_REFUSED | OVER_REFUSED | raises for alpha in [1/(n+1), 1/n) (F4) |
| `mapie/cqr/asymmetric` | OVER_REFUSED | REFUSED | raises when n < 2/alpha although the per-side index k' <= n: 5 cells, at n = 9, alpha = 0.2 and n = 19, alpha = 0.1 (F4) |
| `mapie/cv_plus/K=5`, `K=10` | PASS | CONSERVATIVE | lower endpoint one order statistic too high at n = 999, alpha = 0.05 (F5) |
| `crepes/split_abs/default` | CONSERVATIVE | CONSERVATIVE | k + 1 at integer boundaries (F2) |
| `crepes/lac/unsmoothed` | CONSERVATIVE | CONSERVATIVE | same boundary effect for sets (F3) |
| `crepes/class_conditional/unsmoothed` | CONSERVATIVE | - | same boundary effect for sets (F3); run at n <= 99 per class only |
| `puncc/jackknife_plus/K=n` | ERROR | - | crashes on folds of size one, so every cell (F6) |
| `puncc/cv_plus/K=5`, `K=10` | ERROR | ERROR | crash at alpha = 1/(n+1) and on folds of size one; k + 1 at n = 99, 999 (4 CONSERVATIVE cells each) (F6) |
| `torchcp/split_abs/default`, `torchcp/cqr/default` | ERROR | ERROR | crash where k > n instead of returning a trivial interval (F8) |

These rows pass every cell. Some refuse only where `k > n`, which is valid.

- MAPIE jackknife+.
- crepes smoothed LAC and smoothed class-conditional.
- puncc split, CQR, LAC, APS (both settings) and class-conditional LAC.
- TorchCP LAC, APS (both settings) and class-conditional LAC.

## 3. Oracle controls

The reference implementations run through the same adapters, statistics and report
code as the libraries.

**Size.** The reference rows produce:

- 0 Holm rejections in 675 statistical cells;
- 0 non-PASS cells in 889 cells (rank recovery and the trivial-set checks included).

The cell p-value is `2 min(p_mean, p_gof)` of two discrete tests, so it is conservative
by construction and not uniform under the null. The calibration check therefore uses the
exact two-sided mean test alone. It rejects at 0.05 in 19 of 402 exact-law reference
cells (4.7%), against a nominal 5%. This count is descriptive. The cells are not
independent: the alphas of one unit and the reference rows on one DGP use the same
calibration draws (common random numbers), so a binomial test on the count would not
give a valid p-value. The 0 Holm rejections above do not depend on independence.

**Power.** Four deliberately wrong mutants of split regression and LAC are run. Cells
where a mutant happens to use the correct order statistic are excluded. Examples:
`ceil(n(1-alpha)) = ceil((n+1)(1-alpha))` at n = 9, 19, 99, 999 for alpha = 0.1 and
0.2. The counts below are Holm detections / cells:

| Mutant | n = 5-10 | n = 19-20 | n = 49-50 | n = 99-100 | n = 999-1000 |
|---|---|---|---|---|---|
| `k_minus_1` | 32/32 | 29/32 | 25/36 | 18/36 | 6/24 |
| `k_plus_1` | 29/32 | 26/32 | 25/36 | 15/36 | 6/24 |
| `no_correction_linear` | 32/32 | 25/32 | 22/36 | 15/36 | 6/24 |
| `n_instead_of_n_plus_1` | 16/16 | 11/12 | 13/20 | 6/12 | 0/9 |

Rank recovery reads the order statistic off a regression interval. It is deterministic,
and on the continuous-score DGPs it catches every regression mutant cell at every n,
including n = 1000. That is why the "any detection" counts in
[summary.md](docs/results/default/summary.md) are higher. On the tied-score DGP, a
one-step error often selects the same tied value, so the output is identical and
nothing can detect it. The
statistical test alone loses power above n = 100: one order statistic moves coverage by
1/(n+1), which is about 0.001 at n = 999, while the 95% interval half-width there is
about 0.0024. Classification mutants rely on the statistical test only, so a one-step
error in a classifier at n >= 100 can go undetected. Section 7 covers this limitation.

## 4. Findings

The coverage figures below are the mean over 200 draws × 500 test points (fewer test
points on the toy datasets), with a 95% t interval from the empirical spread of the 200
covered counts. Holm p-values are adjusted over all 3058 statistical cells.

### F1. MAPIE APS `include_last_label=False` does not follow the law; its coverage follows the model

On the synthetic `cls_gauss` data it under-covers by 0.25-0.38:

| n | alpha | Exact | Observed [95% CI] |
|---|---|---|---|
| 10 | 0.2 | 0.818 | 0.530 [0.524, 0.537] |
| 19 | 0.1 | 0.900 | 0.554 [0.550, 0.558] |
| 99 | 0.05 | 0.950 | 0.572 [0.568, 0.575] |
| 1000 | 0.1 | 0.900 | 0.560 [0.557, 0.563] |

On the digits data, with an accurate model, it over-covers in all 8 cells:

| n | alpha | Exact | Observed [95% CI] | Holm p |
|---|---|---|---|---|
| 10 | 0.2 | 0.818 | 0.964 [0.962, 0.966] | 3e-303 |
| 19 | 0.1 | 0.900 | 0.974 [0.972, 0.976] | 2e-121 |
| 50 | 0.1 | 0.902 | 0.972 [0.971, 0.974] | 0 |
| 99 | 0.2 | 0.800 | 0.959 [0.958, 0.960] | 0 |

All 25 FAIL cells (all on `cls_gauss`) have Holm p = 0 at double precision. There,
coverage is about 0.53-0.57 whatever the target, from n = 10 to n = 1000. On digits it
is about 0.96-0.97 whatever the target. Neither moves with n or alpha, so this is not a
finite-sample effect: the coverage is set by the model, not by the order statistic.

**Mechanism.** We checked it on the same data against an independent computation and
in MAPIE's source (`conformity_scores/sets/utils.py`). MAPIE's APS calibration scores
are randomized: the cumulative probability up to the true label minus
`U × p(true label)`. With `False`, the test-time rule is deterministic: it keeps the
labels whose cumulative probability stays at or below the threshold, but it always keeps
the top label, since the cut-off is `max(q, smallest cumulative probability)`. The
calibration scores and the prediction rule therefore do not match, and nothing ties
coverage to the order statistic.

- With the `cls_gauss` classifier the true label is often ranked low (see below), so the
  rule drops it far more often than alpha allows.
- With the digits model (top-1 accuracy about 0.96), the sets are mostly the top label
  alone, so coverage is roughly the top-1 accuracy, well above 1 - alpha.

The installed docstring says that `True` and `False` "may result in a coverage higher
than 1 - alpha". The digits cells fit that sentence. The `cls_gauss` cells do not: there
`False` gives far lower coverage, which a user cannot know in advance without
evaluating the model.

**The `cls_gauss` classifier is anti-informative.** Its fixed weights
(`models.FixedClassifier`) do not line up with the class means of the DGP
(`data.CLS_MEANS`). On 100,000 test draws its top-1 accuracy is 0.119, below the 0.25 of
chance. The true label is ranked first, second, third and last in 11.9%, 23.1%, 22.8% and
42.2% of draws, and classes 1 and 2 are predicted as classes 0 and 1 about 91% of the
time. The exact laws hold for any fixed model, so every other result is unaffected. This
choice does, however, maximize the size of the F1 under-coverage. With a reasonable
model the same rule over-covers instead, as the digits cells show.

**Related settings.**

- `include_last_label=True` is CONSERVATIVE in every cell where it runs: 0.971
  [0.970, 0.972] against 0.900 at n = 1000 on `cls_gauss`, and 0.992 against 0.900 at
  n = 99 on digits. MAPIE documents this.
- `"randomized"` matches the exact law wherever it runs, on both datasets: 0.901
  [0.899, 0.904] against 0.900 at n = 999 on `cls_gauss`, and 0.901 [0.896, 0.905] at
  n = 99 on digits.

Repros: `mapie__aps__include_last_label-False__coverage.py` (z = -50.7) and
`mapie__aps__include_last_label-True__coverage.py` (z = +14.4).

### F2. crepes regression uses order statistic k + 1 at integer boundaries (over-coverage)

`WrapRegressor.predict_int` computes the index as `int((1 - confidence)(n + 1))` in
floating point, and `1 - 0.9` evaluates to `0.09999999999999998`. Wherever
`(n + 1) × alpha` is an integer, the index is one too small. The interval then uses the
(k+1)-th smallest score instead of the k-th.

On the continuous-score data (`reg_gauss`, `reg_hetero_t`, diabetes), rank recovery saw
this in 200 of 200 draws in every cell where `(n + 1) alpha` is an integer and alpha is
0.1 or 0.2:

- n = 9, 19, 49, 99, 999 (diabetes: n = 19, 99, the toy sizes);
- the edge level alpha = 1/(n+1) at n = 5 and n = 1000.

On the tied-score DGP (`reg_tied`) the k-th and (k+1)-th smallest scores are often the
same value, so the error is visible only in the draws where they differ: 200 of 200 at
n = 5 (edge level) and n = 9, alpha = 0.1, but only 2 to 29 of 200 in the other
flagged cells (for example 20 of 200 at n = 19, alpha = 0.2), and in none at n = 49 and
99 with alpha = 0.1.

There, crepes returns infinite intervals where the k = n-th score gives a finite valid
one.

It did not appear at the paired n = 10, 20, 50, 100, 1000, or at alpha = 0.05.
`1 - 0.95` rounds upward, so alpha = 0.05 is unaffected.

The over-coverage is 1/(n+1). Examples:

| n | alpha | Exact | Observed [95% CI] | Holm p |
|---|---|---|---|---|
| 19 | 0.1 | 0.900 | 0.949 [0.943, 0.956] | 2e-43 |
| 9 | 0.2 | 0.800 | 0.901 [0.886, 0.915] | 4e-64 |
| 999 | 0.1 | 0.900 | 0.903 [0.900, 0.905] | 1 (rank recovery only) |

The cells are flagged as CONSERVATIVE, not FAIL: the intervals remain valid but are
wider than necessary. The pattern matches DESIGN hypothesis 1 exactly.

Repro: `crepes__split_abs__default__rank.py`. At n = 9, alpha = 0.2 it uses order
statistic 9 instead of 8.

### F3. crepes unsmoothed classification is conservative at the same boundaries

`crepes/lac/unsmoothed` and `crepes/class_conditional/unsmoothed` are CONSERVATIVE at
the same integer boundaries. Holm p runs from 2.4e-5 (n = 99) down to 0 at double
precision (n <= 19). Examples on the synthetic data:

| Row | n | alpha | Exact | Observed [95% CI] |
|---|---|---|---|---|
| `crepes/lac/unsmoothed` | 19 | 0.1 | 0.900 | 0.947 [0.940, 0.954] |
| `crepes/lac/unsmoothed` | 9 | 0.2 | 0.800 | 0.894 [0.881, 0.908] |
| `crepes/class_conditional/unsmoothed` (n per class) | 19 | 0.1 | 0.900 | 0.950 [0.946, 0.953] |

On the digits data at n = 19, alpha = 0.1, `crepes/lac/unsmoothed` gives 0.948.

The unsmoothed set is `{y : p(y) >= 1 - confidence}` with a non-randomized p-value. At
an integer boundary this includes the (k+1)-th statistic, so the effect would remain
even in exact arithmetic. This is DESIGN hypothesis 2. The smoothed rows pass every
cell, for example 0.900 at n = 999, alpha = 0.1.

Repro: `crepes__lac__unsmoothed__coverage.py` (z = +15.4 at n = 9, alpha = 0.2).

### F4. MAPIE refuses feasible levels alpha in [1/(n+1), 1/n)

MAPIE's split regressor, LAC and APS classifiers and symmetric CQR raise ValueError
("Number of samples of the score is too low ... must be lower than the number of
samples") at alpha = 1/(n+1). That level has `k = n`, and a finite valid set exists. The
cause is a check that requires `n >= 1/alpha` rather than `(n+1)(1-alpha) <= n`.

For these rows this is OVER_REFUSED at alpha = 1/(n+1) at every n from 5 to 1000. It is
not unsafe, but the user gets no set at all.

The asymmetric CQR variant is different. It applies the check to alpha/2, so it raises
whenever n < 2/alpha. At alpha = 1/(n+1) the per-side index k' exceeds n, so its
refusal there is valid (REFUSED). It over-refuses only when 1/(n+1) <= alpha/2 < 1/n,
where `k' = ceil((n+1)(1 - alpha/2)) = n` is feasible. In this grid that is 5 cells:
n = 9 with alpha = 0.2, and n = 19 with alpha = 0.1, on the DGPs where those sizes run.

**Related: `allow_infinite_bounds=True`.** `SplitConformalRegressor.predict_interval`
documents this option as allowing infinite bounds. With it set, the split regressor
still raises where k > n instead of returning (-inf, inf). The message says to "set
unbounded=True", which is an internal argument the public option does not forward to.
This is REFUSED, not unsafe. `CrossConformalRegressor` honours the option.

Repros:

- `mapie__split_abs__default__raises.py`
- `mapie__lac__default__raises.py`
- `mapie__cqr__symmetric__raises.py`
- `mapie__cqr__asymmetric__raises.py`
- `mapie__aps__include_last_label-*__raises-2.py`
- `manual__mapie__split_abs__allow_infinite_bounds.py` (hand-written)

### F5. MAPIE CV+ lower endpoint off by one at n = 999, alpha = 0.05 (over-coverage)

With the constant model, CV+ is exactly split conformal on all n points (DESIGN 3.4), so
both endpoints must use the k-th smallest |y|. At n = 999, alpha = 0.05, for both K = 5
and K = 10, the lower endpoint uses 951 instead of 950 in 200 of 200 draws. The upper
endpoint is correct.

Coverage is 0.9508 [0.9491, 0.9526] against 0.9500. Monte Carlo cannot see this; only
rank recovery does.

The likely cause is floating point in MAPIE's lower-quantile level
`alpha_ref = (1 - 2 alpha) × reverse + alpha` used for the two-sided "plus" quantiles.
No other cell of either row is affected, and jackknife+ passes everywhere.

Repro: `mapie__cv_plus__K-5__rank.py` and `K-10`, deterministic. It prints lower 951,
upper 950, expected 950.

### F6. puncc CV+ and jackknife+ crash in three settings and are off by one at boundaries

- **Every fold of size one crashes.** `CVPlus` raises
  `TypeError: object of type 'numpy.float64' has no len()` whenever a fold holds a
  single point. That covers `K = n` (jackknife+), so all 66 jackknife+ cells are ERROR,
  and also `K = 10` at n = 19.
- **alpha = 1/(n+1) crashes.** At that level the quantile level `(1 - alpha)(1 + 1/n)`
  equals 1, and puncc raises
  `ValueError: All coordinates of [q] must be in the open interval (0, 1)`. This happens
  at n = 20, 49, 50, 99, 100, 999 for K = 5 and K = 10, although k = n is feasible.
- **One order statistic too high.** At n = 99 and n = 999 with alpha in {0.1, 0.2}, both
  endpoints use k + 1 in 200 of 200 draws. The likely cause is floating point in
  `(1 - alpha)(1 + 1/n)`, as in F2. Coverage moves by 1/(n+1), for example 0.909
  [0.905, 0.914] against 0.900 at n = 99.

All six puncc repros were re-run under puncc's declared `numpy<2` (Python 3.12, numpy
1.26.4) and reproduce there; see `puncc_numpy1_recheck.txt`.

Repros:

- `puncc__jackknife_plus__K-n__raises.py`
- `puncc__cv_plus__K-10__raises.py` (fold of size one)
- `puncc__cv_plus__K-5__raises.py` and `puncc__cv_plus__K-10__raises-2.py` (q = 1)
- `puncc__cv_plus__K-5__rank.py` and `puncc__cv_plus__K-10__rank.py`

### F7. MAPIE APS crashes when a class is missing from a small calibration set

At n = 5 (33 of 200 draws) and n = 9 (1 of 200), the calibration labels can contain only
two of the four classes. MAPIE then infers a binary target and raises "Invalid
conformity score for binary target". It does this although the prefit classifier
declares four classes. One failed draw marks the whole cell ERROR.

Repro: `mapie__aps__include_last_label-*__raises.py`. Seed 3 at n = 5 raises.

### F8. TorchCP split regression and CQR crash where k > n

At every cell with k > n, for example n = 19, alpha = 0.045, `SplitPredictor.predict`
raises `AttributeError: 'float' object has no attribute 'shape'`. The threshold is the
Python float `torch.inf`, not a tensor.

The design predicted a trivial interval with a warning (hypothesis 4). TorchCP's
classifiers return full sets correctly in the same situation. Everywhere else, both
TorchCP regression rows are exact, including on the diabetes data.

Repros: `torchcp__split_abs__default__raises.py` and `torchcp__cqr__default__raises.py`.

## 5. Pre-registered hypotheses

| # | Hypothesis | Verdict |
|---|---|---|
| 1 | crepes regression is conservative by one order statistic at integer boundaries | **Confirmed** (F2). Exactly the predicted cells (n in {9, 19, 49, 99, 999}, alpha in {0.1, 0.2}), not the paired n, plus the edge level alpha = 1/(n+1) at n = 5 and 1000. |
| 2 | crepes unsmoothed classification is conservative at integer boundaries | **Confirmed** (F3). Smoothed rows pass. |
| 3 | MAPIE APS `True` conservative, `False` under-covers, `"randomized"` passes | **Partly refuted: model-dependent** (F1). `True` is conservative and `"randomized"` passes in every cell where they run (both are also affected by F4 and F7). `False` under-covers on `cls_gauss`, whose classifier is anti-informative, but over-covers by a wide margin on digits. It does not follow the law in either direction. |
| 4 | k > n behaviour differs, and all libraries are valid | **Partly refuted.** puncc refuses (valid). crepes returns trivial sets (valid, with a warning). MAPIE refuses even with `allow_infinite_bounds=True` on the split regressor (F4). TorchCP regression crashes (F8), while its classifiers return full sets. |
| 5 | MAPIE asymmetric CQR has coverage (2k' - (n+1))/(n+1) | **Confirmed where it runs.** For example 0.9177 [0.9124, 0.9230] against 0.92 at n = 49, alpha = 0.1, with rank recovery exact per side. It over-refuses some feasible levels (F4). |
| 6 | MAPIE RAPS follows the law with n_eff = n - ceil(0.2 n) | **Not tested.** RAPS was cut from v0.1 (DESIGN section 2). |
| 7 | TorchCP float32 creates ties at large n | **No evidence.** TorchCP LAC and randomized APS pass at n = 1000, and LAC bracketing gives offset 0 in all draws. The only float32 effect seen was in conformcheck's own rank tolerance (section 6), not in TorchCP's coverage. |

## 6. Checks against adapter mistakes

- **Documented usage.** Every adapter is tested against the library's documented usage
  written out by hand on the same data (`tests/test_adapters.py`). For example, MAPIE's
  `SplitConformalRegressor` with `prefit=True` gives identical arrays.
- **Standalone repros.** Every finding was reproduced by a script that does not import
  conformcheck. Those scripts call the public API directly with a fixed model.
- **F1 cross-check.** MAPIE's sets were compared with an independent APS computation on
  the same data, and the randomized calibration scores were inspected directly.
- **TorchCP CQR artifact.** The first report showed 7 FAIL cells for `torchcp/cqr` on
  the diabetes data. They came from conformcheck's rank tolerance (`1e-6 × |q|`), which
  was too tight for a float32 interval endpoint near 150 minus a float64 prediction.
  Their coverage matched the law (Holm p = 1). The tolerance now scales with the
  magnitude of the endpoints. The 61 TorchCP regression units were re-run, and those
  cells now pass. This was a bug in conformcheck, not in TorchCP.
- **Review corrections (report only, same run).** A review of the first version of this
  report led to these changes, all rebuilt from the same committed `units.jsonl.gz`
  without re-running any library:
  - coverage intervals are now t intervals from the empirical spread of the counts. The
    first version used the variance of the exact law, which is the null variance and
    the wrong spread in the cells where an interval matters. No status or p-value
    changed;
  - the headline excuses a documented row only for its documented status, which moved
    it from 14 to 15 rows;
  - F1 now reports the digits cells, where the same setting over-covers;
  - the size check is reported as a count without a binomial p-value, because the
    cells share calibration draws.
- **Earlier fixes.** Two earlier pipeline errors were fixed before the final run:
  - interval half-widths had hidden one-sided off-by-ones, so rank recovery became
    per-endpoint;
  - a zero-variance t-test had flagged all-covered bound cells.

  See the git history.

## 7. Limitations

- **Monte Carlo power falls with n.** With R = 200 and m = 500, a one-order-statistic
  error is statistically invisible above roughly n = 100 (power table in section 3).
  Rank recovery closes this gap for split regression, CQR and CV+/jackknife+ with the
  constant model, but not for classification. A one-step error in a classifier at
  n = 1000 would be missed. The `full` study (R = 2000, m = 1000) has more power but was
  not run.
- **Tests on the mean.** The exact law is tested through the mean of covered counts and
  a goodness-of-fit test on their distribution. Rows whose law is only a bound (CV+ and
  jackknife+ with a real model) or a mean (asymmetric CQR, smoothed p-values) get a
  one-sided t-test or a mean test only. A library could have the right mean and the
  wrong spread there.
- **One-sided cells cannot flag over-coverage.** Deterministic APS has an atom in its
  score distribution, so it is tested one-sided. This hides large over-coverage, for
  example:
  - puncc APS `rand=False` covers 1.000 against 0.80 at n = 1000;
  - TorchCP APS `randomized=False` covers 0.95 against 0.80.

  Both are valid. The reference deterministic APS gives 0.946 in the same cell, so
  puncc's sets are wider than the reference, but the oracle does not grade this.
- **The model shapes effect sizes, and for F1 the direction.** The `cls_gauss`
  classifier is a fixed softmax model that is anti-informative (top-1 accuracy 0.119
  against 0.25 for chance; F1). That makes the deterministic-APS score atom large and
  maximizes the F1 under-coverage. With the accurate digits model the same MAPIE setting
  over-covers. The exact laws hold for any fixed model, so the other findings do not
  depend on this choice. No synthetic DGP with an informative classifier was run; digits
  is the only informative-model comparison.
- **CV+ bounds where K does not divide n.** Barber et al. (2021, Thm 4) assume folds of
  equal size n/K. The `lower` cells of CV+ with a real model at n = 19, 49, 99 and 999
  apply the same formula with n/K as a fraction, which is an extrapolation. All of those
  cells pass, so no result depends on it.
- **A single seed.** The run uses one seed and one machine (Windows, CPU). The
  deterministic findings (F2, F4, F5, F6, F8) do not depend on the seed. The statistical
  ones have Holm p far below the threshold.
- **puncc under numpy 2.** puncc declares `numpy<2`, and the main run used numpy 2.5.4
  through a lockfile override. Every puncc finding was re-checked under numpy 1.26.4, but
  the PASS cells of puncc were not.
- **Not covered:**
  - RAPS, time-series methods, weighted conformal and conformal risk control;
  - GPU runs;
  - class-conditional methods on the digits data;
  - mondrian/conditional regression.
- **The plan estimate was low.** It predicted 20 min for a 45 min run. Treat it as a
  lower bound until the probe covers mid-range n.
- **CI has never run.** The workflow (pull_request and workflow_dispatch) is configured
  but has never run, because the repository has not been pushed. All tests were run
  locally only.
- **Library versions move.** These are statements about MAPIE 1.6.0, crepes 0.9.1,
  puncc 0.9.3 and TorchCP 1.2.1. Re-run `conformcheck repro --verify` against newer
  versions before citing a finding.

## 8. Reproducing

```sh
uv sync --all-extras
uv run conformcheck plan --study default
uv run python scripts/run_study.py --study default --out runs/default
uv run conformcheck report runs/default
uv run conformcheck repro runs/default --verify
```

To rebuild the report from the committed per-unit records without re-running, gunzip
`docs/results/default/units.jsonl.gz` into `runs/default/units.jsonl`, copy
`run.json` next to it, and run `conformcheck report runs/default`.
