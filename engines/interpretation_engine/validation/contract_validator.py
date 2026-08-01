"""Contract validator for Pack 03 runtimes.

Validates public runtime contracts only. No BaZi logic.
"""

from __future__ import annotations

from engines.interpretation_engine.runtime.contracts import RuntimeContract
from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)
from engines.interpretation_engine.validation.runtime_validator import RuntimeValidator


class ContractValidator:
    """Validate Pack 03 runtime contract surface and readiness."""

    def __init__(self, *, runtime_validator: RuntimeValidator | None = None) -> None:
        """Initialize with optional injected RuntimeValidator."""
        self._runtime_validator = runtime_validator or RuntimeValidator()

    def validate(self, runtime: RuntimeContract | None) -> ValidationReport:
        """Validate a runtime contract."""
        domain = ValidationDomain.CONTRACTS.value
        if runtime is None:
            issue = ValidationIssue(
                code="contract_required",
                domain=domain,
                message="runtime contract instance is required",
            )
            return ValidationReport(
                success=False,
                messages=("contract_required",),
                issues=(issue,),
                domain=domain,
            )
        report = self._runtime_validator.validate_contract(runtime)
        issues: list[ValidationIssue] = []
        if not report.success:
            issues.append(
                ValidationIssue(
                    code=report.messages[0] if report.messages else "contract_invalid",
                    domain=domain,
                    message="runtime contract validation failed",
                    severity=ValidationSeverity.ERROR,
                    attributes=dict(report.details),
                )
            )
        state = self._runtime_validator.validate_runtime_state(runtime)
        if not state.success:
            issues.append(
                ValidationIssue(
                    code=state.messages[0] if state.messages else "contract_state_invalid",
                    domain=domain,
                    message="runtime state validation failed",
                    attributes=dict(state.details),
                )
            )
        success = report.success and state.success
        messages = report.messages + state.messages
        if success:
            messages = messages + ("contracts_ok",)
        return ValidationReport(
            success=success,
            messages=messages,
            details={"contract": dict(report.details), "state": dict(state.details)},
            issues=tuple(issues),
            domain=domain,
        )
