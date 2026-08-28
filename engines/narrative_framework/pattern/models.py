"""INT-02D Pattern Narrative published models."""

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
from engines.narrative_framework.pattern.constants import (
    PATTERN_BLOCK_TITLES,
    PATTERN_BLOCKS,
    SOURCE_PATH,
    TOPIC_ID,
    UNIT_SCHEMA,
)


@dataclass(slots=True)
class PatternEvidence:
    """Canonical Pattern facts copied from published engine output."""

    pattern_name: str = ""
    pattern_type: str = ""
    pattern_class: str = ""
    temperature_state: str = ""
    dieu_hau: str = ""
    special_pattern: str = ""
    winning_rule: str = ""
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    confidence: float | None = None
    evidence_compact: str = ""
    success_reason: str = ""
    failure_reason: str = ""
    clash_status: str = ""
    combination_status: str = ""
    dung_than: str = ""
    hy_than: str = ""
    ky_than: str = ""
    recommendations: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    missing: tuple[str, ...] = ()
    source_path: str = SOURCE_PATH

    def to_dict(self) -> dict[str, Any]:
        """Serialize copied Pattern facts."""
        return {
            "pattern_name": self.pattern_name,
            "pattern_type": self.pattern_type,
            "pattern_class": self.pattern_class,
            "temperature_state": self.temperature_state,
            "dieu_hau": self.dieu_hau,
            "special_pattern": self.special_pattern,
            "winning_rule": self.winning_rule,
            "matched_rules": list(self.matched_rules),
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "evidence_compact": self.evidence_compact,
            "success_reason": self.success_reason,
            "failure_reason": self.failure_reason,
            "clash_status": self.clash_status,
            "combination_status": self.combination_status,
            "dung_than": self.dung_than,
            "hy_than": self.hy_than,
            "ky_than": self.ky_than,
            "recommendations": list(self.recommendations),
            "metadata": dict(self.metadata),
            "missing": list(self.missing),
            "source_path": self.source_path,
        }


@dataclass(slots=True)
class PatternNarrativeBlock:
    """One Pattern narrative block. Always present."""

    slot: str
    sentences: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return PATTERN_BLOCK_TITLES[self.slot]

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
class PatternNarrativeEvidencePack:
    """Classified Pattern evidence. Group lists are projections, not copies."""

    raw_evidence: PatternEvidence
    evidence_items: tuple[NarrativeEvidenceItem, ...] = ()

    @property
    def positive_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that support the published Pattern."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_POSITIVE
        )

    @property
    def neutral_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items with no directional Pattern contribution."""
        return tuple(
            item
            for item in self.evidence_items
            if item.classification == CLASSIFICATION_NEUTRAL
        )

    @property
    def negative_evidence(self) -> tuple[NarrativeEvidenceItem, ...]:
        """Items that work against the published Pattern."""
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
class PatternNarrativeUnit:
    """Published Pattern narrative: evidence plus five speech blocks."""

    evidence: PatternEvidence
    observation: PatternNarrativeBlock
    reasoning: PatternNarrativeBlock
    impact: PatternNarrativeBlock
    recommendation: PatternNarrativeBlock
    summary: PatternNarrativeBlock
    status: str = "insufficient"
    topic_id: str = TOPIC_ID
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_pack: PatternNarrativeEvidencePack | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Pattern narrative unit."""
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
            "block_order": list(PATTERN_BLOCKS),
        }
        if self.evidence_pack is not None:
            payload["evidence_pack"] = self.evidence_pack.to_dict()
        return payload
