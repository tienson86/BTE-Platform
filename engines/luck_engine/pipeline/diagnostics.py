"""Structured diagnostics for the Canonical Luck Pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

DIAG_TIMELINE_MISSING = "TIMELINE-MISSING"
DIAG_ANALYSIS_MISSING = "ANALYSIS-MISSING"
DIAG_DECISION_MISSING = "DECISION-MISSING"
DIAG_DEP_VIOLATION = "DEP-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_OUT_DUPLICATE = "OUT-DUPLICATE"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"
DIAG_STAGE_DISABLED = "STAGE-DISABLED"
DIAG_PIPE_ORDER = "PIPE-ORDER"


@dataclass(slots=True)
class LuckPipelineDiagnostic:
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
) -> LuckPipelineDiagnostic:
    """Build a structured diagnostic."""
    return LuckPipelineDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


def execution_order_diagnostic(stage_order: Sequence[str]) -> LuckPipelineDiagnostic:
    """Record resolved luck stage order."""
    return diagnostic(
        DIAG_PIPE_ORDER,
        "Canonical luck order resolved",
        severity="info",
        details={"stage_order": list(stage_order)},
    )


def disabled_stage_diagnostic(stage_id: str) -> LuckPipelineDiagnostic:
    """Record a registered but inactive future stage."""
    return diagnostic(
        DIAG_STAGE_DISABLED,
        f"Stage registered but inactive: {stage_id}",
        severity="info",
        stage_id=stage_id,
    )


def pipeline_ok_diagnostic() -> LuckPipelineDiagnostic:
    """Record a successful luck pipeline run."""
    return diagnostic(DIAG_PIPE_OK, "Luck pipeline validation passed", severity="info")


def pipeline_fail_diagnostic(message: str) -> LuckPipelineDiagnostic:
    """Record an orchestration failure without exposing an exception type."""
    return diagnostic(DIAG_PIPE_FAIL, message)
