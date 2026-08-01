"""Dependency validator for Pack 03 graphs and id sets.

Infrastructure only. No BaZi logic.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.validation.models import (
    ValidationDomain,
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)
from engines.interpretation_engine.validation.runtime_validator import RuntimeValidator


class DependencyValidator:
    """Validate dependency availability and optional execution graphs."""

    def __init__(self, *, runtime_validator: RuntimeValidator | None = None) -> None:
        """Initialize with optional injected RuntimeValidator."""
        self._runtime_validator = runtime_validator or RuntimeValidator()

    def validate(
        self,
        *,
        required: tuple[str, ...] = (),
        available: tuple[str, ...] = (),
        dependency_map: Mapping[str, tuple[str, ...]] | None = None,
        execution_graph: Any | None = None,
    ) -> ValidationReport:
        """Validate dependency sets and optional graph collaborators."""
        domain = ValidationDomain.DEPENDENCIES.value
        reports: list[ValidationReport] = []
        issues: list[ValidationIssue] = []

        if required or available:
            base = self._runtime_validator.validate_dependencies(
                required=required,
                available=available,
            )
            reports.append(base)
            if not base.success:
                issues.append(
                    ValidationIssue(
                        code="dependencies_missing",
                        domain=domain,
                        message="required dependencies are missing",
                        attributes=dict(base.details),
                    )
                )

        if dependency_map is not None:
            known = set(dependency_map)
            missing: set[str] = set()
            for node_id, deps in dependency_map.items():
                for dep in deps:
                    if dep not in known and dep not in available:
                        missing.add(dep)
            if missing:
                issues.append(
                    ValidationIssue(
                        code="dependency_map_unresolved",
                        domain=domain,
                        message="dependency map references unresolved ids",
                        attributes={"missing": sorted(missing)},
                    )
                )
                reports.append(
                    ValidationReport(
                        success=False,
                        messages=("dependency_map_unresolved",),
                        details={"missing": sorted(missing)},
                        domain=domain,
                    )
                )
            else:
                reports.append(
                    ValidationReport(
                        success=True,
                        messages=("dependency_map_ok",),
                        details={"nodes": sorted(known)},
                        domain=domain,
                    )
                )

        if execution_graph is not None:
            validate = getattr(execution_graph, "validate", None)
            ok = bool(validate()) if callable(validate) else False
            if not ok:
                issues.append(
                    ValidationIssue(
                        code="execution_graph_invalid",
                        domain=domain,
                        message="execution graph validation failed",
                        severity=ValidationSeverity.ERROR,
                    )
                )
                reports.append(
                    ValidationReport(
                        success=False,
                        messages=("execution_graph_invalid",),
                        domain=domain,
                    )
                )
            else:
                reports.append(
                    ValidationReport(
                        success=True,
                        messages=("execution_graph_ok",),
                        domain=domain,
                    )
                )

        if not reports:
            return ValidationReport(
                success=True,
                messages=("dependencies_ok",),
                domain=domain,
            )

        success = all(report.success for report in reports)
        messages: list[str] = []
        details: dict[str, Any] = {}
        for index, report in enumerate(reports):
            messages.extend(report.messages)
            details[f"check_{index}"] = {
                "success": report.success,
                "messages": list(report.messages),
                "details": dict(report.details),
            }
        if success:
            messages.append("dependencies_ok")
        return ValidationReport(
            success=success,
            messages=tuple(messages),
            details=details,
            issues=tuple(issues),
            domain=domain,
        )
