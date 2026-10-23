# conformcheck default study: report

This report covers the `default` study as of round 2 (2026-10-24). It runs four Python
conformal-prediction libraries (37 library-method rows) and a set of reference and mutant
rows through the exact finite-sample laws of split conformal prediction. All numbers
below come from [docs/results/default](docs/results/default). Each finding has a
standalone repro script in [docs/results/default/repros](docs/results/default/repros).
The scripts depend only on numpy, scikit-learn and the library concerned, and exit 1
while the problem reproduces.

The design, the formulas and the pre-registered hypotheses are in
[docs/DESIGN.md](docs/DESIGN.md); section 14 there is the round-2 addendum, committed
before the round-2 run.

**Round 2 in brief.** RAPS rows were added (hypothesis 6 is now tested), bracketing
became rank recovery for classification (one-step classifier errors are now caught at any
`n`), and a synthetic DGP with an informative classifier was added. There are two new
findings (F9, F10), F1 and F3 are extended, and one round-2 hypothesis is refuted
(section 5).

## 1. What ran

| | |
|---|---|
| Study | `default` (`src/conformcheck/studies/default.toml`), fingerprint `cbfed0fa569dc01f` |
| Repetitions | R = 200 calibration draws per cell, m = 500 test points per draw (capped by the pool on the toy datasets) |
| Seed | 20261023; common random numbers across libraries (`SeedSequence([seed, crc32(dgp), n, rep])`) |
| n | 5, 9, 10, 19, 20, 49, 50, 99, 100, 999, 1000 (split); 9 to 99 (jackknife+); 19 to 1000 (CV+, K = 5, 10); 5 to 99 per class (class-conditional); 10, 19, 50, 99 (toy data) |
| alpha | 0.05, 0.1, 0.2, plus the edge levels 1/(n+1) (k = n) and 0.9/(n+1) (k = n + 1, trivial set required) |
| DGPs | Gaussian and heteroscedastic-t regression, tied scores, constant model (jackknife+/CV+), four-class Gaussian classification with two fixed models (`cls_gauss`: anti-informative; `cls_gauss_inf`: Bayes posterior), random splits of scikit-learn's diabetes and digits |
| Size | 1412 units, 6302 cells (3889 library cells), 4348 statistical cells |
| Multiple testing | Holm at FWER 0.05 over all 4348 statistical cells; Benjamini-Yekutieli at FDR 0.05 reported alongside |
| Versions | Python 3.13.1, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1, MAPIE 1.6.0, crepes 0.9.1, puncc 0.9.3, TorchCP 1.2.1, torch 2.14.1+cpu |
| Hardware | Windows 11, AMD64, CPU only |

**How the run was assembled.** Unit ids depend only on the unit, `R`, `m` and the seed,
and every unit is deterministic given its seed. The round-2 run directory therefore
started from the 779 v0.1 units (2026-10-23; 4 workers, 45.2 min plus 2.4 min for the
whole v0.1 run) that no round-2 change touches. Then, with 3 workers:

1. 205 LAC and class-conditional units were re-run for the corrected bracketing, plus 120
   new RAPS units: 18.0 min. Every re-run unit reproduced its v0.1 covered counts and
   error counts exactly (205 of 205).
2. 308 units on the new `cls_gauss_inf` DGP: 8.6 min.

`conformcheck plan` now also probes the middle `n` of each group (v0.1 probed only the
smallest and largest and estimated 20 min for a 45 min run). To repeat the whole study
from scratch, see section 8.

### Statuses

Each cell gets one of the following statuses. When several apply, the most severe wins
(listed from most to least severe):

- **ERROR**: the library crashed.
- **FAIL**: under-coverage (statistical rejection, or a rank deficit found by rank
  recovery or bracketing).
- **LAW_MISMATCH**: the distribution of covered counts differs from the law although
  the mean test alone does not reject.
- **CONSERVATIVE**: over-coverage (statistical rejection, or a rank surplus found by
  rank recovery or bracketing).
- **OVER_REFUSED**: the library raised at a level where a finite valid set exists
  (`k <= n`).
- **REFUSED**: the library raised where `k > n`, which is a valid choice.
- **PASS**: none of the above.

## 2. Headline

At n <= 100, **18 of the 37 library-method rows are flagged** in at least one cell:
the same 15 of the 31 v0.1 rows, plus 3 of the 6 new RAPS rows. Flagged means FAIL,
CONSERVATIVE, LAW_MISMATCH, OVER_REFUSED or ERROR. Behaviour the library documents is
excused, and only that behaviour: MAPIE documents `include_last_label=True` as
conservative, so the CONSERVATIVE cells of the APS and RAPS rows with that setting do not
count. Both rows still count, because they also crash or refuse feasible levels, which
MAPIE does not document.

