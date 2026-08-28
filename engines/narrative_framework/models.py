"""INT-02A Topic Narrative models. Contracts only — no composition runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .contracts import (
    BLOCK_IDS,
    BLOCK_TITLES_VI,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    NARRATIVE_BLOCKS,
)
from .exceptions import NarrativeFrameworkError

_VALID_STATUS = frozenset({"complete", "partial", "insufficient"})
_VALID_OWNERS = frozenset({"engine_result", "sentence_library", "narrative_framework"})


@dataclass(slots=True)
class NarrativeSentence:
    """One customer-facing sentence bound to a published fact or marked empty."""

    sentence_id: str
    role: str
    text: str
    source_path: str
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the sentence contract."""
        return {
            "sentence_id": self.sentence_id,
            "role": self.role,
            "text": self.text,
            "source_path": self.source_path,
            "owner": self.owner,
        }


@dataclass(slots=True)
class NarrativeBlock:
    """One required narrative block. Always present, even when insufficient."""

    slot: str
    sentences: tuple[NarrativeSentence, ...] = ()
    available: bool = False
    insufficient: bool = True

    @property
    def section_id(self) -> str:
        """Canonical section identifier."""
        return BLOCK_IDS[self.slot]

    @property
    def title(self) -> str:
        """Canonical Vietnamese title."""
        return BLOCK_TITLES_VI[self.slot]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the block contract."""
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
class TopicEvidencePack:
    """Read-only published facts for one topic. Never recalculated."""

    topic_id: str
    facts: Mapping[str, Any] = field(default_factory=dict)
    missing: tuple[str, ...] = ()
    source_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize the evidence pack."""
        return {
            "topic_id": self.topic_id,
            "facts": dict(self.facts),
            "missing": list(self.missing),
            "source_path": self.source_path,
        }


@dataclass(slots=True)
class TopicNarrativeUnit:
    """Canonical five-block narrative for one analytical topic."""

    topic_id: str
    source_path: str
    blocks: Mapping[str, NarrativeBlock]
    status: str
    evidence_refs: tuple[str, ...] = ()
    schema_version: str = FRAMEWORK_VERSION

    def __post_init__(self) -> None:
        """Reject units that drop or reorder required blocks."""
        if tuple(self.blocks.keys()) != NARRATIVE_BLOCKS:
            raise NarrativeFrameworkError(
                "TopicNarrativeUnit.blocks must contain the five required slots in order."
            )
        if self.status not in _VALID_STATUS:
            raise NarrativeFrameworkError(f"Invalid status: {self.status}")
        for slot, block in self.blocks.items():
            if block.slot != slot:
                raise NarrativeFrameworkError("Block slot must match map key.")
            for sentence in block.sentences:
                if sentence.role != slot:
                    raise NarrativeFrameworkError("Sentence role must match parent block.")
                if sentence.owner not in _VALID_OWNERS:
                    raise NarrativeFrameworkError(f"Invalid sentence owner: {sentence.owner}")

    def to_dict(self) -> dict[str, Any]:
        """Serialize the topic narrative unit."""
        return {
            "topic_id": self.topic_id,
            "source_path": self.source_path,
            "blocks": {slot: block.to_dict() for slot, block in self.blocks.items()},
            "status": self.status,
            "evidence_refs": list(self.evidence_refs),
            "schema_version": self.schema_version,
        }


def empty_topic_unit(topic_id: str, source_path: str) -> TopicNarrativeUnit:
    """Return an honest insufficient unit with all five blocks present."""
    blocks = {
        slot: NarrativeBlock(slot=slot, sentences=(), available=False, insufficient=True)
        for slot in NARRATIVE_BLOCKS
    }
    return TopicNarrativeUnit(
        topic_id=topic_id,
        source_path=source_path,
        blocks=blocks,
        status="insufficient",
    )
