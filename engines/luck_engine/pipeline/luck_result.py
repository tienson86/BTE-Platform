"""Canonical Luck Result — the only official Luck Pipeline output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.luck_engine.pipeline.diagnostics import LuckPipelineDiagnostic
from engines.luck_engine.pipeline.luck_audit import LuckAudit
from engines.luck_engine.pipeline.luck_trace import LuckTrace
from engines.luck_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

RESULT_FIELDS: tuple[str, ...] = (
    "timeline_result",
    "analysis_result",
    "decision_result",
    "overall_luck_result",
    "luck_trace",
    "luck_audit",
    "luck_confidence",
    "luck_diagnostics",
    "luck_pipeline_version",
    "component_versions",
)


@dataclass(slots=True)
class CanonicalLuckResult:
    """Canonical Luck Result aggregated from Timeline → Analysis → Decision."""

    pipeline_id: str
    luck_pipeline_version: str
    success: bool
    timeline_result: dict[str, Any] | None = None
    analysis_result: dict[str, Any] | None = None
    decision_result: dict[str, Any] | None = None
    overall_luck_result: dict[str, Any] | None = None
    luck_trace: LuckTrace | None = None
    luck_audit: LuckAudit | None = None
    luck_confidence: dict[str, Any] | None = None
    luck_diagnostics: tuple[LuckPipelineDiagnostic, ...] = ()
    component_versions: dict[str, str] = field(default_factory=dict)
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical luck result."""
        return {
            "pipeline_id": self.pipeline_id,
            "luck_pipeline_version": self.luck_pipeline_version,
            "success": self.success,
            "timeline_result": self.timeline_result,
            "analysis_result": self.analysis_result,
            "decision_result": self.decision_result,
            "overall_luck_result": self.overall_luck_result,
            "luck_trace": None if self.luck_trace is None else self.luck_trace.to_dict(),
            "luck_audit": None if self.luck_audit is None else self.luck_audit.to_dict(),
            "luck_confidence": self.luck_confidence,
            "luck_diagnostics": [item.to_dict() for item in self.luck_diagnostics],
            "component_versions": dict(self.component_versions),
            "errors": list(self.errors),
        }


def build_overall_luck_result(
    *,
    timeline_result: Mapping[str, Any] | None,
    analysis_result: Mapping[str, Any] | None,
    decision_result: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Compose the official overall luck payload from stage snapshots."""
    decision = dict(decision_result or {})
    analysis = dict(analysis_result or {})
    timeline = dict(timeline_result or {})
    return {
        "opportunity_score": decision.get("opportunity_score"),
        "risk_score": decision.get("risk_score"),
        "luck_priority": decision.get("luck_priority"),
        "decision_confidence": decision.get("decision_confidence"),
        "timeline_version": timeline.get("timeline_version"),
        "analysis_version": analysis.get("analysis_version"),
        "decision_version": decision.get("decision_version"),
    }


def build_canonical_luck_result(
    *,
    success: bool,
    timeline_result: Mapping[str, Any] | None,
    analysis_result: Mapping[str, Any] | None,
    decision_result: Mapping[str, Any] | None,
    luck_trace: LuckTrace | None,
    luck_audit: LuckAudit | None,
    diagnostics: Sequence[LuckPipelineDiagnostic],
    component_versions: Mapping[str, str],
    errors: Sequence[str],
    pipeline_id: str = PIPELINE_ID,
    pipeline_version: str = PIPELINE_VERSION,
) -> CanonicalLuckResult:
    """Assemble the canonical result from completed stage snapshots."""
    decision = dict(decision_result or {})
    confidence = decision.get("decision_confidence")
    if not isinstance(confidence, dict):
        confidence = None
    return CanonicalLuckResult(
        pipeline_id=pipeline_id,
        luck_pipeline_version=pipeline_version,
        success=success,
        timeline_result=None if timeline_result is None else dict(timeline_result),
        analysis_result=None if analysis_result is None else dict(analysis_result),
        decision_result=None if decision_result is None else dict(decision_result),
        overall_luck_result=build_overall_luck_result(
            timeline_result=timeline_result,
            analysis_result=analysis_result,
            decision_result=decision_result,
        ),
        luck_trace=luck_trace,
        luck_audit=luck_audit,
        luck_confidence=confidence,
        luck_diagnostics=tuple(diagnostics),
        component_versions=dict(component_versions),
        errors=tuple(errors),
    )
