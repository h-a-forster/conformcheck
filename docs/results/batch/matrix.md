# Conformance matrix: study `batch`

R = 20 repetitions, m = 20 test points (capped by the pool on toy data), seed 20261030. Holm FWER 0.05 over 200 statistical cells; BY FDR 0.05 reported.

Status per row: worst over cells with n <= 100 (small n) and n > 100 (large n).

| row | small n | large n | cells | status counts | note |
|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | FAIL | - | 7 | FAIL 3, OVER_REFUSED 2, REFUSED 2 |  |
| `mapie/aps/include_last_label=True` | CONSERVATIVE | - | 7 | CONSERVATIVE 2, OVER_REFUSED 2, REFUSED 2, PASS 1 | MAPIE documents include_last_label=True as conservative |
| `mapie/aps/include_last_label=randomized` | OVER_REFUSED | - | 7 | OVER_REFUSED 2, REFUSED 2, PASS 3 |  |
| `mapie/cqr/asymmetric` | OVER_REFUSED | - | 7 | OVER_REFUSED 1, REFUSED 4, PASS 2 |  |
| `mapie/cqr/symmetric` | OVER_REFUSED | - | 7 | OVER_REFUSED 2, REFUSED 2, PASS 3 |  |
| `mapie/cv_plus/K=10` | PASS | - | 4 | PASS 4 |  |
| `mapie/cv_plus/K=5` | PASS | - | 4 | PASS 4 |  |
| `mapie/jackknife_plus/default` | PASS | - | 4 | PASS 4 |  |
| `mapie/lac/default` | OVER_REFUSED | - | 7 | OVER_REFUSED 2, REFUSED 2, PASS 3 |  |
| `mapie/raps/include_last_label=True` | ERROR | - | 7 | ERROR 3, CONSERVATIVE 2, REFUSED 2 | MAPIE documents include_last_label=True as conservative |
| `mapie/raps/include_last_label=randomized` | ERROR | - | 7 | ERROR 3, REFUSED 2, PASS 2 |  |
| `mapie/split_abs/allow_infinite_bounds` | REFUSED | - | 7 | REFUSED 2, PASS 5 |  |
| `mapie/split_abs/default` | OVER_REFUSED | - | 7 | OVER_REFUSED 2, REFUSED 2, PASS 3 |  |
| `crepes/class_conditional/smoothed` | PASS | - | 3 | PASS 3 |  |
| `crepes/class_conditional/unsmoothed` | CONSERVATIVE | - | 3 | CONSERVATIVE 2, PASS 1 |  |
| `crepes/lac/smoothed` | PASS | - | 7 | PASS 7 |  |
| `crepes/lac/unsmoothed` | CONSERVATIVE | - | 7 | CONSERVATIVE 2, PASS 5 |  |
| `crepes/split_abs/default` | CONSERVATIVE | - | 7 | CONSERVATIVE 2, PASS 5 |  |
| `puncc/aps/rand=False` | FAIL | - | 7 | FAIL 5, REFUSED 2 |  |
| `puncc/aps/rand=True` | FAIL | - | 7 | FAIL 5, REFUSED 2 |  |
| `puncc/class_conditional/default` | REFUSED | - | 3 | REFUSED 1, PASS 2 |  |
| `puncc/cqr/default` | FAIL | - | 7 | FAIL 5, REFUSED 2 |  |
| `puncc/cv_plus/K=10` | ERROR | - | 4 | ERROR 1, REFUSED 1, PASS 2 |  |
| `puncc/cv_plus/K=5` | ERROR | - | 4 | ERROR 1, REFUSED 1, PASS 2 |  |
| `puncc/jackknife_plus/K=n` | ERROR | - | 4 | ERROR 4 |  |
| `puncc/lac/default` | REFUSED | - | 7 | REFUSED 2, PASS 5 |  |
| `puncc/raps/rand=False` | FAIL | - | 7 | FAIL 5, REFUSED 2 |  |
| `puncc/raps/rand=True` | FAIL | - | 7 | FAIL 5, REFUSED 2 |  |
| `puncc/split_abs/default` | REFUSED | - | 7 | REFUSED 2, PASS 5 |  |
| `torchcp/aps/randomized=False` | PASS | - | 7 | PASS 7 |  |
| `torchcp/aps/randomized=True` | PASS | - | 7 | PASS 7 |  |
| `torchcp/class_conditional/default` | PASS | - | 3 | PASS 3 |  |
| `torchcp/cqr/default` | ERROR | - | 7 | ERROR 2, PASS 5 |  |
| `torchcp/lac/default` | PASS | - | 7 | PASS 7 |  |
| `torchcp/raps/randomized=False` | PASS | - | 7 | PASS 7 |  |
| `torchcp/raps/randomized=True` | PASS | - | 7 | PASS 7 |  |
| `torchcp/split_abs/default` | ERROR | - | 7 | ERROR 2, PASS 5 |  |
| `reference/aps/deterministic` | PASS | - | 7 | PASS 7 |  |
| `reference/aps/randomized` | PASS | - | 7 | PASS 7 |  |
| `reference/class_conditional/default` | PASS | - | 3 | PASS 3 |  |
| `reference/cqr/asymmetric` | PASS | - | 7 | PASS 7 |  |
| `reference/cqr/symmetric` | PASS | - | 7 | PASS 7 |  |
| `reference/cv_plus/K=10` | PASS | - | 4 | PASS 4 |  |
| `reference/cv_plus/K=5` | PASS | - | 4 | PASS 4 |  |
| `reference/jackknife_plus/default` | PASS | - | 4 | PASS 4 |  |
| `reference/lac/default` | PASS | - | 7 | PASS 7 |  |
| `reference/lac/smoothed` | PASS | - | 7 | PASS 7 |  |
| `reference/raps/deterministic` | PASS | - | 7 | PASS 7 |  |
| `reference/raps/randomized` | PASS | - | 7 | PASS 7 |  |
| `reference/split_abs/default` | PASS | - | 7 | PASS 7 |  |

