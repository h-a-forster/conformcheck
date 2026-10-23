"""Turn ``units.jsonl`` into the conformance matrix.

Planned outputs (milestone M5, docs/DESIGN.md section 8): ``matrix.json``, ``matrix.csv``
and ``matrix.md`` with one row per library-method-variant and one status per setting:
PASS, FAIL (under-coverage), CONSERVATIVE (over-coverage, with the order-statistic
offset when known), LAW_MISMATCH, REFUSED, ERROR or UNSUPPORTED; Holm and
Benjamini-Yekutieli adjusted p-values; and ``summary.md`` with the headline counts.
"""

from __future__ import annotations
