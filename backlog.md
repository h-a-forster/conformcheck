# Backlog

## In progress

## Waiting on me

- `polish-2026-10-30` is merged through a PR with a merge commit, after the first CI run ever is green.
- `v0.2.0` is tagged, with the CHANGELOG's `[Unreleased]` block folded into `[0.2.0]` and its date set to the tag date.
- GitHub private vulnerability reporting is on, as `SECURITY.md` promises (it is off).
- F1, F9, F10 and F12 are filed upstream or dropped, and puncc#97 has its supporting comment or not (`docs/upstream/`).
- Decided whether the 14 `Co-Authored-By` trailers on `polish-2026-10-30` stay (a rewrite must happen before the merge; `main` has 15 more).

## Decided

- 2026-10-30: the release is 0.2.0, since 0.1.0 was dated but never tagged.
- 2026-10-30: F11 is not filed as a new issue; it is already in puncc#97.

## Proposed

- The batch-size check has run on the default grid (other DGPs, n, toy data).
- `testing.check_*` offers the batch-size check to library authors.
- The `full` study (R = 2000, m = 1000) has run, so APS and RAPS have more power at large n.
- ACI and EnbPI (time series) are covered.
- puncc PASS cells are re-checked under `numpy<2`, not only its findings.
- CV+ `lower` cells with K not dividing n use a proven bound, not the labelled extrapolation.
- Issue texts exist for F2-F8.
- `holm` in `stats.py` leaves NaN as NaN and out of m, as in lpbench and certkkt, in the release after 0.2.0.
