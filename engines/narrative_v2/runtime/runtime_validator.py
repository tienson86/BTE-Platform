"""Narrative V2 skeleton validator.

``validate()`` always PASS unless pipeline ordering is invalid.
No semantic validation in N-IMP-01.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from engines.narrative_v2.runtime.runtime_pipeline import (
    CANONICAL_STAGES,
    PRE_VALIDATE_STAGES,
)


@dataclass(slots=True)
class ValidationOutcome:
    """Skeleton validation result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class RuntimeValidator:
    """Ordering-only validator."""

    def validate(self, executed_stages: Sequence[str]) -> ValidationOutcome:
        """PASS unless executed stages violate canonical order.

        Semantic, language, and customer-safety checks are out of scope.
        """
        executed = tuple(executed_stages)
        if executed == PRE_VALIDATE_STAGES:
            return ValidationOutcome(passed=True)
        if executed == CANONICAL_STAGES:
            return ValidationOutcome(passed=True)
        return ValidationOutcome(
            passed=False,
            reason="pipeline ordering invalid",
        )
