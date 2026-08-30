"""ReasoningNode — one internal semantic graph vertex."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.reasoning.reasoning_reference import ReasoningReference

KIND_OBSERVATION = "observation"
KIND_CAUSE = "cause"
KIND_RELATION = "relation"
KIND_IMPACT_CANDIDATE = "impact_candidate"
KIND_BOUNDARY = "boundary"

ALLOWED_KINDS: frozenset[str] = frozenset(
    {
        KIND_OBSERVATION,
        KIND_CAUSE,
        KIND_RELATION,
        KIND_IMPACT_CANDIDATE,
        KIND_BOUNDARY,
    }
)

STATUS_ACTIVE = "active"
STATUS_INSUFFICIENT = "insufficient"
STATUS_CONFLICT = "conflict"
STATUS_QUALIFIED = "qualified"
STATUS_GAP = "gap"

ALLOWED_NODE_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_ACTIVE,
        STATUS_INSUFFICIENT,
        STATUS_CONFLICT,
        STATUS_QUALIFIED,
        STATUS_GAP,
    }
)


@dataclass(frozen=True, slots=True)
class ReasoningNode:
    """Internal semantic node. No customer prose. No recommendation."""

    reasoning_id: str
    domain: str
    kind: str
    semantic_key: str
    evidence_ids: tuple[str, ...]
    relation: str
    priority: int
    status: str
    references: tuple[ReasoningReference, ...]
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "reasoning_id": self.reasoning_id,
            "semantic_key": self.semantic_key,
            "evidence_ids": list(self.evidence_ids),
            "relation": self.relation,
            "priority": self.priority,
            "status": self.status,
        }
