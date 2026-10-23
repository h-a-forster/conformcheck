"""Checkpointed, resumable, parallel execution of a study.

Planned behaviour (milestone M4, docs/DESIGN.md section 7.3):

* ``runs/<name>/run.json`` holds the configuration fingerprint, seeds and the versions of
  Python, numpy, scipy, scikit-learn and every library under test; resuming with a
  different fingerprint is refused unless ``--force``.
* Units run in a ``ProcessPoolExecutor`` with at most 4 workers; each worker sets
  ``OMP_NUM_THREADS=1`` and ``torch.set_num_threads(1)``.
* The parent process is the only writer: each finished unit is appended as one JSON line
  to ``units.jsonl`` (flushed and fsynced); a rerun skips unit ids already present.
* Progress (done/total, rate, ETA) is appended to ``progress.log`` after every unit.
"""

from __future__ import annotations
