# conformcheck design

Status: design for v0.1, written before implementation (milestone M0). Sections marked
**hypothesis** are predictions from reading library source code. They are not findings
until the study confirms them. Section 14 is the round-2 addendum (RAPS, bracketing, an
informative synthetic classifier), written before its study run; sections 1 to 13 are
kept as written, with the round-2 changes marked inline.

## 1. Goal

Conformal prediction gives a distribution-free guarantee whose finite-sample form is
exact. For split conformal with `n` exchangeable calibration points, continuous scores
and closed sets, the marginal coverage is exactly `k/(n+1)` with
`k = ceil((n+1)(1-alpha))`. This lies in `[1-alpha, 1-alpha+1/(n+1))`. Coverage
conditional on the calibration set follows a known Beta law. These laws make the
libraries testable to the digit: an off-by-one in the order statistic, interpolation,
tie handling or a mismatch between score and set construction all move coverage by a
known, detectable amount.

**Headline deliverable.** A conformance matrix across MAPIE, crepes, puncc and TorchCP.
Each library-method pair is marked PASS, FAIL (under-coverage), CONSERVATIVE (needless
over-coverage) and so on, at small `n`, at the `(n+1)alpha` integer boundary, with ties
and with randomized sets. Every non-PASS entry comes with a verified, standalone minimal
repro. The same oracle ships as a pytest plugin and `conformcheck.testing` helpers that
library authors can run in their own CI.

Prior art. MAPIE checks the coverage of its own split methods
(`plot_coverage_validity.py` in its docs). The TorchCP paper (arXiv:2402.12683)
benchmarks speed, not validity. The crepes and puncc papers do not audit other
libraries. We found no independent cross-library validity audit and no reusable
conformance suite (searched 2026-10-23).

## 2. Scope for v0.1 (after critique)

The default study must run in under 45 CPU-minutes on 4 workers, and the full-size run
is a documented, resumable command.

**In**

| Family | Methods | Libraries |
|---|---|---|
| R1 split regression | absolute residual | MAPIE, crepes, puncc, TorchCP |
| R2 CQR | symmetric correction; MAPIE also asymmetric (its default) | MAPIE, puncc, TorchCP |
| R3 cross methods | jackknife+ (LOO), CV+ (K = 5, 10) | MAPIE, puncc |
| C1 LAC | `1 - p_y` score; crepes hinge (= LAC), smoothed and not | MAPIE, crepes, puncc, TorchCP |
| C2 APS | non-randomized and randomized; MAPIE `include_last_label` False/True/"randomized" | MAPIE, puncc, TorchCP |
| C3 RAPS | fixed (lambda, k_reg); MAPIE tunes lambda internally | MAPIE, puncc, TorchCP (cut from v0.1; added in round 2, section 14) |
| C4 class-conditional | Mondrian by label with LAC score | crepes, puncc, TorchCP |

That gives about 29 library-method-variant rows without RAPS and about 33 with it
(counting MAPIE's two `k > n` modes, both crepes smoothing modes and both APS
randomization modes), plus the control rows (reference and mutants, section 4).

**Cut from the initial scope, and why**

- California housing: it needs a download. The diabetes dataset covers real regression
  data offline. Iris is dropped too: with 150 samples the pool is too small next to
  digits.
- RAPS moves to the last milestone (M8). It is APS plus a penalty and has the same
  law. MAPIE's internal lambda search makes it costly to adapt. It is cut if time runs
  short; the matrix then says "not run".
- The exact distribution test for smoothed p-values (crepes `smoothing=True`) is
  replaced by an exact-mean test (section 3.2.4). The full law has no closed form.
- Rank recovery for classification (bracketing) is diagnostic only, and only for LAC
  and non-randomized APS.
- MAPIE Mondrian: MAPIE 1.6 has no class-conditional classifier, so that cell is
  "unsupported", not cut.

**Out of scope for v0.1**: time-series methods (ACI, EnbPI), weighted conformal under
covariate shift, conformal risk control and Learn-then-Test, and GPU runs. Findings are
reported upstream only after they have been reviewed.

## 3. Oracle

### 3.1 Notation and conventions

- `n` calibration points, `m` test points per repetition, `R` repetitions (independent
  calibration draws) per cell, miscoverage `alpha`.
- `alpha` is the exact rational the user means. A float is read through its shortest
  decimal repr: `0.1` means 1/10 (`conformcheck.laws.as_fraction`). Adapters pass the
  level to the library exactly as a user would type it (`alpha=0.1` or
  `confidence_level=0.9`).
- `k = ceil((n+1)(1-alpha))` and `l = floor((n+1)alpha)`, so `k = n+1-l`.
- Sets are closed: covered if and only if `score <= threshold`.
- An interval is checked as `lo <= y <= hi` with `+-inf` allowed. A set is checked as
  `sets[i, y_i]`.

### 3.2 Exact laws (implemented in `laws.py`)

**3.2.1 Split conformal, distinct scores.** References: Vovk et al. 2005; Lei et al.
2018, Thm 2.2; Vovk 2012; Angelopoulos and Bates 2023, Sec. 3.2.

- If `k > n` (equivalently `alpha < 1/(n+1)`), the only valid set is trivial (infinite
  interval, all labels) and coverage is 1.
