"""Generate and verify a minimal, standalone reproduction script for each finding.

Each script depends only on numpy and the library concerned, prints the library and
numpy versions, builds the exact data from a fixed seed, calls the library and prints
the expected and observed order statistic (deterministic findings) or the Monte Carlo
coverage with its exact standard error (statistical findings). It exits with status 1
while the finding reproduces. Planned in milestone M6 (docs/DESIGN.md section 8.3).
"""

from __future__ import annotations
