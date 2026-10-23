# Conformance matrix: study `default`

R = 200 repetitions, m = 500 test points (capped by the pool on toy data), seed 20261023. Holm FWER 0.05 over 3058 statistical cells; BY FDR 0.05 reported.

Status per row: worst over cells with n <= 100 (small n) and n > 100 (large n).

| row | small n | large n | cells | status counts | note |
|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | ERROR | FAIL | 61 | ERROR 9, FAIL 25, CONSERVATIVE 8, OVER_REFUSED 9, REFUSED 10 |  |
| `mapie/aps/include_last_label=True` | ERROR | CONSERVATIVE | 61 | ERROR 9, CONSERVATIVE 33, OVER_REFUSED 9, REFUSED 10 | MAPIE documents include_last_label=True as conservative |
| `mapie/aps/include_last_label=randomized` | ERROR | OVER_REFUSED | 61 | ERROR 9, OVER_REFUSED 9, REFUSED 10, PASS 33 |  |
| `mapie/cqr/asymmetric` | OVER_REFUSED | REFUSED | 114 | OVER_REFUSED 5, REFUSED 59, PASS 50 |  |
| `mapie/cqr/symmetric` | OVER_REFUSED | OVER_REFUSED | 114 | OVER_REFUSED 22, REFUSED 30, PASS 62 |  |
| `mapie/cv_plus/K=10` | PASS | CONSERVATIVE | 78 | CONSERVATIVE 1, PASS 77 |  |
| `mapie/cv_plus/K=5` | PASS | CONSERVATIVE | 78 | CONSERVATIVE 1, PASS 77 |  |
| `mapie/jackknife_plus/default` | PASS | - | 66 | PASS 66 |  |
| `mapie/lac/default` | OVER_REFUSED | OVER_REFUSED | 61 | OVER_REFUSED 11, REFUSED 15, PASS 35 |  |
| `mapie/split_abs/allow_infinite_bounds` | REFUSED | REFUSED | 157 | REFUSED 43, PASS 114 |  |
| `mapie/split_abs/default` | OVER_REFUSED | OVER_REFUSED | 157 | OVER_REFUSED 31, REFUSED 43, PASS 83 |  |
| `crepes/class_conditional/smoothed` | PASS | - | 38 | PASS 38 |  |
| `crepes/class_conditional/unsmoothed` | CONSERVATIVE | - | 38 | CONSERVATIVE 9, PASS 29 |  |
| `crepes/lac/smoothed` | PASS | PASS | 61 | PASS 61 |  |
| `crepes/lac/unsmoothed` | CONSERVATIVE | CONSERVATIVE | 61 | CONSERVATIVE 10, PASS 51 |  |
| `crepes/split_abs/default` | CONSERVATIVE | CONSERVATIVE | 157 | CONSERVATIVE 35, PASS 122 |  |
| `puncc/aps/rand=False` | REFUSED | REFUSED | 61 | REFUSED 15, PASS 46 |  |
| `puncc/aps/rand=True` | REFUSED | REFUSED | 61 | REFUSED 15, PASS 46 |  |
| `puncc/class_conditional/default` | REFUSED | - | 38 | REFUSED 12, PASS 26 |  |
| `puncc/cqr/default` | REFUSED | REFUSED | 114 | REFUSED 30, PASS 84 |  |
| `puncc/cv_plus/K=10` | ERROR | ERROR | 78 | ERROR 20, CONSERVATIVE 4, REFUSED 14, PASS 40 |  |
| `puncc/cv_plus/K=5` | ERROR | ERROR | 78 | ERROR 12, CONSERVATIVE 4, REFUSED 16, PASS 46 |  |
| `puncc/jackknife_plus/K=n` | ERROR | - | 66 | ERROR 66 |  |
| `puncc/lac/default` | REFUSED | REFUSED | 61 | REFUSED 15, PASS 46 |  |
| `puncc/split_abs/default` | REFUSED | REFUSED | 157 | REFUSED 43, PASS 114 |  |
| `torchcp/aps/randomized=False` | PASS | PASS | 61 | PASS 61 |  |
| `torchcp/aps/randomized=True` | PASS | PASS | 61 | PASS 61 |  |
| `torchcp/class_conditional/default` | PASS | - | 38 | PASS 38 |  |
| `torchcp/cqr/default` | ERROR | ERROR | 114 | ERROR 30, PASS 84 |  |
| `torchcp/lac/default` | PASS | PASS | 61 | PASS 61 |  |
| `torchcp/split_abs/default` | ERROR | ERROR | 157 | ERROR 43, PASS 114 |  |
| `reference/aps/deterministic` | PASS | PASS | 61 | PASS 61 |  |
| `reference/aps/randomized` | PASS | PASS | 61 | PASS 61 |  |
| `reference/class_conditional/default` | PASS | - | 38 | PASS 38 |  |
| `reference/cqr/asymmetric` | PASS | PASS | 114 | PASS 114 |  |
| `reference/cqr/symmetric` | PASS | PASS | 114 | PASS 114 |  |
| `reference/cv_plus/K=10` | PASS | PASS | 78 | PASS 78 |  |
| `reference/cv_plus/K=5` | PASS | PASS | 78 | PASS 78 |  |
| `reference/jackknife_plus/default` | PASS | - | 66 | PASS 66 |  |
| `reference/lac/default` | PASS | PASS | 61 | PASS 61 |  |
| `reference/lac/k_minus_1` | FAIL | FAIL | 61 | FAIL 50, PASS 11 |  |
| `reference/lac/k_plus_1` | CONSERVATIVE | CONSERVATIVE | 61 | CONSERVATIVE 35, PASS 26 |  |
| `reference/lac/n_instead_of_n_plus_1` | FAIL | FAIL | 61 | FAIL 29, PASS 32 |  |
| `reference/lac/no_correction_linear` | FAIL | FAIL | 61 | FAIL 46, PASS 15 |  |
| `reference/lac/smoothed` | PASS | PASS | 61 | PASS 61 |  |
| `reference/split_abs/default` | PASS | PASS | 157 | PASS 157 |  |
| `reference/split_abs/k_minus_1` | FAIL | FAIL | 157 | FAIL 145, PASS 12 |  |
| `reference/split_abs/k_plus_1` | CONSERVATIVE | CONSERVATIVE | 157 | CONSERVATIVE 106, PASS 51 |  |
| `reference/split_abs/n_instead_of_n_plus_1` | FAIL | FAIL | 157 | FAIL 87, PASS 70 |  |
| `reference/split_abs/no_correction_linear` | FAIL | FAIL | 157 | FAIL 145, PASS 12 |  |