- Otherwise the marginal coverage is exactly `k/(n+1)`.
- Coverage given the calibration set is `C ~ Beta(k, n+1-k)`, i.e. `Beta(n+1-l, l)`.
- With `m` test points sharing one calibration set, the covered count is
  `S ~ BetaBinomial(m, k, n+1-k)`, so
  `E S = m k/(n+1)` and `Var S = m a b (a+b+m) / ((a+b)^2 (a+b+1))` with `a = k`,
  `b = n+1-k`.

The count law depends only on the random relative order of the `n+m` scores. It
therefore holds for i.i.d. continuous data, and also for random splits without
replacement of a finite pool with distinct scores (toy datasets), conditional on a
model fitted on disjoint data. It needs no knowledge of the data distribution, so the
same test applies to any score function: absolute residual, CQR, LAC, APS, RAPS, and
randomized scores (which are continuous).

**3.2.2 Ties (discrete scores).** If the score has pmf `p` on an ordered support with CDF
`F`, a correct implementation thresholds at `q = S_(k)`, where
`P(S_(k) <= v) = P(Binomial(n, F(v)) >= k)`. Then:

- coverage `= sum_v P(S_(k) = v) F(v)`, which is at least `k/(n+1)`;
- the count law is the mixture `sum_v P(S_(k) = v) Binomial(m, F(v))`.

Both are exact (`discrete_split_coverage`, `discrete_count_law`). The DGP `reg_tied`
makes `F` known (constant model, integer-valued `Y`). This catches strict-vs-non-strict
comparisons, deduplication and interpolation between tied values.

**3.2.3 Smoothed (randomized) p-values.** Vovk et al. 2005. The p-value is
`p_y = (#{s_i > s} + U (#{s_i = s} + 1)) / (n+1)`, the set is `{y : p_y > alpha}`, and
coverage is exactly `1 - alpha`. Given the calibration set, a test point is covered with
probability `c = (1-f) U_(k) + f U_(k-1)`, where `f = (n+1)alpha - l` and `U_(j)` are
uniform order statistics (`U_(0) = 0`). Using
`Cov(U_(i), U_(j)) = i(n+1-j) / ((n+1)^2 (n+2))` for `i <= j`:

- `Var S = m E c (1 - E c) + m(m-1) Var c`.

crepes compares `p >= 1 - confidence` rather than `p > alpha`. The two differ only on a
null event for smoothed p-values, but not for unsmoothed ones (section 12).

**3.2.4 Laws used per method**

| Method | Law | Test kind |
|---|---|---|
| split abs, CQR symmetric, LAC, APS (deterministic or randomized score), RAPS fixed, Mondrian per class | BetaBinomial(m, k, n+1-k); per class with `n_y`, `m_y` | exact |
| any split method, `reg_tied` | discrete mixture (3.2.2) | exact |
| CQR asymmetric (two one-sided bounds at `alpha/2`) | coverage `(2k' - (n+1))/(n+1)`, `k' = ceil((n+1)(1-alpha/2))`; the misses are disjoint | exact mean, empirical variance |
| smoothed p-values (crepes `smoothing=True`) | mean `1 - alpha`, variance from 3.2.3 | exact mean |
| jackknife+ / CV+, constant model | every LOO/out-of-fold model is identical, so the interval is `[-R_(k), R_(k)]`: split conformal on all `n` points | exact |
| jackknife+, other models | `>= 1 - 2alpha` (Barber et al. 2021, Thm 1) | one-sided |
| CV+, other models | `>= 1 - 2alpha - min{2(1-1/K)/(n/K+1), (1-K/n)/(K+1)}` (Thm 4) | one-sided |
| MAPIE RAPS (lambda tuned on an internal split of size `ceil(0.2 n)`; round 2: `ceil(0.1 n)` in practice, section 14) | BetaBinomial with `n_eff = n - ceil(0.2 n)` (round 2: `n - ceil(0.1 n)`); the tuning split is independent of the calibration part | exact, with `n_eff` reported by the adapter |
| any method with `k > n` | `S = m` surely, or a documented refusal | deterministic |

The constant-model reduction for jackknife+ follows from the definitions (Barber et al.
2021, Sec. 1.2): `q^-_alpha{v_i}` is the `floor(alpha(n+1))`-th smallest value, which
equals `-q^+_alpha{-v_i}`. With `mu_{-i} = 0` the interval is `[-R_(k), R_(k)]`.

### 3.3 Deterministic diagnostics (`diagnostics.py`, no multiplicity)

1. **Rank recovery** (R1, R2 symmetric). The threshold is read off the returned interval,
   e.g. `q = (hi - lo)/2` for the absolute score or `q = q_lo(x) - lo` for CQR. The
   adapter recomputes the calibration scores from the same fixed model, and the library
   used order statistic `k_used = #{s_i <= q (1 + 1e-9)}`. A `q` strictly between order
   statistics means the library interpolates. For TorchCP, scores are compared in
   float32. `k_used = k` in every repetition gives EXACT. `k_used > k` gives
   CONSERVATIVE(+j). `k_used < k` gives FAIL(-j). This detects off-by-ones at any `n`,
   including `n = 1000`, where Monte Carlo has no power (3.5).
2. **Bracketing** (LAC, non-randomized APS). The scores of all labels of all test
   points bracket the threshold: the largest included score is at most `q`, and `q` is
   below the smallest excluded score. Mapped to the calibration order statistics this
   gives a range for `k_used`.
3. **Trivial-set check** (`k > n`). Every interval must be infinite and every set full.
   Allowed alternatives: an exception or warning that names the cause (status REFUSED).
   Returning a finite set is FAIL, deterministically.
