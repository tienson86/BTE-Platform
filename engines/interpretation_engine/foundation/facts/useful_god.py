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
    selected_entity_type: str = ""
    favorable_entity_types: tuple[str, ...] = ()
    unfavorable_entity_types: tuple[str, ...] = ()

    def entity_type_of(self, value: str) -> str:
        """Return canonical K2.1 entity type already stored for this value."""
        text = str(value or "").strip()
        if not text:
            return ""
        if text == self.selected and self.selected_entity_type:
            return self.selected_entity_type
        for name, kind in zip(self.favorable_gods, self.favorable_entity_types):
            if name == text and kind:
                return kind
        for name, kind in zip(self.unfavorable_gods, self.unfavorable_entity_types):
            if name == text and kind:
                return kind
        return ""

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
            "selected_entity_type": self.selected_entity_type,
            "favorable_entity_types": list(self.favorable_entity_types),
            "unfavorable_entity_types": list(self.unfavorable_entity_types),
        }


def lookup_useful_god_entity_type(key: str) -> str:
    """Copy K2.1 entity_type from knowledge. Do not guess from the label."""
    text = str(key or "").strip()
    if not text:
        return ""
    from engines.interpretation_engine.foundation.knowledge.service import (
        retrieve_knowledge,
    )

    entity = retrieve_knowledge("UsefulGod", text)
    if entity is None:
        return ""
    return str(entity.entity_type or "")
