"""Structured diagnostics for the canonical Decision Pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

DIAG_MISSING_PACKAGE = "PKG-MISSING"
DIAG_DEPENDENCY_VIOLATION = "DEP-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CTR-VIOLATION"
DIAG_DUPLICATE_PUBLICATION = "OUT-DUPLICATE"
DIAG_DISABLED_STAGE = "STAGE-DISABLED"
DIAG_VERSION_MISMATCH = "PKG-VERSION"
DIAG_EXECUTION_SUCCESS = "PIPE-OK"
DIAG_EXECUTION_FAILURE = "PIPE-FAIL"
DIAG_EXECUTION_ORDER = "PIPE-ORDER"


@dataclass(slots=True)
class DecisionDiagnostic:
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
) -> DecisionDiagnostic:
    """Build a structured diagnostic."""
    return DecisionDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


def execution_order_diagnostic(stage_order: Sequence[str]) -> DecisionDiagnostic:
    """Record resolved decision stage order."""
    return diagnostic(
        DIAG_EXECUTION_ORDER,
        "Canonical decision order resolved",
        severity="info",
        details={"stage_order": list(stage_order)},
    )


def missing_package_diagnostic(package_id: str, stage_id: str | None = None) -> DecisionDiagnostic:
    """Record a missing released package."""
    return diagnostic(
        DIAG_MISSING_PACKAGE,
        f"Required package not loaded: {package_id}",
        stage_id=stage_id,
        details={"package_id": package_id},
    )


def disabled_stage_diagnostic(stage_id: str) -> DecisionDiagnostic:
    """Record a registered but inactive future stage."""
    return diagnostic(
        DIAG_DISABLED_STAGE,
        f"Stage registered but inactive: {stage_id}",
        severity="info",
        stage_id=stage_id,
    )


def pipeline_ok_diagnostic() -> DecisionDiagnostic:
    """Record a successful decision run."""
    return diagnostic(DIAG_EXECUTION_SUCCESS, "Decision pipeline validation passed", severity="info")


def pipeline_fail_diagnostic(message: str) -> DecisionDiagnostic:
    """Record an orchestration failure without exposing an exception type."""
    return diagnostic(DIAG_EXECUTION_FAILURE, message)