Of the 3889 library cells:

| Status | Cells |
|---|---|
| PASS | 2533 |
| REFUSED | 572 |
| ERROR | 344 |
| CONSERVATIVE | 235 |
| OVER_REFUSED | 155 |
| FAIL | 48 |
| LAW_MISMATCH | 2 |

Only one row under-covers: MAPIE APS with `include_last_label=False`, which accounts for
all 48 FAIL cells (25 on `cls_gauss`, 23 on `cls_gauss_inf`). On the digits data the same
row over-covers (F1). The other flags are of these kinds:

- over-coverage by exactly one order statistic, from floating-point arithmetic on
  `alpha` or from a non-randomized p-value;
- a randomized set rule that does not match its own score (F10), or the documented
  conservatism of `include_last_label=True`;
- a refusal of a feasible level;
- a crash.

The status columns are the worst status over the row's cells with n <= 100 and n > 100,
copied from [matrix.md](docs/results/default/matrix.md).

| Row | Small n | Large n | What |
|---|---|---|---|
| `mapie/aps/include_last_label=False` | ERROR | FAIL | model-dependent coverage: 0.52-0.57 on `cls_gauss`, 0.74-0.87 on `cls_gauss_inf` (FAIL), 0.96-0.97 on digits (CONSERVATIVE) (F1); also F4 and F7 |
| `mapie/aps/include_last_label=True` | ERROR | CONSERVATIVE | conservative, as documented (0.971 vs 0.900 at n = 1000); also crashes (F7) and refuses feasible levels (F4), which are not documented |
| `mapie/aps/include_last_label=randomized` | ERROR | OVER_REFUSED | exact where it runs; crashes when a class is missing from a small calibration set (F7); F4 |
| `mapie/raps/include_last_label=True` | ERROR | CONSERVATIVE | conservative, as documented (0.961 vs 0.900 at n = 1000 on `cls_gauss_inf`); raises at n <= 20 with 4 classes and refuses feasible levels (F9) |
| `mapie/raps/include_last_label=randomized` | ERROR | REFUSED | exact where it runs, at its effective calibration size; raises at small n and refuses feasible levels (F9) |
| `mapie/split_abs/default`, `mapie/lac/default`, `mapie/cqr/symmetric` | OVER_REFUSED | OVER_REFUSED | raises for alpha in [1/(n+1), 1/n) (F4) |
| `mapie/cqr/asymmetric` | OVER_REFUSED | REFUSED | raises when n < 2/alpha although the per-side index k' <= n: 5 cells, at n = 9, alpha = 0.2 and n = 19, alpha = 0.1 (F4) |
| `mapie/cv_plus/K=5`, `K=10` | PASS | CONSERVATIVE | lower endpoint one order statistic too high at n = 999, alpha = 0.05 (F5) |
| `crepes/split_abs/default` | CONSERVATIVE | CONSERVATIVE | k + 1 at integer boundaries (F2) |
| `crepes/lac/unsmoothed` | CONSERVATIVE | CONSERVATIVE | same boundary effect for sets, now also seen by bracketing at n = 99 and 999 (F3) |
| `crepes/class_conditional/unsmoothed` | CONSERVATIVE | - | same boundary effect for sets (F3); run at n <= 99 per class only |
| `puncc/raps/rand=True` | LAW_MISMATCH | CONSERVATIVE | the randomized set rule does not match puncc's own RAPS score: 0.990 vs 0.900 on `cls_gauss`, 0.917 vs 0.900 on `cls_gauss_inf` (F10) |
| `puncc/jackknife_plus/K=n` | ERROR | - | crashes on folds of size one, so every cell (F6) |
| `puncc/cv_plus/K=5`, `K=10` | ERROR | ERROR | crash at alpha = 1/(n+1) and on folds of size one; k + 1 at n = 99, 999 (4 CONSERVATIVE cells each) (F6) |
| `torchcp/split_abs/default`, `torchcp/cqr/default` | ERROR | ERROR | crash where k > n instead of returning a trivial interval (F8) |

These rows pass every cell. Some refuse only where `k > n`, which is valid.

- MAPIE jackknife+.
- crepes smoothed LAC and smoothed class-conditional.
- puncc split, CQR, LAC, APS (both settings), deterministic RAPS and class-conditional
  LAC.
