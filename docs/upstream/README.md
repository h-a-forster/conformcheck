# Upstream issue texts

Drafts of bug reports for the libraries under test, one file per issue, ready to paste
into each project's bug-report template. **None has been filed.** Each was re-checked
on 2026-10-30 against the latest release (MAPIE 1.6.0, puncc 0.9.3) with the repro
named in it.

| File | Library | REPORT.md | Status |
|---|---|---|---|
| [mapie-aps-include-last-label-false.md](mapie-aps-include-last-label-false.md) | MAPIE 1.6.0 (also 1.5.0) | F1 | not filed |
| [mapie-raps-size-raps-ignored.md](mapie-raps-size-raps-ignored.md) | MAPIE 1.6.0 (also 1.5.0) | F9 | not filed |
| [puncc-randomized-raps-set-rule.md](puncc-randomized-raps-set-rule.md) | puncc 0.9.3 | F10 | not filed |
| [puncc-aps-raps-set-size-capped.md](puncc-aps-raps-set-size-capped.md) | puncc 0.9.3 | F11 | not filed |

Findings F2 to F8 have repros in [docs/results/default/repros](../results/default/repros)
but no issue text yet.

Before filing:

- Search the project's open and closed issues again (searched on 2026-10-30: MAPIE
  #236 is related to F1 and is cited in that draft; nothing on F9, F10 or F11).
- Re-run the repro against the project's current release and default branch, and
  update the version lines and output.
- MAPIE's contributing guide asks that LLM-assisted issues and pull requests be reviewed
  by the author before publishing and that LLM use be stated in pull requests.
