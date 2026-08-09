"""Machine-readable Canonical Report Pipeline audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.report_engine.pipeline.diagnostics import (
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_FOUNDATION_MISSING,
    DIAG_LAYOUT_MISSING,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_RENDERER_MISSING,
    ReportPipelineDiagnostic,
)
from engines.report_engine.pipeline.stage_registry import (
    STAGE_FOUNDATION,
    STAGE_LAYOUT,
    STAGE_RENDERING,
)

AUDIT_SCHEMA_KEYS: tuple[str, ...] = (
    "contract_validation",
    "dependency_validation",
    "foundation_legality",
    "layout_legality",
    "render_legality",
    "deterministic_execution",
    "version_compatibility",
    "reason_codes",
    "details",
)


@dataclass(slots=True)
class ReportPipelineAudit:
    """Legality audit for one Canonical Report Pipeline run."""

    contract_validation: str
    dependency_validation: str
    foundation_legality: str
    layout_legality: str
    render_legality: str
    deterministic_execution: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the report pipeline audit."""
        return {
            "contract_validation": self.contract_validation,
            "dependency_validation": self.dependency_validation,
            "foundation_legality": self.foundation_legality,
            "layout_legality": self.layout_legality,
            "render_legality": self.render_legality,
            "deterministic_execution": self.deterministic_execution,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


def _legality(stage_id: str, executed: Sequence[str], fail_codes: set[str]) -> str:
    if fail_codes:
        return "fail"
    if stage_id in executed:
        return "pass"
    return "not_run"


def build_report_pipeline_audit(
    *,
    diagnostics: Sequence[ReportPipelineDiagnostic],
    executed_stages: Sequence[str],
) -> ReportPipelineAudit:
    """Derive audit flags from diagnostics and executed stages."""
    codes = [item.code for item in diagnostics]
    error_codes = {item.code for item in diagnostics if item.severity == "error"}
    contract_fail = DIAG_CONTRACT_VIOLATION in error_codes
    dep_fail = DIAG_DEP_VIOLATION in error_codes
    reason_codes = tuple(
        code
        for code in codes
        if code
        in {
            DIAG_FOUNDATION_MISSING,
            DIAG_LAYOUT_MISSING,
            DIAG_RENDERER_MISSING,
            DIAG_CONTRACT_VIOLATION,
            DIAG_DEP_VIOLATION,
            DIAG_OUT_DUPLICATE,
            DIAG_PIPE_FAIL,
            DIAG_PIPE_OK,
        }
    )
    details: dict[str, Any] = {}
    failed = next((item for item in diagnostics if item.code == DIAG_PIPE_FAIL), None)
    if failed is not None:
        details["stop_reason"] = failed.message
    return ReportPipelineAudit(
        contract_validation="fail" if contract_fail else "pass",
        dependency_validation="fail" if dep_fail else "pass",
        foundation_legality=_legality(
            STAGE_FOUNDATION, executed_stages, {DIAG_FOUNDATION_MISSING} & error_codes
        ),
        layout_legality=_legality(
            STAGE_LAYOUT, executed_stages, {DIAG_LAYOUT_MISSING} & error_codes
        ),
        render_legality=_legality(
            STAGE_RENDERING, executed_stages, {DIAG_RENDERER_MISSING} & error_codes
        ),
        deterministic_execution=True,
        version_compatibility="fail" if contract_fail else "pass",
        reason_codes=reason_codes,
        details=details,
    )
