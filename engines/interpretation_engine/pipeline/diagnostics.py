"""Structured diagnostics for the Canonical Interpretation Pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.exceptions.pipeline_error import InterpretationPipelineError

DIAG_FOUNDATION_MISSING = "FOUNDATION-MISSING"
DIAG_KNOWLEDGE_MISSING = "KNOWLEDGE-MISSING"
DIAG_COMPOSITION_MISSING = "COMPOSITION-MISSING"
DIAG_DEP_VIOLATION = "DEP-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_OUT_DUPLICATE = "OUT-DUPLICATE"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"
DIAG_STAGE_DISABLED = "STAGE-DISABLED"
DIAG_PIPE_ORDER = "PIPE-ORDER"


class CanonicalInterpretationPipelineError(InterpretationPipelineError):
    """Base error for IX-1 Canonical Interpretation Pipeline failures."""


class InterpretationContractViolationError(CanonicalInterpretationPipelineError):
    """Raised when an interpretation pipeline contract check fails."""


class InterpretationDependencyViolationError(CanonicalInterpretationPipelineError):
    """Raised when interpretation pipeline stage order or inputs are violated."""


class InterpretationDuplicatePublicationError(CanonicalInterpretationPipelineError):
    """Raised when a pipeline stage republishes an existing output."""


class InterpretationMissingInputError(CanonicalInterpretationPipelineError):
    """Raised when a required interpretation pipeline input is absent."""

    def __init__(self, diagnostic_code: str, message: str) -> None:
        super().__init__(message)
        self.diagnostic_code = diagnostic_code


@dataclass(slots=True)
class InterpretationPipelineDiagnostic:
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
) -> InterpretationPipelineDiagnostic:
    """Build a structured diagnostic."""
    return InterpretationPipelineDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


def execution_order_diagnostic(stage_order: Sequence[str]) -> InterpretationPipelineDiagnostic:
    """Record resolved interpretation stage order."""
    return diagnostic(
        DIAG_PIPE_ORDER,
        "Canonical interpretation order resolved",
        severity="info",
        details={"stage_order": list(stage_order)},
    )


def disabled_stage_diagnostic(stage_id: str) -> InterpretationPipelineDiagnostic:
    """Record a registered but inactive future stage."""
    return diagnostic(
        DIAG_STAGE_DISABLED,
        f"Stage registered but inactive: {stage_id}",
        severity="info",
        stage_id=stage_id,
    )


def pipeline_ok_diagnostic() -> InterpretationPipelineDiagnostic:
    """Record a successful interpretation pipeline run."""
    return diagnostic(DIAG_PIPE_OK, "Interpretation pipeline validation passed", severity="info")


def pipeline_fail_diagnostic(message: str) -> InterpretationPipelineDiagnostic:
    """Record an orchestration failure without exposing an exception type."""
    return diagnostic(DIAG_PIPE_FAIL, message)
