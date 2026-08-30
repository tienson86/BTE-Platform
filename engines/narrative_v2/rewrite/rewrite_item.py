"""RewriteItem — one customer-language unit. Not a final paragraph."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RewriteReference:
    """Trace from a rewrite unit to approved knowledge."""

    knowledge_id: str
    source_path: str
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RewriteItem:
    """Unit rewrite. Not Summary, Interpretation, or Action Plan."""

    rewrite_id: str
    semantic_key: str
    domain: str
    source_knowledge_ids: tuple[str, ...]
    source_reasoning_ids: tuple[str, ...]
    source_evidence_ids: tuple[str, ...]
    source_meaning: str
    normalized_meaning: str
    customer_language: str
    strategy: str
    style: str
    status: str
    references: tuple[RewriteReference, ...]
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row. No final Narrative paragraph."""
        return {
            "rewrite_id": self.rewrite_id,
            "semantic_key": self.semantic_key,
            "source_knowledge_ids": list(self.source_knowledge_ids),
            "source_meaning": self.source_meaning,
            "strategy": self.strategy,
            "status": self.status,
            "customer_language": self.customer_language,
        }
