"""Version validator for Pack 03 version labels.

Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

import re
from typing import Any

from engines.interpretation_engine.models.version_info import VersionInfo
from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)

_SEMVER_LIKE = re.compile(
    r"^\d+\.\d+\.\d+([.-][0-9A-Za-z.-]+)?$"
)


class VersionValidator:
    """Validate version strings and VersionInfo contracts."""

    def validate_version_string(
        self,
        version: str | None,
        *,
        field_name: str = "version",
        require_semver_like: bool = True,
    ) -> ValidationReport:
        """Validate a single version string."""
        domain = ValidationDomain.VERSIONS.value
        if not version:
            issue = ValidationIssue(
                code="version_required",
                domain=domain,
                message=f"{field_name} is required",
                attributes={"field": field_name},
            )
            return ValidationReport(
                success=False,
                messages=("version_required",),
                issues=(issue,),
                domain=domain,
            )
        if require_semver_like and not _SEMVER_LIKE.match(version):
            issue = ValidationIssue(
                code="version_format_invalid",
                domain=domain,
                message=f"{field_name} must be semver-like",
                severity=ValidationSeverity.ERROR,
                attributes={"field": field_name, "value": version},
            )
            return ValidationReport(
                success=False,
                messages=("version_format_invalid",),
                issues=(issue,),
                domain=domain,
            )
        return ValidationReport(
            success=True,
            messages=("version_ok",),
            details={"field": field_name, "value": version},
            domain=domain,
        )

    def validate_version_info(self, version_info: Any) -> ValidationReport:
        """Validate a VersionInfo instance."""
        domain = ValidationDomain.VERSIONS.value
        if version_info is None:
            issue = ValidationIssue(
                code="version_info_required",
                domain=domain,
                message="version_info is required",
            )
            return ValidationReport(
                success=False,
                messages=("version_info_required",),
                issues=(issue,),
                domain=domain,
            )
        if not isinstance(version_info, VersionInfo):
            issue = ValidationIssue(
                code="version_info_type_invalid",
                domain=domain,
                message="VersionInfo type required",
                attributes={"type": type(version_info).__name__},
            )
            return ValidationReport(
                success=False,
                messages=("version_info_type_invalid",),
                issues=(issue,),
                domain=domain,
            )
        if not version_info.validate():
            issue = ValidationIssue(
                code="version_info_integrity_failed",
                domain=domain,
                message="version_info structural validation failed",
            )
            return ValidationReport(
                success=False,
                messages=("version_info_integrity_failed",),
                issues=(issue,),
                domain=domain,
            )

        schema = self.validate_version_string(
            version_info.schema_version,
            field_name="schema_version",
        )
        engine = self.validate_version_string(
            version_info.engine_version,
            field_name="engine_version",
        )
        model = self.validate_version_string(
            version_info.model_version,
            field_name="model_version",
        )
        success = schema.success and engine.success and model.success
        issues = schema.issues + engine.issues + model.issues
        messages = schema.messages + engine.messages + model.messages
        if success:
            messages = messages + ("versions_ok",)
        return ValidationReport(
            success=success,
            messages=messages,
            details={
                "schema_version": version_info.schema_version,
                "engine_version": version_info.engine_version,
                "model_version": version_info.model_version,
            },
            issues=issues,
            domain=domain,
        )

    def validate_compatibility(
        self,
        *,
        current: str,
        minimum: str,
    ) -> ValidationReport:
        """Validate current version is greater-or-equal to minimum (numeric tuple)."""
        domain = ValidationDomain.VERSIONS.value
        current_report = self.validate_version_string(current, field_name="current")
        minimum_report = self.validate_version_string(minimum, field_name="minimum")
        if not current_report.success or not minimum_report.success:
            return ValidationReport(
                success=False,
                messages=("version_compatibility_input_invalid",),
                issues=current_report.issues + minimum_report.issues,
                domain=domain,
            )
        if self._version_tuple(current) < self._version_tuple(minimum):
            issue = ValidationIssue(
                code="version_too_old",
                domain=domain,
                message="current version is older than minimum",
                attributes={"current": current, "minimum": minimum},
            )
            return ValidationReport(
                success=False,
                messages=("version_too_old",),
                issues=(issue,),
                domain=domain,
            )
        return ValidationReport(
            success=True,
            messages=("version_compatibility_ok",),
            details={"current": current, "minimum": minimum},
            domain=domain,
        )

    def _version_tuple(self, version: str) -> tuple[int, int, int]:
        """Parse leading major.minor.patch integers from a version string."""
        core = version.split("-", 1)[0].split("+", 1)[0]
        parts = core.split(".")
        numbers = [int(parts[index]) if index < len(parts) and parts[index].isdigit() else 0 for index in range(3)]
        return numbers[0], numbers[1], numbers[2]
