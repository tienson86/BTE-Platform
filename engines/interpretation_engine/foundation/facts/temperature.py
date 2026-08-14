"""Temperature analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class TemperatureInterpretationFacts:
    """Structured temperature truth — owned by TemperatureEngine."""

    level: str
    score: float
    label: str
    recommendations: tuple[str, ...]
    evidence: tuple[str, ...]
    rule_ids: tuple[str, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["temperature"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize temperature facts."""
        return {
            "level": self.level,
            "score": self.score,
            "label": self.label,
            "recommendations": list(self.recommendations),
            "evidence": list(self.evidence),
            "rule_ids": list(self.rule_ids),
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
