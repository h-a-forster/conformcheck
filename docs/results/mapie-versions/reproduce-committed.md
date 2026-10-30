# docs/results/default vs runs/mapie-versions-default/1.6.0 (mapie)

## Units

- shared unit ids: 324; raw results identical: 324; different: 0
- only in before: 0; only in after: 0

## Status counts per row (before -> after)

| Row | ERROR | FAIL | LAW_MISMATCH | CONSERVATIVE | OVER_REFUSED | REFUSED | PASS | changed cells |
|---|---|---|---|---|---|---|---|---|
| `mapie/aps/include_last_label=False` | 23 | 48 | 0 | 8 | 17 | 18 | 0 | 0 |
| `mapie/aps/include_last_label=True` | 23 | 0 | 0 | 56 | 17 | 18 | 0 | 0 |
| `mapie/aps/include_last_label=randomized` | 23 | 0 | 0 | 0 | 17 | 18 | 56 | 0 |
| `mapie/cqr/asymmetric` | 0 | 0 | 0 | 0 | 5 | 59 | 50 | 0 |
| `mapie/cqr/symmetric` | 0 | 0 | 0 | 0 | 22 | 30 | 62 | 0 |
| `mapie/cv_plus/K=10` | 0 | 0 | 0 | 1 | 0 | 0 | 77 | 0 |
| `mapie/cv_plus/K=5` | 0 | 0 | 0 | 1 | 0 | 0 | 77 | 0 |
| `mapie/jackknife_plus/default` | 0 | 0 | 0 | 0 | 0 | 0 | 66 | 0 |
| `mapie/lac/default` | 0 | 0 | 0 | 0 | 22 | 30 | 62 | 0 |
| `mapie/raps/include_last_label=True` | 52 | 0 | 0 | 26 | 12 | 24 | 0 | 0 |
| `mapie/raps/include_last_label=randomized` | 52 | 0 | 0 | 0 | 12 | 24 | 26 | 0 |
| `mapie/split_abs/allow_infinite_bounds` | 0 | 0 | 0 | 0 | 0 | 43 | 114 | 0 |
| `mapie/split_abs/default` | 0 | 0 | 0 | 0 | 31 | 43 | 83 | 0 |

## Cells whose status changed

| Row | dgp | n | K | alpha | status | coverage | target | rank offsets | reason |
|---|---|---|---|---|---|---|---|---|---|
| (none) | | | | | | | | | |
