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


@dataclass(slots=True)
class PipelineDiagnostic:
    """Structured diagnostic emitted by the knowledge analysis pipeline."""

    code: str
    message: str
    severity: str = "info"
    stage_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the diagnostic for results and tests."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "stage_id": self.stage_id,
            "details": dict(self.details),
        }


@dataclass(slots=True)
class AnalysisExecutionContext:
    """Shared AX-1 context. Stages append results and never overwrite."""

    chart: Mapping[str, Any]
    diagnostics: list[PipelineDiagnostic] = field(default_factory=list)
    _results: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "chart", dict(self.chart))

    def add_diagnostic(self, diagnostic: PipelineDiagnostic) -> None:
        """Append a structured diagnostic entry."""
        self.diagnostics.append(diagnostic)

    def publish(self, stage_id: str, payload: Mapping[str, Any]) -> None:
        """Publish a stage result. Duplicate execution is rejected."""
        from engines.analysis_engine.exceptions.pipeline_error import (
            DuplicateExecutionError,
        )

        if stage_id in self._results:
            raise DuplicateExecutionError(f"duplicate_execution:{stage_id}")
        self._results[stage_id] = dict(payload)

    def get_result(self, stage_id: str) -> dict[str, Any] | None:
        """Return a published stage result, if present."""
        payload = self._results.get(stage_id)
        return None if payload is None else dict(payload)

    def has_result(self, stage_id: str) -> bool:
        """Return True when the stage has already published."""
        return stage_id in self._results

    def published_stage_ids(self) -> tuple[str, ...]:
        """Return published stage identifiers in insertion order."""
        return tuple(self._results)

    @property
    def seasonal_result(self) -> dict[str, Any] | None:
        """Seasonal stage output, or None before execution."""
        return self.get_result("seasonal")

    @property
    def strength_result(self) -> dict[str, Any] | None:
        """Strength stage output, or None before execution."""
        return self.get_result("strength")

    @property
    def temperature_result(self) -> dict[str, Any] | None:
        """Temperature stage output, or None before execution."""
        return self.get_result("temperature")

    @property
    def pattern_result(self) -> dict[str, Any] | None:
        """Pattern Core stage output, or None before execution."""
        return self.get_result("pattern")

    @property
    def pattern_evaluation_result(self) -> dict[str, Any] | None:
        """Pattern Evaluation stage output, or None before execution."""
        return self.get_result("pattern_evaluation")

    @property
    def useful_god_result(self) -> dict[str, Any] | None:
        """Useful God decision stage output, or None before execution."""
        return self.get_result("useful_god")

    @property
    def luck_cycle_result(self) -> dict[str, Any] | None:
        """Future Luck Cycle stage placeholder."""
        return self.get_result("luck_cycle")
