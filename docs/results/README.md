# Results

Committed outputs of study runs. Only small derived files are kept here; the raw run
directories (`runs/`) are gitignored.

## default/

The `default` study run of 2026-10-23, reported in [REPORT.md](../../REPORT.md).

| File | Contents |
|---|---|
| `run.json` | Study configuration, fingerprint, versions, platform, timing |
| `summary.md` | Headline, oracle controls (size and power), flagged cells per row |
| `matrix.md` | Row summary, status grid per n, and every non-PASS cell |
| `matrix.json` | The same data in machine-readable form |
| `cells.csv` | One line per (row, dgp, n, alpha) cell: coverage, interval, p-values (raw, Holm, BY), rank offsets, status |
| `units.jsonl.gz` | The per-unit checkpoint records the report is built from (gunzip into `runs/default/units.jsonl` and copy `run.json` beside it to rebuild the report) |
| `repros/` | One standalone script per finding, with its captured output (`*.out.txt`); `index.json` lists them with exit codes |
| `repros/puncc_numpy1_recheck.txt` | The puncc repros re-run under puncc's declared `numpy<2` (Python 3.12, numpy 1.26.4) |
| `repros/manual__*.py` | Hand-written repros for behaviour the generator does not cover |

The repro scripts exit 1 while the finding reproduces, 0 when it no longer does, and 2
on an unexpected crash.
