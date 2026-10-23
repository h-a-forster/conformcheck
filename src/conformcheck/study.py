"""Study configuration: parse a study TOML and enumerate work units.

A *cell* is (library, method, variant, dgp, n, alpha). A *unit*, the checkpoint
granularity, is (library, method, variant, dgp, n) with all alphas and all ``R``
repetitions, because libraries fit once and evaluate every alpha. Planned in milestone
M4 (docs/DESIGN.md section 7).
"""

from __future__ import annotations
