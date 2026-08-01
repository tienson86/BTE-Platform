"""Pipeline execution graph interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.stage_base import StageBase


class ExecutionGraph:
    """Public interface for stage dependency graphs.

    Represents ordered execution relationships between stages.
    """

    def add_node(self, stage: StageBase) -> None:
        """Add a stage node to the graph."""
        raise NotImplementedError

    def add_edge(self, from_stage_id: str, to_stage_id: str) -> None:
        """Add a directed dependency edge between stages."""
        raise NotImplementedError

    def nodes(self) -> tuple[str, ...]:
        """Return stage identifiers present in the graph."""
        raise NotImplementedError

    def edges(self) -> tuple[tuple[str, str], ...]:
        """Return directed edges as (from, to) pairs."""
        raise NotImplementedError

    def topological_order(self) -> tuple[str, ...]:
        """Return a valid topological execution order."""
        raise NotImplementedError

    def has_cycle(self) -> bool:
        """Indicate whether the graph contains a cycle."""
        raise NotImplementedError