4. **Differential check** against the reference implementation, for non-randomized
   methods. Reports the maximum endpoint difference or set disagreement rate. A
   difference is information, not a verdict, because conventions differ; the laws
   decide.

### 3.4 Statistical tests (`stats.py`)

Per cell the runner records the counts `S_1..S_R`.

- **Mean test (exact).** `T = sum_r S_r`. Under H0, `T` has the `R`-fold convolution of
  the law's pmf, computed by FFT; the support has length `Rm+1`, at most 2e6. The
  two-sided p-value is `min(1, 2 min(P(T <= t), P(T >= t)))`. A normal approximation
  with the exact variance is computed alongside, as a cross-check in tests. For laws
  with only an exact mean, a t-test uses the exact mean and the empirical variance.
- **Distribution test.** Pearson chi-square of the histogram of `S_r` against the pmf.
  Bins are merged from each tail until every expected count is at least 5;
  `df = bins - 1`. This catches a wrong conditional law with a right mean, e.g. a wrong
  effective `n`.
- **One-sided bound test** (jackknife+/CV+ with real models). A one-sided t-test of mean
  coverage `S/m` against the bound. Only a violation is reported; this test has no
  conservative direction.
- **Cell p-value**: `min(1, 2 min(p_mean, p_gof))` (Bonferroni within the cell).
- **Across cells**: Holm at FWER 0.05 over every statistical cell in the study decides
  the statuses. Benjamini-Yekutieli at FDR 0.05 is reported as a secondary flag.
  Deterministic diagnostics are not hypothesis tests and do not enter the family.
- **Status mapping** (statistical part): Holm-rejected with `T` below its mean is FAIL;
  rejected with `T` above is CONSERVATIVE; rejected on the distribution test only is
  LAW_MISMATCH; otherwise PASS. Every cell also reports the observed mean coverage
  with a 95% interval (exact-variance normal interval for exact laws, t interval
  otherwise), the exact target and `k_used` when known.
- **Combined status per cell.** In order of severity: ERROR > FAIL (deterministic or
  statistical) > LAW_MISMATCH > CONSERVATIVE > REFUSED > PASS. UNSUPPORTED applies
  when the library has no such method or option.
- **Headline aggregation.** For each library-method-variant row, the worst status over
  cells with `n <= 100` is "small-n status". Headline: *k of N rows FAIL or are
  CONSERVATIVE at small n*, with each counted cell listed.

### 3.5 Size and power

Size: the reference implementation runs through every cell of the study. Its cell
p-values must look uniform (KS test reported) and it must get no Holm rejection.

Power for an off-by-one (`k+1` or `k-1`, a shift of `1/(n+1)`) with the mean test,
`alpha = 0.1` and about 2000 cells (Holm critical z about 4.21):

| n | shift | z (R=200, m=500) | power | z (R=2000, m=1000) | power |
|---|---|---|---|---|---|
| 9 | 0.100 | 15.5 | 1.00 | 49.2 | 1.00 |
| 19 | 0.050 | 10.6 | 1.00 | 33.8 | 1.00 |
| 49 | 0.020 | 6.4 | 0.99 | 20.8 | 1.00 |
| 99 | 0.010 | 4.3 | 0.54 | 14.3 | 1.00 |
| 999 | 0.001 | 0.9 | 0.00 | 3.3 | 0.19 |

Derivation: `sd(S/m) = sqrt(Var S)/m` from the BetaBinomial,
`z = shift sqrt(R) / sd(S/m)`. So the default study detects off-by-ones by Monte Carlo
up to `n` of about 50. Beyond that, rank recovery (3.3) is the evidence for split
regression; for other methods the report states the minimum detectable effect,
`(z_crit + 0.84) sd/sqrt(R)` (about 0.012 at n=99 and 0.006 at n=999 in the default
study). The mutant controls measure power empirically.

## 4. Reference implementations and mutants (`reference.py`)

One short numpy function per method, written from the papers. They do not depend on
each other and share no "clever" helpers:

- `split_abs`, `cqr` (symmetric/asymmetric), `lac`, `aps` (deterministic/randomized,
  Romano, Sesia and Candes 2020), `raps` (Angelopoulos et al. 2021),
  `class_conditional_lac`, `smoothed_lac`, `jackknife_plus` and `cv_plus` (Barber et al.
  2021: upper is the `ceil((1-alpha)(n+1))`-th smallest of `mu_{-i}(x) + R_i`, lower is
  the `floor(alpha(n+1))`-th smallest of `mu_{-i}(x) - R_i`; `-inf` when that index is
  0, `+inf` when the upper index exceeds `n`).
- Mutants: `k_minus_1`, `k_plus_1`, `no_correction_linear` (`np.quantile(s, 1-alpha)`),
  `n_instead_of_n_plus_1` (`k = ceil(n(1-alpha))`).
- The reference and mutants are exposed as adapters (library `reference`), so they go
  through the identical runner, tests and report. Expected matrix: reference PASS
  everywhere; `k_minus_1` FAIL; `k_plus_1` CONSERVATIVE; the other two FAIL at small
  `n`. The report shows the observed detection rate per `n` next to section 3.5.

## 5. Adapters (`adapters/`)

Contract: `adapters/base.py`. Adapters call only public APIs, pass levels as a user
would, fit once per repetition, evaluate all alphas from that fit, and never swallow
errors (status `error` or `refused` with the message). The fixed models (`models.py`)
are passed in prefit form, so every library sees the same function.

