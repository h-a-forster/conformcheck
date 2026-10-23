"""Public helpers for library authors who want conformance checks in their own CI.

Planned API (milestone M7, docs/DESIGN.md section 8.4)::

    from conformcheck.testing import check_split_regressor

    def my_split(x_cal, y_cal, x_test, alpha, model):  # returns (m, 2) intervals
        ...

    report = check_split_regressor(my_split, n=(9, 19, 99), alpha=(0.1, 0.2), reps=200)
    report.assert_valid(allow_conservative=False)

``check_split_classifier`` is the classification analogue (returns boolean sets).
"""

from __future__ import annotations
