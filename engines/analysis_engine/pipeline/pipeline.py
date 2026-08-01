"""Pipeline orchestration interface."""

from __future__ import annotations

from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.executor import Executor
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import PipelineResult
from engines.analysis_engine.pipeline.stage_base import StageBase


class Pipeline:
    """Public orchestration interface for the Analysis Engine pipeline.

    Holds ordered stages and delegates execution to the orchestration layer.
    Does not evaluate rules or perform BaZi analysis.
    """

    def __init__(
        self,
        pipeline_id: str,
        name: str = "",
        *,
        stages: tuple[StageBase, ...] = (),
        policy: ExecutionPolicy | None = None,
        executor: Executor | None = None,
    ) -> None:
        """Create a pipeline orchestration instance."""
        self.pipeline_id = pipeline_id
        self.name = name
        self._stages = stages
        self._policy = policy or ExecutionPolicy.default()
        self._executor = executor or Executor(policy=self._policy)

    def run(self, context: PipelineContext) -> PipelineResult:
        """Execute the pipeline against the provided context."""
        if context.pipeline_id != self.pipeline_id:
            context.pipeline_id = self.pipeline_id
        return self._executor.run_as_pipeline_result(
            stages=self._stages,
            pipeline_context=context,
            policy=self._policy,
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
