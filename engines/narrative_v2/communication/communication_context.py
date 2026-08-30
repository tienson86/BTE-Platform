"""ConsultingNarrative — internal styled conversation. Not Presentation."""

from __future__ import annotations

from dataclasses import dataclass

STATUS_STYLED = "styled"
STATUS_PARTIAL = "partial"
STATUS_PASSTHROUGH = "passthrough"
STATUS_UNRESOLVED = "unresolved"
STATUS_REJECTED = "rejected"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_STYLED,
        STATUS_PARTIAL,
        STATUS_PASSTHROUGH,
        STATUS_UNRESOLVED,
        STATUS_REJECTED,
    }
)

SEGMENT_ROLES: tuple[str, ...] = (
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "closing",
)


@dataclass(frozen=True, slots=True)
class ConsultingReference:
    """Provenance copied from conversation. Style does not invent sources."""

    field: str
    rewrite_ids: tuple[str, ...]
    knowledge_ids: tuple[str, ...]
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "field": self.field,
            "rewrite_ids": list(self.rewrite_ids),
            "knowledge_ids": list(self.knowledge_ids),
            "reasoning_ids": list(self.reasoning_ids),
            "evidence_ids": list(self.evidence_ids),
        }


@dataclass(frozen=True, slots=True)
class StyledSegment:
    """One styled conversation turn. Meaning fingerprint must match source."""

    segment_id: str
    role: str
    source_text: str
    styled_text: str
    frame_id: str | None
    source_conversation_ids: tuple[str, ...]
    meaning_fingerprint: str
    status: str
    references: tuple[ConsultingReference, ...]
    metadata: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class ConsultingNarrative:
    """Internal consulting-style narrative. Not Action. Not Presentation."""

    flow: str
    segments: tuple[StyledSegment, ...]
    style_profile: str
    source_conversation_ids: tuple[str, ...]
    references: tuple[ConsultingReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No unrelated payload."""
        rows: list[dict[str, object]] = []
        for segment in self.segments:
            rows.append(
                {
                    "segment_id": segment.segment_id,
                    "role": segment.role,
                    "frame_id": segment.frame_id,
                    "status": segment.status,
                    "meaning_fingerprint": segment.meaning_fingerprint,
                    "source_conversation_ids": list(segment.source_conversation_ids),
                }
            )
        return rows
