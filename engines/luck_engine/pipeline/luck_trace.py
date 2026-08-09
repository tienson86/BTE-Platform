"""Machine-readable Luck Pipeline execution trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.luck_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

TRACE_SCHEMA_KEYS: tuple[str, ...] = (
    "pipeline_id",
    "pipeline_version",
    "timeline_execution",
    "analysis_execution",
    "decision_execution",
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
class LuckTraceStep:
    """Trace record for one luck pipeline stage attempt."""

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
class LuckTrace:
    """Complete luck pipeline run trace."""

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION
    timeline_execution: dict[str, Any] = field(default_factory=dict)
    analysis_execution: dict[str, Any] = field(default_factory=dict)
    decision_execution: dict[str, Any] = field(default_factory=dict)
    published_outputs: tuple[str, ...] = ()
    component_versions: dict[str, str] = field(default_factory=dict)
    started_at: str | None = None
    completed_at: str | None = None
    steps: tuple[LuckTraceStep, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the luck trace."""
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_version": self.pipeline_version,
            "timeline_execution": dict(self.timeline_execution),
            "analysis_execution": dict(self.analysis_execution),
            "decision_execution": dict(self.decision_execution),
            "published_outputs": list(self.published_outputs),
            "component_versions": dict(self.component_versions),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps": [step.to_dict() for step in self.steps],
        }


def step_summary(step: LuckTraceStep) -> dict[str, Any]:
    """Reduce a step to the execution summary published on the trace."""
    return {
        "stage_id": step.stage_id,
        "component": step.component,
        "version": step.version,
        "executed": step.executed,
        "outputs_published": list(step.outputs_published),
        "started_at": step.started_at,
        "completed_at": step.completed_at,
    }


def build_luck_trace(
    *,
    steps: Sequence[LuckTraceStep],
    published_outputs: Sequence[str],
    component_versions: Mapping[str, str],
    started_at: str | None,
    completed_at: str | None,
) -> LuckTrace:
    """Assemble timeline / analysis / decision execution summaries."""
    by_id = {step.stage_id: step for step in steps}
    return LuckTrace(
        timeline_execution=step_summary(by_id["timeline"]) if "timeline" in by_id else {},
        analysis_execution=step_summary(by_id["analysis"]) if "analysis" in by_id else {},
        decision_execution=step_summary(by_id["decision"]) if "decision" in by_id else {},
        published_outputs=tuple(published_outputs),
        component_versions=dict(component_versions),
        started_at=started_at,
        completed_at=completed_at,
        steps=tuple(steps),
    )
