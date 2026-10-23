# conformcheck

[![CI](https://github.com/h-a-forster/conformcheck/actions/workflows/ci.yml/badge.svg)](https://github.com/h-a-forster/conformcheck/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

Finite-sample coverage certification for Python conformal-prediction libraries.

> **Status: pre-alpha, under construction.** The design is fixed
> ([docs/DESIGN.md](docs/DESIGN.md)); the oracle laws are implemented and tested. The
> adapters, the study runner and the conformance matrix are in progress. No results yet.

Split conformal prediction has an exact guarantee. With `n` exchangeable calibration
points and continuous scores, the marginal coverage is exactly `k/(n+1)` with
`k = ceil((n+1)(1-alpha))`. Coverage given the calibration set follows
`Beta(k, n+1-k)`. The number of covered points among `m` test points follows
`BetaBinomial(m, k, n+1-k)`, whatever the data distribution and the model. These laws
let an implementation be tested to the digit. conformcheck checks four ways a library
can get it wrong:

- an off-by-one in the order statistic;
- interpolation between order statistics;
- tie handling;
- a mismatch between how scores are calibrated and how sets are built.

It flags both under-coverage and needless over-coverage.

## What it will do

- **Adapters** behind one interface for [MAPIE](https://github.com/scikit-learn-contrib/MAPIE),
  [crepes](https://github.com/henrikbostrom/crepes), [puncc](https://github.com/deel-ai/puncc)
  and [TorchCP](https://github.com/ml-stat-Sustech/TorchCP) (CPU). They cover split
  regression, CQR, jackknife+ and CV+, LAC, APS (randomized and not), RAPS and
  class-conditional sets.
- **An exact oracle.** It recovers which order statistic a library used (deterministic),
  runs exact tests of the covered-count law, and checks the jackknife+/CV+ bounds.
  Holm and Benjamini-Yekutieli control the multiple testing across cells.
- **A conformance matrix** (library x method x setting: pass / fail / conservative) at
  small `n`, at the `(n+1)alpha` integer boundary, with ties and with randomized sets.
  Every finding gets a standalone minimal repro.
- **A pytest plugin** and `conformcheck.testing` helpers that library authors can run in
  their own CI.

## Install (development)

```sh
git clone https://github.com/h-a-forster/conformcheck
cd conformcheck
uv sync --all-extras      # core + all libraries under test (CPU torch)
uv run pytest
uv run conformcheck libraries
```

The core needs only numpy, scipy and scikit-learn. The libraries under test are
optional extras: `mapie`, `crepes`, `puncc`, `torchcp`, `all`.

## Notes on dependencies

- puncc 0.9.3 declares `numpy<2`. This repository's lockfile overrides that pin. Any
  puncc finding is re-checked under `numpy<2` before it is reported.
- `import torchcp` pulls in `torchsort`, `torch_geometric` and `transformers` for
  modules conformcheck never uses. They are left out of the lock and replaced by inert
  import stubs when missing.
- TorchCP is LGPL-3.0. conformcheck imports it as an optional dependency and does not
  vendor or modify it.

## Documentation

- [docs/DESIGN.md](docs/DESIGN.md): formulas, oracle, study design, milestones.
- [AGENTS.md](AGENTS.md): conventions, architecture map and current status.

## License

MIT. See [LICENSE](LICENSE).
