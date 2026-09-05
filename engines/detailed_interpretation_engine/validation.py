"""Pack 07 validation result models. No domain inference."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import PACK07_VALIDATOR_VERSION
from engines.detailed_interpretation_engine.enums import IssueSeverity, ValidationStatus


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One validation finding. Does not invent domain truth."""

    code: str
    severity: IssueSeverity
    layer: str
    field: str = ""
    message: str = ""
    expected: str = ""
    actual: str = ""
    trace_id: str = ""
    validator: str = ""
    analysis_id: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize a validation issue."""
        return {
            "code": self.code,
            "severity": self.severity.value,
            "layer": self.layer,
            "field": self.field,
            "message": self.message,
            "expected": self.expected,
            "actual": self.actual,
            "trace_id": self.trace_id,
            "validator": self.validator,
            "analysis_id": self.analysis_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ValidationIssue:
        """Rebuild a validation issue."""
        payload = data or {}
        return cls(
            code=as_str(payload.get("code")),
            severity=as_enum(IssueSeverity, payload.get("severity"), IssueSeverity.ERROR),
            layer=as_str(payload.get("layer")),
            field=as_str(payload.get("field")),
            message=as_str(payload.get("message")),
            expected=as_str(payload.get("expected")),
            actual=as_str(payload.get("actual")),
            trace_id=as_str(payload.get("trace_id")),
            validator=as_str(payload.get("validator")),
            analysis_id=as_str(payload.get("analysis_id")),
        )


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Outcome of one Pack 07 validator pass."""

    status: ValidationStatus = ValidationStatus.PASS
    errors: tuple[ValidationIssue, ...] = ()
    warnings: tuple[ValidationIssue, ...] = ()
    validated_at: str = ""
    validator_version: str = PACK07_VALIDATOR_VERSION
    analysis_id: str = ""
    trace_ids: tuple[str, ...] = ()

    @property
    def issues(self) -> tuple[ValidationIssue, ...]:
        """All issues, errors first."""
        return self.errors + self.warnings

    def to_dict(self) -> dict[str, Any]:
        """Serialize a validation result."""
        return {
            "status": self.status.value,
            "errors": [item.to_dict() for item in self.errors],
            "warnings": [item.to_dict() for item in self.warnings],
            "validated_at": self.validated_at,
            "validator_version": self.validator_version,
            "analysis_id": self.analysis_id,
            "trace_ids": list(self.trace_ids),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ValidationResult:
        """Rebuild a validation result."""
        payload = data or {}
        errors_raw = payload.get("errors") or ()
        warnings_raw = payload.get("warnings") or ()
        return cls(
            status=as_enum(ValidationStatus, payload.get("status"), ValidationStatus.PASS),
            errors=tuple(
                ValidationIssue.from_dict(item) for item in errors_raw if isinstance(item, Mapping)
            ),
            warnings=tuple(
                ValidationIssue.from_dict(item) for item in warnings_raw if isinstance(item, Mapping)
            ),
            validated_at=as_str(payload.get("validated_at")),
            validator_version=as_str(payload.get("validator_version"), PACK07_VALIDATOR_VERSION),
            analysis_id=as_str(payload.get("analysis_id")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


def utc_now_iso() -> str:
    """UTC timestamp for validated_at. Must not feed content hashing."""
    return datetime.now(timezone.utc).isoformat()


def result_from_issues(
    issues: tuple[ValidationIssue, ...] | list[ValidationIssue],
    *,
    analysis_id: str,
    validator_version: str = PACK07_VALIDATOR_VERSION,
) -> ValidationResult:
    """Fold issues into PASS / PASS_WITH_WARNINGS / FAIL."""
    errors = tuple(
        item
        for item in issues
        if item.severity in (IssueSeverity.ERROR, IssueSeverity.CRITICAL)
    )
    warnings = tuple(item for item in issues if item.severity is IssueSeverity.WARNING)
    if errors:
        status = ValidationStatus.FAIL
    elif warnings:
        status = ValidationStatus.PASS_WITH_WARNINGS
    else:
        status = ValidationStatus.PASS
    traces = tuple(item.trace_id for item in issues if item.trace_id)
    return ValidationResult(
        status=status,
        errors=errors,
        warnings=warnings,
        validated_at=utc_now_iso(),
        validator_version=validator_version,
        analysis_id=analysis_id,
        trace_ids=traces,
    )
