"""Useful God analytical truth facts for interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class UsefulGodCandidateFact:
    """One useful-god candidate with rule evidence."""

    useful_god: str
    rule_id: str
    confidence: float
    reason: str
    candidate_type: str = ""
    rule_group: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize one candidate."""
        return {
            "useful_god": self.useful_god,
            "rule_id": self.rule_id,
            "confidence": self.confidence,
            "reason": self.reason,
            "candidate_type": self.candidate_type,
            "rule_group": self.rule_group,
        }


@dataclass(frozen=True, slots=True)
class UsefulGodInterpretationFacts:
    """Structured useful-god truth — owned by UsefulGodEngine."""

    selected: str
    candidate_type: str
    confidence: float
    reason: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    candidates: tuple[UsefulGodCandidateFact, ...]
    rule_ids: tuple[str, ...]
    presence: DataAvailability
    status: DataAvailability
    day_master: str
    day_master_element: str
    month_branch: str
    season: str
    strength_level: str
    strength_score: float
    temperature_level: str
    five_elements: dict[str, int | None]
    owner: str = DOMAIN_OWNERS["useful_god"]
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize useful-god facts."""
        return {
            "selected": self.selected,
            "candidate_type": self.candidate_type,
            "confidence": self.confidence,
            "reason": self.reason,
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "candidates": [item.to_dict() for item in self.candidates],
            "rule_ids": list(self.rule_ids),
            "presence": self.presence.value,
            "status": self.status.value,
            "day_master": self.day_master,
            "day_master_element": self.day_master_element,
            "month_branch": self.month_branch,
            "season": self.season,
            "strength_level": self.strength_level,
            "strength_score": self.strength_score,
            "temperature_level": self.temperature_level,
            "five_elements": dict(self.five_elements),
            "owner": self.owner,
            "diagnostics": list(self.diagnostics),
        }