## Status grid (worst over dgps and alphas at each n)

P pass, C conservative, F fail, L law mismatch, O refused a feasible level, R refused with k > n, E error, . not run.

| row | 9 | 10 | 20 | 100 |
|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | F | . | . | F |
| `mapie/aps/include_last_label=True` | O | . | . | C |
| `mapie/aps/include_last_label=randomized` | O | . | . | O |
| `mapie/cqr/asymmetric` | O | . | . | R |
| `mapie/cqr/symmetric` | O | . | . | O |
| `mapie/cv_plus/K=10` | . | . | P | . |
| `mapie/cv_plus/K=5` | . | . | P | . |
| `mapie/jackknife_plus/default` | . | P | . | . |
| `mapie/lac/default` | O | . | . | O |
| `mapie/raps/include_last_label=True` | E | . | . | C |
| `mapie/raps/include_last_label=randomized` | E | . | . | R |
| `mapie/split_abs/allow_infinite_bounds` | R | . | . | R |
| `mapie/split_abs/default` | O | . | . | O |
| `crepes/class_conditional/smoothed` | P | . | . | . |
| `crepes/class_conditional/unsmoothed` | C | . | . | . |
| `crepes/lac/smoothed` | P | . | . | P |
| `crepes/lac/unsmoothed` | C | . | . | P |
| `crepes/split_abs/default` | C | . | . | P |
| `puncc/aps/rand=False` | F | . | . | F |
| `puncc/aps/rand=True` | F | . | . | F |
| `puncc/class_conditional/default` | R | . | . | . |
| `puncc/cqr/default` | F | . | . | F |
| `puncc/cv_plus/K=10` | . | . | E | . |
| `puncc/cv_plus/K=5` | . | . | E | . |
| `puncc/jackknife_plus/K=n` | . | E | . | . |
| `puncc/lac/default` | R | . | . | R |
| `puncc/raps/rand=False` | F | . | . | F |
| `puncc/raps/rand=True` | F | . | . | F |
| `puncc/split_abs/default` | R | . | . | R |
| `torchcp/aps/randomized=False` | P | . | . | P |
| `torchcp/aps/randomized=True` | P | . | . | P |
| `torchcp/class_conditional/default` | P | . | . | . |
| `torchcp/cqr/default` | E | . | . | E |
| `torchcp/lac/default` | P | . | . | P |
| `torchcp/raps/randomized=False` | P | . | . | P |
| `torchcp/raps/randomized=True` | P | . | . | P |
| `torchcp/split_abs/default` | E | . | . | E |
| `reference/aps/deterministic` | P | . | . | P |
| `reference/aps/randomized` | P | . | . | P |
| `reference/class_conditional/default` | P | . | . | . |
| `reference/cqr/asymmetric` | P | . | . | P |
| `reference/cqr/symmetric` | P | . | . | P |
| `reference/cv_plus/K=10` | . | . | P | . |
| `reference/cv_plus/K=5` | . | . | P | . |
| `reference/jackknife_plus/default` | . | P | . | . |
| `reference/lac/default` | P | . | . | P |
| `reference/lac/smoothed` | P | . | . | P |
| `reference/raps/deterministic` | P | . | . | P |
| `reference/raps/randomized` | P | . | . | P |
| `reference/split_abs/default` | P | . | . | P |

