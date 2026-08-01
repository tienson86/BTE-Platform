"""Pipeline scheduler interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.execution_graph import ExecutionGraph
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


class Scheduler:
    """Public interface for scheduling stage execution order.

    Consumes an execution graph and produces an ordered stage plan.
    """

    def build_plan(self, graph: ExecutionGraph) -> tuple[str, ...]:
        """Build an ordered stage execution plan from a graph."""
        raise NotImplementedError

    def next_stage(
        self,
        plan: tuple[str, ...],
        completed: tuple[str, ...],
    ) -> str | None:
        """Return the next stage identifier to execute."""
        raise NotImplementedError

    def is_complete(
        self,
        plan: tuple[str, ...],
        completed: tuple[str, ...],
    ) -> bool:
        """Indicate whether the plan has been fully executed."""
        raise NotImplementedError

    def can_run(self, stage_id: str, context: PipelineContext) -> bool:
        """Indicate whether a stage is eligible to run in the current context."""
        raise NotImplementedError