## Status grid (worst over dgps and alphas at each n)

P pass, C conservative, F fail, L law mismatch, O refused a feasible level, R refused with k > n, E error, . not run.

| row | 5 | 9 | 10 | 19 | 20 | 49 | 50 | 99 | 100 | 999 | 1000 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | E | E | F | F | F | F | F | F | F | F | F |
| `mapie/aps/include_last_label=True` | E | E | C | C | C | C | C | C | C | C | C |
| `mapie/aps/include_last_label=randomized` | E | E | O | O | O | O | O | O | O | O | O |
| `mapie/cqr/asymmetric` | R | O | R | O | R | R | R | R | R | R | R |
| `mapie/cqr/symmetric` | O | O | O | O | O | O | O | O | O | O | O |
| `mapie/cv_plus/K=10` | . | . | . | P | P | P | P | P | P | C | P |
| `mapie/cv_plus/K=5` | . | . | . | P | P | P | P | P | P | C | P |
| `mapie/jackknife_plus/default` | . | P | P | P | P | P | P | P | . | . | . |
| `mapie/lac/default` | O | O | O | O | O | O | O | O | O | O | O |
| `mapie/split_abs/allow_infinite_bounds` | R | R | R | R | R | R | R | R | R | R | R |
| `mapie/split_abs/default` | O | O | O | O | O | O | O | O | O | O | O |
| `crepes/class_conditional/smoothed` | P | P | P | P | P | P | P | P | . | . | . |
| `crepes/class_conditional/unsmoothed` | C | C | P | C | P | C | P | C | . | . | . |
| `crepes/lac/smoothed` | P | P | P | P | P | P | P | P | P | P | P |
| `crepes/lac/unsmoothed` | C | C | P | C | P | C | P | C | P | P | C |
| `crepes/split_abs/default` | C | C | P | C | P | C | P | C | P | C | C |
| `puncc/aps/rand=False` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/aps/rand=True` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/class_conditional/default` | R | R | R | R | R | R | R | R | . | . | . |
| `puncc/cqr/default` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/cv_plus/K=10` | . | . | . | E | E | E | E | E | E | E | R |
| `puncc/cv_plus/K=5` | . | . | . | R | E | E | E | E | E | E | R |
| `puncc/jackknife_plus/K=n` | . | E | E | E | E | E | E | E | . | . | . |
| `puncc/lac/default` | R | R | R | R | R | R | R | R | R | R | R |
| `puncc/split_abs/default` | R | R | R | R | R | R | R | R | R | R | R |
| `torchcp/aps/randomized=False` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/aps/randomized=True` | P | P | P | P | P | P | P | P | P | P | P |
| `torchcp/class_conditional/default` | P | P | P | P | P | P | P | P | . | . | . |
| `torchcp/cqr/default` | E | E | E | E | E | E | E | E | E | E | E |
| `torchcp/lac/default` | P | P | P | P | P | P | P | P | P | P | P |
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
| `reference/split_abs/default` | P | P | P | P | P | P | P | P | P | P | P |
| `reference/split_abs/k_minus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/split_abs/k_plus_1` | C | C | C | C | C | C | C | C | C | C | C |
| `reference/split_abs/n_instead_of_n_plus_1` | F | F | F | F | F | F | F | F | F | F | F |
| `reference/split_abs/no_correction_linear` | F | F | F | F | F | F | F | F | F | F | F |

