"""Strength analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class StrengthInterpretationFacts:
    """Structured strength truth — owned by StrengthEngine."""

    level: str
    score: float
    label: str
    confidence: float
    evidence: tuple[str, ...]
    rule_ids: tuple[str, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["strength"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize strength facts."""
        return {
            "level": self.level,
            "score": self.score,
            "label": self.label,
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "rule_ids": list(self.rule_ids),
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
