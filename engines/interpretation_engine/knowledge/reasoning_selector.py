"""Deterministic reasoning selection. Catalog ids are copied, never modified."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection


@dataclass(slots=True)
class ReasoningSelection:
    """Selected reasoning chain, graph, and trace identifiers."""

    reasoning_id: str
    knowledge_id: str
    chain_id: str
    graph_id: str
    trace_id: str
    trace_nodes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one reasoning selection."""
        return {
            "reasoning_id": self.reasoning_id,
            "knowledge_id": self.knowledge_id,
            "chain_id": self.chain_id,
            "graph_id": self.graph_id,
            "trace_id": self.trace_id,
            "trace_nodes": list(self.trace_nodes),
        }


class ReasoningSelector:
    """Copy released reasoning identifiers from selected knowledge. No edits."""

    def select(self, knowledge: Sequence[KnowledgeSelection]) -> tuple[ReasoningSelection, ...]:
        """Emit one reasoning selection per selected knowledge item."""
        selected: list[ReasoningSelection] = []
        for item in knowledge:
            spec = item.spec
            selected.append(
                ReasoningSelection(
                    reasoning_id=spec.reasoning_id,
                    knowledge_id=spec.knowledge_id,
                    chain_id=spec.reasoning_chain_id,
                    graph_id=spec.reasoning_graph_id,
                    trace_id=spec.reasoning_trace_id,
                    trace_nodes=(spec.reasoning_trace_id,),
                )
            )
        return tuple(sorted(selected, key=lambda item: item.reasoning_id))
