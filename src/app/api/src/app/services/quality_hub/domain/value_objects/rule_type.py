"""Value object for the kind of rule being enforced."""

from __future__ import annotations

from enum import Enum

class RuleType(Enum):
    COVERAGE_MIN = "coverage_min"
    TESTS_MAX_FAIL = "tests_max_fail"
    LINT_MAX_ERROR = "lint_max_error"
    SAST_MAX_CRITICAL = "sast_max_critical"