- TorchCP LAC, APS (both settings), RAPS (both settings) and class-conditional LAC.

## 3. Oracle controls

The reference implementations run through the same adapters, statistics and report
code as the libraries.

**Size.** The reference rows produce:

- 0 Holm rejections in 1010 statistical cells;
- 0 non-PASS cells in 1329 cells (rank recovery, bracketing and the trivial-set checks
  included).

The cell p-value is `2 min(p_mean, p_gof)` of two discrete tests, so it is conservative
by construction and not uniform under the null. The calibration check therefore uses the
exact two-sided mean test alone. It rejects at 0.05 in 20 of 562 exact-law reference
cells (3.6%), against a nominal 5%. This count is descriptive. The cells are not
independent: the alphas of one unit and the reference rows on one DGP use the same
calibration draws (common random numbers), so a binomial test on the count would not
give a valid p-value. The 0 Holm rejections above do not depend on independence.

**Power.** Four deliberately wrong mutants of split regression and of LAC are run. Cells
where a mutant happens to use the correct order statistic are excluded. Examples:
`ceil(n(1-alpha)) = ceil((n+1)(1-alpha))` at n = 9, 19, 99, 999 for alpha = 0.1 and
0.2. The counts below are detections / cells by the Holm test alone and, in brackets, by
any check (adding rank recovery for regression and bracketing for LAC):

| Mutant | n = 5-10 | n = 19-20 | n = 49-50 | n = 99-100 | n = 999-1000 |
|---|---|---|---|---|---|
| split `k_minus_1` | 23/23 (23) | 20/23 (23) | 16/26 (20) | 12/26 (20) | 4/16 (16) |
| split `k_plus_1` | 20/23 (23) | 17/23 (23) | 16/26 (22) | 9/26 (22) | 4/16 (16) |
| LAC `k_minus_1` | 16/16 (16) | 16/16 (16) | 17/18 (18) | 11/18 (18) | 4/16 (16) |
| LAC `k_plus_1` | 16/16 (16) | 16/16 (16) | 17/18 (18) | 10/18 (18) | 4/16 (16) |
| LAC `no_correction_linear` | 16/16 (16) | 14/16 (16) | 13/18 (18) | 9/18 (18) | 4/16 (16) |
| LAC `n_instead_of_n_plus_1` | 8/8 (8) | 6/6 (6) | 9/10 (10) | 2/6 (6) | 0/6 (6) |

The per-n counts for every mutant are in [summary.md](docs/results/default/summary.md).
The statistical test alone loses power above n = 100: one order statistic moves coverage
by 1/(n+1), about 0.001 at n = 999, while the 95% interval half-width there is about
0.0024.

- **Regression.** Rank recovery reads the order statistic off an interval. On the
  continuous-score DGPs it catches every regression mutant cell at every n, including
  n = 1000. On the tied-score DGP a one-step error often selects the same tied value, so
  the output is identical and nothing can detect it; those cells are the gaps in the
  bracketed counts.
- **Classification (new in round 2).** Bracketing places the threshold between the
  largest included and the smallest excluded `1 - p` score among all labels of all test
  points, and maps that to a range of calibration order statistics. A one-step error is
  visible in a repetition whenever a test score falls between `s_(k)` and its neighbour.
  At n = 999-1000 that happened in roughly half of the 200 repetitions, so every LAC
  mutant cell is caught. In v0.1 bracketing was diagnostic only, and a bug hid positive
  offsets (section 6).

## 4. Findings

The coverage figures below are the mean over 200 draws × 500 test points (fewer test
points on the toy datasets), with a 95% t interval from the empirical spread of the 200
covered counts. Holm p-values are adjusted over all 4348 statistical cells.

### F1. MAPIE APS `include_last_label=False` does not follow the law; its coverage follows the model

On the synthetic `cls_gauss` data (anti-informative classifier, see below) it
under-covers by 0.25-0.38:

| n | alpha | Exact | Observed [95% CI] |
|---|---|---|---|
| 10 | 0.2 | 0.818 | 0.530 [0.524, 0.537] |
| 19 | 0.1 | 0.900 | 0.554 [0.550, 0.558] |
| 99 | 0.05 | 0.950 | 0.572 [0.568, 0.575] |
| 1000 | 0.1 | 0.900 | 0.560 [0.557, 0.563] |