## Non-PASS cells (libraries)

| row | dgp | n | alpha | k | status | coverage [95% CI] | target | rank offsets lower|upper or bracket (reps) | Holm p | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9000 [0.8716, 0.9284] | 0.8000 | bracket {"1": 20} | 0.0013 | bracket +1 in 20 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | bracket {"0": 1, "1": 19} | 3.5e-13 | bracket +1 in 19 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9325 [0.8975, 0.9675] | 0.8000 | bracket {"0": 9, "1": 11} | 0.00078 | bracket +1 in 11 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | bracket {"0": 5, "1": 15} | 5.3e-08 | bracket +1 in 15 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9175 [0.8757, 0.9593] | 0.8000 | {"1|1": 20} | 0.017 | rank +1 in 20 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | {"1|1": 20} | 5.3e-08 | rank +1 in 20 reps |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.2 | 8 | FAIL | 0.5150 [0.4421, 0.5879] | 0.8000 |  | 9.2e-11 | Holm p=9.2e-11, coverage 0.5150 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.2 | 81 | FAIL | 0.5225 [0.4686, 0.5764] | 0.8020 |  | 1.6e-13 | Holm p=1.6e-13, coverage 0.5225 vs 0.8020 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.1 | 91 | FAIL | 0.5450 [0.4872, 0.6028] | 0.9010 |  | 1.8e-13 | Holm p=1.8e-13, coverage 0.5450 vs 0.9010 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.9025 [0.8746, 0.9304] | 0.8020 |  | 0.00022 | Holm p=0.00022, coverage 0.9025 vs 0.8020 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9750 [0.9608, 0.9892] | 0.9010 |  | 3.8e-05 | Holm p=3.8e-05, coverage 0.9750 vs 0.9010 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.2 | 8 | OVER_REFUSED |  | 0.8000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.1 | 9 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.8850 [0.8545, 0.9155] | 0.8022 |  | 0.024 | Holm p=0.024, coverage 0.8850 vs 0.8022 |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9750 [0.9630, 0.9870] | 0.9011 |  | 4.8e-05 | Holm p=4.8e-05, coverage 0.9750 vs 0.9011 |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 20/20 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (100) is too low to reach the requ |
| `mapie/split_abs/default` | reg_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.2 | 8 | FAIL | 0.9900 [0.9737, 1.0000] | 0.8000 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -2.978, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445 |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.1 | 9 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9000 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455 |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=False` | cls_gauss | 100 | 0.2 | 81 | FAIL | 1.0000 [1.0000, 1.0000] | 0.8020 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 0.1 | 91 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9010 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 1/101 | 100 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9901 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.2 | 8 | FAIL | 0.7975 [0.7047, 0.8903] | 0.8000 |  | 1 | batch shuffled: set size -0.080, coverage -0.035; size=1: set size -2.540, coverage -0.685; size=3: set size -0.712, coverage -0.267; size=7: set size +0.025, coverage -0.002 (Holm p=5.2e-14) |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.1 | 9 | FAIL | 0.9175 [0.8642, 0.9708] | 0.9000 |  | 1 | batch shuffled: set size +0.037, coverage +0.015; size=1: set size -2.803, coverage -0.805; size=3: set size -0.920, coverage -0.378; size=7: set size -0.018, coverage -0.020 (Holm p=7.2e-21) |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=True` | cls_gauss | 100 | 0.2 | 81 | FAIL | 0.7950 [0.7571, 0.8329] | 0.8020 |  | 1 | batch shuffled: set size -0.008, coverage -0.010; size=1: set size -2.615, coverage -0.667; size=3: set size -0.752, coverage -0.265; size=7: set size -0.018, coverage -0.020 (Holm p=2.2e-22) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 0.1 | 91 | FAIL | 0.9175 [0.8920, 0.9430] | 0.9010 |  | 1 | batch shuffled: set size -0.045, coverage -0.023; size=1: set size -2.840, coverage -0.790; size=3: set size -0.948, coverage -0.378; size=7: set size -0.027, coverage -0.017 (Holm p=4.6e-30) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 1/101 | 100 | FAIL | 0.9925 [0.9839, 1.0000] | 0.9901 |  | 1 | batch shuffled: set size +0.010, coverage +0.005; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.453; size=7: set size -0.013, coverage -0.008 (Holm p=2.2e-37) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/class_conditional/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_gauss | 9 | 0.2 | 8 | FAIL | 0.8250 [0.7744, 0.8756] | 0.8000 | {"0|0": 20} | 1 | batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 9 | 0.1 | 9 | FAIL | 0.9025 [0.8627, 0.9423] | 0.9000 | {"0|0": 20} | 1 | batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_gauss | 100 | 0.2 | 81 | FAIL | 0.8050 [0.7621, 0.8479] | 0.8020 | {"0|0": 20} | 1 | batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 0.1 | 91 | FAIL | 0.9100 [0.8723, 0.9477] | 0.9010 | {"0|0": 20} | 1 | batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 1/101 | 100 | FAIL | 0.9925 [0.9839, 1.0000] | 0.9901 | {"0|0": 20} | 1 | batch size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=10` | reg_gauss | 20 | 1/21 | 20 | ERROR |  | 0.8593 |  |  | 20/20 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 0.8688 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cv_plus/K=5` | reg_gauss | 20 | 1/21 | 20 | ERROR |  | 0.7798 |  |  | 20/20 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 0.7893 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 0.2 | 9 | ERROR |  | 0.6000 |  |  | 20/20 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 0.1 | 10 | ERROR |  | 0.8000 |  |  | 20/20 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 1/11 | 10 | ERROR |  | 0.8182 |  |  | 20/20 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 9/110 | 11 | ERROR |  | 0.8364 |  |  | 20/20 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/lac/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/lac/default` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.2 | 8 | FAIL | 0.9900 [0.9737, 1.0000] | 0.8000 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -2.980, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445 |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.1 | 9 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9000 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455 |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=False` | cls_gauss | 100 | 0.2 | 81 | FAIL | 1.0000 [1.0000, 1.0000] | 0.8020 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 0.1 | 91 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9010 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 1/101 | 100 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9901 |  | 1 | batch size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.2 | 8 | FAIL | 0.9300 [0.8619, 0.9981] | 0.8000 |  | 0.0014 | Holm p=0.0014, coverage 0.9300 vs 0.8000; batch shuffled: set size -0.040, coverage +0.007; size=1: set size -2.858, coverage -0.817; size=3: set size -0.963, coverage -0.388; size=7: set size +0.013, coverage +0.020 (Holm p=3.4e-17) |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.1 | 9 | FAIL | 0.9925 [0.9810, 1.0000] | 0.9000 |  | 3e-05 | Holm p=3e-05, coverage 0.9925 vs 0.9000; batch shuffled: set size +0.020, coverage +0.008; size=1: set size -2.978, coverage -0.880; size=3: set size -1.078, coverage -0.448; size=7: set size -0.005, coverage -0.005 (Holm p=5e-29) |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.2 | 81 | FAIL | 0.9825 [0.9688, 0.9962] | 0.8020 |  | 0 | Holm p=0, coverage 0.9825 vs 0.8020; batch shuffled: set size -0.002, coverage -0.008; size=1: set size -2.950, coverage -0.855; size=3: set size -1.050, coverage -0.443; size=7: set size -0.005, coverage -0.013 (Holm p=4.6e-32) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.1 | 91 | FAIL | 0.9925 [0.9839, 1.0000] | 0.9010 |  | 2e-10 | Holm p=2e-10, coverage 0.9925 vs 0.9010; batch shuffled: set size +0.003, coverage -0.003; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.452; size=7: set size +0.000, coverage +0.008 (Holm p=5.6e-39) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 1/101 | 100 | FAIL | 1.0000 [1.0000, 1.0000] | 0.9901 |  | 1 | batch shuffled: set size +0.000, coverage +0.000; size=1: set size -3.000, coverage -0.872; size=3: set size -1.100, coverage -0.460; size=7: set size -0.005, coverage +0.000 (Holm p=0) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `torchcp/cqr/default` | reg_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 20/20 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 20/20 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 20/20 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 20/20 reps raised AttributeError: 'float' object has no attribute 'shape' |