Versions locked for the study (PyPI, checked 2026-10-23): MAPIE 1.6.0 (BSD-3-Clause,
released 2026-10-19), crepes 0.9.1 (BSD-3-Clause), puncc 0.9.3 (MIT), TorchCP 1.2.1
(LGPL-3.0, imported only, never vendored), torch 2.14.1+cpu, scikit-learn 1.9.1, numpy
2.5.4 (2.4.6 on Python 3.11), scipy 1.18.1. Every run records the versions it actually
used.

### 5.1 MAPIE 1.6.0 (v1 API)

- `SplitConformalRegressor(estimator, confidence_level, conformity_score="absolute", prefit=True)`,
  then `.conformalize(X, y)` and `.predict_interval(X)`, which returns
  `(y_pred, y_pis)` with `y_pis` of shape `(m, 2, n_levels)`. A list of confidence
  levels is evaluated in one call.
- Quantile (`mapie/utils.py::_compute_regression_quantile`, `_compute_classification_quantile`):
  `np.quantile(scores, ceil((n+1)(1-alpha))/n, method="lower")`. In exact arithmetic
  this is the `k`-th order statistic. When `k > n` it raises `ValueError` unless
  `allow_infinite_bounds=True` (then `+-inf`). Both variants are run: the default
  (expected REFUSED) and `allow_infinite_bounds=True` (expected trivial intervals).
- `ConformalizedQuantileRegressor(estimator=[lower, upper, median], confidence_level, prefit=True)`.
  `predict_interval(X, symmetric_correction=False)` is the default. It corrects each
  side at level `alpha/2` (asymmetric law, 3.2.4). `symmetric_correction=True` is
  standard CQR.
- `CrossConformalRegressor(estimator, confidence_level, method="plus", cv=LeaveOneOut() | KFold(K, shuffle=True, random_state))`,
  then `.fit_conformalize(X, y)` and `.predict_interval(X, allow_infinite_bounds=True)`.
- `SplitConformalClassifier(estimator, confidence_level, conformity_score="lac" | "aps" | "raps", prefit=True, random_state)`,
  then `.predict_set(X, conformity_score_params={"include_last_label": ...})`, which
  returns sets of shape `(m, K, n_levels)`. APS calibration scores are always
  randomized (`cumsum - U p_y`). Comparisons use a tolerance `EPSILON = 1e-8`. RAPS
  holds out `size_raps = 0.2` of the calibration data to tune lambda and `k_reg`.

### 5.2 crepes 0.9.1

- `WrapRegressor(learner).calibrate(X, y)`, then `.predict_int(X, confidence)`. The
  core is `ConformalRegressor.predict_int`: scores sorted descending, index
  `int((1 - confidence)(n+1)) - 1`. When that index is negative it returns `+-inf` with
  a warning (the correct trivial set).
- `WrapClassifier(learner).calibrate(X, y, class_cond=False | True, nc=hinge)`, then
  `.predict_set(X, confidence, smoothing=True | False, labels=False)`, which returns a
  0/1 matrix. The default is `smoothing=True`. The set is `{y : p_y >= 1 - confidence}`
  (`base.py::ConformalClassifier.predict_set`); p-values come from `p_values_batch`.
- crepes uses the global `np.random` state when a `seed` is given; the adapter passes the
  repetition seed.
- Cost: unsmoothed and smoothed p-values are computed in Python loops over the test
  points (about 74 ms per call at n=100, m=1000, K=4). Budgeted in section 7.

### 5.3 puncc 0.9.3

- Predictors: `deel.puncc.api.prediction.BasePredictor(model, is_trained=True)`; for
  classification, a subclass whose `predict` returns `predict_proba`; for CQR,
  `DualPredictor([lo, hi], is_trained=[True, True])`.
- `SplitCP(predictor, train=False).fit(X_calib=, y_calib=)`, then `.predict(X, alpha)`,
  which returns `(y_pred, lo, hi)`. Same pattern for `CQR`. `CVPlus(predictor, K=, random_state=)`
  uses `.fit(X=, y=)`, and its `predict` returns `y_pred=None`.
- Quantile (`api/calibration.py::BaseCalibrator.compute_quantile`): `np.quantile` with
  `method="inverted_cdf"` at level `1 - alpha` over the scores with `+inf` appended
  (the `n+1` augmentation). `alpha_calib_check` raises `ValueError` when
  `alpha < 1/(n+1)` (expected REFUSED).
- `LAC`, `APS(rand=)`, `RAPS(lambd=, k_reg=, rand=)` and `ClasswiseLAC` take `alpha`
  in `predict` and return lists of labels; the adapter converts them to a boolean
  matrix.
- **Dependency override.** puncc declares `numpy<2.0.0`, which conflicts with scipy
  1.18 and has no Python 3.13 wheels. The lockfile overrides it to `numpy>=1.26`. Every
  puncc finding must be re-run under `numpy<2`, Python 3.12, before it is reported:
  `uv run --isolated --python 3.12 --with "puncc==0.9.3" --with "numpy<2" python <repro>`.
  This is part of the M6 done-check.

### 5.4 TorchCP 1.2.1 (CPU)

