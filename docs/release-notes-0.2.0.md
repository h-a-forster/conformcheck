# conformcheck 0.2.0

Released 2026-10-30. Install from git (conformcheck is not on PyPI):

```sh
uv pip install "conformcheck @ git+https://github.com/h-a-forster/conformcheck@v0.2.0"
```

## Highlights

- **RAPS rows** for MAPIE, puncc and TorchCP (37 library-method rows, up from 31), with
  reference implementations. MAPIE RAPS is tested at the calibration size it actually
  uses.
- **Bracketing as rank recovery for classification**: LAC and class-conditional LAC get
  a deterministic order-statistic check, so one-step errors are caught at any `n`.
- **An informative classifier** (`cls_gauss_inf`, the Bayes posterior) next to the
  anti-informative `cls_gauss`, so model-dependent effects can be told apart from the
  laws.

## Results (default study, round 2)

MAPIE 1.6.0, crepes 0.9.1, puncc 0.9.3, TorchCP 1.2.1; R = 200 draws × 500 test points,
4348 statistical cells, Holm FWER 0.05.

- 18 of the 37 library-method rows are flagged at n <= 100.
- Reference rows: 0 Holm rejections in 1010 statistical cells, 0 non-PASS cells.
- New findings: F9 (MAPIE ignores `RAPSConformityScore(size_raps=...)`) and F10 (puncc
  randomized RAPS set rule does not match its score). Also F11 (puncc APS and RAPS sets
  capped at the number of test points per call; found in code review, outside the study
  grid), which was already reported upstream in
  [puncc#97](https://github.com/deel-ai/puncc/pull/97). F1 (MAPIE APS `include_last_label=False`) now also under-covers with the
  informative classifier.
- MAPIE 1.5.0 vs 1.6.0: under 1.5.0 all 13 MAPIE rows are flagged at n <= 100 (9 under
  1.6.0). 1.5.0 returns finite intervals where `k > n` (CV+, jackknife+, split with
  `allow_infinite_bounds=True`; coverage down to 0.828 against 1) and uses one order
  statistic too many for LAC, CQR and randomized APS and RAPS (87 cells). The 1.6.0
  run reproduced the round-2 records exactly.

Details: [REPORT.md](../REPORT.md). Issue texts for F1, F9 and F10, re-checked on
2026-10-30 against MAPIE 1.6.0 and puncc 0.9.3 (still the latest releases), are in
[docs/upstream](upstream/README.md); none has been filed. For F11 that folder has a
supporting comment for puncc#97 instead.

## Fixes

- `report` and `repro` use only the records of the study in `run.json`, and records
  computed under other library versions are re-run rather than relabelled.
- `diagnostics.bracket_rank` returned a lower end one too low.
- Coverage intervals use the empirical spread of the counts and are clipped to [0, 1].
- Study files are validated on load; `run` refuses to start without the libraries it
  needs unless `--allow-missing` is given.

The full list is in [CHANGELOG.md](../CHANGELOG.md).

## Compatibility

- `check_split_regressor` has a new `score` argument (`"auto"` by default), and
  `check_split_classifier` accepts `score="lac"`.
- Run directories made by 0.1.0 can still be reported; records without stored versions
  take the versions in their `run.json`.
- 0.1.0 is described in the changelog but was never tagged.