## Batch-size invariance

The test points of each repetition were predicted again in chunks (size=1, size=3, size=7) and in one shuffled call, and compared with the full batch: 235 cells, 60 of them randomized (paired test on mean set size and coverage, Holm across those cells); 25 cells are not invariant.

| row | dgp | n | alpha | batch status | detail |
|---|---|---|---|---|---|
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.2 | FAIL | size=1: differs in 20/20 reps (400 points), set size -2.978, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445 |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.1 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 0.2 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 0.1 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=False` | cls_gauss | 100 | 1/101 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.2 | FAIL | shuffled: set size -0.080, coverage -0.035; size=1: set size -2.540, coverage -0.685; size=3: set size -0.712, coverage -0.267; size=7: set size +0.025, coverage -0.002 (Holm p=5.2e-14) |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.1 | FAIL | shuffled: set size +0.037, coverage +0.015; size=1: set size -2.803, coverage -0.805; size=3: set size -0.920, coverage -0.378; size=7: set size -0.018, coverage -0.020 (Holm p=7.2e-21) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 0.2 | FAIL | shuffled: set size -0.008, coverage -0.010; size=1: set size -2.615, coverage -0.667; size=3: set size -0.752, coverage -0.265; size=7: set size -0.018, coverage -0.020 (Holm p=2.2e-22) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 0.1 | FAIL | shuffled: set size -0.045, coverage -0.023; size=1: set size -2.840, coverage -0.790; size=3: set size -0.948, coverage -0.378; size=7: set size -0.027, coverage -0.017 (Holm p=4.6e-30) |
| `puncc/aps/rand=True` | cls_gauss | 100 | 1/101 | FAIL | shuffled: set size +0.010, coverage +0.005; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.453; size=7: set size -0.013, coverage -0.008 (Holm p=2.2e-37) |
| `puncc/cqr/default` | reg_gauss | 9 | 0.2 | FAIL | size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 9 | 0.1 | FAIL | size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 0.2 | FAIL | size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 0.1 | FAIL | size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/cqr/default` | reg_gauss | 100 | 1/101 | FAIL | size=1: status differs in 20/20 reps (RuntimeError: Each Y_pred must contain lower and higher quan) |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.2 | FAIL | size=1: differs in 20/20 reps (400 points), set size -2.980, coverage -0.878; size=3: differs in 20/20 reps (394 points), set size -1.080, coverage -0.445 |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.1 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.887; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.455 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 0.2 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 0.1 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=False` | cls_gauss | 100 | 1/101 | FAIL | size=1: differs in 20/20 reps (400 points), set size -3.000, coverage -0.872; size=3: differs in 20/20 reps (400 points), set size -1.100, coverage -0.460 |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.2 | FAIL | shuffled: set size -0.040, coverage +0.007; size=1: set size -2.858, coverage -0.817; size=3: set size -0.963, coverage -0.388; size=7: set size +0.013, coverage +0.020 (Holm p=3.4e-17) |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.1 | FAIL | shuffled: set size +0.020, coverage +0.008; size=1: set size -2.978, coverage -0.880; size=3: set size -1.078, coverage -0.448; size=7: set size -0.005, coverage -0.005 (Holm p=5e-29) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.2 | FAIL | shuffled: set size -0.002, coverage -0.008; size=1: set size -2.950, coverage -0.855; size=3: set size -1.050, coverage -0.443; size=7: set size -0.005, coverage -0.013 (Holm p=4.6e-32) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.1 | FAIL | shuffled: set size +0.003, coverage -0.003; size=1: set size -2.985, coverage -0.865; size=3: set size -1.085, coverage -0.452; size=7: set size +0.000, coverage +0.008 (Holm p=5.6e-39) |
| `puncc/raps/rand=True` | cls_gauss | 100 | 1/101 | FAIL | shuffled: set size +0.000, coverage +0.000; size=1: set size -3.000, coverage -0.872; size=3: set size -1.100, coverage -0.460; size=7: set size -0.005, coverage +0.000 (Holm p=0) |
