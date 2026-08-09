"""Structured diagnostics for the canonical Analysis Pipeline."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.analysis_engine.pipeline.execution_context import PipelineDiagnostic

DIAG_EXECUTION_ORDER = "PIPE-ORDER"
DIAG_MISSING_PACKAGE = "PKG-MISSING"
DIAG_CONTRACT_VIOLATION = "CTR-VIOLATION"
DIAG_DEPENDENCY_VIOLATION = "DEP-VIOLATION"
DIAG_DUPLICATE_OUTPUT = "OUT-DUPLICATE"
DIAG_VERSION_MISMATCH = "PKG-VERSION"
DIAG_DISABLED_STAGE = "STAGE-DISABLED"
DIAG_UNDECLARED_OUTPUT = "OUT-UNDECLARED"
DIAG_PIPELINE_OK = "PIPE-OK"
DIAG_PIPELINE_FAIL = "PIPE-FAIL"


def diagnostic(
    code: str,
    message: str,
    *,
    severity: str = "error",
    stage_id: str | None = None,
    details: Mapping[str, Any] | None = None,
) -> PipelineDiagnostic:
    """Build a structured pipeline diagnostic."""
    return PipelineDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


def execution_order_diagnostic(stage_order: Sequence[str]) -> PipelineDiagnostic:
    """Record the resolved execution order."""
    return diagnostic(
        DIAG_EXECUTION_ORDER,
        "Canonical execution order resolved",
        severity="info",
        details={"stage_order": list(stage_order)},
    )


def missing_package_diagnostic(package_id: str, stage_id: str | None = None) -> PipelineDiagnostic:
    """Record a missing released package."""
    return diagnostic(
        DIAG_MISSING_PACKAGE,
        f"Required package not loaded: {package_id}",
        stage_id=stage_id,
        details={"package_id": package_id},
    )


def contract_violation_diagnostic(
    message: str,
    *,
    stage_id: str | None = None,
    details: Mapping[str, Any] | None = None,
) -> PipelineDiagnostic:
    """Record a package or stage contract violation."""
    return diagnostic(
        DIAG_CONTRACT_VIOLATION,
        message,
        stage_id=stage_id,
        details=details,
    )


def dependency_violation_diagnostic(
    message: str,
    *,
    stage_id: str | None = None,
) -> PipelineDiagnostic:
    """Record a dependency or order violation."""
    return diagnostic(
        DIAG_DEPENDENCY_VIOLATION,
        message,
        stage_id=stage_id,
    )


def duplicate_output_diagnostic(
    name: str,
    *,
    stage_id: str | None = None,
) -> PipelineDiagnostic:
    """Record a duplicate stage or field publication."""
    return diagnostic(
        DIAG_DUPLICATE_OUTPUT,
        f"Duplicate publication rejected: {name}",
        stage_id=stage_id,
        details={"name": name},
    )


def version_mismatch_diagnostic(
    package_id: str,
    actual: str,
    expected: str,
    *,
    stage_id: str | None = None,
) -> PipelineDiagnostic:
    """Record an incompatible package version."""
    return diagnostic(
        DIAG_VERSION_MISMATCH,
        f"Version mismatch: {package_id} {actual} does not satisfy {expected}",
        stage_id=stage_id,
        details={
            "package_id": package_id,
            "actual": actual,
            "expected": expected,
        },
    )


def disabled_stage_diagnostic(stage_id: str) -> PipelineDiagnostic:
    """Record that a registered stage was skipped because it is inactive."""
    return diagnostic(
        DIAG_DISABLED_STAGE,
        f"Stage registered but inactive: {stage_id}",
        severity="info",
        stage_id=stage_id,
    )


def pipeline_ok_diagnostic() -> PipelineDiagnostic:
    """Record a successful canonical run."""
    return diagnostic(
        DIAG_PIPELINE_OK,
        "Canonical pipeline validation passed",
        severity="info",
    )


def pipeline_fail_diagnostic(message: str) -> PipelineDiagnostic:
    """Record an orchestration failure without exposing an exception."""
    return diagnostic(DIAG_PIPELINE_FAIL, message)
