# Conformance matrix: study `default`

R = 200 repetitions, m = 500 test points (capped by the pool on toy data), seed 20261023. Holm FWER 0.05 over 4348 statistical cells; BY FDR 0.05 reported.

Status per row: worst over cells with n <= 100 (small n) and n > 100 (large n).

| row | small n | large n | cells | status counts | note |
|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | ERROR | FAIL | 114 | ERROR 23, FAIL 48, CONSERVATIVE 8, OVER_REFUSED 17, REFUSED 18 |  |
| `mapie/aps/include_last_label=True` | ERROR | CONSERVATIVE | 114 | ERROR 23, CONSERVATIVE 56, OVER_REFUSED 17, REFUSED 18 | MAPIE documents include_last_label=True as conservative |
| `mapie/aps/include_last_label=randomized` | ERROR | OVER_REFUSED | 114 | ERROR 23, OVER_REFUSED 17, REFUSED 18, PASS 56 |  |
| `mapie/cqr/asymmetric` | OVER_REFUSED | REFUSED | 114 | OVER_REFUSED 5, REFUSED 59, PASS 50 |  |
| `mapie/cqr/symmetric` | OVER_REFUSED | OVER_REFUSED | 114 | OVER_REFUSED 22, REFUSED 30, PASS 62 |  |
| `mapie/cv_plus/K=10` | PASS | CONSERVATIVE | 78 | CONSERVATIVE 1, PASS 77 |  |
| `mapie/cv_plus/K=5` | PASS | CONSERVATIVE | 78 | CONSERVATIVE 1, PASS 77 |  |
| `mapie/jackknife_plus/default` | PASS | - | 66 | PASS 66 |  |
| `mapie/lac/default` | OVER_REFUSED | OVER_REFUSED | 114 | OVER_REFUSED 22, REFUSED 30, PASS 62 |  |
| `mapie/raps/include_last_label=True` | ERROR | CONSERVATIVE | 114 | ERROR 52, CONSERVATIVE 26, OVER_REFUSED 12, REFUSED 24 | MAPIE documents include_last_label=True as conservative |
| `mapie/raps/include_last_label=randomized` | ERROR | REFUSED | 114 | ERROR 52, OVER_REFUSED 12, REFUSED 24, PASS 26 |  |
| `mapie/split_abs/allow_infinite_bounds` | REFUSED | REFUSED | 157 | REFUSED 43, PASS 114 |  |
| `mapie/split_abs/default` | OVER_REFUSED | OVER_REFUSED | 157 | OVER_REFUSED 31, REFUSED 43, PASS 83 |  |
| `crepes/class_conditional/smoothed` | PASS | - | 38 | PASS 38 |  |
| `crepes/class_conditional/unsmoothed` | CONSERVATIVE | - | 38 | CONSERVATIVE 9, PASS 29 |  |
| `crepes/lac/smoothed` | PASS | PASS | 114 | PASS 114 |  |
| `crepes/lac/unsmoothed` | CONSERVATIVE | CONSERVATIVE | 114 | CONSERVATIVE 28, PASS 86 |  |
| `crepes/split_abs/default` | CONSERVATIVE | CONSERVATIVE | 157 | CONSERVATIVE 35, PASS 122 |  |
| `puncc/aps/rand=False` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/aps/rand=True` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/class_conditional/default` | REFUSED | - | 38 | REFUSED 12, PASS 26 |  |
| `puncc/cqr/default` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/cv_plus/K=10` | ERROR | ERROR | 78 | ERROR 20, CONSERVATIVE 4, REFUSED 14, PASS 40 |  |
| `puncc/cv_plus/K=5` | ERROR | ERROR | 78 | ERROR 12, CONSERVATIVE 4, REFUSED 16, PASS 46 |  |
| `puncc/jackknife_plus/K=n` | ERROR | - | 66 | ERROR 66 |  |
| `puncc/lac/default` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/raps/rand=False` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/raps/rand=True` | LAW_MISMATCH | CONSERVATIVE | 114 | LAW_MISMATCH 2, CONSERVATIVE 63, REFUSED 30, PASS 19 |  |
| `puncc/split_abs/default` | REFUSED | REFUSED | 157 | REFUSED 43, PASS 114 |  |
| `torchcp/aps/randomized=False` | PASS | PASS | 114 | PASS 114 |  |
| `torchcp/aps/randomized=True` | PASS | PASS | 114 | PASS 114 |  |
| `torchcp/class_conditional/default` | PASS | - | 38 | PASS 38 |  |
| `torchcp/cqr/default` | ERROR | ERROR | 114 | ERROR 30, PASS 84 |  |
| `torchcp/lac/default` | PASS | PASS | 114 | PASS 114 |  |
| `torchcp/raps/randomized=False` | PASS | PASS | 114 | PASS 114 |  |
| `torchcp/raps/randomized=True` | PASS | PASS | 114 | PASS 114 |  |
| `torchcp/split_abs/default` | ERROR | ERROR | 157 | ERROR 43, PASS 114 |  |
| `reference/aps/deterministic` | PASS | PASS | 114 | PASS 114 |  |
| `reference/aps/randomized` | PASS | PASS | 114 | PASS 114 |  |
| `reference/class_conditional/default` | PASS | - | 38 | PASS 38 |  |
| `reference/cqr/asymmetric` | PASS | PASS | 114 | PASS 114 |  |
| `reference/cqr/symmetric` | PASS | PASS | 114 | PASS 114 |  |
| `reference/cv_plus/K=10` | PASS | PASS | 78 | PASS 78 |  |
| `reference/cv_plus/K=5` | PASS | PASS | 78 | PASS 78 |  |
| `reference/jackknife_plus/default` | PASS | - | 66 | PASS 66 |  |
| `reference/lac/default` | PASS | PASS | 114 | PASS 114 |  |
| `reference/lac/k_minus_1` | FAIL | FAIL | 114 | FAIL 114 |  |
| `reference/lac/k_plus_1` | CONSERVATIVE | CONSERVATIVE | 114 | CONSERVATIVE 84, PASS 30 |  |
| `reference/lac/n_instead_of_n_plus_1` | FAIL | FAIL | 114 | FAIL 66, PASS 48 |  |
| `reference/lac/no_correction_linear` | FAIL | FAIL | 114 | FAIL 114 |  |
| `reference/lac/smoothed` | PASS | PASS | 114 | PASS 114 |  |
| `reference/raps/deterministic` | PASS | PASS | 114 | PASS 114 |  |
| `reference/raps/randomized` | PASS | PASS | 114 | PASS 114 |  |
| `reference/split_abs/default` | PASS | PASS | 157 | PASS 157 |  |
| `reference/split_abs/k_minus_1` | FAIL | FAIL | 157 | FAIL 145, PASS 12 |  |
| `reference/split_abs/k_plus_1` | CONSERVATIVE | CONSERVATIVE | 157 | CONSERVATIVE 106, PASS 51 |  |
| `reference/split_abs/n_instead_of_n_plus_1` | FAIL | FAIL | 157 | FAIL 87, PASS 70 |  |
| `reference/split_abs/no_correction_linear` | FAIL | FAIL | 157 | FAIL 145, PASS 12 |  |

## Status grid (worst over dgps and alphas at each n)

P pass, C conservative, F fail, L law mismatch, O refused a feasible level, R refused with k > n, E error, . not run.

| row | 5 | 9 | 10 | 19 | 20 | 49 | 50 | 99 | 100 | 999 | 1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | E | E | E | F | F | F | F | F | F | F | F |
| `mapie/aps/include_last_label=True` | E | E | E | C | C | C | C | C | C | C | C |
| `mapie/aps/include_last_label=randomized` | E | E | E | O | O | O | O | O | O | O | O |
| `mapie/cqr/asymmetric` | R | O | R | O | R | R | R | R | R | R | R |
| `mapie/cqr/symmetric` | O | O | O | O | O | O | O | O | O | O | O |
| `mapie/cv_plus/K=10` | . | . | . | P | P | P | P | P | P | C | P |
| `mapie/cv_plus/K=5` | . | . | . | P | P | P | P | P | P | C | P |
| `mapie/jackknife_plus/default` | . | P | P | P | P | P | P | P | . | . | . |
| `mapie/lac/default` | O | O | O | O | O | O | O | O | O | O | O |
| `mapie/raps/include_last_label=True` | E | E | E | E | E | C | E | C | C | C | C |
| `mapie/raps/include_last_label=randomized` | E | E | E | E | E | O | E | O | O | R | R |
| `mapie/split_abs/allow_infinite_bounds` | R | R | R | R | R | R | R | R | R | R | R |
| `mapie/split_abs/default` | O | O | O | O | O | O | O | O | O | O | O |
| `crepes/class_conditional/smoothed` | P | P | P | P | P | P | P | P | . | . | . |
| `crepes/class_conditional/unsmoothed` | C | C | P | C | P | C | P | C | . | . | . |
| `crepes/lac/smoothed` | P | P | P | P | P | P | P | P | P | P | P |
| `crepes/lac/unsmoothed` | C | C | P | C | P | C | P | C | P | C | C |
| `crepes/split_abs/default` | C | C | P | C | P | C | P | C | P | C | C |
| `puncc/aps/rand=False` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/aps/rand=True` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/class_conditional/default` | R | R | R | R | R | R | R | R | . | . | . |
| `puncc/cqr/default` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/cv_plus/K=10` | . | . | . | E | E | E | E | E | E | E | R |
| `puncc/cv_plus/K=5` | . | . | . | R | E | E | E | E | E | E | R |
| `puncc/jackknife_plus/K=n` | . | E | E | E | E | E | E | E | . | . | . |
| `puncc/lac/default` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/raps/rand=False` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/raps/rand=True` | C | L | C | C | L | C | C | C | C | C | C |
| `puncc/split_abs/default` | R | R | R | R | R | R | R | R | R | R | R |
| `torchcp/aps/randomized=False` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/aps/randomized=True` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/class_conditional/default` | P | P | P | P | P | P | P | P | . | . | . |
| `torchcp/cqr/default` | E | E | E | E | E | E | E | E | E | E | E |
| `torchcp/lac/default` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/raps/randomized=False` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/raps/randomized=True` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/split_abs/default` | E | E | E | E | E | E | E | E | E | E | E |
| `reference/aps/deterministic` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/aps/randomized` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/class_conditional/default` | P | P | P | P | P | P | P | P | . | . | . |
| `reference/cqr/asymmetric` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/cqr/symmetric` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/cv_plus/K=10` | . | . | . | P | P | P | P | P | P | P | P |
| `reference/cv_plus/K=5` | . | . | . | P | P | P | P | P | P | P | P |
| `reference/jackknife_plus/default` | . | P | P | P | P | P | P | P | . | . | . |
| `reference/lac/default` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/lac/k_minus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/lac/k_plus_1` | C | C | C | C | C | C | C | C | C | C | C |
| `reference/lac/n_instead_of_n_plus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/lac/no_correction_linear` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/lac/smoothed` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/raps/deterministic` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/raps/randomized` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/split_abs/default` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/split_abs/k_minus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/split_abs/k_plus_1` | C | C | C | C | C | C | C | C | C | C | C |
| `reference/split_abs/n_instead_of_n_plus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/split_abs/no_correction_linear` | F | F | F | F | F | F | F | F | F | F | F |

## Non-PASS cells (libraries)

| row | dgp | n | alpha | k | status | coverage [95% CI] | target | rank offsets lower|upper or bracket (reps) | Holm p | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `crepes/class_conditional/unsmoothed` | cls_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.8333 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9010 [0.8947, 0.9073] | 0.8000 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8494 [0.8431, 0.8557] | 0.8000 | bracket {"1": 200} | 7.2e-73 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9495 [0.9458, 0.9531] | 0.9000 | bracket {"1": 200} | 1.1e-208 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8162 [0.8117, 0.8207] | 0.8000 | bracket {"1": 200} | 1.7e-08 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9172 [0.9138, 0.9206] | 0.9000 | bracket {"1": 200} | 2.9e-17 | bracket +1 in 200 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.8115 [0.8075, 0.8155] | 0.8000 | bracket {"0": 1, "1": 199} | 4.9e-06 | bracket +1 in 199 reps |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9110 [0.9082, 0.9138] | 0.9000 | bracket {"0": 1, "1": 199} | 2.6e-11 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.8333 | bracket {"0": 1, "1": 199} | 0 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.8942 [0.8805, 0.9080] | 0.8000 | bracket {"1": 200} | 1.5e-48 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8431 [0.8323, 0.8540] | 0.8000 | bracket {"0": 3, "1": 197} | 3.2e-09 | bracket +1 in 197 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9466 [0.9395, 0.9536] | 0.9000 | bracket {"0": 5, "1": 195} | 5.2e-39 | bracket +1 in 195 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8168 [0.8090, 0.8246] | 0.8000 | bracket {"0": 3, "1": 197} | 0.27 | bracket +1 in 197 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9183 [0.9128, 0.9238] | 0.9000 | bracket {"0": 5, "1": 195} | 4.5e-06 | bracket +1 in 195 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.8126 [0.8069, 0.8184] | 0.8000 | bracket {"0": 17, "1": 183} | 0.25 | bracket +1 in 183 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9131 [0.9088, 0.9174] | 0.9000 | bracket {"0": 15, "1": 185} | 3.4e-05 | bracket +1 in 185 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.8009 [0.7980, 0.8038] | 0.8000 | bracket {"0": 97, "1": 103} | 1 | bracket +1 in 103 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.8996 [0.8973, 0.9019] | 0.9000 | bracket {"0": 106, "1": 94} | 1 | bracket +1 in 94 reps |
| `crepes/lac/unsmoothed` | cls_gauss | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9990 | bracket {"0": 84, "1": 116} | 0 | bracket +1 in 116 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.8333 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 9 | 0.2 | 8 | CONSERVATIVE | 0.9051 [0.8929, 0.9174] | 0.8000 | bracket {"1": 200} | 2.2e-79 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 19 | 0.2 | 16 | CONSERVATIVE | 0.8503 [0.8397, 0.8610] | 0.8000 | bracket {"0": 1, "1": 199} | 4.1e-12 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 19 | 0.1 | 18 | CONSERVATIVE | 0.9514 [0.9453, 0.9575] | 0.9000 | bracket {"0": 1, "1": 199} | 2e-57 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 49 | 0.2 | 40 | CONSERVATIVE | 0.8197 [0.8124, 0.8270] | 0.8000 | bracket {"0": 6, "1": 194} | 0.0091 | bracket +1 in 194 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 49 | 0.1 | 45 | CONSERVATIVE | 0.9207 [0.9153, 0.9260] | 0.9000 | bracket {"0": 1, "1": 199} | 1.3e-08 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.8086 [0.8029, 0.8143] | 0.8000 | bracket {"0": 9, "1": 191} | 1 | bracket +1 in 191 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9075 [0.9031, 0.9119] | 0.9000 | bracket {"0": 4, "1": 196} | 0.52 | bracket +1 in 196 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.7998 [0.7967, 0.8029] | 0.8000 | bracket {"0": 75, "1": 125} | 1 | bracket +1 in 125 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9020 [0.8998, 0.9043] | 0.9000 | bracket {"0": 53, "1": 147} | 1 | bracket +1 in 147 reps |
| `crepes/lac/unsmoothed` | cls_gauss_inf | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9990 | bracket {"1": 200} | 0 | bracket +1 in 200 reps |
| `crepes/lac/unsmoothed` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.8435 [0.8321, 0.8549] | 0.8000 | bracket {"0": 11, "1": 189} | 2e-09 | bracket +1 in 189 reps |
| `crepes/lac/unsmoothed` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9476 [0.9398, 0.9555] | 0.9000 | bracket {"0": 1, "1": 199} | 6.6e-48 | bracket +1 in 199 reps |
| `crepes/lac/unsmoothed` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.8043 [0.7979, 0.8108] | 0.8000 | bracket {"0": 32, "1": 168} | 1 | bracket +1 in 168 reps |
| `crepes/lac/unsmoothed` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9060 [0.9014, 0.9105] | 0.9000 | bracket {"0": 18, "1": 182} | 1 | bracket +1 in 182 reps |
| `crepes/split_abs/default` | diabetes | 19 | 0.2 | 16 | CONSERVATIVE | 0.8548 [0.8442, 0.8654] | 0.8000 | {"1|1": 200} | 2.8e-12 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 19 | 0.1 | 18 | CONSERVATIVE | 0.9513 [0.9436, 0.9590] | 0.9000 | {"1|1": 200} | 8.4e-64 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 99 | 0.2 | 80 | CONSERVATIVE | 0.8109 [0.8041, 0.8177] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 99 | 0.1 | 90 | CONSERVATIVE | 0.9100 [0.9053, 0.9147] | 0.9000 | {"1|1": 200} | 0.33 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.8333 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9006 [0.8864, 0.9148] | 0.8000 | {"1|1": 200} | 5.6e-64 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8573 [0.8474, 0.8671] | 0.8000 | {"1|1": 200} | 3.5e-13 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9493 [0.9426, 0.9560] | 0.9000 | {"1|1": 200} | 3.4e-43 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8193 [0.8112, 0.8274] | 0.8000 | {"1|1": 200} | 0.015 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9157 [0.9097, 0.9218] | 0.9000 | {"1|1": 200} | 0.00093 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8032, 0.8145] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9103 [0.9059, 0.9147] | 0.9000 | {"1|1": 200} | 0.032 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.8029 [0.7995, 0.8063] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9027 [0.9003, 0.9051] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9990 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.8333 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 9 | 0.2 | 8 | CONSERVATIVE | 0.8860 [0.8711, 0.9008] | 0.8000 | {"1|1": 200} | 7.9e-59 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9000 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 19 | 0.2 | 16 | CONSERVATIVE | 0.8492 [0.8385, 0.8600] | 0.8000 | {"1|1": 200} | 4.7e-12 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 19 | 0.1 | 18 | CONSERVATIVE | 0.9481 [0.9418, 0.9543] | 0.9000 | {"1|1": 200} | 3e-39 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 49 | 0.2 | 40 | CONSERVATIVE | 0.8174 [0.8087, 0.8262] | 0.8000 | {"1|1": 200} | 0.13 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 49 | 0.1 | 45 | CONSERVATIVE | 0.9180 [0.9122, 0.9237] | 0.9000 | {"1|1": 200} | 8.8e-06 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 99 | 0.2 | 80 | CONSERVATIVE | 0.8069 [0.8010, 0.8127] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 99 | 0.1 | 90 | CONSERVATIVE | 0.9079 [0.9035, 0.9123] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 999 | 0.2 | 800 | CONSERVATIVE | 0.8000 [0.7970, 0.8031] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 999 | 0.1 | 900 | CONSERVATIVE | 0.9017 [0.8994, 0.9040] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9990 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9427 | {"1|1": 200} | 2.1e-14 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 9 | 0.2 | 8 | CONSERVATIVE | 0.9927 [0.9864, 0.9991] | 0.9346 | {"0|0": 171, "1|1": 29} | 7.3e-12 | rank +1 in 29 reps |
| `crepes/split_abs/default` | reg_tied | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9860 | {"1|1": 200} | 0.71 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 19 | 0.2 | 16 | CONSERVATIVE | 0.9843 [0.9752, 0.9934] | 0.9531 | {"0|0": 180, "1|1": 20} | 0.023 | rank +1 in 20 reps |
| `crepes/split_abs/default` | reg_tied | 19 | 0.1 | 18 | CONSERVATIVE | 1.0000 [1.0000, 1.0000] | 0.9959 | {"0|0": 196, "1|1": 4} | 1 | rank +1 in 4 reps |
| `crepes/split_abs/default` | reg_tied | 49 | 0.2 | 40 | CONSERVATIVE | 0.9934 [0.9875, 0.9992] | 0.9791 | {"0|0": 195, "1|1": 5} | 1 | rank +1 in 5 reps |
| `crepes/split_abs/default` | reg_tied | 99 | 0.2 | 80 | CONSERVATIVE | 0.9972 [0.9933, 1.0000] | 0.9937 | {"0|0": 198, "1|1": 2} | 1 | rank +1 in 2 reps |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.5326 [0.5223, 0.5428] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.5178 [0.5089, 0.5267] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.2 | 9 | FAIL | 0.5303 [0.5239, 0.5367] | 0.8182 |  | 0 | Holm p=0, coverage 0.5303 vs 0.8182 |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.1 | 10 | FAIL | 0.5594 [0.5553, 0.5636] | 0.9091 |  | 0 | Holm p=0, coverage 0.5594 vs 0.9091 |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.2 | 16 | FAIL | 0.5186 [0.5128, 0.5245] | 0.8000 |  | 0 | Holm p=0, coverage 0.5186 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.1 | 18 | FAIL | 0.5536 [0.5496, 0.5577] | 0.9000 |  | 0 | Holm p=0, coverage 0.5536 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.2 | 17 | FAIL | 0.5314 [0.5263, 0.5365] | 0.8095 |  | 0 | Holm p=0, coverage 0.5314 vs 0.8095 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.1 | 19 | FAIL | 0.5585 [0.5545, 0.5625] | 0.9048 |  | 0 | Holm p=0, coverage 0.5585 vs 0.9048 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.05 | 20 | FAIL | 0.5697 [0.5665, 0.5729] | 0.9524 |  | 0 | Holm p=0, coverage 0.5697 vs 0.9524 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.2 | 40 | FAIL | 0.5251 [0.5207, 0.5295] | 0.8000 |  | 0 | Holm p=0, coverage 0.5251 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.1 | 45 | FAIL | 0.5576 [0.5543, 0.5610] | 0.9000 |  | 0 | Holm p=0, coverage 0.5576 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.05 | 48 | FAIL | 0.5715 [0.5682, 0.5747] | 0.9600 |  | 0 | Holm p=0, coverage 0.5715 vs 0.9600 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.2 | 41 | FAIL | 0.5317 [0.5274, 0.5360] | 0.8039 |  | 0 | Holm p=0, coverage 0.5317 vs 0.8039 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.1 | 46 | FAIL | 0.5623 [0.5587, 0.5659] | 0.9020 |  | 0 | Holm p=0, coverage 0.5623 vs 0.9020 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.05 | 49 | FAIL | 0.5747 [0.5714, 0.5780] | 0.9608 |  | 0 | Holm p=0, coverage 0.5747 vs 0.9608 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.2 | 80 | FAIL | 0.5299 [0.5261, 0.5336] | 0.8000 |  | 0 | Holm p=0, coverage 0.5299 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.1 | 90 | FAIL | 0.5605 [0.5571, 0.5640] | 0.9000 |  | 0 | Holm p=0, coverage 0.5605 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.05 | 95 | FAIL | 0.5718 [0.5684, 0.5752] | 0.9500 |  | 0 | Holm p=0, coverage 0.5718 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.2 | 81 | FAIL | 0.5323 [0.5291, 0.5356] | 0.8020 |  | 0 | Holm p=0, coverage 0.5323 vs 0.8020 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.1 | 91 | FAIL | 0.5619 [0.5592, 0.5646] | 0.9010 |  | 0 | Holm p=0, coverage 0.5619 vs 0.9010 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.05 | 96 | FAIL | 0.5738 [0.5711, 0.5764] | 0.9505 |  | 0 | Holm p=0, coverage 0.5738 vs 0.9505 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.2 | 800 | FAIL | 0.5290 [0.5259, 0.5321] | 0.8000 |  | 0 | Holm p=0, coverage 0.5290 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.1 | 900 | FAIL | 0.5603 [0.5573, 0.5634] | 0.9000 |  | 0 | Holm p=0, coverage 0.5603 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.05 | 950 | FAIL | 0.5720 [0.5689, 0.5750] | 0.9500 |  | 0 | Holm p=0, coverage 0.5720 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.2 | 801 | FAIL | 0.5291 [0.5259, 0.5323] | 0.8002 |  | 0 | Holm p=0, coverage 0.5291 vs 0.8002 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.1 | 901 | FAIL | 0.5599 [0.5566, 0.5632] | 0.9001 |  | 0 | Holm p=0, coverage 0.5599 vs 0.9001 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.05 | 951 | FAIL | 0.5715 [0.5683, 0.5747] | 0.9500 |  | 0 | Holm p=0, coverage 0.5715 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 5 | 0.2 | 5 | ERROR | 0.7977 [0.7865, 0.8089] | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 9 | 0.2 | 8 | ERROR | 0.7620 [0.7541, 0.7699] | 0.8000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 10 | 0.2 | 9 | ERROR | 0.7690 [0.7607, 0.7773] | 0.8182 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 10 | 0.1 | 10 | ERROR | 0.8263 [0.8161, 0.8364] | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 10 | 1/11 | 10 | ERROR |  | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 19 | 0.2 | 16 | FAIL | 0.7498 [0.7449, 0.7548] | 0.8000 |  | 2.2e-62 | Holm p=2.2e-62, coverage 0.7498 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 19 | 0.1 | 18 | FAIL | 0.8061 [0.7990, 0.8133] | 0.9000 |  | 6.4e-112 | Holm p=6.4e-112, coverage 0.8061 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 20 | 0.2 | 17 | FAIL | 0.7515 [0.7466, 0.7564] | 0.8095 |  | 2.3e-66 | Holm p=2.3e-66, coverage 0.7515 vs 0.8095 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 20 | 0.1 | 19 | FAIL | 0.8105 [0.8029, 0.8181] | 0.9048 |  | 3.7e-110 | Holm p=3.7e-110, coverage 0.8105 vs 0.9048 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 20 | 0.05 | 20 | FAIL | 0.8665 [0.8575, 0.8754] | 0.9524 |  | 1.1e-160 | Holm p=1.1e-160, coverage 0.8665 vs 0.9524 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 49 | 0.2 | 40 | FAIL | 0.7459 [0.7421, 0.7496] | 0.8000 |  | 6e-67 | Holm p=6e-67, coverage 0.7459 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 49 | 0.1 | 45 | FAIL | 0.8014 [0.7963, 0.8065] | 0.9000 |  | 0 | Holm p=0, coverage 0.8014 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 49 | 0.05 | 48 | FAIL | 0.8736 [0.8674, 0.8798] | 0.9600 |  | 0 | Holm p=0, coverage 0.8736 vs 0.9600 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 50 | 0.2 | 41 | FAIL | 0.7435 [0.7400, 0.7469] | 0.8039 |  | 1.3e-88 | Holm p=1.3e-88, coverage 0.7435 vs 0.8039 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 50 | 0.1 | 46 | FAIL | 0.7988 [0.7936, 0.8041] | 0.9020 |  | 0 | Holm p=0, coverage 0.7988 vs 0.9020 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 50 | 0.05 | 49 | FAIL | 0.8693 [0.8627, 0.8758] | 0.9608 |  | 0 | Holm p=0, coverage 0.8693 vs 0.9608 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.2 | 80 | FAIL | 0.7390 [0.7357, 0.7423] | 0.8000 |  | 8.2e-119 | Holm p=8.2e-119, coverage 0.7390 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.1 | 90 | FAIL | 0.7907 [0.7865, 0.7950] | 0.9000 |  | 0 | Holm p=0, coverage 0.7907 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.05 | 95 | FAIL | 0.8494 [0.8443, 0.8544] | 0.9500 |  | 0 | Holm p=0, coverage 0.8494 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 100 | 0.2 | 81 | FAIL | 0.7454 [0.7421, 0.7486] | 0.8020 |  | 5e-93 | Holm p=5e-93, coverage 0.7454 vs 0.8020 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 100 | 0.1 | 91 | FAIL | 0.7991 [0.7951, 0.8031] | 0.9010 |  | 0 | Holm p=0, coverage 0.7991 vs 0.9010 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 100 | 0.05 | 96 | FAIL | 0.8546 [0.8495, 0.8597] | 0.9505 |  | 0 | Holm p=0, coverage 0.8546 vs 0.9505 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.2 | 800 | FAIL | 0.7394 [0.7367, 0.7422] | 0.8000 |  | 0 | Holm p=0, coverage 0.7394 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.1 | 900 | FAIL | 0.7918 [0.7891, 0.7945] | 0.9000 |  | 0 | Holm p=0, coverage 0.7918 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.05 | 950 | FAIL | 0.8463 [0.8437, 0.8489] | 0.9500 |  | 0 | Holm p=0, coverage 0.8463 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 1000 | 0.2 | 801 | FAIL | 0.7391 [0.7363, 0.7419] | 0.8002 |  | 0 | Holm p=0, coverage 0.7391 vs 0.8002 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 1000 | 0.1 | 901 | FAIL | 0.7903 [0.7876, 0.7930] | 0.9001 |  | 0 | Holm p=0, coverage 0.7903 vs 0.9001 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 1000 | 0.05 | 951 | FAIL | 0.8447 [0.8422, 0.8473] | 0.9500 |  | 0 | Holm p=0, coverage 0.8447 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | digits | 10 | 0.2 | 9 | CONSERVATIVE | 0.9637 [0.9619, 0.9656] | 0.8182 |  | 4.1e-303 | Holm p=4.1e-303, coverage 0.9637 vs 0.8182 |
| `mapie/aps/include_last_label=False` | digits | 10 | 0.1 | 10 | CONSERVATIVE | 0.9765 [0.9744, 0.9785] | 0.9091 |  | 1.8e-50 | Holm p=1.8e-50, coverage 0.9765 vs 0.9091 |
| `mapie/aps/include_last_label=False` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.9614 [0.9600, 0.9629] | 0.8000 |  | 0 | Holm p=0, coverage 0.9614 vs 0.8000 |
| `mapie/aps/include_last_label=False` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9740 [0.9723, 0.9757] | 0.9000 |  | 2.3e-121 | Holm p=2.3e-121, coverage 0.9740 vs 0.9000 |
| `mapie/aps/include_last_label=False` | digits | 50 | 0.2 | 41 | CONSERVATIVE | 0.9595 [0.9583, 0.9607] | 0.8039 |  | 0 | Holm p=0, coverage 0.9595 vs 0.8039 |
| `mapie/aps/include_last_label=False` | digits | 50 | 0.1 | 46 | CONSERVATIVE | 0.9722 [0.9708, 0.9735] | 0.9020 |  | 0 | Holm p=0, coverage 0.9722 vs 0.9020 |
| `mapie/aps/include_last_label=False` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.9592 [0.9580, 0.9603] | 0.8000 |  | 0 | Holm p=0, coverage 0.9592 vs 0.8000 |
| `mapie/aps/include_last_label=False` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9710 [0.9699, 0.9722] | 0.9000 |  | 0 | Holm p=0, coverage 0.9710 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.9120 [0.8940, 0.9300] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.8831 [0.8669, 0.8993] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.2 | 9 | CONSERVATIVE | 0.9084 [0.8967, 0.9202] | 0.8182 |  | 3.7e-58 | Holm p=3.7e-58, coverage 0.9084 vs 0.8182 |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.1 | 10 | CONSERVATIVE | 0.9677 [0.9612, 0.9742] | 0.9091 |  | 5.7e-41 | Holm p=5.7e-41, coverage 0.9677 vs 0.9091 |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8893 [0.8792, 0.8994] | 0.8000 |  | 7.1e-99 | Holm p=7.1e-99, coverage 0.8893 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9580 [0.9522, 0.9639] | 0.9000 |  | 2.8e-87 | Holm p=2.8e-87, coverage 0.9580 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.2 | 17 | CONSERVATIVE | 0.9153 [0.9067, 0.9240] | 0.8095 |  | 8e-173 | Holm p=8e-173, coverage 0.9153 vs 0.8095 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.1 | 19 | CONSERVATIVE | 0.9681 [0.9628, 0.9734] | 0.9048 |  | 2e-181 | Holm p=2e-181, coverage 0.9681 vs 0.9048 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.05 | 20 | CONSERVATIVE | 0.9887 [0.9859, 0.9916] | 0.9524 |  | 1.3e-112 | Holm p=1.3e-112, coverage 0.9887 vs 0.9524 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.9004 [0.8939, 0.9069] | 0.8000 |  | 0 | Holm p=0, coverage 0.9004 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9659 [0.9623, 0.9695] | 0.9000 |  | 0 | Holm p=0, coverage 0.9659 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.05 | 48 | CONSERVATIVE | 0.9912 [0.9900, 0.9925] | 0.9600 |  | 9.3e-153 | Holm p=9.3e-153, coverage 0.9912 vs 0.9600 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.2 | 41 | CONSERVATIVE | 0.9071 [0.9007, 0.9135] | 0.8039 |  | 0 | Holm p=0, coverage 0.9071 vs 0.8039 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.1 | 46 | CONSERVATIVE | 0.9691 [0.9657, 0.9725] | 0.9020 |  | 0 | Holm p=0, coverage 0.9691 vs 0.9020 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.05 | 49 | CONSERVATIVE | 0.9928 [0.9915, 0.9940] | 0.9608 |  | 1.1e-220 | Holm p=1.1e-220, coverage 0.9928 vs 0.9608 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.9094 [0.9047, 0.9141] | 0.8000 |  | 0 | Holm p=0, coverage 0.9094 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9706 [0.9683, 0.9729] | 0.9000 |  | 0 | Holm p=0, coverage 0.9706 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.05 | 95 | CONSERVATIVE | 0.9902 [0.9891, 0.9913] | 0.9500 |  | 0 | Holm p=0, coverage 0.9902 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.9093 [0.9047, 0.9139] | 0.8020 |  | 0 | Holm p=0, coverage 0.9093 vs 0.8020 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9693 [0.9670, 0.9716] | 0.9010 |  | 0 | Holm p=0, coverage 0.9693 vs 0.9010 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.05 | 96 | CONSERVATIVE | 0.9899 [0.9887, 0.9911] | 0.9505 |  | 0 | Holm p=0, coverage 0.9899 vs 0.9505 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.9069 [0.9047, 0.9091] | 0.8000 |  | 0 | Holm p=0, coverage 0.9069 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9711 [0.9698, 0.9723] | 0.9000 |  | 0 | Holm p=0, coverage 0.9711 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.05 | 950 | CONSERVATIVE | 0.9901 [0.9895, 0.9908] | 0.9500 |  | 0 | Holm p=0, coverage 0.9901 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9064 [0.9040, 0.9088] | 0.8002 |  | 0 | Holm p=0, coverage 0.9064 vs 0.8002 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9710 [0.9698, 0.9723] | 0.9001 |  | 0 | Holm p=0, coverage 0.9710 vs 0.9001 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9906 [0.9899, 0.9913] | 0.9500 |  | 0 | Holm p=0, coverage 0.9906 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 5 | 0.2 | 5 | ERROR | 0.9334 [0.9239, 0.9429] | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 9 | 0.2 | 8 | ERROR | 0.9137 [0.9055, 0.9220] | 0.8000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 10 | 0.2 | 9 | ERROR | 0.9189 [0.9107, 0.9272] | 0.8182 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 10 | 0.1 | 10 | ERROR | 0.9599 [0.9539, 0.9658] | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 10 | 1/11 | 10 | ERROR |  | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 19 | 0.2 | 16 | CONSERVATIVE | 0.9144 [0.9087, 0.9200] | 0.8000 |  | 2.3e-151 | Holm p=2.3e-151, coverage 0.9144 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 19 | 0.1 | 18 | CONSERVATIVE | 0.9582 [0.9542, 0.9621] | 0.9000 |  | 6.4e-37 | Holm p=6.4e-37, coverage 0.9582 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 20 | 0.2 | 17 | CONSERVATIVE | 0.9173 [0.9120, 0.9226] | 0.8095 |  | 1.9e-136 | Holm p=1.9e-136, coverage 0.9173 vs 0.8095 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 20 | 0.1 | 19 | CONSERVATIVE | 0.9607 [0.9566, 0.9647] | 0.9048 |  | 2.2e-38 | Holm p=2.2e-38, coverage 0.9607 vs 0.9048 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 20 | 0.05 | 20 | CONSERVATIVE | 0.9807 [0.9776, 0.9837] | 0.9524 |  | 4.1e-13 | Holm p=4.1e-13, coverage 0.9807 vs 0.9524 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 49 | 0.2 | 40 | CONSERVATIVE | 0.9145 [0.9108, 0.9181] | 0.8000 |  | 0 | Holm p=0, coverage 0.9145 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 49 | 0.1 | 45 | CONSERVATIVE | 0.9595 [0.9569, 0.9620] | 0.9000 |  | 3.1e-205 | Holm p=3.1e-205, coverage 0.9595 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 49 | 0.05 | 48 | CONSERVATIVE | 0.9856 [0.9840, 0.9872] | 0.9600 |  | 9.9e-52 | Holm p=9.9e-52, coverage 0.9856 vs 0.9600 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 50 | 0.2 | 41 | CONSERVATIVE | 0.9126 [0.9089, 0.9164] | 0.8039 |  | 0 | Holm p=0, coverage 0.9126 vs 0.8039 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 50 | 0.1 | 46 | CONSERVATIVE | 0.9575 [0.9545, 0.9604] | 0.9020 |  | 9.9e-153 | Holm p=9.9e-153, coverage 0.9575 vs 0.9020 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 50 | 0.05 | 49 | CONSERVATIVE | 0.9844 [0.9826, 0.9861] | 0.9608 |  | 2.6e-39 | Holm p=2.6e-39, coverage 0.9844 vs 0.9608 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.9098 [0.9069, 0.9127] | 0.8000 |  | 0 | Holm p=0, coverage 0.9098 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9566 [0.9545, 0.9588] | 0.9000 |  | 0 | Holm p=0, coverage 0.9566 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.05 | 95 | CONSERVATIVE | 0.9798 [0.9783, 0.9813] | 0.9500 |  | 5.7e-160 | Holm p=5.7e-160, coverage 0.9798 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 100 | 0.2 | 81 | CONSERVATIVE | 0.9144 [0.9112, 0.9175] | 0.8020 |  | 0 | Holm p=0, coverage 0.9144 vs 0.8020 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 100 | 0.1 | 91 | CONSERVATIVE | 0.9594 [0.9570, 0.9617] | 0.9010 |  | 0 | Holm p=0, coverage 0.9594 vs 0.9010 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 100 | 0.05 | 96 | CONSERVATIVE | 0.9816 [0.9800, 0.9833] | 0.9505 |  | 4.8e-234 | Holm p=4.8e-234, coverage 0.9816 vs 0.9505 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.9139 [0.9119, 0.9159] | 0.8000 |  | 0 | Holm p=0, coverage 0.9139 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9591 [0.9578, 0.9605] | 0.9000 |  | 0 | Holm p=0, coverage 0.9591 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9811 [0.9802, 0.9820] | 0.9500 |  | 0 | Holm p=0, coverage 0.9811 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9124 [0.9106, 0.9143] | 0.8002 |  | 0 | Holm p=0, coverage 0.9124 vs 0.8002 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9576 [0.9563, 0.9589] | 0.9001 |  | 0 | Holm p=0, coverage 0.9576 vs 0.9001 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9801 [0.9792, 0.9811] | 0.9500 |  | 0 | Holm p=0, coverage 0.9801 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | digits | 10 | 0.2 | 9 | CONSERVATIVE | 0.9857 [0.9845, 0.9870] | 0.8182 |  | 0 | Holm p=0, coverage 0.9857 vs 0.8182 |
| `mapie/aps/include_last_label=True` | digits | 10 | 0.1 | 10 | CONSERVATIVE | 0.9917 [0.9908, 0.9927] | 0.9091 |  | 8.2e-159 | Holm p=8.2e-159, coverage 0.9917 vs 0.9091 |
| `mapie/aps/include_last_label=True` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.9857 [0.9848, 0.9866] | 0.8000 |  | 0 | Holm p=0, coverage 0.9857 vs 0.8000 |
| `mapie/aps/include_last_label=True` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9915 [0.9907, 0.9923] | 0.9000 |  | 0 | Holm p=0, coverage 0.9915 vs 0.9000 |
| `mapie/aps/include_last_label=True` | digits | 50 | 0.2 | 41 | CONSERVATIVE | 0.9845 [0.9838, 0.9853] | 0.8039 |  | 0 | Holm p=0, coverage 0.9845 vs 0.8039 |
| `mapie/aps/include_last_label=True` | digits | 50 | 0.1 | 46 | CONSERVATIVE | 0.9914 [0.9908, 0.9920] | 0.9020 |  | 0 | Holm p=0, coverage 0.9914 vs 0.9020 |
| `mapie/aps/include_last_label=True` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.9845 [0.9838, 0.9852] | 0.8000 |  | 0 | Holm p=0, coverage 0.9845 vs 0.8000 |
| `mapie/aps/include_last_label=True` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9919 [0.9913, 0.9925] | 0.9000 |  | 0 | Holm p=0, coverage 0.9919 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.8380 [0.8165, 0.8596] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.7934 [0.7747, 0.8121] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.2 | 5 | ERROR | 0.8478 [0.8276, 0.8679] | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 32/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.2 | 8 | ERROR | 0.8024 [0.7849, 0.8200] | 0.8000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 3/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.2 | 9 | ERROR | 0.8169 [0.7999, 0.8339] | 0.8182 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.1 | 10 | ERROR | 0.9051 [0.8926, 0.9177] | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 10 | 1/11 | 10 | ERROR |  | 0.9091 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | diabetes | 10 | 0.1 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | diabetes | 19 | 0.1 | 18 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 5 | 0.2 | 5 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 5 | 1/6 | 5 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.2 | 8 | OVER_REFUSED |  | 0.8000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.1 | 9 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 10 | 0.1 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 10 | 1/11 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 19 | 0.1 | 18 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 19 | 0.05 | 19 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 20 | 0.05 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 20 | 1/21 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 5 | 0.2 | 5 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 5 | 1/6 | 5 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 9 | 0.2 | 8 | OVER_REFUSED |  | 0.8000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 9 | 0.1 | 9 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 10 | 0.1 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 10 | 1/11 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 19 | 0.1 | 18 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 19 | 0.05 | 19 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 20 | 0.05 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 20 | 1/21 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/asymmetric` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cqr/symmetric` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/cv_plus/K=10` | reg_constant | 999 | 0.05 | 950 | CONSERVATIVE | 0.9508 [0.9491, 0.9526] | 0.9500 | {"1|0": 200} | 1 | rank +1 in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 999 | 0.05 | 950 | CONSERVATIVE | 0.9508 [0.9491, 0.9526] | 0.9500 | {"1|0": 200} | 1 | rank +1 in 200 reps |
| `mapie/lac/default` | cls_gauss | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/lac/default` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 5 | 0.2 | 5 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 10 | 1/11 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 19 | 0.05 | 19 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss | 20 | 0.2 | 17 | ERROR |  | 0.8421 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss | 20 | 0.1 | 19 | ERROR |  | 0.9474 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss | 20 | 0.05 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss | 20 | 1/21 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8992 [0.8916, 0.9068] | 0.8000 |  | 7.5e-280 | Holm p=7.5e-280, coverage 0.8992 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss | 49 | 0.1 | 45 | OVER_REFUSED |  | 0.9111 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 49 | 0.05 | 48 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 50 | 0.2 | 41 | CONSERVATIVE | 0.9081 [0.9013, 0.9149] | 0.8043 |  | 7.9e-287 | Holm p=7.9e-287, coverage 0.9081 vs 0.8043 |
| `mapie/raps/include_last_label=True` | cls_gauss | 50 | 0.1 | 46 | OVER_REFUSED |  | 0.9130 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 50 | 0.05 | 49 | OVER_REFUSED |  | 0.9565 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.9092 [0.9042, 0.9141] | 0.8000 |  | 0 | Holm p=0, coverage 0.9092 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9687 [0.9661, 0.9714] | 0.9000 |  | 0 | Holm p=0, coverage 0.9687 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss | 99 | 0.05 | 95 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.9105 [0.9056, 0.9154] | 0.8022 |  | 0 | Holm p=0, coverage 0.9105 vs 0.8022 |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9705 [0.9682, 0.9728] | 0.9011 |  | 0 | Holm p=0, coverage 0.9705 vs 0.9011 |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 0.05 | 96 | OVER_REFUSED |  | 0.9560 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.9067 [0.9043, 0.9090] | 0.8000 |  | 0 | Holm p=0, coverage 0.9067 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9712 [0.9699, 0.9724] | 0.9000 |  | 0 | Holm p=0, coverage 0.9712 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss | 999 | 0.05 | 950 | CONSERVATIVE | 0.9902 [0.9895, 0.9909] | 0.9500 |  | 0 | Holm p=0, coverage 0.9902 vs 0.9500 |
| `mapie/raps/include_last_label=True` | cls_gauss | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9069 [0.9045, 0.9094] | 0.8002 |  | 0 | Holm p=0, coverage 0.9069 vs 0.8002 |
| `mapie/raps/include_last_label=True` | cls_gauss | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9709 [0.9696, 0.9722] | 0.9001 |  | 0 | Holm p=0, coverage 0.9709 vs 0.9001 |
| `mapie/raps/include_last_label=True` | cls_gauss | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9904 [0.9897, 0.9911] | 0.9501 |  | 0 | Holm p=0, coverage 0.9904 vs 0.9501 |
| `mapie/raps/include_last_label=True` | cls_gauss | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 5 | 0.2 | 5 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 5 | 1/6 | 5 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 10 | 1/11 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 19 | 0.05 | 19 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 20 | 0.2 | 17 | ERROR |  | 0.8421 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 20 | 0.1 | 19 | ERROR |  | 0.9474 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 20 | 0.05 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 20 | 1/21 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 49 | 0.2 | 40 | CONSERVATIVE | 0.9188 [0.9150, 0.9227] | 0.8000 |  | 0 | Holm p=0, coverage 0.9188 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 49 | 0.1 | 45 | OVER_REFUSED |  | 0.9111 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 49 | 0.05 | 48 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 50 | 0.2 | 41 | CONSERVATIVE | 0.9175 [0.9135, 0.9216] | 0.8043 |  | 0 | Holm p=0, coverage 0.9175 vs 0.8043 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 50 | 0.1 | 46 | OVER_REFUSED |  | 0.9130 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 50 | 0.05 | 49 | OVER_REFUSED |  | 0.9565 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.9174 [0.9144, 0.9203] | 0.8000 |  | 0 | Holm p=0, coverage 0.9174 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9606 [0.9584, 0.9628] | 0.9000 |  | 0 | Holm p=0, coverage 0.9606 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.05 | 95 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 100 | 0.2 | 81 | CONSERVATIVE | 0.9211 [0.9179, 0.9242] | 0.8022 |  | 0 | Holm p=0, coverage 0.9211 vs 0.8022 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 100 | 0.1 | 91 | CONSERVATIVE | 0.9607 [0.9582, 0.9632] | 0.9011 |  | 0 | Holm p=0, coverage 0.9607 vs 0.9011 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 100 | 0.05 | 96 | OVER_REFUSED |  | 0.9560 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.9174 [0.9155, 0.9193] | 0.8000 |  | 0 | Holm p=0, coverage 0.9174 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9630 [0.9617, 0.9643] | 0.9000 |  | 0 | Holm p=0, coverage 0.9630 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9852 [0.9843, 0.9862] | 0.9500 |  | 0 | Holm p=0, coverage 0.9852 vs 0.9500 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9160 [0.9141, 0.9180] | 0.8002 |  | 0 | Holm p=0, coverage 0.9160 vs 0.8002 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9613 [0.9598, 0.9627] | 0.9001 |  | 0 | Holm p=0, coverage 0.9613 vs 0.9001 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9844 [0.9835, 0.9854] | 0.9501 |  | 0 | Holm p=0, coverage 0.9844 vs 0.9501 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | digits | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | digits | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | digits | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | digits | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=True` | digits | 50 | 0.2 | 41 | ERROR |  | 0.8043 |  |  | 200/200 reps raised ValueError: The test_size = 5 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | digits | 50 | 0.1 | 46 | ERROR |  | 0.9130 |  |  | 200/200 reps raised ValueError: The test_size = 5 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=True` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.9807 [0.9799, 0.9814] | 0.8000 |  | 0 | Holm p=0, coverage 0.9807 vs 0.8000 |
| `mapie/raps/include_last_label=True` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9864 [0.9856, 0.9872] | 0.9000 |  | 0 | Holm p=0, coverage 0.9864 vs 0.9000 |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 5 | 0.2 | 5 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 10 | 1/11 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 19 | 0.05 | 19 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 20 | 0.2 | 17 | ERROR |  | 0.8421 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 20 | 0.1 | 19 | ERROR |  | 0.9474 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 20 | 0.05 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 20 | 1/21 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 49 | 0.1 | 45 | OVER_REFUSED |  | 0.9111 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 49 | 0.05 | 48 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 50 | 0.1 | 46 | OVER_REFUSED |  | 0.9130 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 50 | 0.05 | 49 | OVER_REFUSED |  | 0.9565 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 99 | 0.05 | 95 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 100 | 0.05 | 96 | OVER_REFUSED |  | 0.9560 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.2 | 5 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 5 | 1/6 | 5 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.2 | 8 | ERROR |  | 0.8889 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.1 | 9 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 10 | 1/11 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.05 | 19 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 20 | 0.2 | 17 | ERROR |  | 0.8421 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 20 | 0.1 | 19 | ERROR |  | 0.9474 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 20 | 0.05 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 20 | 1/21 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised ValueError: The test_size = 2 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.1 | 45 | OVER_REFUSED |  | 0.9111 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.05 | 48 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.02 | 49 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 50 | 0.1 | 46 | OVER_REFUSED |  | 0.9130 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 50 | 0.05 | 49 | OVER_REFUSED |  | 0.9565 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 50 | 1/51 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.05 | 95 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 100 | 0.05 | 96 | OVER_REFUSED |  | 0.9560 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 100 | 1/101 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 1000 | 1/1001 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | digits | 10 | 0.2 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | digits | 10 | 0.1 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | digits | 19 | 0.2 | 16 | ERROR |  | 0.8333 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | digits | 19 | 0.1 | 18 | ERROR |  | 0.9444 |  |  | 200/200 reps raised ValueError: The least populated classes in y have only 1 member, which is too fe |
| `mapie/raps/include_last_label=randomized` | digits | 50 | 0.2 | 41 | ERROR |  | 0.8043 |  |  | 200/200 reps raised ValueError: The test_size = 5 should be greater or equal to the number of classe |
| `mapie/raps/include_last_label=randomized` | digits | 50 | 0.1 | 46 | ERROR |  | 0.9130 |  |  | 200/200 reps raised ValueError: The test_size = 5 should be greater or equal to the number of classe |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (19) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (20) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (49) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (50) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (99) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (100) is too low to reach the requ |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (999) is too low to reach the requ |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (1000) is too low to reach the req |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (19) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (20) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (49) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (50) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (99) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (100) is too low to reach the requ |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (999) is too low to reach the requ |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (1000) is too low to reach the req |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (5) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (9) is too low to reach the reques |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (10) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (19) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (20) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (49) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (50) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (99) is too low to reach the reque |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: The number of calibration samples (100) is too low to reach the requ |
| `mapie/split_abs/default` | reg_gauss | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.8333 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 5 | 1/6 | 5 | OVER_REFUSED |  | 0.9427 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 9 | 0.1 | 9 | OVER_REFUSED |  | 0.9860 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9995 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9997 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 49 | 0.02 | 49 | OVER_REFUSED |  | 1.0000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 50 | 1/51 | 50 | OVER_REFUSED |  | 1.0000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 99 | 0.01 | 99 | OVER_REFUSED |  | 1.0000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 100 | 1/101 | 100 | OVER_REFUSED |  | 1.0000 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/split_abs/default` | reg_tied | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `puncc/aps/rand=False` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/aps/rand=False` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/aps/rand=False` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=False` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/aps/rand=False` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/aps/rand=False` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/aps/rand=False` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/aps/rand=False` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/aps/rand=False` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/aps/rand=False` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/aps/rand=False` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/aps/rand=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/aps/rand=False` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/aps/rand=False` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/aps/rand=False` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/aps/rand=False` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/aps/rand=False` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/aps/rand=False` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=False` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/aps/rand=False` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/aps/rand=False` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/aps/rand=False` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/aps/rand=False` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/aps/rand=False` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/aps/rand=False` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/aps/rand=False` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/aps/rand=False` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/aps/rand=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/aps/rand=False` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/aps/rand=True` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/aps/rand=True` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/aps/rand=True` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=True` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/aps/rand=True` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/aps/rand=True` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/aps/rand=True` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/aps/rand=True` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/aps/rand=True` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/aps/rand=True` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/aps/rand=True` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/aps/rand=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/aps/rand=True` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/aps/rand=True` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/aps/rand=True` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/aps/rand=True` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/aps/rand=True` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/aps/rand=True` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/aps/rand=True` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/aps/rand=True` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/aps/rand=True` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/aps/rand=True` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/aps/rand=True` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/aps/rand=True` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/aps/rand=True` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/aps/rand=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/aps/rand=True` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/aps/rand=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/aps/rand=True` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/class_conditional/default` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/class_conditional/default` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/class_conditional/default` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/class_conditional/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/class_conditional/default` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/class_conditional/default` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/class_conditional/default` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/class_conditional/default` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/class_conditional/default` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/class_conditional/default` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/class_conditional/default` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/class_conditional/default` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cqr/default` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/cqr/default` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/cqr/default` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/cqr/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/cqr/default` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/cqr/default` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/cqr/default` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cqr/default` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cqr/default` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cqr/default` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cqr/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cqr/default` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cqr/default` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/cqr/default` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/cqr/default` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/cqr/default` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/cqr/default` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/cqr/default` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/cqr/default` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/cqr/default` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/cqr/default` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cqr/default` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cqr/default` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cqr/default` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cqr/default` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cqr/default` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cqr/default` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/cv_plus/K=10` | reg_constant | 19 | 0.2 | 16 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_constant | 19 | 0.1 | 18 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_constant | 19 | 0.05 | 19 | ERROR |  | 0.9500 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_constant | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_constant | 20 | 1/21 | 20 | ERROR |  | 0.9524 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cv_plus/K=10` | reg_constant | 49 | 0.02 | 49 | ERROR |  | 0.9800 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cv_plus/K=10` | reg_constant | 50 | 1/51 | 50 | ERROR |  | 0.9804 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8029, 0.8146] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.1 | 90 | CONSERVATIVE | 0.9092 [0.9048, 0.9136] | 0.9000 | {"1|1": 200} | 0.32 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.01 | 99 | ERROR |  | 0.9900 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=10` | reg_constant | 100 | 1/101 | 100 | ERROR |  | 0.9901 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.2 | 800 | CONSERVATIVE | 0.7995 [0.7963, 0.8027] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.1 | 900 | CONSERVATIVE | 0.8998 [0.8975, 0.9022] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.001 | 999 | ERROR |  | 0.9990 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cv_plus/K=10` | reg_constant | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/cv_plus/K=10` | reg_gauss | 19 | 0.2 | 16 | ERROR |  | 0.5569 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_gauss | 19 | 0.1 | 18 | ERROR |  | 0.7569 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_gauss | 19 | 0.05 | 19 | ERROR |  | 0.8569 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_gauss | 19 | 0.045 | 20 | ERROR |  | 0.8669 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/cv_plus/K=10` | reg_gauss | 20 | 1/21 | 20 | ERROR |  | 0.8593 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 0.8688 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cv_plus/K=10` | reg_gauss | 49 | 0.02 | 49 | ERROR |  | 0.8876 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 0.8916 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cv_plus/K=10` | reg_gauss | 50 | 1/51 | 50 | ERROR |  | 0.8881 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 0.8920 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cv_plus/K=10` | reg_gauss | 99 | 0.01 | 99 | ERROR |  | 0.8983 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 0.9003 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=10` | reg_gauss | 100 | 1/101 | 100 | ERROR |  | 0.8984 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 0.9004 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=10` | reg_gauss | 999 | 0.001 | 999 | ERROR |  | 0.9802 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 0.9804 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cv_plus/K=10` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 0.9804 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/cv_plus/K=5` | reg_constant | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/cv_plus/K=5` | reg_constant | 20 | 1/21 | 20 | ERROR |  | 0.9524 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cv_plus/K=5` | reg_constant | 49 | 0.02 | 49 | ERROR |  | 0.9800 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cv_plus/K=5` | reg_constant | 50 | 1/51 | 50 | ERROR |  | 0.9804 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8029, 0.8146] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.1 | 90 | CONSERVATIVE | 0.9092 [0.9048, 0.9136] | 0.9000 | {"1|1": 200} | 0.32 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.01 | 99 | ERROR |  | 0.9900 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=5` | reg_constant | 100 | 1/101 | 100 | ERROR |  | 0.9901 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.2 | 800 | CONSERVATIVE | 0.7995 [0.7963, 0.8027] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.1 | 900 | CONSERVATIVE | 0.8998 [0.8975, 0.9022] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.001 | 999 | ERROR |  | 0.9990 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cv_plus/K=5` | reg_constant | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/cv_plus/K=5` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 0.7872 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/cv_plus/K=5` | reg_gauss | 20 | 1/21 | 20 | ERROR |  | 0.7798 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 0.7893 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/cv_plus/K=5` | reg_gauss | 49 | 0.02 | 49 | ERROR |  | 0.8119 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 0.8159 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/cv_plus/K=5` | reg_gauss | 50 | 1/51 | 50 | ERROR |  | 0.8153 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 0.8193 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/cv_plus/K=5` | reg_gauss | 99 | 0.01 | 99 | ERROR |  | 0.9031 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 0.9051 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=5` | reg_gauss | 100 | 1/101 | 100 | ERROR |  | 0.9040 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 0.9060 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=5` | reg_gauss | 999 | 0.001 | 999 | ERROR |  | 0.9900 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 0.9902 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/cv_plus/K=5` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 0.9902 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/jackknife_plus/K=n` | reg_constant | 9 | 0.2 | 8 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 10 | 0.2 | 9 | ERROR |  | 0.8182 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 10 | 0.1 | 10 | ERROR |  | 0.9091 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 10 | 1/11 | 10 | ERROR |  | 0.9091 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 19 | 0.2 | 16 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 19 | 0.1 | 18 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 19 | 0.05 | 19 | ERROR |  | 0.9500 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 20 | 0.2 | 17 | ERROR |  | 0.8095 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 20 | 0.1 | 19 | ERROR |  | 0.9048 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 20 | 0.05 | 20 | ERROR |  | 0.9524 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 20 | 1/21 | 20 | ERROR |  | 0.9524 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 49 | 0.2 | 40 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 49 | 0.1 | 45 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 49 | 0.05 | 48 | ERROR |  | 0.9600 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 49 | 0.02 | 49 | ERROR |  | 0.9800 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 50 | 0.2 | 41 | ERROR |  | 0.8039 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 50 | 0.1 | 46 | ERROR |  | 0.9020 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 50 | 0.05 | 49 | ERROR |  | 0.9608 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 50 | 1/51 | 50 | ERROR |  | 0.9804 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 99 | 0.2 | 80 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 99 | 0.1 | 90 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 99 | 0.05 | 95 | ERROR |  | 0.9500 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 99 | 0.01 | 99 | ERROR |  | 0.9900 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_constant | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 9 | 0.2 | 8 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 9 | 0.1 | 9 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 9 | 0.09 | 10 | ERROR |  | 0.8200 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 9 | 0.05 | 10 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 0.2 | 9 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 0.1 | 10 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 1/11 | 10 | ERROR |  | 0.8182 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 9/110 | 11 | ERROR |  | 0.8364 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 10 | 0.05 | 11 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 19 | 0.2 | 16 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 19 | 0.1 | 18 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 19 | 0.05 | 19 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 19 | 0.045 | 20 | ERROR |  | 0.9100 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 20 | 0.2 | 17 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 20 | 0.1 | 19 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 20 | 0.05 | 20 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 20 | 1/21 | 20 | ERROR |  | 0.9048 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 20 | 3/70 | 21 | ERROR |  | 0.9143 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 49 | 0.2 | 40 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 49 | 0.1 | 45 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 49 | 0.05 | 48 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 49 | 0.02 | 49 | ERROR |  | 0.9600 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 49 | 0.018 | 50 | ERROR |  | 0.9640 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 50 | 0.2 | 41 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 50 | 0.1 | 46 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 50 | 0.05 | 49 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 50 | 1/51 | 50 | ERROR |  | 0.9608 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 50 | 3/170 | 51 | ERROR |  | 0.9647 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 99 | 0.2 | 80 | ERROR |  | 0.6000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 99 | 0.1 | 90 | ERROR |  | 0.8000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 99 | 0.05 | 95 | ERROR |  | 0.9000 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 99 | 0.01 | 99 | ERROR |  | 0.9800 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/jackknife_plus/K=n` | reg_gauss | 99 | 0.009 | 100 | ERROR |  | 0.9820 |  |  | 200/200 reps raised TypeError: object of type 'numpy.float64' has no len() |
| `puncc/lac/default` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/lac/default` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/lac/default` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/lac/default` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/lac/default` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/lac/default` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/lac/default` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/lac/default` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/lac/default` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/lac/default` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/lac/default` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/lac/default` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/lac/default` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/lac/default` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/lac/default` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/lac/default` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/lac/default` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/lac/default` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/lac/default` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/lac/default` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/lac/default` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/lac/default` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/lac/default` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/lac/default` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/lac/default` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/lac/default` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/lac/default` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/lac/default` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/lac/default` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/lac/default` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/raps/rand=False` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/raps/rand=False` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/raps/rand=False` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=False` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/raps/rand=False` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/raps/rand=False` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/raps/rand=False` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/raps/rand=False` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/raps/rand=False` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/raps/rand=False` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/raps/rand=False` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/raps/rand=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=False` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=False` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/raps/rand=False` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/raps/rand=False` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/raps/rand=False` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/raps/rand=False` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=False` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/raps/rand=False` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/raps/rand=False` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/raps/rand=False` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/raps/rand=False` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/raps/rand=False` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/raps/rand=False` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/raps/rand=False` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/raps/rand=False` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=False` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/raps/rand=True` | cls_gauss | 5 | 0.2 | 5 | CONSERVATIVE | 0.9390 [0.9207, 0.9573] | 0.8333 |  | 4.7e-187 | Holm p=4.7e-187, coverage 0.9390 vs 0.8333 |
| `puncc/raps/rand=True` | cls_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 0.9388 [0.9204, 0.9572] | 0.8333 |  | 1.4e-206 | Holm p=1.4e-206, coverage 0.9388 vs 0.8333 |
| `puncc/raps/rand=True` | cls_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/raps/rand=True` | cls_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/raps/rand=True` | cls_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9427 [0.9274, 0.9580] | 0.8000 |  | 0 | Holm p=0, coverage 0.9427 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 0.9836 [0.9760, 0.9912] | 0.9000 |  | 1.3e-233 | Holm p=1.3e-233, coverage 0.9836 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=True` | cls_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/raps/rand=True` | cls_gauss | 10 | 0.2 | 9 | CONSERVATIVE | 0.9638 [0.9535, 0.9741] | 0.8182 |  | 0 | Holm p=0, coverage 0.9638 vs 0.8182 |
| `puncc/raps/rand=True` | cls_gauss | 10 | 0.1 | 10 | CONSERVATIVE | 0.9902 [0.9860, 0.9943] | 0.9091 |  | 3.1e-227 | Holm p=3.1e-227, coverage 0.9902 vs 0.9091 |
| `puncc/raps/rand=True` | cls_gauss | 10 | 1/11 | 10 | CONSERVATIVE | 0.9899 [0.9857, 0.9941] | 0.9091 |  | 5.6e-233 | Holm p=5.6e-233, coverage 0.9899 vs 0.9091 |
| `puncc/raps/rand=True` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/raps/rand=True` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/raps/rand=True` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.9603 [0.9515, 0.9692] | 0.8000 |  | 0 | Holm p=0, coverage 0.9603 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9900 [0.9884, 0.9916] | 0.9000 |  | 0 | Holm p=0, coverage 0.9900 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss | 19 | 0.05 | 19 | CONSERVATIVE | 0.9962 [0.9952, 0.9972] | 0.9500 |  | 7.4e-250 | Holm p=7.4e-250, coverage 0.9962 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/raps/rand=True` | cls_gauss | 20 | 0.2 | 17 | CONSERVATIVE | 0.9755 [0.9702, 0.9807] | 0.8095 |  | 0 | Holm p=0, coverage 0.9755 vs 0.8095 |
| `puncc/raps/rand=True` | cls_gauss | 20 | 0.1 | 19 | CONSERVATIVE | 0.9928 [0.9915, 0.9941] | 0.9048 |  | 0 | Holm p=0, coverage 0.9928 vs 0.9048 |
| `puncc/raps/rand=True` | cls_gauss | 20 | 0.05 | 20 | CONSERVATIVE | 0.9972 [0.9965, 0.9979] | 0.9524 |  | 2.8e-276 | Holm p=2.8e-276, coverage 0.9972 vs 0.9524 |
| `puncc/raps/rand=True` | cls_gauss | 20 | 1/21 | 20 | CONSERVATIVE | 0.9969 [0.9962, 0.9976] | 0.9524 |  | 3.3e-244 | Holm p=3.3e-244, coverage 0.9969 vs 0.9524 |
| `puncc/raps/rand=True` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/raps/rand=True` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.9734 [0.9699, 0.9769] | 0.8000 |  | 0 | Holm p=0, coverage 0.9734 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9923 [0.9914, 0.9933] | 0.9000 |  | 0 | Holm p=0, coverage 0.9923 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss | 49 | 0.05 | 48 | CONSERVATIVE | 0.9973 [0.9968, 0.9978] | 0.9600 |  | 0 | Holm p=0, coverage 0.9973 vs 0.9600 |
| `puncc/raps/rand=True` | cls_gauss | 49 | 0.02 | 49 | CONSERVATIVE | 0.9990 [0.9988, 0.9992] | 0.9800 |  | 9.1e-174 | Holm p=9.1e-174, coverage 0.9990 vs 0.9800 |
| `puncc/raps/rand=True` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/raps/rand=True` | cls_gauss | 50 | 0.2 | 41 | CONSERVATIVE | 0.9778 [0.9757, 0.9799] | 0.8039 |  | 0 | Holm p=0, coverage 0.9778 vs 0.8039 |
| `puncc/raps/rand=True` | cls_gauss | 50 | 0.1 | 46 | CONSERVATIVE | 0.9933 [0.9925, 0.9941] | 0.9020 |  | 0 | Holm p=0, coverage 0.9933 vs 0.9020 |
| `puncc/raps/rand=True` | cls_gauss | 50 | 0.05 | 49 | CONSERVATIVE | 0.9979 [0.9975, 0.9983] | 0.9608 |  | 0 | Holm p=0, coverage 0.9979 vs 0.9608 |
| `puncc/raps/rand=True` | cls_gauss | 50 | 1/51 | 50 | CONSERVATIVE | 0.9990 [0.9988, 0.9993] | 0.9804 |  | 3.2e-180 | Holm p=3.2e-180, coverage 0.9990 vs 0.9804 |
| `puncc/raps/rand=True` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/raps/rand=True` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.9799 [0.9782, 0.9816] | 0.8000 |  | 0 | Holm p=0, coverage 0.9799 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9931 [0.9925, 0.9937] | 0.9000 |  | 0 | Holm p=0, coverage 0.9931 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss | 99 | 0.05 | 95 | CONSERVATIVE | 0.9974 [0.9970, 0.9978] | 0.9500 |  | 0 | Holm p=0, coverage 0.9974 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss | 99 | 0.01 | 99 | CONSERVATIVE | 0.9995 [0.9994, 0.9997] | 0.9900 |  | 8e-126 | Holm p=8e-126, coverage 0.9995 vs 0.9900 |
| `puncc/raps/rand=True` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.9795 [0.9781, 0.9808] | 0.8020 |  | 0 | Holm p=0, coverage 0.9795 vs 0.8020 |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9931 [0.9925, 0.9938] | 0.9010 |  | 0 | Holm p=0, coverage 0.9931 vs 0.9010 |
| `puncc/raps/rand=True` | cls_gauss | 100 | 0.05 | 96 | CONSERVATIVE | 0.9974 [0.9970, 0.9978] | 0.9505 |  | 0 | Holm p=0, coverage 0.9974 vs 0.9505 |
| `puncc/raps/rand=True` | cls_gauss | 100 | 1/101 | 100 | CONSERVATIVE | 0.9997 [0.9995, 0.9998] | 0.9901 |  | 1.8e-139 | Holm p=1.8e-139, coverage 0.9997 vs 0.9901 |
| `puncc/raps/rand=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=True` | cls_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.9804 [0.9794, 0.9814] | 0.8000 |  | 0 | Holm p=0, coverage 0.9804 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9936 [0.9931, 0.9941] | 0.9000 |  | 0 | Holm p=0, coverage 0.9936 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss | 999 | 0.05 | 950 | CONSERVATIVE | 0.9974 [0.9971, 0.9977] | 0.9500 |  | 0 | Holm p=0, coverage 0.9974 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss | 999 | 0.001 | 999 | CONSERVATIVE | 1.0000 [0.9999, 1.0000] | 0.9990 |  | 0 | Holm p=0, coverage 1.0000 vs 0.9990 |
| `puncc/raps/rand=True` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=True` | cls_gauss | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9795 [0.9786, 0.9804] | 0.8002 |  | 0 | Holm p=0, coverage 0.9795 vs 0.8002 |
| `puncc/raps/rand=True` | cls_gauss | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9935 [0.9929, 0.9940] | 0.9001 |  | 0 | Holm p=0, coverage 0.9935 vs 0.9001 |
| `puncc/raps/rand=True` | cls_gauss | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9973 [0.9969, 0.9977] | 0.9500 |  | 0 | Holm p=0, coverage 0.9973 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [0.9999, 1.0000] | 0.9990 |  | 0 | Holm p=0, coverage 1.0000 vs 0.9990 |
| `puncc/raps/rand=True` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/raps/rand=True` | cls_gauss_inf | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/raps/rand=True` | cls_gauss_inf | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/raps/rand=True` | cls_gauss_inf | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/raps/rand=True` | cls_gauss_inf | 9 | 0.1 | 9 | LAW_MISMATCH | 0.9239 [0.9119, 0.9360] | 0.9000 |  | 2.4e-07 | Holm p=2.4e-07, coverage 0.9239 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/raps/rand=True` | cls_gauss_inf | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/raps/rand=True` | cls_gauss_inf | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/raps/rand=True` | cls_gauss_inf | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/raps/rand=True` | cls_gauss_inf | 19 | 0.2 | 16 | CONSERVATIVE | 0.8295 [0.8178, 0.8412] | 0.8000 |  | 0.0088 | Holm p=0.0088, coverage 0.8295 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/raps/rand=True` | cls_gauss_inf | 20 | 1/21 | 20 | LAW_MISMATCH | 0.9653 [0.9599, 0.9707] | 0.9524 |  | 0.018 | Holm p=0.018, coverage 0.9653 vs 0.9524 |
| `puncc/raps/rand=True` | cls_gauss_inf | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/raps/rand=True` | cls_gauss_inf | 49 | 0.2 | 40 | CONSERVATIVE | 0.8295 [0.8219, 0.8371] | 0.8000 |  | 1.3e-09 | Holm p=1.3e-09, coverage 0.8295 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 49 | 0.1 | 45 | CONSERVATIVE | 0.9229 [0.9179, 0.9278] | 0.9000 |  | 3.2e-11 | Holm p=3.2e-11, coverage 0.9229 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 49 | 0.05 | 48 | CONSERVATIVE | 0.9715 [0.9681, 0.9750] | 0.9600 |  | 3.3e-06 | Holm p=3.3e-06, coverage 0.9715 vs 0.9600 |
| `puncc/raps/rand=True` | cls_gauss_inf | 49 | 0.02 | 49 | CONSERVATIVE | 0.9886 [0.9866, 0.9906] | 0.9800 |  | 1.6e-10 | Holm p=1.6e-10, coverage 0.9886 vs 0.9800 |
| `puncc/raps/rand=True` | cls_gauss_inf | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/raps/rand=True` | cls_gauss_inf | 50 | 0.2 | 41 | CONSERVATIVE | 0.8305 [0.8229, 0.8381] | 0.8039 |  | 1.4e-07 | Holm p=1.4e-07, coverage 0.8305 vs 0.8039 |
| `puncc/raps/rand=True` | cls_gauss_inf | 50 | 0.1 | 46 | CONSERVATIVE | 0.9197 [0.9145, 0.9249] | 0.9020 |  | 7.1e-06 | Holm p=7.1e-06, coverage 0.9197 vs 0.9020 |
| `puncc/raps/rand=True` | cls_gauss_inf | 50 | 0.05 | 49 | CONSERVATIVE | 0.9701 [0.9668, 0.9734] | 0.9608 |  | 0.0022 | Holm p=0.0022, coverage 0.9701 vs 0.9608 |
| `puncc/raps/rand=True` | cls_gauss_inf | 50 | 1/51 | 50 | CONSERVATIVE | 0.9870 [0.9846, 0.9893] | 0.9804 |  | 4e-12 | Holm p=4e-12, coverage 0.9870 vs 0.9804 |
| `puncc/raps/rand=True` | cls_gauss_inf | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/raps/rand=True` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.8209 [0.8151, 0.8267] | 0.8000 |  | 2.8e-08 | Holm p=2.8e-08, coverage 0.8209 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9169 [0.9130, 0.9208] | 0.9000 |  | 1.3e-10 | Holm p=1.3e-10, coverage 0.9169 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 99 | 0.05 | 95 | CONSERVATIVE | 0.9619 [0.9589, 0.9649] | 0.9500 |  | 7.3e-12 | Holm p=7.3e-12, coverage 0.9619 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss_inf | 99 | 0.01 | 99 | CONSERVATIVE | 0.9948 [0.9937, 0.9960] | 0.9900 |  | 2.3e-20 | Holm p=2.3e-20, coverage 0.9948 vs 0.9900 |
| `puncc/raps/rand=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/raps/rand=True` | cls_gauss_inf | 100 | 0.2 | 81 | CONSERVATIVE | 0.8319 [0.8257, 0.8381] | 0.8020 |  | 5.9e-17 | Holm p=5.9e-17, coverage 0.8319 vs 0.8020 |
| `puncc/raps/rand=True` | cls_gauss_inf | 100 | 0.1 | 91 | CONSERVATIVE | 0.9213 [0.9173, 0.9252] | 0.9010 |  | 4.3e-12 | Holm p=4.3e-12, coverage 0.9213 vs 0.9010 |
| `puncc/raps/rand=True` | cls_gauss_inf | 100 | 0.05 | 96 | CONSERVATIVE | 0.9651 [0.9622, 0.9680] | 0.9505 |  | 3.6e-17 | Holm p=3.6e-17, coverage 0.9651 vs 0.9505 |
| `puncc/raps/rand=True` | cls_gauss_inf | 100 | 1/101 | 100 | CONSERVATIVE | 0.9960 [0.9948, 0.9971] | 0.9901 |  | 2.3e-27 | Holm p=2.3e-27, coverage 0.9960 vs 0.9901 |
| `puncc/raps/rand=True` | cls_gauss_inf | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.8276 [0.8247, 0.8305] | 0.8000 |  | 5.7e-81 | Holm p=5.7e-81, coverage 0.8276 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9200 [0.9180, 0.9219] | 0.9000 |  | 1.6e-81 | Holm p=1.6e-81, coverage 0.9200 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9636 [0.9622, 0.9650] | 0.9500 |  | 1.4e-90 | Holm p=1.4e-90, coverage 0.9636 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.001 | 999 | CONSERVATIVE | 0.9999 [0.9998, 1.0000] | 0.9990 |  | 2e-14 | Holm p=2e-14, coverage 0.9999 vs 0.9990 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=True` | cls_gauss_inf | 1000 | 0.2 | 801 | CONSERVATIVE | 0.8270 [0.8240, 0.8299] | 0.8002 |  | 5.9e-103 | Holm p=5.9e-103, coverage 0.8270 vs 0.8002 |
| `puncc/raps/rand=True` | cls_gauss_inf | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9183 [0.9163, 0.9203] | 0.9001 |  | 3.9e-65 | Holm p=3.9e-65, coverage 0.9183 vs 0.9001 |
| `puncc/raps/rand=True` | cls_gauss_inf | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9633 [0.9618, 0.9648] | 0.9500 |  | 4e-74 | Holm p=4e-74, coverage 0.9633 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss_inf | 1000 | 1/1001 | 1000 | CONSERVATIVE | 0.9998 [0.9997, 0.9999] | 0.9990 |  | 1.6e-11 | Holm p=1.6e-11, coverage 0.9998 vs 0.9990 |
| `puncc/raps/rand=True` | cls_gauss_inf | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/split_abs/default` | reg_gauss | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_gauss | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/split_abs/default` | reg_gauss | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_gauss | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/split_abs/default` | reg_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/split_abs/default` | reg_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/split_abs/default` | reg_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/split_abs/default` | reg_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/split_abs/default` | reg_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/split_abs/default` | reg_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/split_abs/default` | reg_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/split_abs/default` | reg_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/split_abs/default` | reg_hetero_t | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_hetero_t | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/split_abs/default` | reg_hetero_t | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_hetero_t | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_hetero_t | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_hetero_t | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/split_abs/default` | reg_hetero_t | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/split_abs/default` | reg_hetero_t | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/split_abs/default` | reg_hetero_t | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/split_abs/default` | reg_hetero_t | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/split_abs/default` | reg_hetero_t | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/split_abs/default` | reg_hetero_t | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/split_abs/default` | reg_hetero_t | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/split_abs/default` | reg_hetero_t | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/split_abs/default` | reg_hetero_t | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0008991008991008991, n=1000) 0.00089910 |
| `puncc/split_abs/default` | reg_tied | 5 | 0.15 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.15, n=5) 0.15 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_tied | 5 | 0.1 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.1, n=5) 0.1 < 0.16666666666666666 for a |
| `puncc/split_abs/default` | reg_tied | 5 | 0.05 | 6 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=5) 0.05 < 0.16666666666666666 for |
| `puncc/split_abs/default` | reg_tied | 9 | 0.09 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.09, n=9) 0.09 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_tied | 9 | 0.05 | 10 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=9) 0.05 < 0.1 for at least one of |
| `puncc/split_abs/default` | reg_tied | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.08181818181818182, n=10) 0.081818181818 |
| `puncc/split_abs/default` | reg_tied | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.05, n=10) 0.05 < 0.09090909090909091 fo |
| `puncc/split_abs/default` | reg_tied | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.045, n=19) 0.045 < 0.05 for at least on |
| `puncc/split_abs/default` | reg_tied | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.04285714285714286, n=20) 0.042857142857 |
| `puncc/split_abs/default` | reg_tied | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.018, n=49) 0.018 < 0.02 for at least on |
| `puncc/split_abs/default` | reg_tied | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.01764705882352941, n=50) 0.017647058823 |
| `puncc/split_abs/default` | reg_tied | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/split_abs/default` | reg_tied | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `torchcp/cqr/default` | reg_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 999 | 0.0009 | 1000 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_gauss | 1000 | 9/10010 | 1001 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 999 | 0.0009 | 1000 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/cqr/default` | reg_hetero_t | 1000 | 9/10010 | 1001 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 999 | 0.0009 | 1000 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_gauss | 1000 | 9/10010 | 1001 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 999 | 0.0009 | 1000 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_hetero_t | 1000 | 9/10010 | 1001 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 10 | 9/110 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 10 | 0.05 | 11 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 19 | 0.045 | 20 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 20 | 3/70 | 21 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 49 | 0.018 | 50 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 50 | 3/170 | 51 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 99 | 0.009 | 100 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
| `torchcp/split_abs/default` | reg_tied | 100 | 9/1010 | 101 | ERROR |  | 1.0000 |  |  | 200/200 reps raised AttributeError: 'float' object has no attribute 'shape' |
