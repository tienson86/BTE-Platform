"""Structured diagnostics for the Canonical Report Pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

DIAG_FOUNDATION_MISSING = "FOUNDATION-MISSING"
DIAG_LAYOUT_MISSING = "LAYOUT-MISSING"
DIAG_RENDERER_MISSING = "RENDERER-MISSING"
DIAG_DEP_VIOLATION = "DEP-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_OUT_DUPLICATE = "OUT-DUPLICATE"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"
DIAG_STAGE_DISABLED = "STAGE-DISABLED"
DIAG_PIPE_ORDER = "PIPE-ORDER"


class CanonicalReportPipelineError(Exception):
    """Base error for RX-1 Canonical Report Pipeline failures."""


class ReportContractViolationError(CanonicalReportPipelineError):
    """Raised when a report pipeline contract check fails."""


class ReportDependencyViolationError(CanonicalReportPipelineError):
    """Raised when report pipeline stage order or inputs are violated."""


class ReportDuplicatePublicationError(CanonicalReportPipelineError):
    """Raised when a pipeline stage republishes an existing output."""


class ReportMissingInputError(CanonicalReportPipelineError):
    """Raised when a required report pipeline input is absent."""

    def __init__(self, diagnostic_code: str, message: str) -> None:
        super().__init__(message)
        self.diagnostic_code = diagnostic_code


@dataclass(slots=True)
class ReportPipelineDiagnostic:
    """Machine-readable diagnostic. No exception payload."""

    code: str
    message: str
    severity: str = "error"
    stage_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the diagnostic."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "stage_id": self.stage_id,
            "details": dict(self.details),
        }


def diagnostic(
    code: str,
    message: str,
    *,
    severity: str = "error",
    stage_id: str | None = None,
    details: Mapping[str, Any] | None = None,
) -> ReportPipelineDiagnostic:
    """Build a structured diagnostic."""
    return ReportPipelineDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


def execution_order_diagnostic(stage_order: Sequence[str]) -> ReportPipelineDiagnostic:
    """Record resolved report stage order."""
    return diagnostic(
        DIAG_PIPE_ORDER,
        "Canonical report order resolved",
        severity="info",
        details={"stage_order": list(stage_order)},
    )


def disabled_stage_diagnostic(stage_id: str) -> ReportPipelineDiagnostic:
    """Record a registered but inactive future stage."""
    return diagnostic(
        DIAG_STAGE_DISABLED,
        f"Stage registered but inactive: {stage_id}",
        severity="info",
        stage_id=stage_id,
    )


def pipeline_ok_diagnostic() -> ReportPipelineDiagnostic:
    """Record a successful report pipeline run."""
    return diagnostic(DIAG_PIPE_OK, "Report pipeline validation passed", severity="info")


def pipeline_fail_diagnostic(message: str) -> ReportPipelineDiagnostic:
    """Record an orchestration failure without exposing an exception type."""
    return diagnostic(DIAG_PIPE_FAIL, message)
