"""INT-02F integrated narrative models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.integration.constants import (
    INTEGRATED_BLOCK_TITLES,
    INTEGRATED_BLOCKS,
    SOURCE_PATH,
    TOPIC_ID,
    UNIT_SCHEMA,
)


@dataclass(slots=True)
class IntegratedNarrativeBlock:
    """One integrated narrative block. Always present."""

    slot: str
    sentences: tuple[str, ...] = ()
    source_paths: tuple[str, ...] = ()
    topic_ids: tuple[str, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return INTEGRATED_BLOCK_TITLES[self.slot]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the block."""
        return {
            "slot": self.slot,
            "title": self.title,
            "sentences": list(self.sentences),
            "source_paths": list(self.source_paths),
            "topic_ids": list(self.topic_ids),
            "available": self.available,
            "insufficient": self.insufficient,
            "empty_copy": INSUFFICIENT_COPY if self.insufficient else "",
        }


@dataclass(slots=True)
class IntegratedNarrativeUnit:
    """Chart-level narrative assembled from frozen topic units."""

    executive_summary: IntegratedNarrativeBlock
    observation: IntegratedNarrativeBlock
    reasoning: IntegratedNarrativeBlock
    impact: IntegratedNarrativeBlock
    recommendation: IntegratedNarrativeBlock
    summary: IntegratedNarrativeBlock
    topics: tuple[str, ...] = ()
    status: str = "insufficient"
    topic_id: str = TOPIC_ID
    schema_version: str = UNIT_SCHEMA
    source_path: str = SOURCE_PATH
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the integrated narrative unit."""
        return {
            "topic_id": self.topic_id,
            "schema_version": self.schema_version,
            "source_path": self.source_path,
            "status": self.status,
            "topics": list(self.topics),
            "executive_summary": self.executive_summary.to_dict(),
            "observation": self.observation.to_dict(),
            "reasoning": self.reasoning.to_dict(),
            "impact": self.impact.to_dict(),
            "recommendation": self.recommendation.to_dict(),
            "summary": self.summary.to_dict(),
            "evidence_refs": list(self.evidence_refs),
            "block_order": list(INTEGRATED_BLOCKS),
        }
