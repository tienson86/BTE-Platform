"""Top-level pipeline orchestration executor."""

from __future__ import annotations

from uuid import uuid4

from engines.analysis_engine.pipeline.execution_context import ExecutionContext
from engines.analysis_engine.pipeline.execution_hooks import (
    ExecutionHooks,
    NoOpExecutionHooks,
)
from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.execution_result import ExecutionResult
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_executor import PipelineExecutor
from engines.analysis_engine.pipeline.pipeline_result import PipelineResult
from engines.analysis_engine.pipeline.stage_base import StageBase
from engines.analysis_engine.pipeline.stage_executor import StageExecutor


class Executor:
    """Public orchestration facade for Analysis Engine pipelines.

    Coordinates stage ordering and execution only.
    Does not evaluate rules, score charts, or apply BaZi logic.
    """

    def __init__(
        self,
        *,
        pipeline_executor: PipelineExecutor | None = None,
        stage_executor: StageExecutor | None = None,
        hooks: ExecutionHooks | None = None,
        policy: ExecutionPolicy | None = None,
    ) -> None:
        """Initialize orchestration dependencies."""
        resolved_hooks = hooks or NoOpExecutionHooks()
        resolved_stage_executor = stage_executor or StageExecutor()
        self._pipeline_executor = pipeline_executor or PipelineExecutor(
            stage_executor=resolved_stage_executor,
            hooks=resolved_hooks,
        )
        self._policy = policy or ExecutionPolicy.default()

    def run(
        self,
        *,
        stages: tuple[StageBase, ...],
        pipeline_context: PipelineContext,
        policy: ExecutionPolicy | None = None,
        execution_id: str | None = None,
    ) -> ExecutionResult:
        """Run pipeline orchestration and return an immutable execution result."""
        resolved_policy = policy or self._policy
        context = ExecutionContext.from_pipeline_context(
            execution_id=execution_id or str(uuid4()),
            pipeline_context=pipeline_context,
            policy=resolved_policy,
            trace=(),
        )
        return self._pipeline_executor.execute(stages=stages, context=context)

    def run_as_pipeline_result(
        self,
        *,
        stages: tuple[StageBase, ...],
        pipeline_context: PipelineContext,
        policy: ExecutionPolicy | None = None,
        execution_id: str | None = None,
    ) -> PipelineResult:
        """Run orchestration and adapt the result to PipelineResult."""
        result = self.run(
            stages=stages,
            pipeline_context=pipeline_context,
            policy=policy,
            execution_id=execution_id,
        )
        return PipelineResult(
            pipeline_id=result.pipeline_id,
            success=result.success,
            outcomes=result.outcomes,
            errors=result.errors,
        )
