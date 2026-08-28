"""INT-02B Strength Narrative published models."""

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
from engines.narrative_framework.strength.constants import (
    SOURCE_PATH,
    STRENGTH_BLOCK_TITLES,
    STRENGTH_BLOCKS,
    TOPIC_ID,
    UNIT_SCHEMA,
)


@dataclass(slots=True)
class StrengthEvidence:
    """Canonical Strength facts copied from published engine output."""

    season_strength: float | None = None
    root_strength: float | None = None
    support_strength: float | None = None
    control_strength: float | None = None
    drain_strength: float | None = None
    temperature_state: str = ""
    special_rules: tuple[str, ...] = ()
    special_rule_details: tuple[dict[str, Any], ...] = ()
    confidence: float | None = None
    strength_level: str = ""
    score: float | None = None
    reasoning: str = ""
    evidence_compact: str = ""
    missing: tuple[str, ...] = ()
    source_path: str = SOURCE_PATH

    def to_dict(self) -> dict[str, Any]:
        """Serialize copied Strength facts."""
        return {
            "season_strength": self.season_strength,
            "root_strength": self.root_strength,
            "support_strength": self.support_strength,
            "control_strength": self.control_strength,
            "drain_strength": self.drain_strength,
            "temperature_state": self.temperature_state,
            "special_rules": list(self.special_rules),
            "special_rule_details": [dict(item) for item in self.special_rule_details],
            "confidence": self.confidence,
            "strength_level": self.strength_level,
            "score": self.score,
            "reasoning": self.reasoning,
            "evidence_compact": self.evidence_compact,
            "missing": list(self.missing),
            "source_path": self.source_path,
        }


@dataclass(slots=True)
class StrengthNarrativeBlock:
    """One Strength narrative block. Always present."""

    slot: str
    sentences: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return STRENGTH_BLOCK_TITLES[self.slot]

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
class StrengthNarrativeEvidencePack:
    """Classified Strength evidence. Group lists are projections, not copies."""

    raw_evidence: StrengthEvidence
    evidence_items: tuple[NarrativeEvidenceItem, ...] = ()

    @property
    def positive_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that increase Day Master strength."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_POSITIVE
        )

    @property
    def neutral_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items with no directional Strength contribution."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_NEUTRAL
        )

    @property
    def negative_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that reduce Day Master strength."""
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
class StrengthNarrativeUnit:
    """Published Strength narrative: evidence plus five speech blocks."""

    evidence: StrengthEvidence
    observation: StrengthNarrativeBlock
    reasoning: StrengthNarrativeBlock
    impact: StrengthNarrativeBlock
    recommendation: StrengthNarrativeBlock
    summary: StrengthNarrativeBlock
    status: str = "insufficient"
    topic_id: str = TOPIC_ID
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_pack: StrengthNarrativeEvidencePack | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Strength narrative unit."""
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
            "block_order": list(STRENGTH_BLOCKS),
        }
        if self.evidence_pack is not None:
            payload["evidence_pack"] = self.evidence_pack.to_dict()
        return payload
