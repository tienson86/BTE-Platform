"""Shen Sha analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability, EvidenceStatus


@dataclass(frozen=True, slots=True)
class ShenShaItemFact:
    """One Shen Sha match — never fabricate evidence."""

    name: str
    position: str
    source: str
    rule_id: str
    evidence: str
    evidence_status: EvidenceStatus
    matched_condition: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize one Shen Sha item."""
        return {
            "name": self.name,
            "position": self.position,
            "source": self.source,
            "rule_id": self.rule_id,
            "evidence": self.evidence,
            "evidence_status": self.evidence_status.value,
            "matched_condition": self.matched_condition,
        }


@dataclass(frozen=True, slots=True)
class ShenShaInterpretationFacts:
    """Structured Shen Sha truth — owned by ShenShaService."""

    items: tuple[ShenShaItemFact, ...]
    status: DataAvailability
    owner: str = DOMAIN_OWNERS["shensha"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize Shen Sha facts."""
        return {
            "items": [item.to_dict() for item in self.items],
            "status": self.status.value,
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
