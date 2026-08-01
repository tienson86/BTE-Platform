"""Shared validation models for Pack 03 validation framework.

Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationDomain(str, Enum):
    """Validation domains covered by the framework."""

    CONTRACTS = "contracts"
    REGISTRIES = "registries"
    CONTEXT = "context"
    METADATA = "metadata"
    DEPENDENCIES = "dependencies"
    VERSIONS = "versions"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Immutable validation issue."""

    code: str
    domain: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate issue structural integrity."""
        return bool(self.code and self.domain and self.message)


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Immutable validation report used across Pack 03 validators."""

    success: bool
    messages: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)
    issues: tuple[ValidationIssue, ...] = ()
    domain: str = ""

    def validate(self) -> bool:
        """Validate report structural integrity."""
        for issue in self.issues:
            if not issue.validate():
                return False
        return True

    def error_codes(self) -> tuple[str, ...]:
        """Return issue codes with ERROR severity."""
        return tuple(
            issue.code
            for issue in self.issues
            if issue.severity is ValidationSeverity.ERROR
        )

    @staticmethod
    def merge(
        *reports: ValidationReport,
        domain: str = "framework",
    ) -> ValidationReport:
        """Merge multiple reports into one aggregate report."""
        messages: list[str] = []
        issues: list[ValidationIssue] = []
        details: dict[str, Any] = {}
        success = True
        for index, report in enumerate(reports):
            success = success and report.success
            messages.extend(report.messages)
            issues.extend(report.issues)
            key = report.domain or f"report_{index}"
            details[key] = {
                "success": report.success,
                "messages": list(report.messages),
                "issue_count": len(report.issues),
            }
        if success:
            messages.append("validation_framework_ok")
        return ValidationReport(
            success=success,
            messages=tuple(messages),
            details=details,
            issues=tuple(issues),
            domain=domain,
        )
