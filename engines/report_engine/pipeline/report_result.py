"""Canonical Report Pipeline result — the only official RX-1 output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.report_engine.pipeline.diagnostics import ReportPipelineDiagnostic
from engines.report_engine.pipeline.report_audit import ReportPipelineAudit
from engines.report_engine.pipeline.report_trace import ReportPipelineTrace
from engines.report_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

RESULT_FIELDS: tuple[str, ...] = (
    "foundation_result",
    "layout_result",
    "rendering_result",
    "canonical_report_artifact",
    "report_trace",
    "report_audit",
    "report_diagnostics",
    "report_pipeline_version",
    "component_versions",
)


@dataclass(slots=True)
class CanonicalReportResult:
    """Official Report Pipeline aggregate. Nested RE-3 artifact is preserved."""

    pipeline_id: str
    report_pipeline_version: str
    success: bool
    foundation_result: dict[str, Any] | None = None
    layout_result: dict[str, Any] | None = None
    rendering_result: dict[str, Any] | None = None
    canonical_report_artifact: dict[str, Any] | None = None
    report_trace: ReportPipelineTrace | None = None
    report_audit: ReportPipelineAudit | None = None
    report_diagnostics: tuple[ReportPipelineDiagnostic, ...] = ()
    component_versions: dict[str, str] = field(default_factory=dict)
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical report pipeline result."""
        return {
            "pipeline_id": self.pipeline_id,
            "report_pipeline_version": self.report_pipeline_version,
            "success": self.success,
            "foundation_result": self.foundation_result,
            "layout_result": self.layout_result,
            "rendering_result": self.rendering_result,
            "canonical_report_artifact": self.canonical_report_artifact,
            "report_trace": None if self.report_trace is None else self.report_trace.to_dict(),
            "report_audit": None if self.report_audit is None else self.report_audit.to_dict(),
            "report_diagnostics": [item.to_dict() for item in self.report_diagnostics],
            "component_versions": dict(self.component_versions),
            "errors": list(self.errors),
        }


def build_canonical_report_result(
    *,
    success: bool,
    foundation_result: Mapping[str, Any] | None,
    layout_result: Mapping[str, Any] | None,
    rendering_result: Mapping[str, Any] | None,
    report_trace: ReportPipelineTrace | None,
    report_audit: ReportPipelineAudit | None,
    diagnostics: Sequence[ReportPipelineDiagnostic],
    component_versions: Mapping[str, str],
    errors: Sequence[str],
    pipeline_id: str = PIPELINE_ID,
    pipeline_version: str = PIPELINE_VERSION,
) -> CanonicalReportResult:
    """Assemble the official pipeline result from completed stage snapshots."""
    rendering = None if rendering_result is None else dict(rendering_result)
    return CanonicalReportResult(
        pipeline_id=pipeline_id,
        report_pipeline_version=pipeline_version,
        success=success,
        foundation_result=None if foundation_result is None else dict(foundation_result),
        layout_result=None if layout_result is None else dict(layout_result),
        rendering_result=rendering,
        canonical_report_artifact=rendering,
        report_trace=report_trace,
        report_audit=report_audit,
        report_diagnostics=tuple(diagnostics),
        component_versions=dict(component_versions),
        errors=tuple(errors),
    )
