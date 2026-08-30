"""NarrativeReasoningContext — internal semantic graph only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.reasoning.reasoning_edge import ReasoningEdge
from engines.narrative_v2.reasoning.reasoning_node import (
    KIND_BOUNDARY,
    KIND_IMPACT_CANDIDATE,
    KIND_OBSERVATION,
    ReasoningNode,
)
from engines.narrative_v2.reasoning.reasoning_reference import ReasoningReference


@dataclass(frozen=True, slots=True)
class ReasoningContractGap:
    """Approved reasoning relationship that is not available this sprint."""

    field: str
    reason: str
    rule_id: str | None = None


@dataclass(frozen=True, slots=True)
class NarrativeReasoningContext:
    """Reasoning graph. No customer text, headline, summary, or action."""

    nodes: tuple[ReasoningNode, ...]
    edges: tuple[ReasoningEdge, ...]
    observations: tuple[ReasoningNode, ...]
    impacts: tuple[ReasoningNode, ...]
    boundaries: tuple[ReasoningNode, ...]
    references: tuple[ReasoningReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str
    contract_gaps: tuple[ReasoningContractGap, ...]

    def node(self, reasoning_id: str) -> ReasoningNode | None:
        """Return one node by deterministic id."""
        for entry in self.nodes:
            if entry.reasoning_id == reasoning_id:
                return entry
        return None

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No customer prose. No debug dump."""
        return [entry.to_trace_record() for entry in self.nodes]


def partition_nodes(
    nodes: tuple[ReasoningNode, ...],
) -> tuple[tuple[ReasoningNode, ...], tuple[ReasoningNode, ...], tuple[ReasoningNode, ...]]:
    """Split nodes into observation, impact, and boundary tuples."""
    observations = tuple(node for node in nodes if node.kind == KIND_OBSERVATION)
    impacts = tuple(node for node in nodes if node.kind == KIND_IMPACT_CANDIDATE)
    boundaries = tuple(node for node in nodes if node.kind == KIND_BOUNDARY)
    return observations, impacts, boundaries
