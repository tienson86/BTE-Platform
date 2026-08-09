"""Canonical Decision Result aggregated from Foundation → Priority → Override."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.decision_engine.pipeline.decision_audit import DecisionAudit
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.decision_trace import DecisionTrace
from engines.decision_engine.pipeline.diagnostics import DecisionDiagnostic
from engines.decision_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

RESULT_FIELDS: tuple[str, ...] = (
    "foundation",
    "priority",
    "override",
    "final_useful_god",
    "final_favorable_gods",
    "final_unfavorable_gods",
    "decision_trace",
    "decision_audit",
    "decision_confidence",
    "decision_diagnostics",
    "decision_pipeline_version",
    "package_versions",
)


@dataclass(slots=True)
class CanonicalDecisionResult:
    """Canonical Decision Result. Downstream consumers read this contract only."""

    pipeline_id: str
    decision_pipeline_version: str
    success: bool
    foundation: dict[str, Any] | None = None
    priority: dict[str, Any] | None = None
    override: dict[str, Any] | None = None
    final_useful_god: Any = None
    final_favorable_gods: Any = None
    final_unfavorable_gods: Any = None
    decision_trace: DecisionTrace | None = None
    decision_audit: DecisionAudit | None = None
    decision_confidence: Any = None
    decision_diagnostics: Any = None
    package_versions: dict[str, str] = field(default_factory=dict)
    stage_order: tuple[str, ...] = ()
    diagnostics: tuple[DecisionDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical result."""
        return {
            "pipeline_id": self.pipeline_id,
            "decision_pipeline_version": self.decision_pipeline_version,
            "success": self.success,
            "foundation": self.foundation,
            "priority": self.priority,
            "override": self.override,
            "final_useful_god": self.final_useful_god,
            "final_favorable_gods": self.final_favorable_gods,
            "final_unfavorable_gods": self.final_unfavorable_gods,
            "decision_trace": None if self.decision_trace is None else self.decision_trace.to_dict(),
            "decision_audit": None if self.decision_audit is None else self.decision_audit.to_dict(),
            "decision_confidence": self.decision_confidence,
            "decision_diagnostics": self.decision_diagnostics,
            "package_versions": dict(self.package_versions),
            "stage_order": list(self.stage_order),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "errors": list(self.errors),
        }


def build_decision_result(
    *,
    context: DecisionExecutionContext,
    diagnostics: Sequence[DecisionDiagnostic],
    errors: Sequence[str],
    stage_order: Sequence[str],
    package_versions: Mapping[str, str],
    trace: DecisionTrace,
    audit: DecisionAudit,
    success: bool,
    pipeline_id: str = PIPELINE_ID,
    pipeline_version: str = PIPELINE_VERSION,
) -> CanonicalDecisionResult:
    """Assemble the canonical Decision Result from a completed run."""
    override = context.override_result or {}
    priority = context.priority_result or {}
    foundation = context.foundation_result or {}
    return CanonicalDecisionResult(
        pipeline_id=pipeline_id,
        decision_pipeline_version=pipeline_version,
        success=success,
        foundation=context.foundation_result,
        priority=context.priority_result,
        override=context.override_result,
        final_useful_god=override.get("final_useful_god"),
        final_favorable_gods=override.get("final_favorable_gods"),
        final_unfavorable_gods=override.get("final_unfavorable_gods"),
        decision_trace=trace,
        decision_audit=audit,
        decision_confidence=(
            override.get("override_confidence")
            or priority.get("resolution_confidence")
            or foundation.get("decision_confidence")
        ),
        decision_diagnostics=(
            override.get("decision_audit")
            or priority.get("resolution_diagnostics")
            or foundation.get("decision_diagnostics")
        ),
        package_versions=dict(package_versions),
        stage_order=tuple(stage_order),
        diagnostics=tuple(diagnostics),
        errors=tuple(errors),
    )
