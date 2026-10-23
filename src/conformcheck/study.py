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
import math
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
    "split": {"regression": ("split_abs", "cqr"), "classification": ("lac", "aps", "raps")},
    "tied": {"regression": ("split_abs",)},
    "jackknife_plus": {"regression": ("jackknife_plus",)},
    "cv_plus": {"regression": ("cv_plus",)},
    "class_conditional": {"classification": ("class_conditional",)},
    "toy": {"regression": ("split_abs", "cqr"), "classification": ("lac", "aps", "raps")},
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

    @classmethod
    def from_config(cls, cfg: dict[str, Any], source: str = "") -> Study:
        """Inverse of :meth:`config` (as stored in ``run.json``): same units, same uids."""
        d = dict(cfg)
        grids = tuple(
            Grid(
                name=str(g["name"]),
                n=tuple(int(v) for v in g["n"]),
                dgps=tuple(str(v) for v in g["dgps"]),
                alphas=None if g.get("alphas") is None else tuple(str(a) for a in g["alphas"]),
                edge_alphas=g.get("edge_alphas"),
                n_folds=tuple(int(k) for k in g.get("n_folds", ())),
            )
            for g in d.pop("grids")
        )
        return cls(
            **{
                **d,
                "alphas": tuple(str(a) for a in d["alphas"]),
                "mutants": tuple(str(x) for x in d.get("mutants", ())),
            },
            grids=grids,
            source=source,
        )


REQUIRED_KEYS = ("name", "seed", "reps", "test_points", "alphas")


def load_study(name_or_path: str | Path, reps: int | None = None) -> Study:
    """Load a built-in study (``smoke``, ``default``, ``full``) or a TOML file.

    The configuration is validated here, so a bad file fails before any work starts:
    every problem raises ``ValueError`` (the CLI maps it to exit code 2, which the
    resume wrapper does not retry).
    """
    p = Path(name_or_path)
    if p.suffix == ".toml" and p.exists():
        text, source = p.read_text(encoding="utf-8"), str(p)
    else:
        res = resources.files("conformcheck.studies").joinpath(f"{name_or_path}.toml")
        if not res.is_file():
            raise FileNotFoundError(f"no built-in study {name_or_path!r} and no such file")
        text, source = res.read_text(encoding="utf-8"), f"builtin:{name_or_path}"
    raw = tomllib.loads(text)
    try:
        return _parse_study(raw, source, reps)
    except (KeyError, TypeError) as exc:  # wrong types slipping past the checks below
        raise ValueError(f"{source}: invalid study configuration: {exc!r}") from exc


