"""NarrativeKnowledgeContext — approved knowledge matches and gaps."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.knowledge.knowledge_item import KnowledgeItem
from engines.narrative_v2.knowledge.knowledge_reference import KnowledgeReference


@dataclass(frozen=True, slots=True)
class KnowledgeMatch:
    """One semantic_key → knowledge_id binding."""

    semantic_key: str
    knowledge_id: str
    source: str
    status: str
    version: str | None
    resolution_status: str
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class KnowledgeUnresolved:
    """Explicit unresolved semantic key. Prefer this over guessing."""

    semantic_key: str
    reason: str
    required_source: str
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row for an unresolved key."""
        return {
            "semantic_key": self.semantic_key,
            "reasoning_ids": list(self.reasoning_ids),
            "knowledge_id": None,
            "source": self.required_source,
            "status": None,
            "version": None,
            "resolution_status": "unresolved",
        }


@dataclass(frozen=True, slots=True)
class KnowledgeContractGap:
    """Knowledge contract gap. Not filled in this sprint."""

    field: str
    reason: str


@dataclass(frozen=True, slots=True)
class NarrativeKnowledgeContext:
    """Resolved knowledge. No final summary, interpretation, or action plan."""

    items: tuple[KnowledgeItem, ...]
    matches: tuple[KnowledgeMatch, ...]
    unresolved: tuple[KnowledgeUnresolved, ...]
    references: tuple[KnowledgeReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str
    contract_gaps: tuple[KnowledgeContractGap, ...] = ()

    def item(self, knowledge_id: str) -> KnowledgeItem | None:
        """Return one item by stable knowledge id."""
        for entry in self.items:
            if entry.knowledge_id == knowledge_id:
                return entry
        return None

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No customer narrative. No full file dump."""
        rows = [entry.to_trace_record() for entry in self.items]
        rows.extend(entry.to_trace_record() for entry in self.unresolved)
        return rows
