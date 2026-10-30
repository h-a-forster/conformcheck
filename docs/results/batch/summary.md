# Summary: study `batch`

Versions: conformcheck 0.2.0, crepes 0.9.1, mapie 1.6.0, numpy 2.5.4, puncc 0.9.3, python 3.13.1, scikit-learn 1.9.1, scipy 1.18.1, torch 2.14.1+cpu, torchcp 1.2.1

**Headline.** 22 of 37 library-method rows are flagged (FAIL, CONSERVATIVE, LAW_MISMATCH, OVER_REFUSED or ERROR) in at least one cell with n <= 100. A documented row is excused only for its documented status.

Small-n status counts: CONSERVATIVE 4, ERROR 7, FAIL 6, OVER_REFUSED 5, PASS 11, REFUSED 4

## Oracle controls

Size (reference implementations through the same pipeline): reference_cells = 78, reference_statistical_cells = 59, reference_holm_rejections = 0, reference_nonpass_cells = 0, reference_raw_rejections_at_0.05 = 1, reference_exact_mean_tests = 27, reference_exact_mean_rejections_at_0.05 = 0, reference_exact_mean_rejection_rate = 0

Power (mutants of split regression and LAC; statistical detections / cells per n, deterministic rank recovery or bracketing included in 'any'; cells where the mutant uses the correct order statistic are excluded):


## Flagged rows

### `mapie/aps/include_last_label=False`

- cls_gauss n=9 a=1/5: FAIL (Holm p=9.2e-11, coverage 0.5150 vs 0.8000)
- cls_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: FAIL (Holm p=1.6e-13, coverage 0.5225 vs 0.8020)
- cls_gauss n=100 a=1/10: FAIL (Holm p=1.8e-13, coverage 0.5450 vs 0.9010)
- cls_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/aps/include_last_label=True` (MAPIE documents include_last_label=True as conservative)

- cls_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: CONSERVATIVE (Holm p=0.00022, coverage 0.9025 vs 0.8020)
- cls_gauss n=100 a=1/10: CONSERVATIVE (Holm p=3.8e-05, coverage 0.9750 vs 0.9010)
- cls_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/aps/include_last_label=randomized`

- cls_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/cqr/asymmetric`

- reg_gauss n=9 a=1/5: OVER_REFUSED (refused a feasible level (k <= n))
- reg_gauss n=9 a=1/10: REFUSED (refused (k > n))
- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=1/101: REFUSED (refused (k > n))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/cqr/symmetric`

- reg_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/lac/default`

- cls_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/raps/include_last_label=True` (MAPIE documents include_last_label=True as conservative)

- cls_gauss n=9 a=1/5: ERROR (20/20 reps raised)
- cls_gauss n=9 a=1/10: ERROR (20/20 reps raised)
- cls_gauss n=9 a=9/100: ERROR (20/20 reps raised)
- cls_gauss n=100 a=1/5: CONSERVATIVE (Holm p=0.024, coverage 0.8850 vs 0.8022)
- cls_gauss n=100 a=1/10: CONSERVATIVE (Holm p=4.8e-05, coverage 0.9750 vs 0.9011)
- cls_gauss n=100 a=1/101: REFUSED (refused (k > n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/raps/include_last_label=randomized`

- cls_gauss n=9 a=1/5: ERROR (20/20 reps raised)
- cls_gauss n=9 a=1/10: ERROR (20/20 reps raised)
- cls_gauss n=9 a=9/100: ERROR (20/20 reps raised)
- cls_gauss n=100 a=1/101: REFUSED (refused (k > n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/split_abs/allow_infinite_bounds`

- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `mapie/split_abs/default`

- reg_gauss n=9 a=1/10: OVER_REFUSED (refused a feasible level (k <= n))
- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=1/101: OVER_REFUSED (refused a feasible level (k <= n))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `crepes/class_conditional/unsmoothed`

- cls_gauss n=9 a=1/5: CONSERVATIVE (bracket +1 in 20 reps)
- cls_gauss n=9 a=1/10: CONSERVATIVE (bracket +1 in 19 reps)

### `crepes/lac/unsmoothed`

- cls_gauss n=9 a=1/5: CONSERVATIVE (bracket +1 in 11 reps)
- cls_gauss n=9 a=1/10: CONSERVATIVE (bracket +1 in 15 reps)

### `crepes/split_abs/default`

- reg_gauss n=9 a=1/5: CONSERVATIVE (rank +1 in 20 reps)
- reg_gauss n=9 a=1/10: CONSERVATIVE (rank +1 in 20 reps)

### `puncc/aps/rand=False`

- cls_gauss n=9 a=1/5: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -2.978, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445)
- cls_gauss n=9 a=1/10: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455)
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=1/10: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=1/101: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/aps/rand=True`

- cls_gauss n=9 a=1/5: FAIL (batch shuffled: set size -0.080, coverage -0.035; size=1: set size -2.540, coverage -0.685; size=3: set size -0.712, coverage -0.267; size=7: set size +0.025, coverage -0.002 (Holm p=5.2e-14))
- cls_gauss n=9 a=1/10: FAIL (batch shuffled: set size +0.037, coverage +0.015; size=1: set size -2.803, coverage -0.805; size=3: set size -0.920, coverage -0.378; size=7: set size -0.018, coverage -0.020 (Holm p=7.2e-21))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: FAIL (batch shuffled: set size -0.008, coverage -0.010; size=1: set size -2.615, coverage -0.667; size=3: set size -0.752, coverage -0.265; size=7: set size -0.018, coverage -0.020 (Holm p=2.2e-22))
- cls_gauss n=100 a=1/10: FAIL (batch shuffled: set size -0.045, coverage -0.023; size=1: set size -2.840, coverage -0.790; size=3: set size -0.948, coverage -0.378; size=7: set size -0.027, coverage -0.017 (Holm p=4.6e-30))
- cls_gauss n=100 a=1/101: FAIL (batch shuffled: set size +0.010, coverage +0.005; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.453; size=7: set size -0.013, coverage -0.008 (Holm p=2.2e-37))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/class_conditional/default`

- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))

### `puncc/cqr/default`

- reg_gauss n=9 a=1/5: FAIL (batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan))
- reg_gauss n=9 a=1/10: FAIL (batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan))
- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=1/5: FAIL (batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan))
- reg_gauss n=100 a=1/10: FAIL (batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan))
- reg_gauss n=100 a=1/101: FAIL (batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/cv_plus/K=10`

- reg_gauss n=20 a=1/21: ERROR (20/20 reps raised)
- reg_gauss n=20 a=3/70: REFUSED (refused (k > n))

### `puncc/cv_plus/K=5`

- reg_gauss n=20 a=1/21: ERROR (20/20 reps raised)
- reg_gauss n=20 a=3/70: REFUSED (refused (k > n))

### `puncc/jackknife_plus/K=n`

- reg_gauss n=10 a=1/5: ERROR (20/20 reps raised)
- reg_gauss n=10 a=1/10: ERROR (20/20 reps raised)
- reg_gauss n=10 a=1/11: ERROR (20/20 reps raised)
- reg_gauss n=10 a=9/110: ERROR (20/20 reps raised)

### `puncc/lac/default`

- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/raps/rand=False`

- cls_gauss n=9 a=1/5: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -2.980, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445)
- cls_gauss n=9 a=1/10: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455)
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=1/10: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=1/101: FAIL (batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460)
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/raps/rand=True`

- cls_gauss n=9 a=1/5: FAIL (Holm p=0.0014, coverage 0.9300 vs 0.8000; batch shuffled: set size -0.040, coverage +0.007; size=1: set size -2.858, coverage -0.817; size=3: set size -0.963, coverage -0.388; size=7: set size +0.013, coverage +0.020 (Holm p=3.4e-17))
- cls_gauss n=9 a=1/10: FAIL (Holm p=3e-05, coverage 0.9925 vs 0.9000; batch shuffled: set size +0.020, coverage +0.008; size=1: set size -2.978, coverage -0.880; size=3: set size -1.078, coverage -0.448; size=7: set size -0.005, coverage -0.005 (Holm p=5e-29))
- cls_gauss n=9 a=9/100: REFUSED (refused (k > n))
- cls_gauss n=100 a=1/5: FAIL (Holm p=0, coverage 0.9825 vs 0.8020; batch shuffled: set size -0.002, coverage -0.008; size=1: set size -2.950, coverage -0.855; size=3: set size -1.050, coverage -0.443; size=7: set size -0.005, coverage -0.013 (Holm p=4.6e-32))
- cls_gauss n=100 a=1/10: FAIL (Holm p=2e-10, coverage 0.9925 vs 0.9010; batch shuffled: set size +0.003, coverage -0.003; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.452; size=7: set size +0.000, coverage +0.008 (Holm p=5.6e-39))
- cls_gauss n=100 a=1/101: FAIL (batch shuffled: set size +0.000, coverage +0.000; size=1: set size -3.000, coverage -0.872; size=3: set size -1.100, coverage -0.460; size=7: set size -0.005, coverage +0.000 (Holm p=0))
- cls_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `puncc/split_abs/default`

- reg_gauss n=9 a=9/100: REFUSED (refused (k > n))
- reg_gauss n=100 a=9/1010: REFUSED (refused (k > n))

### `torchcp/cqr/default`

- reg_gauss n=9 a=9/100: ERROR (20/20 reps raised)
- reg_gauss n=100 a=9/1010: ERROR (20/20 reps raised)

### `torchcp/split_abs/default`

- reg_gauss n=9 a=9/100: ERROR (20/20 reps raised)
- reg_gauss n=100 a=9/1010: ERROR (20/20 reps raised)

