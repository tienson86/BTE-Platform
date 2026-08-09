"""Execution trace and canonical Analysis Result for AX-2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.analysis_engine.pipeline.execution_context import (
    AnalysisExecutionContext,
    PipelineDiagnostic,
)
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.pipeline.stage_registry import (
    PIPELINE_ID_V2,
    PIPELINE_VERSION_V2,
)


@dataclass(slots=True)
class StageTraceEntry:
    """Trace record for one stage attempt."""

    stage_id: str
    package_id: str | None
    package_version: str | None
    enabled: bool
    executed: bool
    outputs_published: tuple[str, ...] = ()
    started_at: str | None = None
    completed_at: str | None = None
    diagnostics: tuple[dict[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize one stage trace entry."""
        return {
            "stage_id": self.stage_id,
            "package_id": self.package_id,
            "package_version": self.package_version,
            "enabled": self.enabled,
            "executed": self.executed,
            "outputs_published": list(self.outputs_published),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "diagnostics": list(self.diagnostics),
        }


@dataclass(slots=True)
class ExecutionTrace:
    """Complete run trace consumed by future Report Engine."""

    pipeline_id: str = PIPELINE_ID_V2
    pipeline_version: str = PIPELINE_VERSION_V2
    started_at: str | None = None
    completed_at: str | None = None
    stages: tuple[StageTraceEntry, ...] = ()
    package_versions: dict[str, str] = field(default_factory=dict)
    outputs_published: tuple[str, ...] = ()
    diagnostics: tuple[PipelineDiagnostic, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the execution trace."""
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_version": self.pipeline_version,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "stages": [entry.to_dict() for entry in self.stages],
            "package_versions": dict(self.package_versions),
            "outputs_published": list(self.outputs_published),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }


@dataclass(slots=True)
class CanonicalAnalysisResult:
    """Canonical Analysis Result aggregated from released packages."""

    pipeline_id: str
    pipeline_version: str
    success: bool
    seasonal: dict[str, Any] | None = None
    strength: dict[str, Any] | None = None
    temperature: dict[str, Any] | None = None
    pattern: dict[str, Any] | None = None
    pattern_evaluation: dict[str, Any] | None = None
    useful_god: dict[str, Any] | None = None
    diagnostics: tuple[PipelineDiagnostic, ...] = ()
    execution_trace: ExecutionTrace = field(default_factory=ExecutionTrace)
    package_versions: dict[str, str] = field(default_factory=dict)
    stage_order: tuple[str, ...] = ()
    outcomes: tuple[StageOutcome, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical result for downstream consumers."""
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_version": self.pipeline_version,
            "success": self.success,
            "seasonal": self.seasonal,
            "strength": self.strength,
            "temperature": self.temperature,
            "pattern": self.pattern,
            "pattern_evaluation": self.pattern_evaluation,
            "useful_god": self.useful_god,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "execution_trace": self.execution_trace.to_dict(),
            "package_versions": dict(self.package_versions),
            "stage_order": list(self.stage_order),
            "errors": list(self.errors),
        }


def build_analysis_result(
    *,
    context: AnalysisExecutionContext,
    outcomes: Sequence[StageOutcome],
    diagnostics: Sequence[PipelineDiagnostic],
    errors: Sequence[str],
    stage_order: Sequence[str],
    package_versions: Mapping[str, str],
    trace: ExecutionTrace,
    success: bool,
    pipeline_id: str = PIPELINE_ID_V2,
    pipeline_version: str = PIPELINE_VERSION_V2,
) -> CanonicalAnalysisResult:
    """Assemble the canonical Analysis Result from a completed run."""
    return CanonicalAnalysisResult(
        pipeline_id=pipeline_id,
        pipeline_version=pipeline_version,
        success=success,
        seasonal=context.seasonal_result,
        strength=context.strength_result,
        temperature=context.temperature_result,
        pattern=context.pattern_result,
        pattern_evaluation=context.pattern_evaluation_result,
        useful_god=context.useful_god_result,
        diagnostics=tuple(diagnostics),
        execution_trace=trace,
        package_versions=dict(package_versions),
        stage_order=tuple(stage_order),
        outcomes=tuple(outcomes),
        errors=tuple(errors),
    )
