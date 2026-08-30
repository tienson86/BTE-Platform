"""DecisionItem — internal priority choice. Not an Action. Not astrology."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionReference:
    """Trace from a Decision to rewrite and knowledge."""

    rewrite_id: str
    knowledge_id: str
    source_path: str
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DecisionItem:
    """What should be prioritized. Not yet the concrete task."""

    decision_id: str
    semantic_key: str
    title: str
    description: str
    priority: int
    source_rewrite_ids: tuple[str, ...]
    source_knowledge_ids: tuple[str, ...]
    source_reasoning_ids: tuple[str, ...]
    source_evidence_ids: tuple[str, ...]
    status: str
    references: tuple[DecisionReference, ...]
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "decision_id": self.decision_id,
            "semantic_key": self.semantic_key,
            "title": self.title,
            "priority": self.priority,
            "source_rewrite_ids": list(self.source_rewrite_ids),
            "source_knowledge_ids": list(self.source_knowledge_ids),
            "status": self.status,
        }
