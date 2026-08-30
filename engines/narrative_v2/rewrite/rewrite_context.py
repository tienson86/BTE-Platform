"""CommercialRewriteContext — unit rewrites only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.rewrite.rewrite_item import RewriteItem, RewriteReference


@dataclass(frozen=True, slots=True)
class RewriteUnresolved:
    """Explicit unresolved rewrite. Prefer this over inventing language."""

    semantic_key: str
    reason: str
    knowledge_ids: tuple[str, ...]
    source_meaning: str | None = None

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row for an unresolved rewrite."""
        return {
            "rewrite_id": None,
            "semantic_key": self.semantic_key,
            "source_knowledge_ids": list(self.knowledge_ids),
            "source_meaning": self.source_meaning,
            "strategy": None,
            "status": "unresolved",
        }


@dataclass(frozen=True, slots=True)
class RewriteContractGap:
    """Rewrite contract gap. Not filled in this sprint."""

    field: str
    reason: str


@dataclass(frozen=True, slots=True)
class CommercialRewriteContext:
    """Rewrite units. No overview, interpretation, action plan, or presentation."""

    items: tuple[RewriteItem, ...]
    unresolved: tuple[RewriteUnresolved, ...]
    references: tuple[RewriteReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str
    contract_gaps: tuple[RewriteContractGap, ...] = ()

    def item(self, rewrite_id: str) -> RewriteItem | None:
        """Return one rewrite unit by stable id."""
        for entry in self.items:
            if entry.rewrite_id == rewrite_id:
                return entry
        return None

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No final Narrative dump."""
        rows = [entry.to_trace_record() for entry in self.items]
        rows.extend(entry.to_trace_record() for entry in self.unresolved)
        return rows
