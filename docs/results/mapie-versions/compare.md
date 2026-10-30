# runs/mapie-versions-default/1.5.0 vs runs/mapie-versions-default/1.6.0 (mapie)

## Units

- shared unit ids: 324; raw results identical: 163; different: 161
- only in before: 0; only in after: 0

## Status counts per row (before -> after)

| Row | ERROR | FAIL | LAW_MISMATCH | CONSERVATIVE | OVER_REFUSED | REFUSED | PASS | changed cells |
|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | 23 | 47 -> 48 | 1 -> 0 | 8 | 17 | 18 | 0 | 1 |
| `mapie/aps/include_last_label=True` | 23 | 0 | 0 | 56 | 17 | 18 | 0 | 0 |
| `mapie/aps/include_last_label=randomized` | 23 | 0 | 0 | 14 -> 0 | 17 | 18 | 42 -> 56 | 14 |
| `mapie/cqr/asymmetric` | 0 | 0 | 0 | 17 -> 0 | 5 | 59 | 33 -> 50 | 17 |
| `mapie/cqr/symmetric` | 0 | 0 | 0 | 26 -> 0 | 22 | 30 | 36 -> 62 | 26 |
| `mapie/cv_plus/K=10` | 0 | 8 -> 0 | 0 | 1 | 0 | 0 | 69 -> 77 | 8 |
| `mapie/cv_plus/K=5` | 0 | 8 -> 0 | 0 | 1 | 0 | 0 | 69 -> 77 | 8 |
| `mapie/jackknife_plus/default` | 0 | 9 -> 0 | 0 | 0 | 0 | 0 | 57 -> 66 | 9 |
| `mapie/lac/default` | 0 | 0 | 0 | 26 -> 0 | 22 | 30 | 36 -> 62 | 26 |
| `mapie/raps/include_last_label=True` | 52 | 0 | 0 | 26 | 12 | 24 | 0 | 0 |
| `mapie/raps/include_last_label=randomized` | 52 | 0 | 0 | 4 -> 0 | 12 | 24 | 22 -> 26 | 4 |
| `mapie/split_abs/allow_infinite_bounds` | 0 | 43 -> 0 | 0 | 0 | 0 | 0 -> 43 | 114 | 43 |
| `mapie/split_abs/default` | 0 | 0 | 0 | 0 | 31 | 43 | 83 | 0 |

## Cells whose status changed