On `cls_gauss_inf` (the same data distribution with the Bayes-posterior classifier, top-1
accuracy 0.708) it still under-covers, by 0.05-0.11, in all 23 cells where it runs on the
base alphas (the cells at n <= 10 are ERROR, F7):

| n | alpha | Exact | Observed [95% CI] | Holm p |
|---|---|---|---|---|
| 19 | 0.2 | 0.800 | 0.750 [0.745, 0.755] | 2e-62 |
| 20 | 0.1 | 0.905 | 0.811 [0.803, 0.818] | 4e-110 |
| 100 | 0.05 | 0.950 | 0.855 [0.850, 0.860] | 0 |
| 999 | 0.1 | 0.900 | 0.792 [0.789, 0.795] | 0 |

On the digits data (top-1 accuracy about 0.96) it over-covers in all 8 cells:

| n | alpha | Exact | Observed [95% CI] | Holm p |
|---|---|---|---|---|
| 10 | 0.2 | 0.818 | 0.964 [0.962, 0.966] | 3e-303 |
| 19 | 0.1 | 0.900 | 0.974 [0.972, 0.976] | 2e-121 |
| 50 | 0.1 | 0.902 | 0.972 [0.971, 0.974] | 0 |
| 99 | 0.2 | 0.800 | 0.959 [0.958, 0.960] | 0 |

Every FAIL cell has Holm p below 1e-60. Coverage does not move with n in any of the three
settings, so this is not a finite-sample effect. On `cls_gauss` and digits it barely
moves with alpha either; on `cls_gauss_inf` it rises with 1 - alpha (0.74, 0.79, 0.85
for alpha = 0.2, 0.1, 0.05 at n = 999) but stays 0.05-0.11 below it.

**Mechanism.** We checked it on the same data against an independent computation and
in MAPIE's source (`conformity_scores/sets/utils.py`). MAPIE's APS calibration scores
are randomized: the cumulative probability up to the true label minus
`U × p(true label)`. With `False`, the test-time rule is deterministic: it keeps the
labels whose cumulative probability stays at or below the threshold, but it always keeps
the top label, since the cut-off is `max(q, smallest cumulative probability)`. The
calibration scores and the prediction rule therefore do not match, and nothing ties
coverage to the order statistic. Dropping the label that crosses the threshold loses
coverage; always keeping the top label adds it. Which effect wins depends on how often
the true label is ranked first:

- with the `cls_gauss` classifier the true label is often ranked low (see below), so the
  rule drops it far more often than alpha allows;
- with the Bayes-posterior classifier the true label is first 71% of the time, and the
  rule still drops it too often, by less;
- with the digits model the sets are mostly the top label alone, so coverage is roughly
  the top-1 accuracy, well above 1 - alpha.

The installed docstring says that `True` and `False` "may result in a coverage higher
than 1 - alpha". The digits cells fit that sentence. The two synthetic settings do not:
there `False` gives lower coverage, which a user cannot know in advance without
evaluating the model. Round-2 hypothesis 8 predicted over-coverage on `cls_gauss_inf`;
it is refuted (section 5).

**The `cls_gauss` classifier is anti-informative.** Its fixed weights
(`models.FixedClassifier`) do not line up with the class means of the DGP
(`data.CLS_MEANS`). On 100,000 test draws its top-1 accuracy is 0.118, below the 0.25 of
chance. The true label is ranked first, second, third and last in 11.8%, 23.1%, 23.1% and
42.0% of draws. The exact laws hold for any fixed model, so the law-based findings are
unaffected, but this choice maximizes the size of model-dependent effects (F1, F10).
`cls_gauss_inf` was added in round 2 for that reason: it ranks the true label first,
second, third and last in 70.8%, 21.3%, 5.4% and 2.5% of draws.

**Related settings.**

- `include_last_label=True` is CONSERVATIVE in every cell where it runs: 0.971
  [0.970, 0.972] against 0.900 at n = 1000 on `cls_gauss`, 0.958 [0.956, 0.959] on
  `cls_gauss_inf`, and 0.992 against 0.900 at n = 99 on digits. MAPIE documents this.
- `"randomized"` matches the exact law wherever it runs, on all three datasets: 0.901
  [0.899, 0.904] against 0.900 at n = 999 on `cls_gauss`, 0.900 [0.898, 0.903] at
  n = 1000 on `cls_gauss_inf`, and 0.901 [0.896, 0.905] at n = 99 on digits.

Repros: `mapie__aps__include_last_label-False__coverage.py` and
`mapie__aps__include_last_label-True__coverage.py` (on `cls_gauss`).

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
99 with alpha = 0.1. There, crepes returns infinite intervals where the k = n-th score
gives a finite valid one.

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
the same integer boundaries. Examples on the synthetic data:

