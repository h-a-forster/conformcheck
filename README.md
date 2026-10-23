# conformcheck

[![CI](https://github.com/h-a-forster/conformcheck/actions/workflows/ci.yml/badge.svg)](https://github.com/h-a-forster/conformcheck/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

Finite-sample coverage certification for Python conformal-prediction libraries.

Split conformal prediction has an exact guarantee. With `n` exchangeable calibration
points and continuous scores, the marginal coverage is exactly `k/(n+1)` with
`k = ceil((n+1)(1-alpha))`, and the number of covered points among `m` test points that
share one calibration set follows `BetaBinomial(m, k, n+1-k)`, whatever the data
distribution and the model. That makes an implementation testable to the digit.
conformcheck runs library methods through these laws and reports, per method and
setting, whether the library is exact, under-covers, over-covers, refuses a feasible
level or crashes. Every finding comes with a standalone repro script.

It covers [MAPIE](https://github.com/scikit-learn-contrib/MAPIE),
[crepes](https://github.com/henrikbostrom/crepes), [puncc](https://github.com/deel-ai/puncc)
and [TorchCP](https://github.com/ml-stat-Sustech/TorchCP) (CPU): split regression, CQR,
jackknife+ and CV+, LAC, APS (randomized and not) and class-conditional sets, 31
library-method rows in all.

## Results of the default study

The default study ran MAPIE 1.6.0, crepes 0.9.1, puncc 0.9.3 and TorchCP 1.2.1. It used
R = 200 calibration draws × 500 test points per cell and 3058 statistical cells, with
Holm FWER 0.05. **15 of the 31 library-method rows are flagged at n <= 100.** Only one
row under-covers: MAPIE APS with `include_last_label=False`, whose coverage follows the
model rather than the law (far below target with an anti-informative synthetic
classifier, far above it on digits). The other flags are over-coverage by one order
statistic, MAPIE's documented conservatism of `include_last_label=True`, refusals of a
level where a valid set exists, and crashes. The reference rows produced 0 false alarms.
Details, intervals and limitations are in [REPORT.md](REPORT.md).

| Finding | Kind | Size |
|---|---|---|
| MAPIE APS `include_last_label=False` | coverage set by the model, not the law | about 0.55 at a 0.90 target on synthetic data (under), about 0.97 on digits (over), every n |
| crepes split regression and unsmoothed LAC | k + 1 at integer `(n+1) alpha` (float `1 - 0.9`) | 0.949 vs 0.900 at n = 19 |
| MAPIE split, LAC, APS, symmetric CQR | refuse feasible `alpha` in `[1/(n+1), 1/n)` | every n |
| MAPIE asymmetric CQR | refuses when `n < 2/alpha` although `k' <= n` | n = 9, alpha = 0.2; n = 19, alpha = 0.1 |
| MAPIE CV+ (K = 5, 10) | lower endpoint uses k + 1 at n = 999, alpha = 0.05 | found by rank recovery |
| puncc CV+ / jackknife+ | crash on folds of size one and at `alpha = 1/(n+1)`; k + 1 at n = 99, 999 | jackknife+ errors in every cell |
| TorchCP split regression and CQR | crash where `k > n` instead of a trivial interval | every `k > n` cell |

An excerpt of the matrix (worst status over the DGPs and alphas at each n):

```text
row                                    n=5  9   10  19  20  49  50  99  100 999 1000
mapie/aps/include_last_label=False     E    E   F   F   F   F   F   F   F   F   F
mapie/split_abs/default                O    O   O   O   O   O   O   O   O   O   O
crepes/split_abs/default               C    C   P   C   P   C   P   C   P   C   C
crepes/lac/smoothed                    P    P   P   P   P   P   P   P   P   P   P
puncc/split_abs/default                R    R   R   R   R   R   R   R   R   R   R
torchcp/lac/default                    P    P   P   P   P   P   P   P   P   P   P
reference/split_abs/default            P    P   P   P   P   P   P   P   P   P   P
reference/split_abs/k_minus_1          F    F   F   F   F   F   F   F   F   F   F

P pass  C conservative  F fail  O refuses a feasible level  R refuses only k > n  E error
```

Each finding has a standalone repro under
[docs/results/default/repros](docs/results/default/repros).

## How it works

- **Exact laws** (`conformcheck.laws`): the order statistic `k`, the BetaBinomial count
  law, the exact law with tied scores, the asymmetric CQR coverage, and the jackknife+
  and CV+ bounds of Barber et al. (2021). `alpha` is read as the exact decimal it
  denotes (`0.1` is 1/10), so the oracle has no floating-point rounding of its own.
- **Rank recovery** (deterministic): for regression, the order statistic a library used
  is read off each endpoint of the interval it returns. This detects an off-by-one at
  any `n`, including `n = 1000`, where Monte Carlo has no power.
- **Statistical tests**: an exact test of the summed covered counts (FFT convolution of
  the law) plus a chi-square goodness-of-fit test per cell, Holm across all cells
  (FWER 0.05), Benjamini-Yekutieli reported alongside.
- **Self-validation**: reference implementations and four deliberately wrong mutants
  (`k-1`, `k+1`, `n` instead of `n+1`, no finite-sample correction) run through the
  same pipeline, so the false-alarm rate and the power are measured, not assumed.
- **Edge cases on purpose**: small `n`, pairs of `n` on and off the `(n+1)alpha` integer
  boundary, `alpha = 1/(n+1)` (`k = n`) and `alpha < 1/(n+1)` (`k > n`, the set must be
  trivial), tied scores, randomized sets, and random splits of real datasets.

The full design, with formulas and references, is in [docs/DESIGN.md](docs/DESIGN.md).

## Install

conformcheck is not on PyPI. Install it from git with [uv](https://docs.astral.sh/uv/):

```sh
# as a library (the oracle, the testing helpers and the pytest plugin)
uv pip install "conformcheck @ git+https://github.com/h-a-forster/conformcheck"

# to run the study: clone and sync with every library under test (CPU torch)
git clone https://github.com/h-a-forster/conformcheck
cd conformcheck
uv sync --all-extras
uv run conformcheck libraries
```

The core needs only numpy, scipy and scikit-learn. To run the libraries under test, use
`uv sync --all-extras` in a clone, as above. That is the only supported way: the
repository's lockfile carries dependency overrides (puncc declares `numpy<2`; TorchCP
requires `torchsort`, which has no wheels on some platforms). The optional extras
`mapie`, `crepes`, `puncc`, `torchcp` and `all` exist, but outside the clone `puncc` does
not resolve from wheels on Python 3.13, and `torchcp` does not resolve on Windows.
`conformcheck run` refuses to start when a library the study needs is missing, unless
`--libraries` or `--allow-missing` is given.

## Quick start

Check your own split-conformal implementation in a test:

```python
from conformcheck.testing import check_split_regressor


def my_split(x_cal, y_cal, x_test, alpha, model):
    """Return (m, 2) intervals; model is a fixed, fitted regressor."""
    scores = abs(y_cal - model.predict(x_cal))
    ...


def test_my_split_is_exact():
    report = check_split_regressor(my_split, n=(9, 19, 99), alpha=(0.1, 0.2), reps=200)
    report.assert_valid(allow_conservative=False)
```

Rank recovery assumes the absolute-residual score. By default (`score="auto"`) it is
applied only to intervals of that shape; pass `score="other"` for a different score
(for example a normalised residual), which then gets the statistical test alone, or
`score="abs"` to force it. `check_split_classifier` does the same for set-valued
classifiers. Under pytest,
`--conformcheck-reps` and `--conformcheck-seed` change the defaults. A failing check
reads like this (a deliberate `k - 1` bug):

```text
AssertionError: 1 of 1 conformance cells failed
conformcheck check_split_regressor: 1 cells, R=200, m=500, Holm FWER 0.05
  n=19    alpha=0.1    k=18    FAIL         coverage 0.8507 (exact 0.9000) Holm p=1.4e-17 order statistic -1 (rank recovery)
```

Run the library study:

```sh
uv run conformcheck plan --study default        # unit count and time estimate
uv run python scripts/run_study.py --study default --out runs/default   # resumable
uv run conformcheck report runs/default         # matrix.md, summary.md, cells.csv
uv run conformcheck repro runs/default --verify # standalone repro per finding
```

`runs/<name>/progress.log` shows progress; rerunning the same command resumes from the
last finished unit. `--study smoke` runs in under a minute; `--study full` (R=2000,
m=1000) takes hours.

## Validating the oracle

- `uv run pytest` runs the test suite, including exact reference values for the laws,
  null-calibration and power tests of the statistical layer, and the adapters' checks
  against each library's documented usage. `uv run pytest -m "not slow"` is what CI runs.
- In every study the reference rows must pass and the mutant rows must be caught; the
  report prints both (see "Oracle controls" in [REPORT.md](REPORT.md)).
- Each finding has a repro under [docs/results/default/repros](docs/results/default/repros)
  that imports only numpy, scikit-learn and the library, and exits 1 while the problem
  reproduces.

## Notes on dependencies

- puncc 0.9.3 declares `numpy<2`. This repository's lockfile overrides that pin. Every
  puncc finding was re-checked under `numpy<2` (Python 3.12) before being reported.
- `import torchcp` pulls in `torchsort`, `torch_geometric` and `transformers` for
  modules conformcheck never uses. They are left out of the lock and replaced by inert
  import stubs when missing.
- TorchCP is LGPL-3.0. conformcheck imports it as an optional dependency and does not
  vendor or modify it.

## Documentation

- [REPORT.md](REPORT.md): the default study, its findings and its limitations.
- [docs/DESIGN.md](docs/DESIGN.md): formulas, oracle, study design, pre-registered
  hypotheses.
- [docs/results/default](docs/results/default): matrix, summary, cell table and repros.
- [AGENTS.md](AGENTS.md): conventions, architecture map and current status.

## Citation

If you use conformcheck, please cite it via [CITATION.cff](CITATION.cff):

```bibtex
@software{conformcheck,
  title  = {conformcheck: finite-sample coverage certification for conformal-prediction libraries},
  author = {{conformcheck contributors}},
  year   = {2026},
  url    = {https://github.com/h-a-forster/conformcheck},
  version = {0.1.0}
}
```

## License

MIT. See [LICENSE](LICENSE).
