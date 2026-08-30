"""ConversationNarrative — internal flowed interpretation. Not Presentation."""

from __future__ import annotations

from dataclasses import dataclass

STATUS_PARTIAL = "partial"
STATUS_INSUFFICIENT = "insufficient"
STATUS_INVALID = "invalid"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_PARTIAL,
        STATUS_INSUFFICIENT,
        STATUS_INVALID,
    }
)


@dataclass(frozen=True, slots=True)
class ConversationReference:
    """Provenance copied from interpretation. Conversation does not invent sources."""

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
class ConversationNarrative:
    """Internal conversation flow. Not Action. Not Presentation."""

    observation: str | None
    reasoning: str | None
    meaning: str | None
    impact: str | None
    recommendation: str | None
    closing: str | None
    flow: str
    references: tuple[ConversationReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No unrelated payload."""
        rows = [entry.to_trace_record() for entry in self.references]
        rows.append(
            {
                "field": "flow",
                "merged_closing": self.closing is None,
                "status": self.status,
            }
        )
        return rows
