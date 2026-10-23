"""Study configuration: parse a study TOML, enumerate work units, and map cells to laws.

A *cell* is (library, method, variant, dgp, n, alpha). A *unit*, the checkpoint
granularity, is (library, method, variant, dgp, n) with all alphas and all ``R``
repetitions, because libraries fit once and evaluate every alpha (docs/DESIGN.md,
section 7). :func:`cell_law` says which exact law, mean or bound a cell is tested
against (section 3.2.4).
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from importlib import resources
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats as sps

from conformcheck import laws
from conformcheck.adapters._common import LibraryAdapter
from conformcheck.data import get_dgp
from conformcheck.laws import CoverageLaw

# Which methods run on which grid, per task of the grid's dgp.
GRID_METHODS: dict[str, dict[str, tuple[str, ...]]] = {
    "split": {"regression": ("split_abs", "cqr"), "classification": ("lac", "aps")},
    "tied": {"regression": ("split_abs",)},
    "jackknife_plus": {"regression": ("jackknife_plus",)},
    "cv_plus": {"regression": ("cv_plus",)},
    "class_conditional": {"classification": ("class_conditional",)},
    "toy": {"regression": ("split_abs", "cqr"), "classification": ("lac", "aps")},
}


@dataclass(frozen=True)
class Grid:
    name: str
    n: tuple[int, ...]
    dgps: tuple[str, ...]
    alphas: tuple[str, ...] | None = None
    edge_alphas: bool | None = None
    n_folds: tuple[int, ...] = ()


@dataclass(frozen=True)
class Study:
    name: str
    seed: int
    reps: int
    test_points: int
    workers: int
    fwer: float
    fdr: float
    alphas: tuple[str, ...]
    edge_alphas: bool
    grids: tuple[Grid, ...]
    reference: bool = True
    mutants: tuple[str, ...] = ()
    source: str = ""

    def config(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("source")
        return d


def load_study(name_or_path: str | Path, reps: int | None = None) -> Study:
    """Load a built-in study (``smoke``, ``default``, ``full``) or a TOML file."""
    p = Path(name_or_path)
    if p.suffix == ".toml" and p.exists():
        text, source = p.read_text(encoding="utf-8"), str(p)
    else:
        res = resources.files("conformcheck.studies").joinpath(f"{name_or_path}.toml")
        if not res.is_file():
            raise FileNotFoundError(f"no built-in study {name_or_path!r} and no such file")
        text, source = res.read_text(encoding="utf-8"), f"builtin:{name_or_path}"
    raw = tomllib.loads(text)
    grids = []
    for gname, g in raw.get("grids", {}).items():
        if gname not in GRID_METHODS:
            raise ValueError(f"unknown grid {gname!r}; known: {sorted(GRID_METHODS)}")
        grids.append(
            Grid(
                name=gname,
                n=tuple(int(v) for v in g["n"]),
                dgps=tuple(g["dgps"]),
                alphas=tuple(str(a) for a in g["alphas"]) if "alphas" in g else None,
                edge_alphas=g.get("edge_alphas"),
                n_folds=tuple(int(k) for k in g.get("n_folds", ())),
            )
        )
    controls = raw.get("controls", {})
    return Study(
        name=str(raw["name"]),
        seed=int(raw["seed"]),
        reps=int(reps if reps is not None else raw["reps"]),
        test_points=int(raw["test_points"]),
        workers=min(int(raw.get("workers", 4)), 4),
        fwer=float(raw.get("fwer", 0.05)),
        fdr=float(raw.get("fdr", 0.05)),
        alphas=tuple(str(a) for a in raw["alphas"]),
        edge_alphas=bool(raw.get("edge_alphas", True)),
        grids=tuple(grids),
        reference=bool(controls.get("reference", True)),
        mutants=tuple(controls.get("mutants", ())),
        source=source,
    )


def fingerprint(study: Study, extra: dict[str, Any] | None = None) -> str:
    payload = {"study": study.config(), **(extra or {})}
    blob = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def frac_str(a: Fraction) -> str:
    return f"{a.numerator}/{a.denominator}"


def grid_alphas(study: Study, grid: Grid, n: int) -> tuple[Fraction, ...]:
    """Base alphas (exact decimals) plus, if enabled, the edge levels ``1/(n+1)``
    (``k = n``) and ``0.9/(n+1)`` (``k = n + 1``: trivial set required)."""
    base = grid.alphas if grid.alphas is not None else study.alphas
    edge = study.edge_alphas if grid.edge_alphas is None else grid.edge_alphas
    vals = {laws.as_fraction(a) for a in base}
    if edge:
        vals.add(Fraction(1, n + 1))
        vals.add(Fraction(9, 10 * (n + 1)))
    return tuple(sorted(vals, reverse=True))


@dataclass(frozen=True)
class Unit:
    """One checkpoint unit: an adapter on one dgp and one ``n`` with all alphas."""

    adapter: str
    method: str
    dgp: str
    n: int
    alphas: tuple[str, ...]
    grid: str
    n_folds: int | None = None
    per_class: bool = False
    meta: dict[str, Any] = field(default_factory=dict, compare=False, hash=False)

    def key(self) -> dict[str, Any]:
        return {
            "adapter": self.adapter,
            "dgp": self.dgp,
            "n": self.n,
            "alphas": list(self.alphas),
            "grid": self.grid,
            "n_folds": self.n_folds,
            "per_class": self.per_class,
        }

    def uid(self, study: Study) -> str:
        payload = {**self.key(), "reps": study.reps, "m": study.test_points, "seed": study.seed}
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]

    def fractions(self) -> list[Fraction]:
        return [Fraction(a) for a in self.alphas]


def _include(adapter: LibraryAdapter, study: Study) -> bool:
    if adapter.spec.library != "reference":
        return True
    if not study.reference:
        return False
    v = adapter.spec.variant
    from conformcheck.reference import MUTANTS

    return v not in MUTANTS or v in study.mutants


def enumerate_units(
    study: Study,
    adapters: dict[str, LibraryAdapter] | None = None,
    libraries: set[str] | None = None,
) -> list[Unit]:
    """Every unit of the study, in a deterministic order."""
    if adapters is None:
        from conformcheck.adapters import registry

        adapters = registry()
    units: list[Unit] = []
    for grid in study.grids:
        for dgp_name in grid.dgps:
            dgp = get_dgp(dgp_name)
            methods = GRID_METHODS[grid.name].get(dgp.task, ())
            for key, ad in adapters.items():
                if ad.spec.method not in methods or not _include(ad, study):
                    continue
                if libraries is not None and ad.spec.library not in libraries:
                    continue
                if grid.name == "cv_plus" and ad.n_folds not in grid.n_folds:
                    continue
                for n in grid.n:
                    if grid.name == "cv_plus" and ad.n_folds is not None and ad.n_folds > n:
                        continue
                    if dgp.pool_size is not None and n >= dgp.pool_size:
                        continue
                    alphas = tuple(frac_str(a) for a in grid_alphas(study, grid, n))
                    units.append(
                        Unit(
                            adapter=key,
                            method=ad.spec.method,
                            dgp=dgp_name,
                            n=n,
                            alphas=alphas,
                            grid=grid.name,
                            n_folds=ad.n_folds,
                            per_class=grid.name == "class_conditional",
                        )
                    )
    return units


# --- laws per cell ----------------------------------------------------------------------


@dataclass(frozen=True)
class CellLaw:
    """What a cell is tested against.

    ``kind``: ``exact`` (full pmf of the count), ``mean`` (exact mean only), ``lower``
    (a guaranteed lower bound on coverage) or ``trivial`` (``k > n``: every set must be
    trivial, a deterministic check). ``k`` is the order statistic used by rank recovery.
    """

    kind: str
    target: float
    law: CoverageLaw | None = None
    k: int | None = None
    description: str = ""
    one_sided: bool = False  # only under-coverage is tested (scores with atoms)


# Deterministic APS scores have an atom at 1 (the true label ranked last), so ties occur
# and only add coverage: these rows are tested one-sided (docs/DESIGN.md, section 6).
DETERMINISTIC_APS = {"deterministic", "rand=False", "randomized=False"}


def _class_conditional_law(n: int, alpha: Fraction, m: int, n_classes: int) -> CoverageLaw:
    m_y = m // n_classes
    k = laws.split_index(n, alpha)
    pmf_y = sps.betabinom.pmf(np.arange(m_y + 1), m_y, k, n + 1 - k)
    pmf = pmf_y
    for _ in range(n_classes - 1):
        pmf = np.convolve(pmf, pmf_y)
    pmf = pmf / pmf.sum()
    return CoverageLaw(
        "exact",
        m_y * n_classes,
        k / (n + 1),
        pmf,
        f"sum of {n_classes} BetaBinomial(m_y={m_y}, {k}, {n + 1 - k})",
    )


def cell_law(
    *,
    method: str,
    variant: str,
    library: str,
    dgp: str,
    n: int,
    alpha: Fraction,
    m: int,
    n_folds: int | None = None,
) -> CellLaw:
    """The law a cell is tested against (docs/DESIGN.md, section 3.2.4)."""
    d = get_dgp(dgp)
    smoothed = variant == "smoothed"
    k = laws.split_index(n, alpha)
    if smoothed:
        return CellLaw(
            "mean",
            float(1 - alpha),
            CoverageLaw("mean", m, float(1 - alpha)),
            None,
            "smoothed p-values: mean 1 - alpha",
        )
    if method == "class_conditional":
        if k > n:
            return CellLaw("trivial", 1.0, None, k, f"k={k} > n_y={n}")
        law = _class_conditional_law(n, alpha, m, d.n_classes)
        return CellLaw("exact", law.coverage, law, k, law.description)
    if method == "cqr" and variant == "asymmetric":
        k2 = laws.split_index(n, alpha / 2)
        if k2 > n:
            return CellLaw("trivial", 1.0, None, k2, f"k'={k2} > n={n}")
        cov = float(laws.asymmetric_cqr_coverage(n, alpha))
        return CellLaw(
            "mean",
            cov,
            CoverageLaw("mean", m, cov),
            k2,
            f"asymmetric CQR: (2k'-(n+1))/(n+1), k'={k2}",
        )
    if method in ("jackknife_plus", "cv_plus") and dgp != "reg_constant":
        if method == "jackknife_plus":
            bound = float(laws.jackknife_plus_bound(alpha))
            desc = "jackknife+ >= 1 - 2 alpha (Barber et al. 2021, Thm 1)"
        else:
            assert n_folds is not None
            bound = float(laws.cv_plus_bound(n, n_folds, alpha))
            desc = f"CV+ (K={n_folds}) bound (Barber et al. 2021, Thm 4)"
        return CellLaw("lower", bound, CoverageLaw("lower", m, bound), None, desc)
    if k > n:
        return CellLaw("trivial", 1.0, None, k, f"k={k} > n={n}")
    if d.score_pmf is not None and method == "split_abs":
        law = laws.discrete_count_law(n, alpha, m, d.score_pmf)
        return CellLaw("exact", law.coverage, law, k, law.description)
    law = laws.split_count_law(n, alpha, m)
    one_sided = method == "aps" and variant in DETERMINISTIC_APS
    desc = law.description + ("; one-sided (score atom at 1)" if one_sided else "")
    return CellLaw("exact", law.coverage, law, k, desc, one_sided)
