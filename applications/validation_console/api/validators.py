"""Validation helpers for Golden Dataset Manager."""

from __future__ import annotations

from typing import Any

from applications.validation_console.api.models import GoldenCase


class ValidationIssue:
    """One validation finding."""

    def __init__(
        self,
        *,
        code: str,
        severity: str,
        message: str,
        path: str = "",
    ) -> None:
        self.code = code
        self.severity = severity
        self.message = message
        self.path = path

    def to_dict(self) -> dict[str, Any]:
        """Serialize issue."""
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


def validate_dataset_payload(
    *,
    name: str,
    cases: list[dict[str, Any]] | None = None,
) -> list[ValidationIssue]:
    """Validate create/import payload."""
    issues: list[ValidationIssue] = []
    if not name or not str(name).strip():
        issues.append(
            ValidationIssue(
                code="missing_name",
                severity="error",
                message="name is required",
                path="name",
            )
        )
    if cases is None:
        return issues
    seen: set[str] = set()
    for index, raw in enumerate(cases):
        case_issues = validate_case_payload(raw, path_prefix=f"cases[{index}]")
        issues.extend(case_issues)
        case_id = str(raw.get("case_id") or "")
        if case_id:
            if case_id in seen:
                issues.append(
                    ValidationIssue(
                        code="duplicate_case_id",
                        severity="error",
                        message=f"Duplicate case_id: {case_id}",
                        path=f"cases[{index}].case_id",
                    )
                )
            seen.add(case_id)
    return issues


def validate_case_payload(
    payload: dict[str, Any],
    *,
    path_prefix: str = "case",
) -> list[ValidationIssue]:
    """Validate one golden case payload."""
    issues: list[ValidationIssue] = []
    case_id = payload.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        issues.append(
            ValidationIssue(
                code="missing_case_id",
                severity="error",
                message="case_id is required",
                path=f"{path_prefix}.case_id",
            )
        )
    description = payload.get("description")
    if not isinstance(description, str) or not description.strip():
        issues.append(
            ValidationIssue(
                code="missing_description",
                severity="error",
                message="description is required",
                path=f"{path_prefix}.description",
            )
        )
    if not isinstance(payload.get("input_fixture"), dict):
        issues.append(
            ValidationIssue(
                code="invalid_input_fixture",
                severity="error",
                message="input_fixture must be an object",
                path=f"{path_prefix}.input_fixture",
            )
        )
    if not isinstance(payload.get("expected_output"), dict):
        issues.append(
            ValidationIssue(
                code="invalid_expected_output",
                severity="error",
                message="expected_output must be an object",
                path=f"{path_prefix}.expected_output",
            )
        )
    elif not payload.get("expected_output"):
        issues.append(
            ValidationIssue(
                code="empty_expected_output",
                severity="warning",
                message="expected_output is empty",
                path=f"{path_prefix}.expected_output",
            )
        )
    return issues


def validate_cases(cases: list[GoldenCase]) -> list[ValidationIssue]:
    """Validate persisted cases."""
    issues: list[ValidationIssue] = []
    for index, case in enumerate(cases):
        issues.extend(
            validate_case_payload(case.to_dict(), path_prefix=f"cases[{index}]")
        )
    return issues
