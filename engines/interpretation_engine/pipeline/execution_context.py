"""Interpretation pipeline execution context for orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.pipeline.execution_policy import ExecutionPolicy


@dataclass(slots=True)
class PipelineContext:
    """Mutable context contract passed through interpretation pipeline stages.

    Holds orchestration attributes only. Does not embed BaZi interpretation content.
    """

    context_id: str
    pipeline_id: str
    source_final_result_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    stage_outputs: dict[str, Any] = field(default_factory=dict)

    def get_attribute(self, key: str) -> Any:
        """Return a context attribute by key."""
        return self.attributes.get(key)

    def set_attribute(self, key: str, value: Any) -> None:
        """Assign a context attribute by key."""
        self.attributes[key] = value

    def get_stage_output(self, stage_id: str) -> Any:
        """Return output produced by a prior stage."""
        return self.stage_outputs.get(stage_id)


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Immutable orchestration context for an interpretation pipeline run."""

    execution_id: str
    pipeline_id: str
    context_id: str
    policy: ExecutionPolicy
    source_final_result_id: str | None = None
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
            source_final_result_id=pipeline_context.source_final_result_id,
            attributes=dict(pipeline_context.attributes),
            stage_outputs=dict(pipeline_context.stage_outputs),
            trace=trace,
        )

    def to_pipeline_context(self) -> PipelineContext:
        """Materialize a mutable pipeline context copy for stage invocation."""
        return PipelineContext(
            context_id=self.context_id,
            pipeline_id=self.pipeline_id,
            source_final_result_id=self.source_final_result_id,
            attributes=dict(self.attributes),
            stage_outputs=dict(self.stage_outputs),
        )

    def with_stage_output(
        self,
        stage_id: str,
        payload: Mapping[str, Any],
    ) -> ExecutionContext:
        """Return a new context with an appended stage output snapshot."""
        outputs = dict(self.stage_outputs)
        outputs[stage_id] = dict(payload)
        return ExecutionContext(
            execution_id=self.execution_id,
            pipeline_id=self.pipeline_id,
            context_id=self.context_id,
            policy=self.policy,
            source_final_result_id=self.source_final_result_id,
            attributes=dict(self.attributes),
            stage_outputs=outputs,
            trace=self.trace + (stage_id,),
        )