- Classification: `SplitPredictor(score_function=LAC() | APS(randomized=) | RAPS(penalty=, kreg=, randomized=), model=None)`,
  then `.calculate_threshold(logits, labels, alpha)` and `.predict_with_logits(logits)`,
  which returns an int `(m, K)` tensor. Logits are `log(p)` in float32;
  `softmax(log p) = p` up to rounding. `ClassConditionalPredictor` has the same API.
- Regression: `SplitPredictor(score_function=ABS() | CQR(), model=Identity(), device="cpu")`.
  The device must be given because the identity module has no parameters. The
  "features" fed to the identity model are the fixed model's predictions (`(n,1)`, or
  `(n,2)` for CQR). `calibrate(DataLoader)`, then `predict(x)` returns `(m, 1, 2)`.
- Quantile (`utils/common.py::calculate_conformal_value`): `torch.kthvalue(scores, ceil((N+1)(1-alpha)))`,
  computed in floating point; `+inf` with a warning when `k > n`.
- Seeds: randomized scores use `torch.rand`, so the adapter calls `torch.manual_seed`.
  Workers set `torch.set_num_threads(1)`.
- **Import stubs.** `import torchcp` imports `torchsort` (no Windows wheels),
  `torch_geometric` and `transformers` at module level. They are removed from the lock
  by override and replaced at import time by inert placeholder modules
  (`adapters/_import_stubs.py`), only when they are not installed. Verified: torchcp
  imports and calibrates (`tests/test_import_stubs.py`).

## 6. Data (`data.py`, `models.py`)

| DGP | Definition | Model | Used by |
|---|---|---|---|
| `reg_gauss` | `X ~ U[0,1]^2`, `Y = 2X_1 + N(0,1)` | `FixedRegressor(intercept=0.3)`; CQR models `2x - 1.0` and `2x + 1.2` (miscalibrated) | R1, R2, R3 (bound) |
| `reg_hetero_t` | `Y = sin(2 pi X_1) + (0.5 + X_1) t_3` | `FixedRegressor(slope=0, amplitude=0.8)` | R1, R2 |
| `reg_tied` | `Y` uniform on `{-3,...,3}`, `X ~ U[0,1]` | `ConstantRegressor(0)`; score `|Y|` has pmf `(1,2,2,2)/7` | R1 (discrete law) |
| `reg_constant` | as `reg_gauss` | `ConstantRegressor(0)` refit by the library | R3 (exact law) |
| `cls_gauss` | `Y ~ Unif{0..3}`, `X|Y ~ N(mu_Y, I_2)` with means on a square of side 2 | `FixedClassifier(temperature=2)` | C1 to C4; stratified draws for C4 |
| `diabetes` | 442 rows; 100 fixed training rows fit `LinearRegression` once | linear; CQR models `f +- training residual quantiles` | R1, R2, R3 (bound) |
| `digits` | 1797 rows; 500 fixed training rows fit `LogisticRegression` once | multinomial logistic | C1, C2, C4 |

Seeds: `SeedSequence([study_seed, dgp_id, n, rep])`, so all libraries see identical data
in a repetition (common random numbers). Library-internal randomness gets a seed spawned
from the same sequence. Toy datasets: each repetition is a random permutation of the
pool minus the training rows, split into calibration `n` and test
`m = min(m, pool - n)`. Ties among scores are counted per repetition. If any ties occur
the cell is tested one-sided, since ties only add coverage.

## 7. Study

### 7.1 Grid (`src/conformcheck/studies/default.toml`)

- Alphas `0.05, 0.1, 0.2`, plus per `n` the edge levels `1/(n+1)` (`k = n`) and
  `0.9/(n+1)` (`k = n+1`, trivial set required).
- Split: `n` in `{5, 9, 10, 19, 20, 49, 50, 99, 100, 999, 1000}`. The pairs (9, 10),
  (19, 20), (49, 50), (99, 100), (999, 1000) put each integer boundary
  `(n+1)alpha in Z` next to a non-boundary `n`.
- Tied: `n <= 100`. Jackknife+: `n <= 99` (LOO refits). CV+: K in {5, 10},
  `19 <= n <= 1000`. Class-conditional: per-class `n_y <= 99`. Toy: `n` in
  `{10, 19, 50, 99}`, alpha `{0.1, 0.2}`.
- Default `R = 200`, `m = 500`. Full: `R = 2000`, `m = 1000` (`studies/full.toml`).

### 7.2 Budget

Measured per call on this machine (Python 3.13, 1 thread, n=100, m=1000): MAPIE split
1.8 ms, crepes split 0.05 ms, puncc split 0.7 ms, TorchCP split 3.5 ms, MAPIE
randomized APS 7.7 ms, puncc randomized APS 3.9 ms, TorchCP randomized APS 2.6 ms,
crepes smoothed LAC 74 ms, MAPIE CV+ K=10 144 ms, MAPIE jackknife+ 268 ms. The
estimate is about 1.5 to 2.5 CPU-hours for the default grid, so 25 to 40 minutes on 4
workers. `conformcheck plan` measures a short probe per unit type and prints the
estimate before running. Rule: if the estimate for `default` exceeds 40 minutes, lower
`reps` (never below 100) or drop `n = 999/1000` for crepes classification, and record
the change in REPORT.md. The full study is about 10x and runs for hours; it is
resumable.

Commands:

```sh
uv sync --all-extras
uv run conformcheck plan --study default
uv run python scripts/run_study.py --study default --out runs/default
uv run conformcheck report runs/default
uv run conformcheck repro runs/default --verify
# full size (hours; resumable, same commands with --study full --out runs/full)
uv run python scripts/run_study.py --study full --out runs/full --attempts 5
```

