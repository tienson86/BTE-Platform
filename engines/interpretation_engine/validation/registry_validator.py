"""Registry validator for Pack 03 registries.

Validates BaseRegistry and InterpreterRegistry readiness.
Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.runtime.registry_base import BaseRegistry
from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
)
from engines.interpretation_engine.validation.runtime_validator import RuntimeValidator


class RegistryValidator:
    """Validate Pack 03 registry structural readiness."""

    def __init__(self, *, runtime_validator: RuntimeValidator | None = None) -> None:
        """Initialize with optional injected RuntimeValidator."""
        self._runtime_validator = runtime_validator or RuntimeValidator()

    def validate(self, registry: BaseRegistry[Any] | None) -> ValidationReport:
        """Validate a BaseRegistry instance."""
        domain = ValidationDomain.REGISTRIES.value
        report = self._runtime_validator.validate_registry(registry)  # type: ignore[arg-type]
        issues: tuple[ValidationIssue, ...] = ()
        if not report.success:
            issues = (
                ValidationIssue(
                    code=report.messages[0] if report.messages else "registry_invalid",
                    domain=domain,
                    message="registry validation failed",
                    attributes=dict(report.details),
                ),
            )
        else:
            report = ValidationReport(
                success=True,
                messages=report.messages + ("registries_ok",),
                details=report.details,
                domain=domain,
            )
            return report
        return ValidationReport(
            success=False,
            messages=report.messages,
            details=report.details,
            issues=issues,
            domain=domain,
        )

    def validate_interpreter_registry(self, registry: Any) -> ValidationReport:
        """Validate InterpreterRegistry via validate_registry() when available."""
        domain = ValidationDomain.REGISTRIES.value
        base = self.validate(registry)
        if not base.success:
            return base
        validate_registry = getattr(registry, "validate_registry", None)
        if callable(validate_registry):
            detailed = validate_registry()
            success = bool(getattr(detailed, "success", False))
            messages = tuple(getattr(detailed, "messages", ()))
            details = dict(getattr(detailed, "details", {}))
            issues: tuple[ValidationIssue, ...] = ()
            if not success:
                issues = (
                    ValidationIssue(
                        code="interpreter_registry_invalid",
                        domain=domain,
                        message="interpreter registry detailed validation failed",
                        attributes=details,
                    ),
                )
            return ValidationReport(
                success=success,
                messages=messages + (("registries_ok",) if success else ()),
                details=details,
                issues=issues,
                domain=domain,
            )
        return base