def _positive_int(value: Any, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{what} must be a positive integer, got {value!r}")
    return int(value)


def _parse_study(raw: dict[str, Any], source: str, reps: int | None) -> Study:
    from conformcheck.reference import MUTANTS

    missing = [k for k in REQUIRED_KEYS if k not in raw]
    if missing:
        raise ValueError(f"{source}: missing required key(s): {', '.join(missing)}")
    alphas = raw["alphas"]
    if not isinstance(alphas, list) or not alphas:
        raise ValueError(f"{source}: 'alphas' must be a non-empty list")
    for a in alphas:
        laws.as_fraction(str(a))  # raises for values outside (0, 1)
    grids = []
    raw_grids = raw.get("grids", {})
    if not raw_grids:
        raise ValueError(f"{source}: no [grids.*] tables")
    for gname, g in raw_grids.items():
        if gname not in GRID_METHODS:
            raise ValueError(f"unknown grid {gname!r}; known: {sorted(GRID_METHODS)}")
        for key in ("n", "dgps"):
            if key not in g or not g[key]:
                raise ValueError(f"{source}: grid {gname!r} needs a non-empty {key!r}")
        ns = tuple(_positive_int(v, f"grid {gname!r} n") for v in g["n"])
        dgps = tuple(str(d) for d in g["dgps"])
        for d in dgps:
            task = get_dgp(d).task  # raises for an unknown dgp
            if task not in GRID_METHODS[gname]:
                raise ValueError(f"{source}: dgp {d!r} ({task}) has no methods on grid {gname!r}")
        folds = tuple(_positive_int(k, f"grid {gname!r} n_folds") for k in g.get("n_folds", ()))
        if gname == "cv_plus" and not folds:
            raise ValueError(f"{source}: grid 'cv_plus' needs a non-empty 'n_folds'")
        g_alphas = None
        if "alphas" in g:
            g_alphas = tuple(str(a) for a in g["alphas"])
            for a in g_alphas:
                laws.as_fraction(a)
        grids.append(
            Grid(
                name=gname,
                n=ns,
                dgps=dgps,
                alphas=g_alphas,
                edge_alphas=g.get("edge_alphas"),
                n_folds=folds,
            )
        )
    controls = raw.get("controls", {})
    mutants = tuple(str(x) for x in controls.get("mutants", ()))
    unknown = [x for x in mutants if x not in MUTANTS]
    if unknown:
        raise ValueError(f"{source}: unknown mutant(s) {unknown}; known: {list(MUTANTS)}")
    fwer = float(raw.get("fwer", 0.05))
    fdr = float(raw.get("fdr", 0.05))
    for what, v in (("fwer", fwer), ("fdr", fdr)):
        if not 0 < v < 1:
            raise ValueError(f"{source}: {what} must lie in (0, 1), got {v}")
    return Study(
        name=str(raw["name"]),
        seed=int(raw["seed"]),
        reps=_positive_int(reps if reps is not None else raw["reps"], "reps"),
        test_points=_positive_int(raw["test_points"], "test_points"),
        workers=min(_positive_int(raw.get("workers", 4), "workers"), 4),
        fwer=fwer,
        fdr=fdr,
        alphas=tuple(str(a) for a in alphas),
        edge_alphas=bool(raw.get("edge_alphas", True)),
        grids=tuple(grids),
        reference=bool(controls.get("reference", True)),
        mutants=mutants,
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
# Deterministic RAPS scores have the same atoms (shifted by the rank penalty).
DETERMINISTIC_APS = {"deterministic", "rand=False", "randomized=False"}
APS_METHODS = ("aps", "raps")

# MAPIE's RAPS holds out a stratified share of the conformalization data to tune lambda
# and k_reg. RAPSConformityScore(size_raps=0.2) is documented, but in MAPIE 1.6.0
# SplitConformalClassifier resets size_raps to None, so scikit-learn's
# StratifiedShuffleSplit default test share 0.1 applies: ceil(0.1 * n) points (computed
# in floating point, as scikit-learn does) are held out (REPORT.md, F9).
MAPIE_RAPS_HOLDOUT = 0.1


def mapie_raps_effective_n(n: int) -> int:
    """Calibration size MAPIE 1.6.0 RAPS uses out of ``n`` conformalization points."""
    return n - math.ceil(MAPIE_RAPS_HOLDOUT * n)


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
    if library == "mapie" and method == "raps":
        n_eff = mapie_raps_effective_n(n)
        k_eff = laws.split_index(n_eff, alpha)
        if k_eff > n_eff:
            return CellLaw("trivial", 1.0, None, k_eff, f"k={k_eff} > n_eff={n_eff}")
        law = laws.split_count_law(n_eff, alpha, m)
        return CellLaw(
            "exact",
            law.coverage,
            law,
            k_eff,
            f"{law.description}; n_eff = n - ceil(0.1 n) = {n_eff} (internal tuning split)",
        )
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
            if not laws.cv_plus_bound_proven(n, n_folds):
                desc += "; K does not divide n, so the bound is extrapolated"
        return CellLaw("lower", bound, CoverageLaw("lower", m, bound), None, desc)
    if k > n:
        return CellLaw("trivial", 1.0, None, k, f"k={k} > n={n}")
    if d.score_pmf is not None and method == "split_abs":
        law = laws.discrete_count_law(n, alpha, m, d.score_pmf)
        return CellLaw("exact", law.coverage, law, k, law.description)
    law = laws.split_count_law(n, alpha, m)
    one_sided = method in APS_METHODS and variant in DETERMINISTIC_APS
    desc = law.description + ("; one-sided (score atom at 1)" if one_sided else "")
    return CellLaw("exact", law.coverage, law, k, desc, one_sided)
