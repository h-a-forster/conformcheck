# Upstream reports

Issues filed from conformcheck's findings, with their state read from GitHub on
2026-11-21 (statsforecast: 2026-11-13). The issue texts are in [upstream/](upstream/README.md).

| Project | Issue | Finding | Filed | State on 2026-11-21 | Outcome |
|---|---|---|---|---|---|
| MAPIE | [#1020](https://github.com/scikit-learn-contrib/MAPIE/issues/1020) | F9: RAPS ignores `size_raps` | 2026-11-07 | open | Another contributor opened fix PR [#1022](https://github.com/scikit-learn-contrib/MAPIE/pull/1022) (open, not merged on 2026-11-21); not in a release (latest 1.6.0) |
| MAPIE | [#1021](https://github.com/scikit-learn-contrib/MAPIE/issues/1021) | F1: APS `include_last_label=False` under-covers | 2026-11-07 | open | Another contributor opened fix PR [#1024](https://github.com/scikit-learn-contrib/MAPIE/pull/1024) on 2026-11-11 ("Fixes #1021": calibrate with non-randomized scores; open, not merged); not in a release (latest 1.6.0) |
| puncc | [#100](https://github.com/deel-ai/puncc/issues/100) | F12: CQR raises for one test point | 2026-11-07 | open | Listed as "resolves #100" in puncc's draft v1.0 refactoring PR [#98](https://github.com/deel-ai/puncc/pull/98) (open); not in a release (latest 0.9.3) |
| puncc | [#101](https://github.com/deel-ai/puncc/issues/101) | F10: randomized RAPS set rule does not match its score | 2026-11-07 | open | Listed as "resolves #101" in the same draft PR [#98](https://github.com/deel-ai/puncc/pull/98) (open); not in a release |
| statsforecast | [#1349](https://github.com/Nixtla/statsforecast/issues/1349) | Tutorial and default `n_windows=2` can cover at most 2/3 ([2026-11-09 study](results/newlib-2026-11-09/README.md)) | 2026-11-09 | closed 2026-11-12 | Closed by a maintainer without a change: `n_windows=2` stays the default as the setting least likely to get in users' way, and users should check coverage for their own setup |

Not filed:

- F11 (puncc APS and RAPS sets capped at the batch size) was already reported in puncc
  pull request [#97](https://github.com/deel-ai/puncc/pull/97) by another contributor. On
  2026-11-04 a maintainer replied that the fix is folded into the puncc v1.0 refactoring;
  #97 is still open on 2026-11-21 and the latest release is 0.9.3.
- Candidate (2026-11-21, not filed, no repro yet): MAPIE randomized RAPS over-covers at
  n = 999, alpha = 0.05 in the full-size APS/RAPS run (0.9514 vs 0.95; REPORT section 7).
- F2 to F8 (crepes F2, F3; MAPIE F4, F5, F7; puncc F6; TorchCP F8) have repros but no
  issue text.
- sktime and darts (2026-11-09 study): the sktime defects were already open (#10757,
  #10758, #10766), and darts chose its k > n behaviour in PR #3227.