## Non-PASS cells (libraries)

| row | dgp | n | alpha | k | status | coverage [95% CI] | target | rank offsets lower|upper (reps) | Holm p | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `crepes/class_conditional/unsmoothed` | cls_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [0.9900, 1.0100] | 0.8333 |  | 0 | Holm p=0, coverage 1.0000 vs 0.8333 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9010 [0.8923, 0.9097] | 0.8000 |  | 0 | Holm p=0, coverage 0.9010 vs 0.8000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [0.9935, 1.0065] | 0.9000 |  | 0 | Holm p=0, coverage 1.0000 vs 0.9000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8494 [0.8428, 0.8559] | 0.8000 |  | 5.1e-73 | Holm p=5.1e-73, coverage 0.8494 vs 0.8000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9495 [0.9446, 0.9543] | 0.9000 |  | 7.7e-209 | Holm p=7.7e-209, coverage 0.9495 vs 0.9000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8162 [0.8116, 0.8208] | 0.8000 |  | 1.2e-08 | Holm p=1.2e-08, coverage 0.8162 vs 0.8000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9172 [0.9138, 0.9207] | 0.9000 |  | 2.1e-17 | Holm p=2.1e-17, coverage 0.9172 vs 0.9000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.8115 [0.8078, 0.8152] | 0.8000 |  | 3.5e-06 | Holm p=3.5e-06, coverage 0.8115 vs 0.8000 |
| `crepes/class_conditional/unsmoothed` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9110 [0.9082, 0.9138] | 0.9000 |  | 1.8e-11 | Holm p=1.8e-11, coverage 0.9110 vs 0.9000 |
| `crepes/lac/unsmoothed` | cls_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [0.9804, 1.0196] | 0.8333 |  | 0 | Holm p=0, coverage 1.0000 vs 0.8333 |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.8942 [0.8774, 0.9111] | 0.8000 |  | 1.1e-48 | Holm p=1.1e-48, coverage 0.8942 vs 0.8000 |
| `crepes/lac/unsmoothed` | cls_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [0.9873, 1.0127] | 0.9000 |  | 0 | Holm p=0, coverage 1.0000 vs 0.9000 |
| `crepes/lac/unsmoothed` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8431 [0.8308, 0.8555] | 0.8000 |  | 2.3e-09 | Holm p=2.3e-09, coverage 0.8431 vs 0.8000 |
| `crepes/lac/unsmoothed` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9466 [0.9373, 0.9558] | 0.9000 |  | 3.7e-39 | Holm p=3.7e-39, coverage 0.9466 vs 0.9000 |
| `crepes/lac/unsmoothed` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9183 [0.9122, 0.9244] | 0.9000 |  | 3.2e-06 | Holm p=3.2e-06, coverage 0.9183 vs 0.9000 |
| `crepes/lac/unsmoothed` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9131 [0.9085, 0.9176] | 0.9000 |  | 2.4e-05 | Holm p=2.4e-05, coverage 0.9131 vs 0.9000 |
| `crepes/lac/unsmoothed` | cls_gauss | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [0.9998, 1.0002] | 0.9990 |  | 0 | Holm p=0, coverage 1.0000 vs 0.9990 |
| `crepes/lac/unsmoothed` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.8435 [0.8312, 0.8558] | 0.8000 |  | 1.4e-09 | Holm p=1.4e-09, coverage 0.8435 vs 0.8000 |
| `crepes/lac/unsmoothed` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9476 [0.9384, 0.9569] | 0.9000 |  | 4.7e-48 | Holm p=4.7e-48, coverage 0.9476 vs 0.9000 |
| `crepes/split_abs/default` | diabetes | 19 | 0.2 | 16 | CONSERVATIVE | 0.8548 [0.8423, 0.8673] | 0.8000 | {"1|1": 200} | 2e-12 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 19 | 0.1 | 18 | CONSERVATIVE | 0.9513 [0.9420, 0.9607] | 0.9000 | {"1|1": 200} | 6.1e-64 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 99 | 0.2 | 80 | CONSERVATIVE | 0.8109 [0.8044, 0.8175] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | diabetes | 99 | 0.1 | 90 | CONSERVATIVE | 0.9100 [0.9051, 0.9149] | 0.9000 | {"1|1": 200} | 0.24 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [0.9804, 1.0196] | 0.8333 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.2 | 8 | CONSERVATIVE | 0.9006 [0.8837, 0.9175] | 0.8000 | {"1|1": 200} | 4e-64 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [0.9873, 1.0127] | 0.9000 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8573 [0.8449, 0.8696] | 0.8000 | {"1|1": 200} | 2.5e-13 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9493 [0.9401, 0.9586] | 0.9000 | {"1|1": 200} | 2.4e-43 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.8193 [0.8111, 0.8274] | 0.8000 | {"1|1": 200} | 0.011 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9157 [0.9096, 0.9218] | 0.9000 | {"1|1": 200} | 0.00066 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8028, 0.8149] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9103 [0.9058, 0.9149] | 0.9000 | {"1|1": 200} | 0.023 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.8029 [0.7999, 0.8059] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9027 [0.9004, 0.9050] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_gauss | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [0.9998, 1.0002] | 0.9990 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [0.9804, 1.0196] | 0.8333 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 9 | 0.2 | 8 | CONSERVATIVE | 0.8860 [0.8691, 0.9028] | 0.8000 | {"1|1": 200} | 5.7e-59 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [0.9873, 1.0127] | 0.9000 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 19 | 0.2 | 16 | CONSERVATIVE | 0.8492 [0.8369, 0.8616] | 0.8000 | {"1|1": 200} | 3.3e-12 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 19 | 0.1 | 18 | CONSERVATIVE | 0.9481 [0.9388, 0.9573] | 0.9000 | {"1|1": 200} | 2.2e-39 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 49 | 0.2 | 40 | CONSERVATIVE | 0.8174 [0.8093, 0.8256] | 0.8000 | {"1|1": 200} | 0.095 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 49 | 0.1 | 45 | CONSERVATIVE | 0.9180 [0.9119, 0.9241] | 0.9000 | {"1|1": 200} | 6.3e-06 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 99 | 0.2 | 80 | CONSERVATIVE | 0.8069 [0.8008, 0.8129] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 99 | 0.1 | 90 | CONSERVATIVE | 0.9079 [0.9034, 0.9124] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 999 | 0.2 | 800 | CONSERVATIVE | 0.8000 [0.7970, 0.8031] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 999 | 0.1 | 900 | CONSERVATIVE | 0.9017 [0.8994, 0.9040] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_hetero_t | 1000 | 1/1001 | 1000 | CONSERVATIVE | 1.0000 [0.9998, 1.0002] | 0.9990 | {"1|1": 200} | 0 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 5 | 1/6 | 5 | CONSERVATIVE | 1.0000 [0.9827, 1.0173] | 0.9427 | {"1|1": 200} | 1.5e-14 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 9 | 0.2 | 8 | CONSERVATIVE | 0.9927 [0.9754, 1.0100] | 0.9346 | {"0|0": 171, "1|1": 29} | 5.2e-12 | rank +1 in 29 reps |
| `crepes/split_abs/default` | reg_tied | 9 | 0.1 | 9 | CONSERVATIVE | 1.0000 [0.9914, 1.0086] | 0.9860 | {"1|1": 200} | 0.5 | rank +1 in 200 reps |
| `crepes/split_abs/default` | reg_tied | 19 | 0.2 | 16 | CONSERVATIVE | 0.9843 [0.9696, 0.9991] | 0.9531 | {"0|0": 180, "1|1": 20} | 0.016 | rank +1 in 20 reps |
| `crepes/split_abs/default` | reg_tied | 19 | 0.1 | 18 | CONSERVATIVE | 1.0000 [0.9953, 1.0047] | 0.9959 | {"0|0": 196, "1|1": 4} | 1 | rank +1 in 4 reps |
| `crepes/split_abs/default` | reg_tied | 49 | 0.2 | 40 | CONSERVATIVE | 0.9934 [0.9830, 1.0037] | 0.9791 | {"0|0": 195, "1|1": 5} | 1 | rank +1 in 5 reps |
| `crepes/split_abs/default` | reg_tied | 99 | 0.2 | 80 | CONSERVATIVE | 0.9972 [0.9913, 1.0030] | 0.9937 | {"0|0": 198, "1|1": 2} | 1 | rank +1 in 2 reps |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.5326 [0.5111, 0.5540] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.5178 [0.5008, 0.5347] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.2 | 9 | FAIL | 0.5303 [0.5147, 0.5459] | 0.8182 |  | 0 | Holm p=0, coverage 0.5303 vs 0.8182 |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.1 | 10 | FAIL | 0.5594 [0.5478, 0.5711] | 0.9091 |  | 0 | Holm p=0, coverage 0.5594 vs 0.9091 |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.2 | 16 | FAIL | 0.5186 [0.5063, 0.5310] | 0.8000 |  | 0 | Holm p=0, coverage 0.5186 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.1 | 18 | FAIL | 0.5536 [0.5444, 0.5629] | 0.9000 |  | 0 | Holm p=0, coverage 0.5536 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.2 | 17 | FAIL | 0.5314 [0.5195, 0.5432] | 0.8095 |  | 0 | Holm p=0, coverage 0.5314 vs 0.8095 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.1 | 19 | FAIL | 0.5585 [0.5496, 0.5673] | 0.9048 |  | 0 | Holm p=0, coverage 0.5585 vs 0.9048 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 0.05 | 20 | FAIL | 0.5697 [0.5632, 0.5761] | 0.9524 |  | 0 | Holm p=0, coverage 0.5697 vs 0.9524 |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.2 | 40 | FAIL | 0.5251 [0.5169, 0.5332] | 0.8000 |  | 0 | Holm p=0, coverage 0.5251 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.1 | 45 | FAIL | 0.5576 [0.5515, 0.5637] | 0.9000 |  | 0 | Holm p=0, coverage 0.5576 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.05 | 48 | FAIL | 0.5715 [0.5675, 0.5755] | 0.9600 |  | 0 | Holm p=0, coverage 0.5715 vs 0.9600 |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.2 | 41 | FAIL | 0.5317 [0.5237, 0.5397] | 0.8039 |  | 0 | Holm p=0, coverage 0.5317 vs 0.8039 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.1 | 46 | FAIL | 0.5623 [0.5563, 0.5683] | 0.9020 |  | 0 | Holm p=0, coverage 0.5623 vs 0.9020 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 0.05 | 49 | FAIL | 0.5747 [0.5708, 0.5786] | 0.9608 |  | 0 | Holm p=0, coverage 0.5747 vs 0.9608 |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.2 | 80 | FAIL | 0.5299 [0.5238, 0.5359] | 0.8000 |  | 0 | Holm p=0, coverage 0.5299 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.1 | 90 | FAIL | 0.5605 [0.5560, 0.5651] | 0.9000 |  | 0 | Holm p=0, coverage 0.5605 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.05 | 95 | FAIL | 0.5718 [0.5685, 0.5751] | 0.9500 |  | 0 | Holm p=0, coverage 0.5718 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.2 | 81 | FAIL | 0.5323 [0.5264, 0.5383] | 0.8020 |  | 0 | Holm p=0, coverage 0.5323 vs 0.8020 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.1 | 91 | FAIL | 0.5619 [0.5574, 0.5664] | 0.9010 |  | 0 | Holm p=0, coverage 0.5619 vs 0.9010 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 0.05 | 96 | FAIL | 0.5738 [0.5705, 0.5770] | 0.9505 |  | 0 | Holm p=0, coverage 0.5738 vs 0.9505 |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.2 | 800 | FAIL | 0.5290 [0.5260, 0.5320] | 0.8000 |  | 0 | Holm p=0, coverage 0.5290 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.1 | 900 | FAIL | 0.5603 [0.5581, 0.5626] | 0.9000 |  | 0 | Holm p=0, coverage 0.5603 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.05 | 950 | FAIL | 0.5720 [0.5703, 0.5736] | 0.9500 |  | 0 | Holm p=0, coverage 0.5720 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.2 | 801 | FAIL | 0.5291 [0.5260, 0.5321] | 0.8002 |  | 0 | Holm p=0, coverage 0.5291 vs 0.8002 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.1 | 901 | FAIL | 0.5599 [0.5576, 0.5621] | 0.9001 |  | 0 | Holm p=0, coverage 0.5599 vs 0.9001 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 0.05 | 951 | FAIL | 0.5715 [0.5698, 0.5732] | 0.9500 |  | 0 | Holm p=0, coverage 0.5715 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | digits | 10 | 0.2 | 9 | CONSERVATIVE | 0.9637 [0.9481, 0.9793] | 0.8182 |  | 2.9e-303 | Holm p=2.9e-303, coverage 0.9637 vs 0.8182 |
| `mapie/aps/include_last_label=False` | digits | 10 | 0.1 | 10 | CONSERVATIVE | 0.9765 [0.9648, 0.9881] | 0.9091 |  | 1.3e-50 | Holm p=1.3e-50, coverage 0.9765 vs 0.9091 |
| `mapie/aps/include_last_label=False` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.9614 [0.9491, 0.9738] | 0.8000 |  | 0 | Holm p=0, coverage 0.9614 vs 0.8000 |
| `mapie/aps/include_last_label=False` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9740 [0.9647, 0.9832] | 0.9000 |  | 1.6e-121 | Holm p=1.6e-121, coverage 0.9740 vs 0.9000 |
| `mapie/aps/include_last_label=False` | digits | 50 | 0.2 | 41 | CONSERVATIVE | 0.9595 [0.9515, 0.9676] | 0.8039 |  | 0 | Holm p=0, coverage 0.9595 vs 0.8039 |
| `mapie/aps/include_last_label=False` | digits | 50 | 0.1 | 46 | CONSERVATIVE | 0.9722 [0.9662, 0.9782] | 0.9020 |  | 0 | Holm p=0, coverage 0.9722 vs 0.9020 |
| `mapie/aps/include_last_label=False` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.9592 [0.9531, 0.9652] | 0.8000 |  | 0 | Holm p=0, coverage 0.9592 vs 0.8000 |
| `mapie/aps/include_last_label=False` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9710 [0.9665, 0.9756] | 0.9000 |  | 0 | Holm p=0, coverage 0.9710 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.9120 [0.8905, 0.9335] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.8831 [0.8661, 0.9000] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.1 | 9 | ERROR |  | 0.9000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.09 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 9 | 0.05 | 10 | ERROR |  | 1.0000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.2 | 9 | CONSERVATIVE | 0.9084 [0.8928, 0.9240] | 0.8182 |  | 2.6e-58 | Holm p=2.6e-58, coverage 0.9084 vs 0.8182 |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.1 | 10 | CONSERVATIVE | 0.9677 [0.9561, 0.9793] | 0.9091 |  | 4.1e-41 | Holm p=4.1e-41, coverage 0.9677 vs 0.9091 |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 1/11 | 10 | OVER_REFUSED |  | 0.9091 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 9/110 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 10 | 0.05 | 11 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.2 | 16 | CONSERVATIVE | 0.8893 [0.8770, 0.9016] | 0.8000 |  | 5.1e-99 | Holm p=5.1e-99, coverage 0.8893 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.1 | 18 | CONSERVATIVE | 0.9580 [0.9488, 0.9673] | 0.9000 |  | 2e-87 | Holm p=2e-87, coverage 0.9580 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.05 | 19 | OVER_REFUSED |  | 0.9500 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 19 | 0.045 | 20 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.2 | 17 | CONSERVATIVE | 0.9153 [0.9035, 0.9272] | 0.8095 |  | 5.7e-173 | Holm p=5.7e-173, coverage 0.9153 vs 0.8095 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.1 | 19 | CONSERVATIVE | 0.9681 [0.9593, 0.9770] | 0.9048 |  | 1.4e-181 | Holm p=1.4e-181, coverage 0.9681 vs 0.9048 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 0.05 | 20 | CONSERVATIVE | 0.9887 [0.9823, 0.9951] | 0.9524 |  | 9.4e-113 | Holm p=9.4e-113, coverage 0.9887 vs 0.9524 |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 1/21 | 20 | OVER_REFUSED |  | 0.9524 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 20 | 3/70 | 21 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.2 | 40 | CONSERVATIVE | 0.9004 [0.8922, 0.9085] | 0.8000 |  | 0 | Holm p=0, coverage 0.9004 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.1 | 45 | CONSERVATIVE | 0.9659 [0.9598, 0.9720] | 0.9000 |  | 0 | Holm p=0, coverage 0.9659 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.05 | 48 | CONSERVATIVE | 0.9912 [0.9872, 0.9952] | 0.9600 |  | 6.6e-153 | Holm p=6.6e-153, coverage 0.9912 vs 0.9600 |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.02 | 49 | OVER_REFUSED |  | 0.9800 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 49 | 0.018 | 50 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.2 | 41 | CONSERVATIVE | 0.9071 [0.8991, 0.9151] | 0.8039 |  | 0 | Holm p=0, coverage 0.9071 vs 0.8039 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.1 | 46 | CONSERVATIVE | 0.9691 [0.9631, 0.9751] | 0.9020 |  | 0 | Holm p=0, coverage 0.9691 vs 0.9020 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 0.05 | 49 | CONSERVATIVE | 0.9928 [0.9888, 0.9967] | 0.9608 |  | 7.9e-221 | Holm p=7.9e-221, coverage 0.9928 vs 0.9608 |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 1/51 | 50 | OVER_REFUSED |  | 0.9804 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 50 | 3/170 | 51 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.2 | 80 | CONSERVATIVE | 0.9094 [0.9033, 0.9154] | 0.8000 |  | 0 | Holm p=0, coverage 0.9094 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.1 | 90 | CONSERVATIVE | 0.9706 [0.9660, 0.9751] | 0.9000 |  | 0 | Holm p=0, coverage 0.9706 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.05 | 95 | CONSERVATIVE | 0.9902 [0.9869, 0.9935] | 0.9500 |  | 0 | Holm p=0, coverage 0.9902 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.2 | 81 | CONSERVATIVE | 0.9093 [0.9033, 0.9153] | 0.8020 |  | 0 | Holm p=0, coverage 0.9093 vs 0.8020 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.1 | 91 | CONSERVATIVE | 0.9693 [0.9648, 0.9738] | 0.9010 |  | 0 | Holm p=0, coverage 0.9693 vs 0.9010 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 0.05 | 96 | CONSERVATIVE | 0.9899 [0.9866, 0.9932] | 0.9505 |  | 0 | Holm p=0, coverage 0.9899 vs 0.9505 |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 1/101 | 100 | OVER_REFUSED |  | 0.9901 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.2 | 800 | CONSERVATIVE | 0.9069 [0.9039, 0.9100] | 0.8000 |  | 0 | Holm p=0, coverage 0.9069 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.1 | 900 | CONSERVATIVE | 0.9711 [0.9688, 0.9734] | 0.9000 |  | 0 | Holm p=0, coverage 0.9711 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.05 | 950 | CONSERVATIVE | 0.9901 [0.9885, 0.9918] | 0.9500 |  | 0 | Holm p=0, coverage 0.9901 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.2 | 801 | CONSERVATIVE | 0.9064 [0.9033, 0.9094] | 0.8002 |  | 0 | Holm p=0, coverage 0.9064 vs 0.8002 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.1 | 901 | CONSERVATIVE | 0.9710 [0.9688, 0.9733] | 0.9001 |  | 0 | Holm p=0, coverage 0.9710 vs 0.9001 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 0.05 | 951 | CONSERVATIVE | 0.9906 [0.9890, 0.9923] | 0.9500 |  | 0 | Holm p=0, coverage 0.9906 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 1/1001 | 1000 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss | 1000 | 9/10010 | 1001 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | digits | 10 | 0.2 | 9 | CONSERVATIVE | 0.9857 [0.9701, 1.0013] | 0.8182 |  | 0 | Holm p=0, coverage 0.9857 vs 0.8182 |
| `mapie/aps/include_last_label=True` | digits | 10 | 0.1 | 10 | CONSERVATIVE | 0.9917 [0.9801, 1.0034] | 0.9091 |  | 5.9e-159 | Holm p=5.9e-159, coverage 0.9917 vs 0.9091 |
| `mapie/aps/include_last_label=True` | digits | 19 | 0.2 | 16 | CONSERVATIVE | 0.9857 [0.9733, 0.9980] | 0.8000 |  | 0 | Holm p=0, coverage 0.9857 vs 0.8000 |
| `mapie/aps/include_last_label=True` | digits | 19 | 0.1 | 18 | CONSERVATIVE | 0.9915 [0.9822, 1.0007] | 0.9000 |  | 0 | Holm p=0, coverage 0.9915 vs 0.9000 |
| `mapie/aps/include_last_label=True` | digits | 50 | 0.2 | 41 | CONSERVATIVE | 0.9845 [0.9765, 0.9926] | 0.8039 |  | 0 | Holm p=0, coverage 0.9845 vs 0.8039 |
| `mapie/aps/include_last_label=True` | digits | 50 | 0.1 | 46 | CONSERVATIVE | 0.9914 [0.9854, 0.9974] | 0.9020 |  | 0 | Holm p=0, coverage 0.9914 vs 0.9020 |
| `mapie/aps/include_last_label=True` | digits | 99 | 0.2 | 80 | CONSERVATIVE | 0.9845 [0.9784, 0.9905] | 0.8000 |  | 0 | Holm p=0, coverage 0.9845 vs 0.8000 |
| `mapie/aps/include_last_label=True` | digits | 99 | 0.1 | 90 | CONSERVATIVE | 0.9919 [0.9874, 0.9965] | 0.9000 |  | 0 | Holm p=0, coverage 0.9919 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.2 | 5 | ERROR | 0.8380 [0.8166, 0.8595] | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 1/6 | 5 | ERROR |  | 0.8333 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.15 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.1 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 5 | 0.05 | 6 | ERROR |  | 1.0000 |  |  | 33/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 9 | 0.2 | 8 | ERROR | 0.7934 [0.7765, 0.8103] | 0.8000 |  |  | 1/200 reps raised ValueError: Invalid conformity score for binary target. The only valid score is |
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
| `mapie/cv_plus/K=10` | reg_constant | 999 | 0.05 | 950 | CONSERVATIVE | 0.9508 [0.9492, 0.9525] | 0.9500 | {"1|0": 200} | 1 | rank +1 in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 999 | 0.05 | 950 | CONSERVATIVE | 0.9508 [0.9492, 0.9525] | 0.9500 | {"1|0": 200} | 1 | rank +1 in 200 reps |
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
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8027, 0.8148] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.1 | 90 | CONSERVATIVE | 0.9092 [0.9047, 0.9138] | 0.9000 | {"1|1": 200} | 0.22 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.01 | 99 | ERROR |  | 0.9900 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=10` | reg_constant | 100 | 1/101 | 100 | ERROR |  | 0.9901 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=10` | reg_constant | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.2 | 800 | CONSERVATIVE | 0.7995 [0.7965, 0.8025] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=10` | reg_constant | 999 | 0.1 | 900 | CONSERVATIVE | 0.8998 [0.8975, 0.9021] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
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
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.2 | 80 | CONSERVATIVE | 0.8088 [0.8027, 0.8148] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.1 | 90 | CONSERVATIVE | 0.9092 [0.9047, 0.9138] | 0.9000 | {"1|1": 200} | 0.22 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.01 | 99 | ERROR |  | 0.9900 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.009, n=99) 0.009 < 0.01 for at least on |
| `puncc/cv_plus/K=5` | reg_constant | 100 | 1/101 | 100 | ERROR |  | 0.9901 |  |  | 200/200 reps raised ValueError: All coordinates of [q] must be in the open interval (0, 1). |
| `puncc/cv_plus/K=5` | reg_constant | 100 | 9/1010 | 101 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.00891089108910891, n=100) 0.00891089108 |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.2 | 800 | CONSERVATIVE | 0.7995 [0.7965, 0.8025] | 0.8000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
| `puncc/cv_plus/K=5` | reg_constant | 999 | 0.1 | 900 | CONSERVATIVE | 0.8998 [0.8975, 0.9021] | 0.9000 | {"1|1": 200} | 1 | rank +1 in 200 reps |
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
