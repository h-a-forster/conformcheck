# Upstream reports

Issues filed from conformcheck's findings, with their state read from GitHub on
2026-11-13. The issue texts are in [upstream/](upstream/README.md).

| Project | Issue | Finding | Filed | State on 2026-11-13 | Outcome |
|---|---|---|---|---|---|
| MAPIE | [#1020](https://github.com/scikit-learn-contrib/MAPIE/issues/1020) | F9: RAPS ignores `size_raps` | 2026-11-07 | open | Another contributor opened fix PR [#1022](https://github.com/scikit-learn-contrib/MAPIE/pull/1022) (open, not merged); not in a release (latest 1.6.0) |
| MAPIE | [#1021](https://github.com/scikit-learn-contrib/MAPIE/issues/1021) | F1: APS `include_last_label=False` under-covers | 2026-11-07 | open | No reply |
| puncc | [#100](https://github.com/deel-ai/puncc/issues/100) | F12: CQR raises for one test point | 2026-11-07 | open | No reply |
| puncc | [#101](https://github.com/deel-ai/puncc/issues/101) | F10: randomized RAPS set rule does not match its score | 2026-11-07 | open | No reply |
| statsforecast | [#1349](https://github.com/Nixtla/statsforecast/issues/1349) | Tutorial and default `n_windows=2` can cover at most 2/3 ([2026-11-09 study](results/newlib-2026-11-09/README.md)) | 2026-11-09 | closed 2026-11-12 | Closed by a maintainer without a change: `n_windows=2` stays the default as the setting least likely to get in users' way, and users should check coverage for their own setup |

Not filed:

- F11 (puncc APS and RAPS sets capped at the batch size) was already reported in puncc
  pull request [#97](https://github.com/deel-ai/puncc/pull/97) by another contributor. On
  2026-11-04 a maintainer replied that the fix is folded into the puncc v1.0 refactoring;
  #97 is still open and the latest release is 0.9.3.
- F2 to F8 have repros but no issue text.
- sktime and darts (2026-11-09 study): the sktime defects were already open (#10757,
  #10758, #10766), and darts chose its k > n behaviour in PR #3227.
