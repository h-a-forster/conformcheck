# Conformance matrix: study `full-aps-raps`

R = 2000 repetitions, m = 1000 test points (capped by the pool on toy data), seed 20261023. Holm FWER 0.05 over 74 statistical cells; BY FDR 0.05 reported.

Status per row: worst over cells with n <= 100 (small n) and n > 100 (large n).

| row | small n | large n | cells | status counts | note |
|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | FAIL | FAIL | 10 | FAIL 6, OVER_REFUSED 2, REFUSED 2 |  |
| `mapie/aps/include_last_label=True` | CONSERVATIVE | CONSERVATIVE | 10 | CONSERVATIVE 6, OVER_REFUSED 2, REFUSED 2 | MAPIE documents include_last_label=True as conservative |
| `mapie/aps/include_last_label=randomized` | OVER_REFUSED | OVER_REFUSED | 10 | OVER_REFUSED 2, REFUSED 2, PASS 6 |  |
| `mapie/raps/include_last_label=True` | CONSERVATIVE | CONSERVATIVE | 10 | CONSERVATIVE 5, OVER_REFUSED 1, REFUSED 4 | MAPIE documents include_last_label=True as conservative |
| `mapie/raps/include_last_label=randomized` | - | CONSERVATIVE | 5 | CONSERVATIVE 1, REFUSED 2, PASS 2 |  |
| `puncc/aps/rand=False` | - | REFUSED | 5 | REFUSED 1, PASS 4 |  |
| `puncc/aps/rand=True` | - | REFUSED | 5 | REFUSED 1, PASS 4 |  |
| `puncc/raps/rand=False` | - | REFUSED | 5 | REFUSED 1, PASS 4 |  |
| `puncc/raps/rand=True` | - | CONSERVATIVE | 5 | CONSERVATIVE 4, REFUSED 1 |  |
| `torchcp/aps/randomized=False` | - | PASS | 5 | PASS 5 |  |
| `torchcp/aps/randomized=True` | - | PASS | 5 | PASS 5 |  |
| `torchcp/raps/randomized=False` | - | PASS | 5 | PASS 5 |  |
| `torchcp/raps/randomized=True` | - | PASS | 5 | PASS 5 |  |
| `reference/aps/deterministic` | - | PASS | 5 | PASS 5 |  |
| `reference/aps/randomized` | - | PASS | 5 | PASS 5 |  |
| `reference/raps/deterministic` | - | PASS | 5 | PASS 5 |  |
| `reference/raps/randomized` | - | PASS | 5 | PASS 5 |  |

## Status grid (worst over dgps and alphas at each n)

P pass, C conservative, F fail, L law mismatch, O refused a feasible level, R refused with k > n, E error, . not run.

| row | 99 | 999 |
|---|---|---|
| `mapie/aps/include_last_label=False` | F | F |
| `mapie/aps/include_last_label=True` | C | C |
| `mapie/aps/include_last_label=randomized` | O | O |
| `mapie/raps/include_last_label=True` | C | C |
| `mapie/raps/include_last_label=randomized` | . | C |
| `puncc/aps/rand=False` | . | R |
| `puncc/aps/rand=True` | . | R |
| `puncc/raps/rand=False` | . | R |
| `puncc/raps/rand=True` | . | C |
| `torchcp/aps/randomized=False` | . | P |
| `torchcp/aps/randomized=True` | . | P |
| `torchcp/raps/randomized=False` | . | P |
| `torchcp/raps/randomized=True` | . | P |
| `reference/aps/deterministic` | . | P |
| `reference/aps/randomized` | . | P |
| `reference/raps/deterministic` | . | P |
| `reference/raps/randomized` | . | P |

## Non-PASS cells (libraries)

