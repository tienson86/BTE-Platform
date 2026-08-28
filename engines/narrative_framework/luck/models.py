"""INT-02E Luck Narrative published models."""

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
from engines.narrative_framework.luck.constants import (
    LUCK_BLOCK_TITLES,
    LUCK_BLOCKS,
    SOURCE_PATH,
    TOPIC_ID,
    UNIT_SCHEMA,
)


@dataclass(slots=True)
class LuckEvidence:
    """Canonical Luck facts copied from published engine output."""

    current_cycle: str = ""
    current_liunian: str = ""
    cycle_index: int | None = None
    age: int | None = None
    reference_year: int | None = None
    timeline: str = ""
    reasoning: str = ""
    confidence: float | None = None
    recommendations: tuple[str, ...] = ()
    luck_stage: str = ""
    support_elements: tuple[str, ...] = ()
    attack_elements: tuple[str, ...] = ()
    support_level: str = ""
    attack_level: str = ""
    missing: tuple[str, ...] = ()
    source_path: str = SOURCE_PATH

    def to_dict(self) -> dict[str, Any]:
        """Serialize copied Luck facts."""
        return {
            "current_cycle": self.current_cycle,
            "current_liunian": self.current_liunian,
            "cycle_index": self.cycle_index,
            "age": self.age,
            "reference_year": self.reference_year,
            "timeline": self.timeline,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "recommendations": list(self.recommendations),
            "luck_stage": self.luck_stage,
            "support_elements": list(self.support_elements),
            "attack_elements": list(self.attack_elements),
            "support_level": self.support_level,
            "attack_level": self.attack_level,
            "missing": list(self.missing),
            "source_path": self.source_path,
        }


@dataclass(slots=True)
class LuckNarrativeBlock:
    """One Luck narrative block. Always present."""

    slot: str
    sentences: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return LUCK_BLOCK_TITLES[self.slot]

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
class LuckNarrativeEvidencePack:
    """Classified Luck evidence. Group lists are projections, not copies."""

    raw_evidence: LuckEvidence
    evidence_items: tuple[NarrativeEvidenceItem, ...] = ()

    @property
    def positive_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that support the published Luck reading."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_POSITIVE
        )

    @property
    def neutral_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items with no directional Luck contribution."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_NEUTRAL
        )

    @property
    def negative_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that work against the published Luck reading."""
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
class LuckNarrativeUnit:
    """Published Luck narrative: evidence plus five speech blocks."""

    evidence: LuckEvidence
    observation: LuckNarrativeBlock
    reasoning: LuckNarrativeBlock
    impact: LuckNarrativeBlock
    recommendation: LuckNarrativeBlock
    summary: LuckNarrativeBlock
    status: str = "insufficient"
    topic_id: str = TOPIC_ID
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_pack: LuckNarrativeEvidencePack | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Luck narrative unit."""
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
            "block_order": list(LUCK_BLOCKS),
        }
        if self.evidence_pack is not None:
            payload["evidence_pack"] = self.evidence_pack.to_dict()
        return payload
