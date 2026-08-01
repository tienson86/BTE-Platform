"""Pipeline execution context for orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Immutable orchestration context for a pipeline run."""

    execution_id: str
    pipeline_id: str
    context_id: str
    policy: ExecutionPolicy
    chart_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)
    stage_outputs: Mapping[str, Any] = field(default_factory=dict)
    trace: tuple[str, ...] = ()

    @classmethod
    def from_pipeline_context(
        cls,
        *,
        execution_id: str,
        pipeline_context: PipelineContext,
        policy: ExecutionPolicy | None = None,
        trace: tuple[str, ...] = (),
    ) -> ExecutionContext:
        """Create an execution context snapshot from a pipeline context."""
        return cls(
            execution_id=execution_id,
            pipeline_id=pipeline_context.pipeline_id,
            context_id=pipeline_context.context_id,
            policy=policy or ExecutionPolicy.default(),
            chart_id=pipeline_context.chart_id,
            attributes=dict(pipeline_context.attributes),
            stage_outputs=dict(pipeline_context.stage_outputs),
            trace=trace,
        )

    def to_pipeline_context(self) -> PipelineContext:
        """Materialize a mutable pipeline context copy for stage invocation."""
        return PipelineContext(
            context_id=self.context_id,
            pipeline_id=self.pipeline_id,
            chart_id=self.chart_id,
            attributes=dict(self.attributes),
            stage_outputs=dict(self.stage_outputs),
        )

    def with_stage_output(self, stage_id: str, payload: Mapping[str, Any]) -> ExecutionContext:
        """Return a new context with an appended stage output snapshot."""
        outputs = dict(self.stage_outputs)
        outputs[stage_id] = dict(payload)
        return ExecutionContext(
            execution_id=self.execution_id,
            pipeline_id=self.pipeline_id,
            context_id=self.context_id,
            policy=self.policy,
            chart_id=self.chart_id,
            attributes=dict(self.attributes),
            stage_outputs=outputs,
            trace=self.trace + (stage_id,),
        )