| row | dgp | n | alpha | k | status | coverage [95% CI] | target | rank offsets lower|upper or bracket (reps) | Holm p | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.2 | 80 | FAIL | 0.7424 [0.7416, 0.7432] | 0.8000 |  | 0 | Holm p=0, coverage 0.7424 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.1 | 90 | FAIL | 0.7958 [0.7946, 0.7970] | 0.9000 |  | 0 | Holm p=0, coverage 0.7958 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.05 | 95 | FAIL | 0.8517 [0.8502, 0.8532] | 0.9500 |  | 0 | Holm p=0, coverage 0.8517 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.2 | 800 | FAIL | 0.7400 [0.7394, 0.7407] | 0.8000 |  | 0 | Holm p=0, coverage 0.7400 vs 0.8000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.1 | 900 | FAIL | 0.7920 [0.7914, 0.7927] | 0.9000 |  | 0 | Holm p=0, coverage 0.7920 vs 0.9000 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.05 | 950 | FAIL | 0.8466 [0.8459, 0.8472] | 0.9500 |  | 0 | Holm p=0, coverage 0.8466 vs 0.9500 |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.9132 [0.9123, 0.9141] | 0.8000 |  | 0 | Holm p=0, coverage 0.9132 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9585 [0.9578, 0.9591] | 0.9000 |  | 0 | Holm p=0, coverage 0.9585 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.05 | 95 | CONSERVATIVE | 0.9812 [0.9808, 0.9817] | 0.9500 |  | 0 | Holm p=0, coverage 0.9812 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.9133 [0.9128, 0.9137] | 0.8000 |  | 0 | Holm p=0, coverage 0.9133 vs 0.8000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9588 [0.9584, 0.9591] | 0.9000 |  | 0 | Holm p=0, coverage 0.9588 vs 0.9000 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9813 [0.9811, 0.9816] | 0.9500 |  | 0 | Holm p=0, coverage 0.9813 vs 0.9500 |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.01 | 99 | OVER_REFUSED |  | 0.9900 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.001 | 999 | OVER_REFUSED |  | 0.9990 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.2 | 80 | CONSERVATIVE | 0.9183 [0.9174, 0.9192] | 0.8000 |  | 0 | Holm p=0, coverage 0.9183 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.1 | 90 | CONSERVATIVE | 0.9607 [0.9600, 0.9614] | 0.9000 |  | 0 | Holm p=0, coverage 0.9607 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.05 | 95 | OVER_REFUSED |  | 0.9556 |  |  | refused a feasible level (k <= n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.01 | 99 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 99 | 0.009 | 100 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.9170 [0.9165, 0.9175] | 0.8000 |  | 0 | Holm p=0, coverage 0.9170 vs 0.8000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9623 [0.9619, 0.9626] | 0.9000 |  | 0 | Holm p=0, coverage 0.9623 vs 0.9000 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9854 [0.9851, 0.9856] | 0.9500 |  | 0 | Holm p=0, coverage 0.9854 vs 0.9500 |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9514 [0.9510, 0.9519] | 0.9500 |  | 2.4e-36 | Holm p=2.4e-36, coverage 0.9514 vs 0.9500 |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.001 | 999 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Number of samples of the score is too low,
1/confidence_level and 1/ |
| `puncc/aps/rand=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/aps/rand=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=False` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.2 | 800 | CONSERVATIVE | 0.8274 [0.8267, 0.8282] | 0.8000 |  | 0 | Holm p=0, coverage 0.8274 vs 0.8000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.1 | 900 | CONSERVATIVE | 0.9202 [0.9197, 0.9207] | 0.9000 |  | 0 | Holm p=0, coverage 0.9202 vs 0.9000 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.05 | 950 | CONSERVATIVE | 0.9641 [0.9637, 0.9645] | 0.9500 |  | 0 | Holm p=0, coverage 0.9641 vs 0.9500 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.001 | 999 | CONSERVATIVE | 0.9998 [0.9998, 0.9998] | 0.9990 |  | 2.1e-205 | Holm p=2.1e-205, coverage 0.9998 vs 0.9990 |
| `puncc/raps/rand=True` | cls_gauss_inf | 999 | 0.0009 | 1000 | REFUSED |  | 1.0000 |  |  | refused (k > n) ValueError: Alpha is too small: (alpha=0.0009, n=999) 0.0009 < 0.001 for at leas |
