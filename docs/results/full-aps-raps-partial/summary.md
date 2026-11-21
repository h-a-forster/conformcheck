# Summary: study `full-aps-raps`

Versions: conformcheck 0.2.0, crepes 0.9.1, mapie 1.6.0, numpy 2.5.4, puncc 0.9.3, python 3.12.10, scikit-learn 1.9.1, scipy 1.18.1, torch 2.14.1+cpu, torchcp 1.2.1

**Headline.** 4 of 13 library-method rows are flagged (FAIL, CONSERVATIVE, LAW_MISMATCH, OVER_REFUSED or ERROR) in at least one cell with n <= 100. A documented row is excused only for its documented status.

Small-n status counts: - 9, CONSERVATIVE 2, FAIL 1, OVER_REFUSED 1

## Oracle controls

Size (reference implementations through the same pipeline): reference_cells = 20, reference_statistical_cells = 16, reference_holm_rejections = 0, reference_nonpass_cells = 0, reference_raw_rejections_at_0.05 = 0, reference_exact_mean_tests = 8, reference_exact_mean_rejections_at_0.05 = 0, reference_exact_mean_rejection_rate = 0

Power (mutants of split regression and LAC; statistical detections / cells per n, deterministic rank recovery or bracketing included in 'any'; cells where the mutant uses the correct order statistic are excluded):


## Flagged rows

### `mapie/aps/include_last_label=False`

- cls_gauss_inf n=99 a=1/5: FAIL (Holm p=0, coverage 0.7424 vs 0.8000)
- cls_gauss_inf n=99 a=1/10: FAIL (Holm p=0, coverage 0.7958 vs 0.9000)
- cls_gauss_inf n=99 a=1/20: FAIL (Holm p=0, coverage 0.8517 vs 0.9500)
- cls_gauss_inf n=99 a=1/100: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=99 a=9/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=1/5: FAIL (Holm p=0, coverage 0.7400 vs 0.8000)
- cls_gauss_inf n=999 a=1/10: FAIL (Holm p=0, coverage 0.7920 vs 0.9000)
- cls_gauss_inf n=999 a=1/20: FAIL (Holm p=0, coverage 0.8466 vs 0.9500)
- cls_gauss_inf n=999 a=1/1000: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `mapie/aps/include_last_label=True` (MAPIE documents include_last_label=True as conservative)

- cls_gauss_inf n=99 a=1/5: CONSERVATIVE (Holm p=0, coverage 0.9132 vs 0.8000)
- cls_gauss_inf n=99 a=1/10: CONSERVATIVE (Holm p=0, coverage 0.9585 vs 0.9000)
- cls_gauss_inf n=99 a=1/20: CONSERVATIVE (Holm p=0, coverage 0.9812 vs 0.9500)
- cls_gauss_inf n=99 a=1/100: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=99 a=9/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=1/5: CONSERVATIVE (Holm p=0, coverage 0.9133 vs 0.8000)
- cls_gauss_inf n=999 a=1/10: CONSERVATIVE (Holm p=0, coverage 0.9588 vs 0.9000)
- cls_gauss_inf n=999 a=1/20: CONSERVATIVE (Holm p=0, coverage 0.9813 vs 0.9500)
- cls_gauss_inf n=999 a=1/1000: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `mapie/aps/include_last_label=randomized`

- cls_gauss_inf n=99 a=1/100: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=99 a=9/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=1/1000: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `mapie/raps/include_last_label=True` (MAPIE documents include_last_label=True as conservative)

- cls_gauss_inf n=99 a=1/5: CONSERVATIVE (Holm p=0, coverage 0.9183 vs 0.8000)
- cls_gauss_inf n=99 a=1/10: CONSERVATIVE (Holm p=0, coverage 0.9607 vs 0.9000)
- cls_gauss_inf n=99 a=1/20: OVER_REFUSED (refused a feasible level (k <= n))
- cls_gauss_inf n=99 a=1/100: REFUSED (refused (k > n))
- cls_gauss_inf n=99 a=9/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=1/5: CONSERVATIVE (Holm p=0, coverage 0.9170 vs 0.8000)
- cls_gauss_inf n=999 a=1/10: CONSERVATIVE (Holm p=0, coverage 0.9623 vs 0.9000)
- cls_gauss_inf n=999 a=1/20: CONSERVATIVE (Holm p=0, coverage 0.9854 vs 0.9500)
- cls_gauss_inf n=999 a=1/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `mapie/raps/include_last_label=randomized`

- cls_gauss_inf n=999 a=1/20: CONSERVATIVE (Holm p=2.4e-36, coverage 0.9514 vs 0.9500)
- cls_gauss_inf n=999 a=1/1000: REFUSED (refused (k > n))
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `puncc/aps/rand=False`

- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `puncc/aps/rand=True`

- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `puncc/raps/rand=False`

- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

### `puncc/raps/rand=True`

- cls_gauss_inf n=999 a=1/5: CONSERVATIVE (Holm p=0, coverage 0.8274 vs 0.8000)
- cls_gauss_inf n=999 a=1/10: CONSERVATIVE (Holm p=0, coverage 0.9202 vs 0.9000)
- cls_gauss_inf n=999 a=1/20: CONSERVATIVE (Holm p=0, coverage 0.9641 vs 0.9500)
- cls_gauss_inf n=999 a=1/1000: CONSERVATIVE (Holm p=2.1e-205, coverage 0.9998 vs 0.9990)
- cls_gauss_inf n=999 a=9/10000: REFUSED (refused (k > n))

