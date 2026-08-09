"""Luck Analysis Result and analysis trace (LE-2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.luck_engine.analysis.analysis_context import AnalysisDiagnostic
from engines.luck_engine.analysis_constants import (
    ANALYSIS_ENGINE_ID,
    ANALYSIS_VERSION,
    PUBLISHED_OUTPUTS,
)


@dataclass(slots=True)
class LuckAnalysisTrace:
    """Analysis trace. Not a Decision Trace."""

    analysis_engine_id: str = ANALYSIS_ENGINE_ID
    analysis_version: str = ANALYSIS_VERSION
    timeline_consumed: dict[str, Any] = field(default_factory=dict)
    analysis_consumed: dict[str, Any] = field(default_factory=dict)
    decision_consumed: dict[str, Any] = field(default_factory=dict)
    impact_stages_executed: tuple[str, ...] = ()
    outputs_published: tuple[str, ...] = ()
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the analysis trace."""
        return {
            "analysis_engine_id": self.analysis_engine_id,
            "analysis_version": self.analysis_version,
            "timeline_consumed": dict(self.timeline_consumed),
            "analysis_consumed": dict(self.analysis_consumed),
            "decision_consumed": dict(self.decision_consumed),
            "impact_stages_executed": list(self.impact_stages_executed),
            "outputs_published": list(self.outputs_published),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(slots=True)
class LuckAnalysisResult:
    """Published Luck Analysis contract for LE-3."""

    success: bool
    analysis_version: str
    seasonal_impact: dict[str, Any] | None = None
    strength_impact: dict[str, Any] | None = None
    temperature_impact: dict[str, Any] | None = None
    pattern_impact: dict[str, Any] | None = None
    pattern_evaluation_impact: dict[str, Any] | None = None
    useful_god_impact: dict[str, Any] | None = None
    overall_analysis_impact: dict[str, Any] | None = None
    analysis_trace: LuckAnalysisTrace | None = None
    analysis_diagnostics: tuple[AnalysisDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the published analysis contract."""
        return {
            "seasonal_impact": self.seasonal_impact,
            "strength_impact": self.strength_impact,
            "temperature_impact": self.temperature_impact,
            "pattern_impact": self.pattern_impact,
            "pattern_evaluation_impact": self.pattern_evaluation_impact,
            "useful_god_impact": self.useful_god_impact,
            "overall_analysis_impact": self.overall_analysis_impact,
            "analysis_trace": (
                None if self.analysis_trace is None else self.analysis_trace.to_dict()
            ),
            "analysis_diagnostics": [item.to_dict() for item in self.analysis_diagnostics],
            "analysis_version": self.analysis_version,
            "success": self.success,
            "errors": list(self.errors),
        }


def luck_analysis_contract() -> dict[str, Any]:
    """Return the published Luck Analysis field contract."""
    return {
        "engine_id": ANALYSIS_ENGINE_ID,
        "analysis_version": ANALYSIS_VERSION,
        "outputs": list(PUBLISHED_OUTPUTS),
        "fortune_scores": False,
        "decisions": False,
        "interpretation": False,
    }


def build_analysis_trace(
    *,
    timeline_snapshot: Mapping[str, Any],
    analysis_snapshot: Mapping[str, Any],
    decision_snapshot: Mapping[str, Any],
    executed_stages: Sequence[str],
    outputs_published: Sequence[str],
    started_at: str | None,
    completed_at: str | None,
) -> LuckAnalysisTrace:
    """Assemble the analysis trace from consumed snapshots."""
    natal = timeline_snapshot.get("natal_chart") or {}
    metadata = timeline_snapshot.get("timeline_metadata") or {}
    return LuckAnalysisTrace(
        timeline_consumed={
            "timeline_id": metadata.get("timeline_id"),
            "timeline_version": timeline_snapshot.get("timeline_version"),
            "chart_id": natal.get("chart_id") if isinstance(natal, Mapping) else None,
        },
        analysis_consumed={
            "pipeline_id": analysis_snapshot.get("pipeline_id"),
            "pipeline_version": analysis_snapshot.get("pipeline_version"),
            "stage_order": list(analysis_snapshot.get("stage_order") or ()),
            "success": analysis_snapshot.get("success"),
        },
        decision_consumed={
            "pipeline_id": decision_snapshot.get("pipeline_id"),
            "decision_pipeline_version": decision_snapshot.get("decision_pipeline_version"),
            "success": decision_snapshot.get("success"),
        },
        impact_stages_executed=tuple(executed_stages),
        outputs_published=tuple(outputs_published),
        started_at=started_at,
        completed_at=completed_at,
    )