| Row | n | alpha | Exact | Observed [95% CI] |
|---|---|---|---|---|
| `crepes/lac/unsmoothed` | 19 | 0.1 | 0.900 | 0.947 [0.940, 0.954] |
| `crepes/lac/unsmoothed` | 9 | 0.2 | 0.800 | 0.894 [0.881, 0.908] |
| `crepes/class_conditional/unsmoothed` (n per class) | 19 | 0.1 | 0.900 | 0.950 [0.946, 0.953] |

On the digits data at n = 19, alpha = 0.1, `crepes/lac/unsmoothed` gives 0.948.

**Bracketing (round 2).** The order statistic is now also read off the sets. It is
k + 1 at exactly the boundary cells and nowhere else, on all three classification
datasets:

- in 183 to 200 of 200 draws at n <= 99 (per class for the class-conditional row);
- in 94 to 147 of 200 draws at n = 999, alpha in {0.1, 0.2}, where the statistical test
  has no power (Holm p = 1; for example 0.8996 against 0.9000 on `cls_gauss`). The other
  draws show no offset because no test score fell between the two order statistics, not
  because the right one was used.

The unsmoothed set is `{y : p(y) >= 1 - confidence}` with a non-randomized p-value. At
an integer boundary this includes the (k+1)-th statistic, so the effect would remain
even in exact arithmetic. This is DESIGN hypothesis 2. The smoothed rows pass every
cell, for example 0.900 at n = 999, alpha = 0.1.

Repro: `crepes__lac__unsmoothed__coverage.py` (n = 9, alpha = 0.2).

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

At n = 5 (33 of 200 draws on `cls_gauss`, 32 on `cls_gauss_inf`), n = 9 (1 and 3 of 200)
and n = 10 (0 and 1 of 200), the calibration labels can contain only two of the four
classes. MAPIE then infers a binary target and raises "Invalid conformity score for
binary target". It does this although the prefit classifier declares four classes. One
failed draw marks the whole cell ERROR.

Repro: `mapie__aps__include_last_label-*__raises.py`. Seed 3 at n = 5 raises.

### F8. TorchCP split regression and CQR crash where k > n

At every cell with k > n, for example n = 19, alpha = 0.045, `SplitPredictor.predict`
raises `AttributeError: 'float' object has no attribute 'shape'`. The threshold is the
Python float `torch.inf`, not a tensor.

The design predicted a trivial interval with a warning (hypothesis 4). TorchCP's
classifiers return full sets correctly in the same situation. Everywhere else, both
TorchCP regression rows are exact, including on the diabetes data.

Repros: `torchcp__split_abs__default__raises.py` and `torchcp__cqr__default__raises.py`.

### F9. MAPIE RAPS ignores `size_raps`, calibrates on n - ceil(0.1 n) points and needs n >= 31 with 4 classes (round 2)

