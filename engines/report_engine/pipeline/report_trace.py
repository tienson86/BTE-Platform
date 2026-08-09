"""Machine-readable Canonical Report Pipeline execution trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.report_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

TRACE_SCHEMA_KEYS: tuple[str, ...] = (
    "pipeline_id",
    "pipeline_version",
    "foundation_execution",
    "layout_execution",
    "render_execution",
    "artifact_creation",
    "published_outputs",
    "component_versions",
    "started_at",
    "completed_at",
    "steps",
)

STEP_SCHEMA_KEYS: tuple[str, ...] = (
    "stage_id",
    "component",
    "version",
    "executed",
    "outputs_published",
    "started_at",
    "completed_at",
)


@dataclass(slots=True)
class ReportPipelineTraceStep:
    """Trace record for one report pipeline stage attempt."""

    stage_id: str
    component: str
    version: str
    executed: bool
    outputs_published: tuple[str, ...] = ()
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize one stage trace step."""
        return {
            "stage_id": self.stage_id,
            "component": self.component,
            "version": self.version,
            "executed": self.executed,
            "outputs_published": list(self.outputs_published),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(slots=True)
class ReportPipelineTrace:
    """Complete report pipeline run trace."""

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION
    foundation_execution: dict[str, Any] = field(default_factory=dict)
    layout_execution: dict[str, Any] = field(default_factory=dict)
    render_execution: dict[str, Any] = field(default_factory=dict)
    artifact_creation: dict[str, Any] = field(default_factory=dict)
    published_outputs: tuple[str, ...] = ()
    component_versions: dict[str, str] = field(default_factory=dict)
    started_at: str | None = None
    completed_at: str | None = None
    steps: tuple[ReportPipelineTraceStep, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the report pipeline trace."""
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_version": self.pipeline_version,
            "foundation_execution": dict(self.foundation_execution),
            "layout_execution": dict(self.layout_execution),
            "render_execution": dict(self.render_execution),
            "artifact_creation": dict(self.artifact_creation),
            "published_outputs": list(self.published_outputs),
            "component_versions": dict(self.component_versions),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps": [step.to_dict() for step in self.steps],
        }


def _step_summary(step: ReportPipelineTraceStep) -> dict[str, Any]:
    return {
        "stage_id": step.stage_id,
        "component": step.component,
        "version": step.version,
        "executed": step.executed,
        "outputs_published": list(step.outputs_published),
        "started_at": step.started_at,
        "completed_at": step.completed_at,
    }


def build_report_pipeline_trace(
    *,
    steps: Sequence[ReportPipelineTraceStep],
    published_outputs: Sequence[str],
    component_versions: Mapping[str, str],
    artifact_id: str | None,
    started_at: str | None,
    completed_at: str | None,
) -> ReportPipelineTrace:
    """Assemble foundation / layout / render execution summaries."""
    by_id = {step.stage_id: step for step in steps}
    render = _step_summary(by_id["rendering"]) if "rendering" in by_id else {}
    artifact_creation = dict(render)
    if artifact_id:
        artifact_creation["artifact_id"] = artifact_id
    return ReportPipelineTrace(
        foundation_execution=_step_summary(by_id["foundation"]) if "foundation" in by_id else {},
        layout_execution=_step_summary(by_id["layout"]) if "layout" in by_id else {},
        render_execution=render,
        artifact_creation=artifact_creation,
        published_outputs=tuple(published_outputs),
        component_versions=dict(component_versions),
        started_at=started_at,
        completed_at=completed_at,
        steps=tuple(steps),
    )
