"""Luck Decision Result, trace, and audit (LE-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.luck_engine.decision.decision_context import LuckDecisionDiagnostic
from engines.luck_engine.decision_constants import (
    DECISION_ENGINE_ID,
    DECISION_VERSION,
    PUBLISHED_OUTPUTS,
)


@dataclass(slots=True)
class LuckDecisionTrace:
    """Luck Decision trace. Not an interpretation log."""

    decision_engine_id: str = DECISION_ENGINE_ID
    decision_version: str = DECISION_VERSION
    timeline_consumed: dict[str, Any] = field(default_factory=dict)
    analysis_consumed: dict[str, Any] = field(default_factory=dict)
    decision_consumed: dict[str, Any] = field(default_factory=dict)
    decision_stages_executed: tuple[str, ...] = ()
    outputs_published: tuple[str, ...] = ()
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the decision trace."""
        return {
            "decision_engine_id": self.decision_engine_id,
            "decision_version": self.decision_version,
            "timeline_consumed": dict(self.timeline_consumed),
            "analysis_consumed": dict(self.analysis_consumed),
            "decision_consumed": dict(self.decision_consumed),
            "decision_stages_executed": list(self.decision_stages_executed),
            "outputs_published": list(self.outputs_published),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(slots=True)
class LuckDecisionAudit:
    """Machine-readable legality audit."""

    contract_validation: str
    dependency_validation: str
    priority_legality: str
    confidence_validation: str
    deterministic_execution: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the decision audit."""
        return {
            "contract_validation": self.contract_validation,
            "dependency_validation": self.dependency_validation,
            "priority_legality": self.priority_legality,
            "confidence_validation": self.confidence_validation,
            "deterministic_execution": self.deterministic_execution,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


@dataclass(slots=True)
class LuckDecisionResult:
    """Published Luck Decision contract for AX-4 / Interpretation."""

    success: bool
    decision_version: str
    opportunity_score: dict[str, Any] | None = None
    risk_score: dict[str, Any] | None = None
    luck_priority: dict[str, Any] | None = None
    decision_confidence: dict[str, Any] | None = None
    decision_reasoning: list[dict[str, Any]] | None = None
    decision_trace: LuckDecisionTrace | None = None
    decision_audit: LuckDecisionAudit | None = None
    overall_luck_decision: dict[str, Any] | None = None
    diagnostics: tuple[LuckDecisionDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the published decision contract."""
        return {
            "opportunity_score": self.opportunity_score,
            "risk_score": self.risk_score,
            "luck_priority": self.luck_priority,
            "decision_confidence": self.decision_confidence,
            "decision_reasoning": self.decision_reasoning,
            "decision_trace": None if self.decision_trace is None else self.decision_trace.to_dict(),
            "decision_audit": None if self.decision_audit is None else self.decision_audit.to_dict(),
            "overall_luck_decision": self.overall_luck_decision,
            "decision_version": self.decision_version,
            "success": self.success,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "errors": list(self.errors),
        }


def luck_decision_contract() -> dict[str, Any]:
    """Return the published Luck Decision field contract."""
    return {
        "engine_id": DECISION_ENGINE_ID,
        "decision_version": DECISION_VERSION,
        "outputs": list(PUBLISHED_OUTPUTS),
        "interpretation": False,
        "reports": False,
    }


def build_decision_trace(
    *,
    timeline_snapshot: Mapping[str, Any],
    luck_analysis_snapshot: Mapping[str, Any],
    analysis_snapshot: Mapping[str, Any],
    decision_snapshot: Mapping[str, Any],
    executed_stages: Sequence[str],
    outputs_published: Sequence[str],
    started_at: str | None,
    completed_at: str | None,
) -> LuckDecisionTrace:
    """Assemble the decision trace from consumed snapshots."""
    natal = timeline_snapshot.get("natal_chart") or {}
    metadata = timeline_snapshot.get("timeline_metadata") or {}
    return LuckDecisionTrace(
        timeline_consumed={
            "timeline_id": metadata.get("timeline_id"),
            "timeline_version": timeline_snapshot.get("timeline_version"),
            "chart_id": natal.get("chart_id") if isinstance(natal, Mapping) else None,
        },
        analysis_consumed={
            "luck_analysis_version": luck_analysis_snapshot.get("analysis_version"),
            "luck_analysis_success": luck_analysis_snapshot.get("success"),
            "pipeline_id": analysis_snapshot.get("pipeline_id"),
            "pipeline_version": analysis_snapshot.get("pipeline_version"),
        },
        decision_consumed={
            "pipeline_id": decision_snapshot.get("pipeline_id"),
            "decision_pipeline_version": decision_snapshot.get("decision_pipeline_version"),
            "success": decision_snapshot.get("success"),
        },
        decision_stages_executed=tuple(executed_stages),
        outputs_published=tuple(outputs_published),
        started_at=started_at,
        completed_at=completed_at,
    )
