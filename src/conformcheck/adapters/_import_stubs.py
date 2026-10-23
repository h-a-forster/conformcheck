"""Import stubs for TorchCP's optional heavy dependencies.

``import torchcp`` imports its graph, LLM and training-loss subpackages, which import
``torch_geometric``, ``transformers`` and ``torchsort`` at module level. conformcheck never
calls that code, and ``torchsort`` has no Windows wheels, so these packages are removed
from the lockfile (see ``[tool.uv] override-dependencies``). Before importing torchcp the
adapter installs a meta-path finder that serves an inert placeholder module for each of
them that is not really installed. Any attribute of a placeholder is a dummy class;
instantiating code paths that need the real package is out of scope.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import sys
import types
from collections.abc import Sequence

STUBBED_ROOTS: tuple[str, ...] = ("torchsort", "torch_geometric", "transformers")


class _PlaceholderFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, roots: Sequence[str]) -> None:
        self.roots = frozenset(roots)

    def find_spec(self, fullname, path=None, target=None):  # type: ignore[override]
        if fullname.split(".")[0] in self.roots:
            return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
        return None

    def create_module(self, spec):  # type: ignore[override]
        module = types.ModuleType(spec.name)
        module.__path__ = []  # type: ignore[attr-defined]
        module.__conformcheck_stub__ = True  # type: ignore[attr-defined]

        def __getattr__(name: str) -> type:
            if name.startswith("__"):
                raise AttributeError(name)
            return type(name, (), {"__module__": spec.name})

        module.__getattr__ = __getattr__  # type: ignore[attr-defined]
        return module

    def exec_module(self, module) -> None:  # type: ignore[override]
        return None


def install(roots: Sequence[str] = STUBBED_ROOTS) -> list[str]:
    """Stub every root in ``roots`` that cannot be imported. Returns the stubbed names.

    Idempotent; packages that are really installed are never shadowed.
    """
    if any(isinstance(f, _PlaceholderFinder) for f in sys.meta_path):
        return [r for r in roots if getattr(sys.modules.get(r), "__conformcheck_stub__", False)]
    missing = [r for r in roots if importlib.util.find_spec(r) is None]
    if missing:
        sys.meta_path.append(_PlaceholderFinder(missing))
    return missing