### 7.3 Execution

- Unit = (library, method, variant, dgp, n) with all alphas and all `R` repetitions.
  Unit id = hash of its spec.
- `runs/<name>/run.json`: config fingerprint, seed, platform, and the versions of
  Python, numpy, scipy, scikit-learn and each library. Resume refuses a changed
  fingerprint unless `--force`.
- `ProcessPoolExecutor(max_workers <= 4)`. Workers set `OMP_NUM_THREADS`,
  `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` to 1, and `torch.set_num_threads(1)`.
- The parent process is the only writer: `units.jsonl` gets one line per finished unit
  (flushed and fsynced) holding counts per alpha, `k_used` per repetition, statuses,
  warnings, timings and `effective_n`. A rerun skips completed ids.
  `progress.log` records done/total, rate and ETA.
- `scripts/run_study.py` retries `conformcheck run` up to `--attempts` times (default
  3) and logs to `attempts.log`.
- Committed results: `docs/results/<study>/` holds `run.json`, `matrix.{md,csv,json}`
  and `summary.md` (small). `units.jsonl` is committed only if under about 5 MB;
  otherwise it stays in `runs/` and is gitignored.

## 8. Outputs

### 8.1 Matrix and report

`conformcheck report` writes `matrix.md/csv/json`. Rows are library/method/variant;
columns are dgp x n x alpha. Each entry has the status, the observed coverage with its
95% interval, the exact target, `k_used` and the Holm/BY adjusted p-values.
`summary.md` holds the headline counts, the control rows (size and power) and the list
of findings. `REPORT.md` at the repository root (milestone M8) is written by hand from
these: exactly what ran (sizes, seeds, versions, durations), the findings with
intervals, and the limitations.

### 8.2 Classification of findings

A non-PASS entry becomes a "finding" only after three checks:

1. The adapter passes the library's own documented example: the M3 done-check includes
   one test per adapter that reproduces a value from the library's docs or tests.
2. The standalone repro (8.3) reproduces it without conformcheck.
3. For puncc, it reproduces under `numpy<2` (5.3).

Documented behaviour (e.g. MAPIE `include_last_label=True` is described as possibly
conservative, and refusals with a clear message) is labelled "documented" in the matrix
and is not counted as a defect in the headline. It is still reported.

### 8.3 Repros (`repro.py`)

One script per finding cluster (same library, method, variant and mechanism), in
`runs/<name>/repros/`. It is standalone (numpy and the library only), prints versions,
builds data from a fixed seed and prints the expected vs observed `k` or coverage with
its exact SE. It exits 1 while the problem reproduces. `--verify` runs each one in a
subprocess and records the exit code. Verified repros are copied to
`docs/results/<study>/repros/`.

### 8.4 Pytest plugin and testing API

- Entry point `pytest11: conformcheck = conformcheck.pytest_plugin`. It is light at
  import, adds `--conformcheck-reps` and `--conformcheck-seed`, and provides the
  `conformcheck_settings` fixture.
- `conformcheck.testing.check_split_regressor(fn, n=..., alpha=..., reps=...)` and
  `check_split_classifier(...)` take a user callable
  `(x_cal, y_cal, x_test, alpha, model) -> intervals | sets`. They run the
  rank-recovery and exact-law tests on the built-in DGPs with Holm across the requested
  cells and return a report with `.assert_valid(allow_conservative=False)` and a
  readable summary.

## 9. Milestones

| # | Deliverable | Done-check |
|---|---|---|
| M0 | Scaffold, `laws.py` with reference values, design | `uv sync`, `uv run pytest`, `uv run ruff check .` green; DESIGN reviewed |
| M1 | `stats.py`: exact mean test (FFT), GOF, one-sided test, Holm, BY | Unit tests: Holm/BY against hand-computed examples and `scipy.stats.false_discovery_control(method="by")`; under simulated H0 (correct split, R=200, 500 cells) the rejection rate at 0.05 is within a binomial 99% interval; the FFT p-value matches the normal approximation within 0.01 for moderate t |
| M2 | `reference.py`, `data.py` | Reference reproduces hand values (e.g. n=19, alpha=0.1 uses the 18th score; jackknife+ with constant model equals split on n); each mutant shifts `k` as designed; a 200-rep run of the reference passes and each mutant is detected at n=19 |
| M3 | Adapters for MAPIE, crepes, puncc, TorchCP; `diagnostics.py` | Per adapter: one test reproducing a documented library example; rank recovery on n=19, alpha=0.1 matches `tmp`-verified values (MAPIE 18, puncc 18, TorchCP 18, crepes 19); `k > n` behaviour captured as REFUSED or trivial; tests marked `adapter`, run in CI |
| M4 | `study.py`, `runner.py`, CLI `plan`/`run` | `smoke` study runs in under 60 s; killing and resuming a run yields identical `units.jsonl` content (test); worker cap 4 enforced; `plan` prints the unit count and time estimate |
| M5 | `report.py`, CLI `report` | Report on the smoke run: reference PASS, `k_plus_1` CONSERVATIVE; matrix files written; statuses reproducible from `units.jsonl` alone |
| M6 | `repro.py`, CLI `repro` | Each generated repro runs standalone and exits 1 for a mutant and 0 for the reference; puncc repros re-run under `numpy<2` |
| M7 | `testing.py`, plugin fixture | A test in `tests/` uses the public API on the reference (passes) and a mutant (fails with a readable message) |
| M8 | Default study run, RAPS if time allows, `REPORT.md`, results in `docs/results/default/` | Run completes under the budget; controls behave as designed (else stop and report); every finding passes 8.2; README headline filled from `summary.md`; AGENTS.md status updated |

