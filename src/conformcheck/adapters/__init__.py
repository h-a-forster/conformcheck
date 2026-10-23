"""Adapters for the libraries under test, plus the reference and mutant controls.

Each library module imports its library lazily, so ``import conformcheck.adapters``
works without any optional dependency installed. :func:`registry` lists every adapter;
:func:`get_adapter` looks one up by its ``library/method/variant`` key.
"""

from __future__ import annotations

from conformcheck.adapters._common import LibraryAdapter
from conformcheck.adapters.base import (
    AlphaOutput,
    ClassificationInput,
    CrossRegressionInput,
    MethodSpec,
    RegressionInput,
)

LIBRARIES: tuple[str, ...] = ("mapie", "crepes", "puncc", "torchcp")


def registry() -> dict[str, LibraryAdapter]:
    """Every adapter by key, libraries first, then reference and mutant controls."""
    from conformcheck.adapters import crepes, mapie, puncc, reference, torchcp

    items: list[LibraryAdapter] = []
    for mod in (mapie, crepes, puncc, torchcp, reference):
        items.extend(mod.adapters())
    out: dict[str, LibraryAdapter] = {}
    for a in items:
        if a.spec.key in out:  # pragma: no cover - defensive
            raise RuntimeError(f"duplicate adapter key {a.spec.key}")
        out[a.spec.key] = a
    return out


def get_adapter(key: str) -> LibraryAdapter:
    reg = registry()
    try:
        return reg[key]
    except KeyError:
        raise KeyError(f"unknown adapter {key!r}") from None


__all__ = [
    "LIBRARIES",
    "AlphaOutput",
    "ClassificationInput",
    "CrossRegressionInput",
    "LibraryAdapter",
    "MethodSpec",
    "RegressionInput",
    "get_adapter",
    "registry",
]
