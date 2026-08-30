"""OverviewSummary — first customer-facing Narrative V2 object. Shadow only."""

from __future__ import annotations

from dataclasses import dataclass

STATUS_COMPLETE = "complete"
STATUS_PARTIAL = "partial"
STATUS_INSUFFICIENT = "insufficient"
STATUS_INVALID = "invalid"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_COMPLETE,
        STATUS_PARTIAL,
        STATUS_INSUFFICIENT,
        STATUS_INVALID,
    }
)

HEADLINE_WORD_LIMIT = 25
SUMMARY_SENTENCE_MIN = 2
SUMMARY_SENTENCE_MAX = 4
CONCLUSION_SENTENCE_MAX = 2


@dataclass(frozen=True, slots=True)
class SummaryReference:
    """Provenance for one populated Overview field."""

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
class OverviewSummary:
    """Executive summary. Not Interpretation. Not Action. Not Presentation."""

    headline: str | None
    summary: str | None
    identity: str | None
    balance: str | None
    conclusion: str | None
    references: tuple[SummaryReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No unrelated payload."""
        return [entry.to_trace_record() for entry in self.references]
