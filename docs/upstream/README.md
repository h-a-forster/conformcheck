# Upstream issue texts

Drafts of bug reports for the libraries under test, one file per issue, ready to paste
into each project's bug-report template. **None has been filed.** F11 is already
reported upstream (puncc pull request #97), so its file is a supporting comment for that
pull request, not a new issue. Each was re-checked
on 2026-10-30 (F12: 2026-11-06) against the latest release (MAPIE 1.6.0, puncc 0.9.3)
with the repro named in it. On 2026-11-06 those were still the latest releases and #97
was still open.

| File | Library | REPORT.md | Status |
|---|---|---|---|
| [mapie-aps-include-last-label-false.md](mapie-aps-include-last-label-false.md) | MAPIE 1.6.0 (also 1.5.0) | F1 | not filed |
| [mapie-raps-size-raps-ignored.md](mapie-raps-size-raps-ignored.md) | MAPIE 1.6.0 (also 1.5.0) | F9 | not filed |
| [puncc-randomized-raps-set-rule.md](puncc-randomized-raps-set-rule.md) | puncc 0.9.3 | F10 | not filed |
| [puncc-aps-raps-set-size-capped.md](puncc-aps-raps-set-size-capped.md) | puncc 0.9.3 | F11 | do not file: already in [deel-ai/puncc#97](https://github.com/deel-ai/puncc/pull/97) (open); optional comment |
| [puncc-cqr-single-test-point.md](puncc-cqr-single-test-point.md) | puncc 0.9.3 | F12 (candidate) | not filed |

Findings F2 to F8 have repros in [docs/results/default/repros](../results/default/repros)
but no issue text yet.

Before filing:

- Search the project's open and closed issues and pull requests again (searched on
  2026-10-30: MAPIE #236 is related to F1 and is cited in that draft; puncc pull request
  #97, opened 2026-10-07 by another contributor, reports F11 with the same fix; nothing
  on F9 or F10; nothing on F12 on 2026-11-06).
- Re-run the repro against the project's current release and default branch, and
  update the version lines and output.
- MAPIE's contributing guide asks that LLM-assisted issues and pull requests be reviewed
  by the author before publishing and that LLM use be stated in pull requests.
