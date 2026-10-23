# MAPIE RAPS: which calibration size does the coverage follow?

Row `mapie/raps/include_last_label=randomized`, cells where MAPIE returned sets in every repetition. Each column tests the covered counts against the exact split law (mean and goodness-of-fit, Bonferroni within the cell) at a candidate calibration size; Holm at 0.05 within each column. Entry: exact coverage / Holm p (**rejected** in bold).

| dgp | n | alpha | n used (adapter) | observed | nominal n | n - ceil(0.1 n) | n - ceil(0.2 n) |
|---|---|---|---|---|---|---|---|
| cls_gauss | 49 | 0.2 | 44 | 0.7944 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss | 50 | 0.2 | 45 | 0.8059 | 0.8039 / 1 | 0.8043 / 1 | 0.8049 / 1 |
| cls_gauss | 99 | 0.2 | 89 | 0.8066 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss | 99 | 0.1 | 89 | 0.8998 | 0.9000 / 1 | 0.9000 / 1 | 0.9000 / 1 |
| cls_gauss | 100 | 0.2 | 90 | 0.8037 | 0.8020 / 1 | 0.8022 / 1 | 0.8025 / 1 |
| cls_gauss | 100 | 0.1 | 90 | 0.9028 | 0.9010 / 1 | 0.9011 / 1 | 0.9012 / 1 |
| cls_gauss | 999 | 0.2 | 899 | 0.8022 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss | 999 | 0.1 | 899 | 0.9018 | 0.9000 / 1 | 0.9000 / 1 | 0.9000 / 1 |
| cls_gauss | 999 | 0.05 | 899 | 0.9514 | 0.9500 / 1 | 0.9500 / 1 | 0.9500 / 1 |
| cls_gauss | 1000 | 0.2 | 900 | 0.7995 | 0.8002 / 1 | 0.8002 / 1 | 0.8002 / 1 |
| cls_gauss | 1000 | 0.1 | 900 | 0.9009 | 0.9001 / 1 | 0.9001 / 1 | 0.9001 / 1 |
| cls_gauss | 1000 | 0.05 | 900 | 0.9494 | 0.9500 / 1 | 0.9501 / 1 | 0.9501 / 0.96 |
| cls_gauss_inf | 49 | 0.2 | 44 | 0.8009 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss_inf | 50 | 0.2 | 45 | 0.8047 | 0.8039 / 1 | 0.8043 / 1 | 0.8049 / 1 |
| cls_gauss_inf | 99 | 0.2 | 89 | 0.8007 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss_inf | 99 | 0.1 | 89 | 0.9011 | 0.9000 / 1 | 0.9000 / 0.7 | 0.9000 / 1 |
| cls_gauss_inf | 100 | 0.2 | 90 | 0.8083 | 0.8020 / 1 | 0.8022 / 1 | 0.8025 / 1 |
| cls_gauss_inf | 100 | 0.1 | 90 | 0.9008 | 0.9010 / 1 | 0.9011 / 1 | 0.9012 / 1 |
| cls_gauss_inf | 999 | 0.2 | 899 | 0.8015 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| cls_gauss_inf | 999 | 0.1 | 899 | 0.9003 | 0.9000 / 1 | 0.9000 / 1 | 0.9000 / 1 |
| cls_gauss_inf | 999 | 0.05 | 899 | 0.9514 | 0.9500 / 1 | 0.9500 / 1 | 0.9500 / 1 |
| cls_gauss_inf | 1000 | 0.2 | 900 | 0.8002 | 0.8002 / 1 | 0.8002 / 1 | 0.8002 / 1 |
| cls_gauss_inf | 1000 | 0.1 | 900 | 0.9005 | 0.9001 / 1 | 0.9001 / 1 | 0.9001 / 1 |
| cls_gauss_inf | 1000 | 0.05 | 900 | 0.9509 | 0.9500 / 1 | 0.9501 / 1 | 0.9501 / 1 |
| digits | 99 | 0.2 | 89 | 0.7995 | 0.8000 / 1 | 0.8000 / 1 | 0.8000 / 1 |
| digits | 99 | 0.1 | 89 | 0.8985 | 0.9000 / 1 | 0.9000 / 1 | 0.9000 / 0.53 |

Holm rejections per candidate: nominal n: 0 of 26, n - ceil(0.1 n): 0 of 26, n - ceil(0.2 n): 0 of 26