| Row | dgp | n | K | alpha | status | coverage | target | rank offsets | reason |
|---|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | cls_gauss_inf | 19 | - | 1/5 | LAW_MISMATCH -> FAIL | 0.7742 -> 0.7498 | 0.8000 | {} -> {} | Holm p=1.3e-62, coverage 0.7498 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9440 -> 0.8881 | 0.9000 | {} -> {} | Holm p=3.4e-49, coverage 0.9440 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8389 -> 0.7874 | 0.8000 | {} -> {} | Holm p=3.4e-07, coverage 0.8389 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9173 -> 0.8964 | 0.9000 | {} -> {} | Holm p=2.2e-05, coverage 0.9173 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9130 -> 0.9028 | 0.9000 | {} -> {} | Holm p=2.4e-05, coverage 0.9130 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9618 -> 0.9508 | 0.9500 | {} -> {} | Holm p=2e-10, coverage 0.9618 vs 0.9500 |
| `mapie/aps/include_last_label=randomized` | cls_gauss | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8153 -> 0.8065 | 0.8000 | {} -> {} | Holm p=0.0018, coverage 0.8153 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9503 -> 0.8997 | 0.9000 | {} -> {} | Holm p=2.7e-40, coverage 0.9503 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8530 -> 0.8031 | 0.8000 | {} -> {} | Holm p=2.1e-12, coverage 0.8530 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9187 -> 0.9011 | 0.9000 | {} -> {} | Holm p=8.3e-07, coverage 0.9187 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8227 -> 0.8025 | 0.8000 | {} -> {} | Holm p=7.8e-05, coverage 0.8227 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | cls_gauss_inf | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9588 -> 0.9491 | 0.9500 | {} -> {} | Holm p=0.00013, coverage 0.9588 vs 0.9500 |
| `mapie/aps/include_last_label=randomized` | digits | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9590 -> 0.9005 | 0.9000 | {} -> {} | Holm p=8.6e-85, coverage 0.9590 vs 0.9000 |
| `mapie/aps/include_last_label=randomized` | digits | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8506 -> 0.8053 | 0.8000 | {} -> {} | Holm p=2.3e-12, coverage 0.8506 vs 0.8000 |
| `mapie/aps/include_last_label=randomized` | digits | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9107 -> 0.9005 | 0.9000 | {} -> {} | Holm p=0.0079, coverage 0.9107 vs 0.9000 |
| `mapie/cqr/asymmetric` | diabetes | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.9093 -> 0.8059 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | diabetes | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9218 -> 0.9018 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | diabetes | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8201 -> 0.8010 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.9034 -> 0.7981 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8383 -> 0.7977 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9224 -> 0.9014 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8167 -> 0.7972 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.9051 -> 0.9031 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9536 -> 0.9517 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_gauss | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.8039 -> 0.8019 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8966 -> 0.8005 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8350 -> 0.7951 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9167 -> 0.8975 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8180 -> 0.7971 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.9022 -> 0.9002 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9521 -> 0.9502 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/asymmetric` | reg_hetero_t | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.8017 -> 0.7996 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | diabetes | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9532 -> 0.9043 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | diabetes | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8527 -> 0.8018 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | diabetes | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9094 -> 0.9006 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | diabetes | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8107 -> 0.8026 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9512 -> 0.9064 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8553 -> 0.8044 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9166 -> 0.8975 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8186 -> 0.7981 | 0.8000 | {"0": 1, "1": 199} -> {"0": 200} | rank +1 in 199 reps |
| `mapie/cqr/symmetric` | reg_gauss | 9 | - | 1/5 | CONSERVATIVE -> PASS | 0.8969 -> 0.8097 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9102 -> 0.9013 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9615 -> 0.9517 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8074 -> 0.7972 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.9040 -> 0.9030 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9530 -> 0.9521 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_gauss | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.8030 -> 0.8018 | 0.8000 | {"0": 1, "1": 199} -> {"0": 200} | rank +1 in 199 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9481 -> 0.8967 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8495 -> 0.7965 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9185 -> 0.8974 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8177 -> 0.7974 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 9 | - | 1/5 | CONSERVATIVE -> PASS | 0.8874 -> 0.7654 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9079 -> 0.8976 | 0.9000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9603 -> 0.9497 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8062 -> 0.7982 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.9015 -> 0.9005 | 0.9000 | {"0": 1, "1": 199} -> {"0": 200} | rank +1 in 199 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9510 -> 0.9499 | 0.9500 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cqr/symmetric` | reg_hetero_t | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.8011 -> 0.8000 | 0.8000 | {"1": 200} -> {"0": 200} | rank +1 in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 100 | 10 | 9/1010 | FAIL -> PASS | 0.9887 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 1000 | 10 | 9/10010 | FAIL -> PASS | 0.9989 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 19 | 10 | 9/200 | FAIL -> PASS | 0.9525 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 20 | 10 | 3/70 | FAIL -> PASS | 0.9560 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 49 | 10 | 9/500 | FAIL -> PASS | 0.9788 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 50 | 10 | 3/170 | FAIL -> PASS | 0.9794 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 99 | 10 | 9/1000 | FAIL -> PASS | 0.9903 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=10` | reg_constant | 999 | 10 | 9/10000 | FAIL -> PASS | 0.9988 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 100 | 5 | 9/1010 | FAIL -> PASS | 0.9887 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 1000 | 5 | 9/10010 | FAIL -> PASS | 0.9989 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 19 | 5 | 9/200 | FAIL -> PASS | 0.9525 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 20 | 5 | 3/70 | FAIL -> PASS | 0.9560 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 49 | 5 | 9/500 | FAIL -> PASS | 0.9788 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 50 | 5 | 3/170 | FAIL -> PASS | 0.9794 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 99 | 5 | 9/1000 | FAIL -> PASS | 0.9903 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/cv_plus/K=5` | reg_constant | 999 | 5 | 9/10000 | FAIL -> PASS | 0.9988 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 10 | - | 1/20 | FAIL -> PASS | 0.9049 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 10 | - | 9/110 | FAIL -> PASS | 0.9049 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 19 | - | 9/200 | FAIL -> PASS | 0.9525 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 20 | - | 3/70 | FAIL -> PASS | 0.9560 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 49 | - | 9/500 | FAIL -> PASS | 0.9788 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 50 | - | 3/170 | FAIL -> PASS | 0.9794 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 9 | - | 1/20 | FAIL -> PASS | 0.9021 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 9 | - | 9/100 | FAIL -> PASS | 0.9021 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/jackknife_plus/default` | reg_constant | 99 | - | 9/1000 | FAIL -> PASS | 0.9903 -> 1.0000 | 1.0000 | {"-1": 200} -> {"0": 200} | finite set when k > n in 200 reps |
| `mapie/lac/default` | cls_gauss | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9466 -> 0.8953 | 0.9000 | {} -> {} | bracket +1 in 195 reps |
| `mapie/lac/default` | cls_gauss | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8431 -> 0.7894 | 0.8000 | {} -> {} | bracket +1 in 197 reps |
| `mapie/lac/default` | cls_gauss | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9183 -> 0.8978 | 0.9000 | {} -> {} | bracket +1 in 195 reps |
| `mapie/lac/default` | cls_gauss | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8168 -> 0.7941 | 0.8000 | {} -> {} | bracket +1 in 197 reps |
| `mapie/lac/default` | cls_gauss | 9 | - | 1/5 | CONSERVATIVE -> PASS | 0.8942 -> 0.7894 | 0.8000 | {} -> {} | bracket +1 in 200 reps |
| `mapie/lac/default` | cls_gauss | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9131 -> 0.9044 | 0.9000 | {} -> {} | bracket +1 in 185 reps |
| `mapie/lac/default` | cls_gauss | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9613 -> 0.9507 | 0.9500 | {} -> {} | bracket +1 in 183 reps |
| `mapie/lac/default` | cls_gauss | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8126 -> 0.8030 | 0.8000 | {} -> {} | bracket +1 in 183 reps |
| `mapie/lac/default` | cls_gauss | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.8996 -> 0.8985 | 0.9000 | {} -> {} | bracket +1 in 94 reps |
| `mapie/lac/default` | cls_gauss | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9510 -> 0.9499 | 0.9500 | {} -> {} | bracket +1 in 109 reps |
| `mapie/lac/default` | cls_gauss | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.8009 -> 0.8000 | 0.8000 | {} -> {} | bracket +1 in 103 reps |
| `mapie/lac/default` | cls_gauss_inf | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9514 -> 0.8982 | 0.9000 | {} -> {} | bracket +1 in 199 reps |
| `mapie/lac/default` | cls_gauss_inf | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8503 -> 0.8016 | 0.8000 | {} -> {} | bracket +1 in 199 reps |
| `mapie/lac/default` | cls_gauss_inf | 49 | - | 1/10 | CONSERVATIVE -> PASS | 0.9207 -> 0.9013 | 0.9000 | {} -> {} | bracket +1 in 199 reps |
| `mapie/lac/default` | cls_gauss_inf | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8197 -> 0.7980 | 0.8000 | {} -> {} | bracket +1 in 194 reps |
| `mapie/lac/default` | cls_gauss_inf | 9 | - | 1/5 | CONSERVATIVE -> PASS | 0.9051 -> 0.8049 | 0.8000 | {} -> {} | bracket +1 in 200 reps |
| `mapie/lac/default` | cls_gauss_inf | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9075 -> 0.8978 | 0.9000 | {} -> {} | bracket +1 in 196 reps |
| `mapie/lac/default` | cls_gauss_inf | 99 | - | 1/20 | CONSERVATIVE -> PASS | 0.9594 -> 0.9482 | 0.9500 | {} -> {} | bracket +1 in 196 reps |
| `mapie/lac/default` | cls_gauss_inf | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8086 -> 0.7992 | 0.8000 | {} -> {} | bracket +1 in 191 reps |
| `mapie/lac/default` | cls_gauss_inf | 999 | - | 1/10 | CONSERVATIVE -> PASS | 0.9020 -> 0.9010 | 0.9000 | {} -> {} | bracket +1 in 147 reps |
| `mapie/lac/default` | cls_gauss_inf | 999 | - | 1/20 | CONSERVATIVE -> PASS | 0.9514 -> 0.9505 | 0.9500 | {} -> {} | bracket +1 in 171 reps |
| `mapie/lac/default` | cls_gauss_inf | 999 | - | 1/5 | CONSERVATIVE -> PASS | 0.7998 -> 0.7988 | 0.8000 | {} -> {} | bracket +1 in 125 reps |
| `mapie/lac/default` | digits | 19 | - | 1/10 | CONSERVATIVE -> PASS | 0.9476 -> 0.8990 | 0.9000 | {} -> {} | bracket +1 in 199 reps |
| `mapie/lac/default` | digits | 19 | - | 1/5 | CONSERVATIVE -> PASS | 0.8435 -> 0.7990 | 0.8000 | {} -> {} | bracket +1 in 189 reps |
| `mapie/lac/default` | digits | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9060 -> 0.8948 | 0.9000 | {} -> {} | bracket +1 in 182 reps |
| `mapie/lac/default` | digits | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8043 -> 0.7940 | 0.8000 | {} -> {} | bracket +1 in 168 reps |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9115 -> 0.8998 | 0.9000 | {} -> {} | Holm p=0.0035, coverage 0.9115 vs 0.9000 |
| `mapie/raps/include_last_label=randomized` | cls_gauss | 99 | - | 1/5 | CONSERVATIVE -> PASS | 0.8176 -> 0.8066 | 0.8000 | {} -> {} | Holm p=0.0001, coverage 0.8176 vs 0.8000 |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 49 | - | 1/5 | CONSERVATIVE -> PASS | 0.8243 -> 0.8009 | 0.8000 | {} -> {} | Holm p=3.8e-05, coverage 0.8243 vs 0.8000 |
| `mapie/raps/include_last_label=randomized` | cls_gauss_inf | 99 | - | 1/10 | CONSERVATIVE -> PASS | 0.9130 -> 0.9011 | 0.9000 | {} -> {} | Holm p=0.0001, coverage 0.9130 vs 0.9000 |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 10 | - | 1/20 | FAIL -> REFUSED | 0.9068 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 10 | - | 9/110 | FAIL -> REFUSED | 0.9068 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 100 | - | 9/1010 | FAIL -> REFUSED | 0.9899 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 1000 | - | 9/10010 | FAIL -> REFUSED | 0.9988 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 19 | - | 9/200 | FAIL -> REFUSED | 0.9493 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 20 | - | 3/70 | FAIL -> REFUSED | 0.9512 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 49 | - | 9/500 | FAIL -> REFUSED | 0.9788 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | - | 1/10 | FAIL -> REFUSED | 0.8280 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | - | 1/20 | FAIL -> REFUSED | 0.8280 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 5 | - | 3/20 | FAIL -> REFUSED | 0.8280 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 50 | - | 3/170 | FAIL -> REFUSED | 0.9812 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 9 | - | 1/20 | FAIL -> REFUSED | 0.9006 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 9 | - | 9/100 | FAIL -> REFUSED | 0.9006 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 99 | - | 9/1000 | FAIL -> REFUSED | 0.9908 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_gauss | 999 | - | 9/10000 | FAIL -> REFUSED | 0.9990 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 10 | - | 1/20 | FAIL -> REFUSED | 0.9012 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 10 | - | 9/110 | FAIL -> REFUSED | 0.9012 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 100 | - | 9/1010 | FAIL -> REFUSED | 0.9915 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 1000 | - | 9/10010 | FAIL -> REFUSED | 0.9991 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 19 | - | 9/200 | FAIL -> REFUSED | 0.9481 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 20 | - | 3/70 | FAIL -> REFUSED | 0.9547 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 49 | - | 9/500 | FAIL -> REFUSED | 0.9800 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | - | 1/10 | FAIL -> REFUSED | 0.8379 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | - | 1/20 | FAIL -> REFUSED | 0.8379 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 5 | - | 3/20 | FAIL -> REFUSED | 0.8379 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 50 | - | 3/170 | FAIL -> REFUSED | 0.9805 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 9 | - | 1/20 | FAIL -> REFUSED | 0.8860 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 9 | - | 9/100 | FAIL -> REFUSED | 0.8860 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 99 | - | 9/1000 | FAIL -> REFUSED | 0.9908 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_hetero_t | 999 | - | 9/10000 | FAIL -> REFUSED | 0.9990 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 10 | - | 1/20 | FAIL -> REFUSED | 0.9939 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 10 | - | 9/110 | FAIL -> REFUSED | 0.9939 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 100 | - | 9/1010 | FAIL -> REFUSED | 1.0000 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 19 | - | 9/200 | FAIL -> REFUSED | 1.0000 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 20 | - | 3/70 | FAIL -> REFUSED | 0.9971 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 49 | - | 9/500 | FAIL -> REFUSED | 1.0000 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | - | 1/10 | FAIL -> REFUSED | 0.9305 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | - | 1/20 | FAIL -> REFUSED | 0.9305 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 5 | - | 3/20 | FAIL -> REFUSED | 0.9305 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 50 | - | 3/170 | FAIL -> REFUSED | 1.0000 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 9 | - | 1/20 | FAIL -> REFUSED | 0.9927 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 9 | - | 9/100 | FAIL -> REFUSED | 0.9927 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
| `mapie/split_abs/allow_infinite_bounds` | reg_tied | 99 | - | 9/1000 | FAIL -> REFUSED | 1.0000 -> - | 1.0000 | {"-1": 200} -> {} | refused (k > n) |