Order of risk: M3 (adapters) is the largest; M1 to M2 must be correct before any
library result is believed.

## 10. Test strategy

- **Laws** (`tests/test_laws.py`, done): hand-derived reference values (table below),
  simulation checks of the BetaBinomial and discrete laws, and bounds identities (CV+
  with `K = n` equals jackknife+).
- **Stats**: known-answer tests, a null calibration simulation and power against
  mutants (marked `slow` when over a few seconds).
- **Reference**: hand-computed tiny examples, e.g. n=4 with explicit scores.
- **Adapters**: documented-example reproduction, an input-shape contract, the `k > n`
  behaviour, and determinism under a fixed seed.
- **Runner**: resume and idempotence, the fingerprint guard, and the worker cap.
- **CI**: `pull_request` and `workflow_dispatch` only. Lint job, plus tests on
  ubuntu py3.11, ubuntu py3.13 and windows py3.13 with all extras (CPU torch).
  `-m "not slow"`.

Reference values (exact, `alpha` decimal):

| n | alpha | k | coverage | notes |
|---|---|---|---|---|
| 5 | 0.1 | 6 | 1 | `k > n`, trivial set |
| 5 | 0.2 | 5 | 5/6 | |
| 9 | 0.1 | 9 | 0.9 | boundary |
| 10 | 0.1 | 10 | 10/11 | |
| 19 | 0.1 | 18 | 0.9 | boundary; `Beta(18, 2)`, Var C = 36/8400 |
| 19 | 0.2 | 16 | 0.8 | boundary |
| 99 | 0.1 | 90 | 0.9 | boundary |
| 100 | 0.1 | 91 | 91/101 | |
| 1000 | 0.05 | 951 | 951/1001 | |
| any | 0.1 | - | jackknife+ >= 0.8 | Barber Thm 1 |
| 100 | 0.1 | K=10 | CV+ >= 0.8 - 9/110 | Barber Thm 4 |
| 19 | 0.1 | k'=19 | asym. CQR 18/20 | |
| BetaBinomial(10, 18, 2) | | | mean 9, var 10800/8400 | |

## 11. Risks and mitigations

| Risk | Mitigation |
|---|---|
| An adapter mistake looks like a library bug | 8.2: documented-example test per adapter, a standalone repro without conformcheck, a second look at the API docs, and the puncc numpy<2 re-check. Never call it a bug until all three pass |
| Mature libraries pass everything (null headline) | The integer-boundary, `k > n`, ties, randomized-set and asymmetric-CQR axes are where differences are likeliest (section 12). A clean PASS matrix is a valid, publishable result and is reported as such |
| Monte Carlo has no power at large n | Rank recovery for split regression; MDE reported per cell; full-size command documented |
| torchcp import stubs break with a new torchcp | Lock pins 1.2.1; `tests/test_import_stubs.py` in CI |
| puncc under numpy 2 differs from numpy 1 | Every puncc finding re-run under `numpy<2` (5.3) |
| crepes classification is slow at large n | Budget includes it; drop n=999/1000 for crepes classification if needed and say so |
| Floating point in the oracle itself | `laws.py` uses `fractions.Fraction`; tests pin the boundary cases |
| Licence: TorchCP is LGPL-3.0 | Optional extra, imported, never vendored or modified; noted in README |
| Upstream version drift | The lock pins versions; `run.json` records them; findings cite exact versions |

## 12. Pre-registered hypotheses (from source reading; to be confirmed or refuted)

Written before any study run. Each one gets a verdict in REPORT.md.

1. **crepes regression is conservative by one order statistic at integer boundaries.**
   `int((1 - confidence)(n+1))` with `confidence = 0.9` evaluates `1 - 0.9` as
   `0.09999999999999998`. At n=19 that gives `l = 1` instead of 2, so `k_used = 19`
   instead of 18 (coverage 0.95 instead of 0.90). Seen once in a scratch call
   (`WrapRegressor`, n=19); predicted for alpha in {0.1, 0.2} at n in {9, 19, 49, 99,
   999} and not at the paired n.
2. **crepes unsmoothed classification is conservative at integer boundaries** because
   the set is `{p >= 1 - confidence}` rather than `{p > alpha}`. This holds in exact
   arithmetic too.
3. **MAPIE APS `include_last_label=True` is conservative and `False` under-covers**,
   because calibration scores are randomized but the set rule is not. MAPIE documents
   the first; the second is the open question. `"randomized"` should PASS.
4. **The `k > n` behaviour differs:** MAPIE raises unless `allow_infinite_bounds=True`;
   puncc raises; crepes and TorchCP return trivial sets with a warning. All are valid.
5. **MAPIE asymmetric CQR (its default) has coverage `(2k'-(n+1))/(n+1)`**, not
   `k/(n+1)`. It is valid, and more conservative at small n.
6. **MAPIE RAPS follows the law with `n_eff = n - ceil(0.2 n)`.** Against nominal `n` it
   would look like LAW_MISMATCH.
7. **TorchCP float32 scores** may create ties at large `n` with near-saturated
   probabilities; if so, this shows up as conservative bracketing, not under-coverage.

