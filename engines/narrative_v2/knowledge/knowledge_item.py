"""KnowledgeItem — one approved knowledge record bound to reasoning."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.knowledge.knowledge_reference import KnowledgeReference


@dataclass(frozen=True, slots=True)
class KnowledgeItem:
    """Approved knowledge copy. Not rewritten. Not an Action Plan."""

    knowledge_id: str
    domain: str
    semantic_key: str
    knowledge_type: str
    status: str
    technical_meaning: str | None
    customer_meaning_candidate: str | None
    boundaries: tuple[str, ...]
    recommendations: tuple[str, ...]
    references: tuple[KnowledgeReference, ...]
    source_path: str
    version: str | None
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row. No full source dump."""
        ref = self.references[0] if self.references else None
        return {
            "semantic_key": self.semantic_key,
            "reasoning_ids": list(ref.reasoning_ids) if ref is not None else [],
            "knowledge_id": self.knowledge_id,
            "source": self.source_path,
            "status": self.status,
            "version": self.version,
            "resolution_status": "resolved",
        }