`RAPSConformityScore` documents `size_raps` (default 0.2) as the share of the
conformalization data held out to tune lambda and k_reg. In MAPIE 1.6.0,
`SplitConformalClassifier.conformalize` calls `set_external_attributes` without it, which
resets `size_raps` to None. scikit-learn's `StratifiedShuffleSplit` then uses its default
test share, 0.1. A user who passes `RAPSConformityScore(size_raps=0.5)` gets a hold-out of
10 points at n = 100, not 50, and finds `size_raps` set to None on their own object.
Repro: `manual__mapie__raps__size_raps_ignored.py` (deterministic; it reads only public
attributes of the user's score object).

Consequences seen in the study:

- **Effective calibration size.** In every repetition MAPIE calibrated on exactly
  `n - ceil(0.1 n)` points (89 at n = 99, 900 at n = 1000; column `effective_n` in
  `cells.csv`). The randomized rule matches the exact law at that size in all 26 cells
  where it runs, on all three datasets (for example 0.9005 [0.8982, 0.9028] against
  0.9001 at n = 1000 on `cls_gauss_inf`). Hypothesis 6 is discussed in section 5.
- **It raises at small n.** The stratified hold-out needs at least one point per class
  and at least two points per class overall. With 4 classes it raises in every
  repetition at n <= 20 ("The test_size = 2 should be greater or equal to the number of
  classes = 4", or "The least populated classes in y have only 1 member"), and with the
  10 digits classes at n <= 50. These exceptions come from scikit-learn and do not name
  the cause in MAPIE's terms; the matrix records them as ERROR (52 cells per row).
- **It refuses levels that are feasible.** MAPIE's level check runs on the hold-out
  size: it requires `1/alpha <= ceil(0.1 n)`. At n = 49 and 50 that refuses alpha = 0.1
  and 0.05, although `k_eff <= n_eff` (OVER_REFUSED, 12 cells per row).
- `include_last_label=True` is conservative, as for APS and as documented: 0.961
  [0.960, 0.963] against 0.900 at n = 1000 on `cls_gauss_inf`.

None of this makes MAPIE's RAPS sets invalid where they are returned. The finding is a
silently ignored parameter, plus a minimum sample size that the user meets as a
scikit-learn error.

Generated repros: `mapie__raps__include_last_label-*__raises*.py` (the level check and
the two scikit-learn errors) and `mapie__raps__include_last_label-True__coverage.py`.

### F10. puncc randomized RAPS: the set rule does not match puncc's own score (over-coverage, round 2)

`puncc/raps/rand=True` (lambda = 0.1, k_reg = 1) is CONSERVATIVE in 63 cells and
LAW_MISMATCH in 2, and the size of the effect depends on the model:

| Data | n | alpha | Exact | Observed [95% CI] | Holm p |
|---|---|---|---|---|---|
| `cls_gauss` | 19 | 0.1 | 0.900 | 0.990 [0.988, 0.992] | 0 |
| `cls_gauss` | 1000 | 0.2 | 0.800 | 0.980 [0.979, 0.980] | 0 |
| `cls_gauss_inf` | 99 | 0.1 | 0.900 | 0.917 [0.913, 0.921] | 1e-10 |
| `cls_gauss_inf` | 1000 | 0.2 | 0.800 | 0.827 [0.824, 0.830] | 6e-103 |
| digits | 99 | 0.1 | 0.900 | 0.903 [0.898, 0.907] | 1 |

**Mechanism.** puncc's calibration score (`api.nonconformity_scores.raps_score`) is the
regularized cumulative mass up to the true label minus `U × p(label)`: only the
probability term is randomized. The prediction rule (`api.prediction_sets.raps_set`)
removes the last candidate label with probability
`excess / (p_L + lambda × 1[L > k_reg])`. The extra `lambda` in the denominator makes
the removal less likely than the score implies whenever the boundary label is ranked
beyond `k_reg`, so labels enter the set more often than `score <= tau` allows. The
reference implementation by the RAPS authors (github.com/aangelopoulos/conformal_classification,
`conformal.py`, function `gcq`) divides by `p_L` alone. The effect is largest with the
anti-informative `cls_gauss` model, where the boundary label is often ranked low, and
vanishes on digits, where the boundary label is usually ranked first. With lambda = 0
(APS) the two rules agree, and `puncc/aps/rand=True` passes every cell.

**Adapter cross-check.** The standalone repro
`manual__puncc__raps__set_rule_vs_score.py` calls the two public puncc functions directly
with one probability vector `(0.45, 0.30, 0.15, 0.10)` and `tau = 0.95`. Over 200,000
uniforms, label 2 is in `raps_set` 40.1% of the time, while `raps_score(label 2) <= tau`
never holds (its score lies in [0.95, 1.10] and equals 0.95 only at U = 1). It reproduces
under numpy 2.5.4 and under puncc's declared `numpy<2` (numpy 1.26.4, Python 3.12). The
sets remain valid (they over-cover), but they are larger than RAPS needs, which works
against the purpose of the regularization. TorchCP's randomized RAPS, whose set is
`score <= tau` with the same score, passes every cell.

Repros: `manual__puncc__raps__set_rule_vs_score.py` and the generated
`puncc__raps__rand-True__coverage.py` (0.954 against 0.833 at n = 5, alpha = 0.2); both
were re-checked under `numpy<2`.

## 5. Pre-registered hypotheses

| # | Hypothesis | Verdict |
|---|---|---|
| 1 | crepes regression is conservative by one order statistic at integer boundaries | **Confirmed** (F2). Exactly the predicted cells (n in {9, 19, 49, 99, 999}, alpha in {0.1, 0.2}), not the paired n, plus the edge level alpha = 1/(n+1) at n = 5 and 1000. |
| 2 | crepes unsmoothed classification is conservative at integer boundaries | **Confirmed** (F3). Smoothed rows pass. |
| 3 | MAPIE APS `True` conservative, `False` under-covers, `"randomized"` passes | **Partly refuted: model-dependent** (F1). `True` is conservative and `"randomized"` passes in every cell where they run (both are also affected by F4 and F7). `False` under-covers on both synthetic models but over-covers on digits. It does not follow the law in either direction. |
| 4 | k > n behaviour differs, and all libraries are valid | **Partly refuted.** puncc refuses (valid). crepes returns trivial sets (valid, with a warning). MAPIE refuses even with `allow_infinite_bounds=True` on the split regressor (F4). TorchCP regression crashes (F8), while its classifiers return full sets. |
| 5 | MAPIE asymmetric CQR has coverage (2k' - (n+1))/(n+1) | **Confirmed where it runs.** For example 0.9177 [0.9124, 0.9230] against 0.92 at n = 49, alpha = 0.1, with rank recovery exact per side. It over-refuses some feasible levels (F4). |
| 6 | MAPIE RAPS follows the law with n_eff = n - ceil(0.2 n) | **Refuted in its number, confirmed in its form** (F9). MAPIE holds out ceil(0.1 n), not ceil(0.2 n), because `size_raps` is ignored. This was found by reading the source while implementing the adapter (DESIGN 14.1) and is confirmed by the calibration size MAPIE reports in every repetition. The coverage matches the law at n - ceil(0.1 n) in all 26 cells where MAPIE runs. The statistical test cannot tell the candidate sizes apart: in those cells the laws at nominal n, n - ceil(0.1 n) and n - ceil(0.2 n) have nearly the same mean, and 0 of 26 cells reject any of them (`raps_neff.md`). The prediction that the nominal-n law would show LAW_MISMATCH is not supported at R = 200. |
| 7 | TorchCP float32 creates ties at large n | **No evidence.** TorchCP LAC, APS and RAPS pass at n = 1000, and LAC bracketing (which now sees both directions) gives offset 0 in every draw. |
| 8 (round 2) | MAPIE APS `False` over-covers on `cls_gauss_inf` | **Refuted** (F1). It under-covers by 0.05-0.11 in all 23 cells where it runs. |
| 9 (round 2) | Randomized RAPS passes in puncc and TorchCP; MAPIE `randomized` passes against n - ceil(0.1 n); MAPIE `True` is conservative | **Partly refuted.** TorchCP passes and the MAPIE parts are confirmed; puncc's randomized RAPS over-covers (F10). |
| 10 (round 2) | Bracketing confirms the crepes boundary effect at large n and finds no offset in the other LAC rows | **Confirmed** (F3). k + 1 at exactly the boundary cells, including n = 999; offset 0 in every draw of MAPIE, puncc and TorchCP LAC and of the reference. |

## 6. Checks against adapter mistakes

- **Documented usage.** Every adapter is tested against the library's documented usage
  written out by hand on the same data (`tests/test_adapters.py`). For example, MAPIE's
  `SplitConformalRegressor` with `prefit=True` gives identical arrays.
- **Standalone repros.** Every finding was reproduced by a script that does not import
  conformcheck. Those scripts call the public API directly with a fixed model.
- **F1 cross-check.** MAPIE's sets were compared with an independent APS computation on
  the same data, and the randomized calibration scores were inspected directly.
- **F9 and F10 cross-checks.** F9 is read off the user's own `RAPSConformityScore`
  object. F10 compares two public puncc functions with each other on fixed inputs, so it
  does not depend on how the adapter calls `RAPS`.
- **Determinism.** The 205 units re-run in round 2 reproduced their v0.1 covered counts
  exactly, so one run directory can hold v0.1 and round-2 units.
- **Bracketing bug (round 2).** `diagnostics.bracket_rank` put the lower end of the
  bracket at `#{s <= a}` instead of `#{s < a} + 1` (with `a` the largest included test
  score). It could never report a positive offset: in v0.1 the `k_plus_1` LAC mutant had
  offset 0 in every draw. Bracketing was diagnostic only in v0.1, so no published status
  depended on it. It is fixed and tested in both directions, and the LAC units were
  re-run.
- **TorchCP CQR artifact (v0.1).** The first v0.1 report showed 7 FAIL cells for
  `torchcp/cqr` on the diabetes data. They came from conformcheck's rank tolerance
  (`1e-6 × |q|`), which was too tight for a float32 interval endpoint near 150 minus a
  float64 prediction. The tolerance now scales with the magnitude of the endpoints, and
  those cells pass. This was a bug in conformcheck, not in TorchCP.
- **Review corrections (v0.1).** Coverage intervals are empirical t intervals; the
  headline excuses a documented row only for its documented status; the size check is a
  count without a binomial p-value. Two earlier pipeline errors (hidden one-sided
  off-by-ones in interval half-widths; a zero-variance t-test) were fixed before the v0.1
  run. See CHANGELOG and the git history.

## 7. Limitations

- **Monte Carlo power falls with n.** With R = 200 and m = 500, a one-order-statistic
  error is statistically invisible above roughly n = 100 (section 3). Rank recovery
  covers split regression, CQR and CV+/jackknife+ with the constant model; bracketing
  now covers LAC and class-conditional LAC. APS and RAPS have neither: their
  deterministic set rules differ between libraries (whether the label that crosses the
  threshold is included), so an offset would grade a convention, and their randomized
  rules use uniforms drawn inside the library. A one-step error in an APS or RAPS
  implementation at n = 1000 would be missed. The `full` study (R = 2000, m = 1000) has
  more power but was not run.
- **Tests on the mean.** The exact law is tested through the mean of covered counts and
  a goodness-of-fit test on their distribution. Rows whose law is only a bound (CV+ and
  jackknife+ with a real model) or a mean (asymmetric CQR, smoothed p-values) get a
  one-sided t-test or a mean test only. A library could have the right mean and the
  wrong spread there.
- **One-sided cells cannot flag over-coverage.** Deterministic APS and RAPS have atoms
  in their score distributions, so they are tested one-sided. This hides large
  over-coverage, for example at n = 1000, alpha = 0.1 on `cls_gauss_inf`:
  - puncc APS `rand=False` covers 0.995;
  - puncc RAPS `rand=False` covers 0.982.

  Both are valid. TorchCP's deterministic APS and RAPS cover 0.898 and 0.900 in the same
  cell, so puncc's deterministic sets are much wider than needed, but the oracle does not
  grade this.
- **The model shapes effect sizes, and for F1 the direction.** Laws hold for any fixed
  model, so the law-based findings do not depend on the classifier. The two
  model-dependent findings (F1, F10) were run on three models: anti-informative,
  Bayes-optimal and an accurate logistic regression on digits. Their sizes differ by an
  order of magnitude between them.
- **MAPIE RAPS law caveat.** MAPIE's hold-out split is stratified by label, so the kept
  calibration points are not a uniformly random subset of the n points, and the n_eff
  law is exact only up to the effect of fixed class counts. No cell rejected it.
- **CV+ bounds where K does not divide n.** Barber et al. (2021, Thm 4) assume folds of
  equal size n/K. The `lower` cells of CV+ with a real model at n = 19, 49, 99 and 999
  apply the same formula with n/K as a fraction, which is an extrapolation. All of those
  cells pass, so no result depends on it.
- **A single seed.** The run uses one seed and one machine (Windows, CPU). The
  deterministic findings (F2, F4, F5, F6, F8, F9 and the F10 mechanism) do not depend on
  the seed. The statistical ones have Holm p far below the threshold.
- **puncc under numpy 2.** puncc declares `numpy<2`, and the main run used numpy 2.5.4
  through a lockfile override. Every puncc finding was re-checked under numpy 1.26.4, but
  the PASS cells of puncc were not.
- **Not covered:**
  - time-series methods (ACI, EnbPI), weighted conformal and conformal risk control;
  - GPU runs;
  - class-conditional methods on the digits data;
  - Mondrian/conditional regression;
  - RAPS with lambda and k_reg other than 0.1 and 1 (puncc, TorchCP).
- **CI has never run.** The workflow (pull_request and workflow_dispatch) is configured
  but has never run, because the repository has not been pushed. All tests were run
  locally only.
- **Library versions move.** These are statements about MAPIE 1.6.0, crepes 0.9.1,
  puncc 0.9.3 and TorchCP 1.2.1. Re-run `conformcheck repro --verify` against newer
  versions before citing a finding.

## 8. Reproducing

From scratch (about an hour of wall time on 3 to 4 workers; resumable):

```sh
uv sync --all-extras
uv run conformcheck plan --study default
uv run python scripts/run_study.py --study default --out runs/default --workers 3
uv run conformcheck report runs/default
uv run conformcheck repro runs/default --verify
uv run python scripts/raps_neff.py runs/default --out runs/default/raps_neff.md
```

To rebuild the report from the committed per-unit records without re-running, gunzip
`docs/results/default/units.jsonl.gz` into `runs/default/units.jsonl`, copy
`run.json` next to it, and run `conformcheck report runs/default`.