## 13. References

- Vovk, Gammerman, Shafer (2005). *Algorithmic Learning in a Random World*. Springer.
- Vovk (2012). Conditional validity of inductive conformal predictors. ACML.
- Lei, G'Sell, Rinaldo, Tibshirani, Wasserman (2018). Distribution-free predictive
  inference for regression. JASA 113(523).
- Romano, Patterson, Candes (2019). Conformalized quantile regression. NeurIPS.
- Romano, Sesia, Candes (2020). Classification with valid and adaptive coverage.
  NeurIPS.
- Angelopoulos, Bates, Malik, Jordan (2021). Uncertainty sets for image classifiers
  using conformal prediction. ICLR.
- Barber, Candes, Ramdas, Tibshirani (2021). Predictive inference with the jackknife+.
  Annals of Statistics 49(1). arXiv:1905.02928.
- Angelopoulos, Bates (2023). Conformal prediction: a gentle introduction. Foundations
  and Trends in Machine Learning. arXiv:2107.07511.
- Holm (1979). A simple sequentially rejective multiple test procedure. Scand. J. Stat.
- Benjamini, Yekutieli (2001). The control of the false discovery rate in multiple
  testing under dependency. Annals of Statistics.
- Libraries: MAPIE https://github.com/scikit-learn-contrib/MAPIE; crepes
  https://github.com/henrikbostrom/crepes; puncc https://github.com/deel-ai/puncc;
  TorchCP https://github.com/ml-stat-Sustech/TorchCP (paper arXiv:2402.12683).

## 14. Round-2 addendum (written 2026-10-24, before the round-2 run)

### 14.1 RAPS rows

- Rows: `mapie/raps/include_last_label=True` (MAPIE's default rule) and
  `=randomized`; `puncc/raps/rand=False|True` and `torchcp/raps/randomized=False|True`
  with fixed `lambda = 0.1`, `k_reg = 1` (penalty `lambda (o - k_reg)^+` with `o` the
  1-based rank, the same convention in both libraries); reference rows
  `reference/raps/deterministic|randomized` with the same parameters. crepes has no RAPS.
- Grids: the split grid (`cls_gauss`, all `n`) and the toy grid (digits).
- Laws: randomized RAPS has a continuous score, so the exact BetaBinomial law applies;
  deterministic RAPS has score atoms and is tested one-sided, like deterministic APS.
- MAPIE: reading the 1.6.0 source while implementing showed that
  `SplitConformalClassifier` resets `RAPSConformityScore.size_raps` to None, so
  scikit-learn's `StratifiedShuffleSplit` default test share 0.1 applies, not the
  documented 0.2. MAPIE cells therefore use `n_eff = n - ceil(0.1 n)` (computed in floating
  point as scikit-learn does), and the adapter records the size MAPIE actually used.
  Two caveats: (1) the hold-out split is stratified by label, so the kept calibration
  points are not a uniformly random subset; the n_eff law is then exact only up to the
  effect of fixing the class counts, which we expect to be far below the resolution of
  R = 200; (2) MAPIE's level check runs on the hold-out size, so levels with
  `alpha < 1/ceil(0.1 n)` are refused although `k_eff <= n_eff` (OVER_REFUSED).
- `scripts/raps_neff.py` tests the MAPIE randomized cells against the law at the nominal
  `n`, at `n - ceil(0.1 n)` and at `n - ceil(0.2 n)` (hypothesis 6).

### 14.2 Bracketing as rank recovery for classification

`diagnostics.bracket_rank` had the lower end of the bracket one too low
(`#{s <= a}` instead of `#{s < a} + 1`, with `a` the largest included test score), which
made it blind to positive offsets. In v0.1 bracketing was diagnostic only, so no status
changed. Round 2 fixes it and promotes it to a deterministic check (like rank recovery)
for LAC and class-conditional LAC (one bracket per class against that class's `k_y`).
With `m = 500` test points and `K` labels, a one-step error is visible in a repetition
whenever some test score falls between `s_(k)` and `s_(k+-1)`; over 200 repetitions a
systematic error is caught with near certainty at any `n`. A set that is not a threshold
set of `1 - p` (beyond the float tolerance) is recorded as `nt` and carries no offset.
APS and RAPS are not bracketed: their deterministic set rules differ between libraries
(whether the label crossing the threshold is included), so an offset would grade a
convention rather than the order statistic.

### 14.3 Informative synthetic classifier

`cls_gauss_inf` draws the same four Gaussians as `cls_gauss` and uses the Bayes
posterior (`logits = mu_c . x - |mu_c|^2 / 2`, temperature 1; top-1 accuracy 0.708 on
100,000 draws, against 0.118 for the `cls_gauss` model). It runs every split
classification row (LAC, APS, RAPS).

### 14.4 Round-2 hypotheses

8. **MAPIE APS `include_last_label=False` over-covers on `cls_gauss_inf`**, as on digits:
   with an informative model the deterministic rule keeps the top label and drops the
   rest more rarely than the randomized calibration scores allow for.
9. **Randomized RAPS passes in puncc and TorchCP; MAPIE RAPS `randomized` passes against
   `n - ceil(0.1 n)`** and `include_last_label=True` is conservative, as for APS.
10. **Bracketing confirms F2/F3-type boundary effects at large n for crepes unsmoothed
    LAC** (k + 1 at n = 999, alpha in {0.1, 0.2}) and finds no offset in the other LAC
    rows.
