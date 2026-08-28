"""INT-02C Useful God Narrative published models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.useful_god.constants import (
    SOURCE_PATH,
    TOPIC_ID,
    UNIT_SCHEMA,
    USEFUL_GOD_BLOCK_TITLES,
    USEFUL_GOD_BLOCKS,
)


@dataclass(slots=True)
class UsefulGodEvidence:
    """Canonical Useful God facts copied from published engine output."""

    useful_god: str = ""
    useful_display: str = ""
    useful_ten_god: str = ""
    useful_stem: str = ""
    useful_element: str = ""
    favorable_gods: tuple[str, ...] = ()
    unfavorable_gods: tuple[str, ...] = ()
    favorable_display: str = ""
    unfavorable_display: str = ""
    winning_rule_id: str = ""
    winning_rule_group: str = ""
    reasoning: str = ""
    confidence: float | None = None
    matched_rules: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    climate_display: str = ""
    climate_reason: str = ""
    climate_preference_label: str = ""
    strength_reason: str = ""
    season_reason: str = ""
    temperature_reason: str = ""
    balance_reason: str = ""
    overall_incomplete: bool = False
    missing: tuple[str, ...] = ()
    source_path: str = SOURCE_PATH

    def to_dict(self) -> dict[str, Any]:
        """Serialize copied Useful God facts."""
        return {
            "useful_god": self.useful_god,
            "useful_display": self.useful_display,
            "useful_ten_god": self.useful_ten_god,
            "useful_stem": self.useful_stem,
            "useful_element": self.useful_element,
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "favorable_display": self.favorable_display,
            "unfavorable_display": self.unfavorable_display,
            "winning_rule_id": self.winning_rule_id,
            "winning_rule_group": self.winning_rule_group,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "matched_rules": list(self.matched_rules),
            "recommendations": list(self.recommendations),
            "climate_display": self.climate_display,
            "climate_reason": self.climate_reason,
            "climate_preference_label": self.climate_preference_label,
            "strength_reason": self.strength_reason,
            "season_reason": self.season_reason,
            "temperature_reason": self.temperature_reason,
            "balance_reason": self.balance_reason,
            "overall_incomplete": self.overall_incomplete,
            "missing": list(self.missing),
            "source_path": self.source_path,
        }


@dataclass(slots=True)
class UsefulGodNarrativeBlock:
    """One Useful God narrative block. Always present."""

    slot: str
    sentences: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return USEFUL_GOD_BLOCK_TITLES[self.slot]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the block."""
        return {
            "slot": self.slot,
            "title": self.title,
            "sentences": list(self.sentences),
            "source_paths": list(self.source_paths),
            "available": self.available,
            "insufficient": self.insufficient,
            "empty_copy": INSUFFICIENT_COPY if self.insufficient else "",
        }


@dataclass(slots=True)
class UsefulGodNarrativeEvidencePack:
    """Classified Useful God evidence. Group lists are projections, not copies."""

    raw_evidence: UsefulGodEvidence
    evidence_items: tuple[NarrativeEvidenceItem, ...] = ()

    @property
    def positive_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that support the published Useful God."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_POSITIVE
        )

    @property
    def neutral_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items with no directional Useful God contribution."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_NEUTRAL
        )

    @property
    def negative_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that restrain or conflict with the published Useful God."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_NEGATIVE
        )

    def item(self, component: str) -> NarrativeEvidenceItem | None:
        """Return the first item for a component, if present."""
        for entry in self.evidence_items:
            if entry.component == component:
                return entry
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize raw evidence plus classified projections."""
        return {
            "raw_evidence": self.raw_evidence.to_dict(),
            "evidence_items": [item.to_dict() for item in self.evidence_items],
            "positive_evidence": [item.to_dict() for item in self.positive_evidence],
            "neutral_evidence": [item.to_dict() for item in self.neutral_evidence],
            "negative_evidence": [item.to_dict() for item in self.negative_evidence],
        }


@dataclass(slots=True)
class UsefulGodNarrativeUnit:
    """Published Useful God narrative: evidence plus five speech blocks."""

    evidence: UsefulGodEvidence
    observation: UsefulGodNarrativeBlock
    reasoning: UsefulGodNarrativeBlock
    impact: UsefulGodNarrativeBlock
    recommendation: UsefulGodNarrativeBlock
    summary: UsefulGodNarrativeBlock
    status: str = "insufficient"
    topic_id: str = TOPIC_ID
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_pack: UsefulGodNarrativeEvidencePack | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Useful God narrative unit."""
        payload = {
            "topic_id": self.topic_id,
            "schema_version": self.schema_version,
            "status": self.status,
            "evidence": self.evidence.to_dict(),
            "observation": self.observation.to_dict(),
            "reasoning": self.reasoning.to_dict(),
            "impact": self.impact.to_dict(),
            "recommendation": self.recommendation.to_dict(),
            "summary": self.summary.to_dict(),
            "evidence_refs": list(self.evidence_refs),
            "block_order": list(USEFUL_GOD_BLOCKS),
        }
        if self.evidence_pack is not None:
            payload["evidence_pack"] = self.evidence_pack.to_dict()
        return payload
