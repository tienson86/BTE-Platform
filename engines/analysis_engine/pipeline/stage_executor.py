"""Pipeline stage executor interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.pipeline.stage_base import StageBase


class StageExecutor:
    """Public interface for executing a single pipeline stage."""

    def execute(self, stage: StageBase, context: PipelineContext) -> StageOutcome:
        """Execute a stage against the provided context."""
        raise NotImplementedError

    def execute_prepare(self, stage: StageBase, context: PipelineContext) -> None:
        """Run the stage prepare phase."""
        raise NotImplementedError

    def execute_body(self, stage: StageBase, context: PipelineContext) -> StageOutcome:
        """Run the stage execute phase."""
        raise NotImplementedError
