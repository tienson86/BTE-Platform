"""Pattern analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class PatternInterpretationFacts:
    """Structured pattern truth — owned by PatternEngine."""

    selected: str
    label: str
    confidence: float
    evidence: tuple[str, ...]
    rule_ids: tuple[str, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["pattern"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize pattern facts."""
        return {
            "selected": self.selected,
            "label": self.label,
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "rule_ids": list(self.rule_ids),
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
