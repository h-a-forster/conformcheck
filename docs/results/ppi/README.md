# Prediction-powered inference: exact coverage of ppi_py (2026-11-21)

A study outside the conformal grid (DESIGN section 15, pre-registered before the run; 15.5
records two corrections made after it): the exact finite-sample coverage of `ppi_py`'s
mean intervals when an LLM evaluation combines 20-200 human labels with judge labels.
REPORT section 4, "Prediction-powered inference", has the summary; this folder holds the
outputs and repros.

## Design

- Truth `Y ~ Bernoulli(pi)`, a binary judge with sensitivity = specificity = `acc`. The
  labelled pairs `(Y, Yhat)` form a 4-cell multinomial; the estimand is `pi`.
- The judge mean `mu = pi acc + (1 - pi)(1 - acc)` is treated as known: the unlabelled
  input is a fixed array of N = 10,000 judge labels with exactly `N mu` ones. The library
  still adds its own `mu (1 - mu) / N` variance term. Coverage is thus conditional on the
  unlabelled mean equal to its expectation; the Monte Carlo `binomial` rows give the
  unconditional coverage beside it.
- Methods: `ppi_mean_ci(..., lam=1)` (PPI), `ppi_mean_ci(...)` with the default
  `lam=None` (PPI++, lambda tuned from the data), both two-sided; label-only baselines
  `classical_mean_ci` (the library's Wald interval) and Clopper-Pearson (scipy).
- Exact law: every labelled outcome's interval is computed by the library and the
  multinomial probabilities of the covering outcomes are summed as exact rationals.
  Outcomes are taken in order of probability until at most 1e-10 is left; `map.md` states
  the largest mass left out (true coverage lies in `[c, c + mass]`). Many outcomes go
  into one d-dimensional library call; every outcome with an endpoint within 1e-9 of `pi`
  is recomputed with a one-dimensional call as a user would make it.
- Grid: n in {20, 50, 100, 200}, acc in {0.7, 0.8, 0.9, 0.95}, pi in {0.02, 0.1, 0.3,
  0.5}, alpha in {0.1, 0.05}: 128 cells per method, no trimming. Below nominal: coverage
  under `1 - alpha - 0.01`.
- `ppi-python` 0.2.3 (released 2024-12-22, the newest release) was read as text before
  it was installed: sdist and wheel hashes match PyPI, the two carry the same `ppi_py`
  package, and nothing runs at import beyond module definitions. Two notes: importing
  `ppi_py` calls `warnings.simplefilter("ignore")`, which silences warnings for the whole
  process, and `load_dataset` downloads by shelling out to `gdown` (only when called; the
  study never calls it). The wheel also installs a top-level `tests` package.

## Results

Exact coverage (no sampling error; at most 2.5e-11 of probability left unevaluated per
cell). Cells below nominal by more than one point, out of 64 per method and alpha:

| alpha | PPI | PPI++ | Wald (labels only) | Clopper-Pearson (labels only) |
|---|---|---|---|---|
| 0.1 | 29 | 50 | 48 | 0 |
| 0.05 | 28 | 45 | 40 | 0 |

That normal intervals under-cover at small n near a base rate of 0 or 1 is known (Brown,
Cai and DasGupta 2001 for Wald), and the PPI and PPI++ guarantees are asymptotic. What
this adds is the exact map at LLM-evaluation label counts, `map.md`. At alpha = 0.1:

- **PPI** (`lam=1`) is below nominal at n = 20 in 14 of 16 (acc, pi) cells. For judges
  with accuracy up to 0.9 it is within about a point by n = 100 (one cell below: 0.8896 at
  acc = 0.8, pi = 0.1) and covers 0.899 or more by n = 200. A more accurate judge makes
  small samples worse, not better: with acc = 0.95 coverage is 0.59-0.62 at
  n = 20 for pi < 0.5, and at pi = 0.02 it is still 0.849 at n = 100 and 0.884 at n = 200
  (not monotone in n). The cause is the rectifier `Y - Yhat`, a rare event for a good
  judge: with probability `acc^n` no labelled pair disagrees, the rectifier variance is
  zero and the interval is the judge mean plus or minus the small unlabelled term, which
  misses `pi` whenever the judge is biased (`mu != pi`).
- **PPI++** (default `lam=None`) is lower than PPI in 62 of 64 cells with pi <= 0.1 and is
  below nominal at n = 200 in all 8 cells with pi <= 0.1 (0.853-0.889). Whenever all
  labels are 0 the tuned lambda is 0 (up to rounding) and the interval collapses onto 0,
  so its coverage is at most `1 - (1 - pi)^n` (0.33 at n = 20, pi = 0.02; the bound holds
  in all 128 cells); at pi = 0.02 its coverage is close to Wald's, and with acc = 0.95
  below it (0.853 vs 0.890 at n = 200). At pi in {0.3, 0.5} it is within a point of
  nominal at n = 200 (0.896 or more); at n = 100, three cells at pi = 0.3 are just below
  (0.886-0.890).
- **Wald** (labels only, `classical_mean_ci`) is below nominal in 48 cells (12 of 16
  (n, pi) cells; it ignores the judge), including pi = 0.1 at n = 200 (0.880).
  **Clopper-Pearson** never is (lowest coverage minus nominal: +0.005), at the price of
  wider intervals.

Pre-registered hypotheses (DESIGN 15.3; REPORT section 5): 11 partly confirmed (every
predicted cell is below nominal, but PPI at pi = 0.5 also falls below in 6 of 32 cells),
12 confirmed, 13 partly confirmed (Wald at pi = 0.02, n = 200, alpha = 0.1 is 0.890,
short by 0.0096, just inside the one-point margin), 14 partly refuted (PPI 0.879 and
PPI++ 0.886-0.890 at n = 100, pi = 0.3).

Monte Carlo cross-check (`mc.md`, DESIGN 15.4): on six cells fixed before the run, 20,000
raw labelled draws (seed 20261121) passed one at a time to the library agree with the exact
coverage in all 18 method-cell comparisons (each exact value inside the 99%
Clopper-Pearson interval of its estimate). The same draws with an unlabelled count from
Binomial(N, mu) give the unconditional coverage: within 0.005 of the exact (conditional)
value in five cells, but at n = 20, acc = 0.95, pi = 0.5 it is 0.946 against 0.983 for PPI
and 0.859 against 0.890 for PPI++. There the judge is unbiased and a labelled sample
without disagreement is likely (`0.95^20 = 0.36`): with the judge mean fixed at `pi` such a
sample's narrow interval always covers, while a random judge mean is missed about 10% of
the time. So holding the judge mean at its expectation can overstate coverage where the
interval rests on the unlabelled term alone. In the other five cells it moves coverage by
at most 0.005 in either direction, so shortfalls of several points do not come from it;
cells within half a point of the threshold could change status unconditionally (only six
cells were checked).

Evaluation checks: no outcome had an endpoint within 1e-9 of `pi` (so the batched and
one-at-a-time calls cannot disagree on a verdict), no interval had a NaN or infinite
endpoint, and `repros/ppi_exact_cell.py`, a full enumeration with one library call per
outcome and no pruning, reproduces the study's n = 20, acc = 0.9, pi = 0.02 cell to six
digits (PPI 0.862751, PPI++ 0.290151, Wald 0.331792).

### A library bug outside the study

`ppi_mean_ci(..., alternative="larger")` (or `"smaller"`) with the default `lam=None`
returns the two-sided interval: after tuning lambda the function calls itself without
passing `alternative` on (`ppi_py/ppi.py`, `ppi_mean_ci`). With `lam` given, the
one-sided interval is correct. Present in 0.2.3 and on the main branch as of 2026-11-21;
`repros/manual__ppi_alternative.py` shows it. Not reported upstream.

## Files

| Path | Contents |
|---|---|
| `map.md` | Coverage map: cells below nominal per method, largest n below nominal, every coverage, hypothesis checks, evaluation checks |
| `coverage.csv` | One line per (method, alpha, n, acc, pi): exact coverage (float and 20 digits), shortfall, mean width, zero-width and NaN mass, mass left out |
| `mc.md` | Monte Carlo cross-check (DESIGN 15.4) |
| `units.jsonl`, `mc.jsonl`, `run.json`, `mc.json` | The per-unit records and run metadata the report is built from |
| `constraints.txt` | Exact package versions of the venv the study ran in |
| `repros/ppi_exact_cell.py` | One cell by full enumeration, one library call per outcome, independent of conformcheck (output in `.out.txt`) |
| `repros/manual__ppi_alternative.py` | One-sided PPI++ request returns the two-sided interval (output in `.out.txt`) |

The repros exit 1 while what they show reproduces, 0 when it no longer does.

## Reproducing

```sh
uv run python scripts/ppi_study.py --out runs/ppi --to docs/results/ppi
uv run python -m conformcheck.ppi report runs/ppi --to docs/results/ppi   # report only
```

The script builds a fresh wheels-only venv (Python 3.13.13, `constraints.txt`), runs the
exact study and the Monte Carlo check in it (both resume from their checkpoints) and
writes the report. Copy `units.jsonl`, `run.json`, `mc.jsonl` and `mc.json` from this
folder into a run directory to rebuild the report without running anything.
