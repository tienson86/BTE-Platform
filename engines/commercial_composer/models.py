"""INT-03A Commercial Narrative models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.commercial_composer.contracts import (
    COMMERCIAL_SECTIONS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    SECTION_IDS,
    SECTION_TITLES_VI,
    SOURCE_PATH,
    UNIT_SCHEMA,
)
from engines.commercial_composer.exceptions import CommercialComposerError
from engines.commercial_composer.rules import CUSTOMER_SECTION_ORDER

_VALID_STATUS = frozenset({"complete", "partial", "insufficient"})


@dataclass(slots=True)
class CommercialSentence:
    """One commercial sentence traced to Integrated Narrative."""

    text: str
    slot: str
    integrated_slots: tuple[str, ...]
    source_paths: tuple[str, ...] = ()
    topic_ids: tuple[str, ...] = ()
    integrated_sentence_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the sentence."""
        return {
            "text": self.text,
            "slot": self.slot,
            "integrated_slots": list(self.integrated_slots),
            "source_paths": list(self.source_paths),
            "topic_ids": list(self.topic_ids),
            "integrated_sentence_ids": list(self.integrated_sentence_ids),
        }


@dataclass(slots=True)
class CommercialNarrativeBlock:
    """One required commercial section. Always present."""

    slot: str
    sentences: tuple[CommercialSentence, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def section_id(self) -> str:
        """Canonical section identifier."""
        return SECTION_IDS[self.slot]

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return SECTION_TITLES_VI[self.slot]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the section."""
        return {
            "slot": self.slot,
            "section_id": self.section_id,
            "title": self.title,
            "sentences": [sentence.to_dict() for sentence in self.sentences],
            "available": self.available,
            "insufficient": self.insufficient,
            "empty_copy": INSUFFICIENT_COPY if self.insufficient else "",
        }


@dataclass(slots=True)
class CommercialNarrativeUnit:
    """Customer-facing commercial reading derived from Integrated Narrative."""

    executive_summary: CommercialNarrativeBlock
    overall_reading: CommercialNarrativeBlock
    current_situation: CommercialNarrativeBlock
    strengths: CommercialNarrativeBlock
    risks: CommercialNarrativeBlock
    key_recommendation: CommercialNarrativeBlock
    conclusion: CommercialNarrativeBlock
    status: str = "insufficient"
    source_path: str = SOURCE_PATH
    schema_version: str = UNIT_SCHEMA
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Reject units that drop or mis-slot required sections."""
        if self.status not in _VALID_STATUS:
            raise CommercialComposerError(f"Invalid status: {self.status}")
        for slot in COMMERCIAL_SECTIONS:
            block = getattr(self, slot)
            if not isinstance(block, CommercialNarrativeBlock):
                raise CommercialComposerError(f"Missing commercial section: {slot}")
            if block.slot != slot:
                raise CommercialComposerError("Block slot must match unit field.")
            for sentence in block.sentences:
                if sentence.slot != slot:
                    raise CommercialComposerError("Sentence slot must match parent block.")
                if not sentence.integrated_slots:
                    raise CommercialComposerError(
                        "Commercial sentence must cite Integrated Narrative."
                    )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the commercial narrative unit."""
        return {
            "schema_version": self.schema_version,
            "source_path": self.source_path,
            "status": self.status,
            "executive_summary": self.executive_summary.to_dict(),
            "overall_reading": self.overall_reading.to_dict(),
            "current_situation": self.current_situation.to_dict(),
            "strengths": self.strengths.to_dict(),
            "risks": self.risks.to_dict(),
            "key_recommendation": self.key_recommendation.to_dict(),
            "conclusion": self.conclusion.to_dict(),
            "evidence_refs": list(self.evidence_refs),
            "section_order": list(COMMERCIAL_SECTIONS),
            "customer_section_order": list(CUSTOMER_SECTION_ORDER),
            "framework_version": FRAMEWORK_VERSION,
        }


def empty_commercial_block(slot: str) -> CommercialNarrativeBlock:
    """Return an insufficient commercial section."""
    return CommercialNarrativeBlock(
        slot=slot,
        sentences=(),
        available=False,
        insufficient=True,
    )


def empty_commercial_unit() -> CommercialNarrativeUnit:
    """Return a structurally complete insufficient unit."""
    return CommercialNarrativeUnit(
        executive_summary=empty_commercial_block("executive_summary"),
        overall_reading=empty_commercial_block("overall_reading"),
        current_situation=empty_commercial_block("current_situation"),
        strengths=empty_commercial_block("strengths"),
        risks=empty_commercial_block("risks"),
        key_recommendation=empty_commercial_block("key_recommendation"),
        conclusion=empty_commercial_block("conclusion"),
        status="insufficient",
    )
