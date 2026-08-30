"""InterpretationNarrative — customer interpretation. Shadow only. Not Action."""

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

OVERVIEW_SENTENCE_MIN = 2
OVERVIEW_SENTENCE_MAX = 4
CLOSING_SENTENCE_MAX = 2

FORMULA_STAGES: tuple[str, ...] = (
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "closing",
)

CONTENT_FIELDS: tuple[str, ...] = ("overview",) + FORMULA_STAGES


@dataclass(frozen=True, slots=True)
class InterpretationReference:
    """Provenance for one populated Interpretation field."""

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
class InterpretationNarrative:
    """Customer interpretation. Not Summary. Not Action. Not Presentation."""

    overview: str | None
    observation: str | None
    reasoning: str | None
    meaning: str | None
    impact: str | None
    recommendation: str | None
    closing: str | None
    references: tuple[InterpretationReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No unrelated payload."""
        return [entry.to_trace_record() for entry in self.references]
