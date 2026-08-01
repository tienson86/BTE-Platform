"""Interpretation pipeline orchestration interface."""

from __future__ import annotations

from engines.interpretation_engine.pipeline.execution_context import (
    ExecutionContext,
    PipelineContext,
)
from engines.interpretation_engine.pipeline.execution_policy import ExecutionPolicy
from engines.interpretation_engine.pipeline.execution_result import ExecutionResult
from engines.interpretation_engine.pipeline.hooks import (
    ExecutionHooks,
    NoOpExecutionHooks,
)
from engines.interpretation_engine.pipeline.pipeline_executor import PipelineExecutor
from engines.interpretation_engine.pipeline.pipeline_result import (
    InterpretationPipelineResult,
)
from engines.interpretation_engine.pipeline.stage_base import StageBase
from engines.interpretation_engine.pipeline.stage_executor import StageExecutor
from engines.interpretation_engine.utils.ids import new_id


class Pipeline:
    """Public orchestration interface for the Interpretation Engine pipeline.

    Holds ordered stages and delegates execution to the orchestration layer.
    Does not evaluate rules or produce BaZi interpretation content.
    """

    def __init__(
        self,
        pipeline_id: str,
        name: str = "",
        *,
        stages: tuple[StageBase, ...] = (),
        policy: ExecutionPolicy | None = None,
        executor: PipelineExecutor | None = None,
        hooks: ExecutionHooks | None = None,
    ) -> None:
        """Create an interpretation pipeline orchestration instance."""
        self.pipeline_id = pipeline_id
        self.name = name
        self._stages = stages
        self._policy = policy or ExecutionPolicy.default()
        resolved_hooks = hooks or NoOpExecutionHooks()
        self._executor = executor or PipelineExecutor(
            stage_executor=StageExecutor(),
            hooks=resolved_hooks,
        )

    def run(
        self,
        context: PipelineContext,
        *,
        execution_id: str | None = None,
    ) -> ExecutionResult:
        """Execute the pipeline against the provided context."""
        if context.pipeline_id != self.pipeline_id:
            context.pipeline_id = self.pipeline_id
        execution_context = ExecutionContext.from_pipeline_context(
            execution_id=execution_id or new_id("exec"),
            pipeline_context=context,
            policy=self._policy,
            trace=(),
        )
        return self._executor.execute(stages=self._stages, context=execution_context)

    def run_as_pipeline_result(
        self,
        context: PipelineContext,
        *,
        execution_id: str | None = None,
    ) -> InterpretationPipelineResult:
        """Execute orchestration and adapt to InterpretationPipelineResult."""
        result = self.run(context, execution_id=execution_id)
        return InterpretationPipelineResult(
            id=result.execution_id,
            pipeline_id=result.pipeline_id,
            success=result.success,
            stage_ids=result.stage_ids(),
            metadata=dict(result.metadata),
            errors=result.errors,
        )

    def validate(self, context: PipelineContext) -> bool:
        """Validate pipeline readiness for the provided context."""
        if not context.context_id:
            return False
        if context.pipeline_id and context.pipeline_id != self.pipeline_id:
            return False
        return True

    def describe(self) -> dict[str, str]:
        """Return a public description of the pipeline identity."""
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "stage_count": str(len(self._stages)),
        }
