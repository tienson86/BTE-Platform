"""
BTE Platform
Interpretation Engine

Integrity Checker

Kiểm tra tính toàn vẹn của toàn bộ dữ liệu
trước khi Engine hoạt động.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntegrityReport:
    """
    Báo cáo kiểm tra toàn vẹn dữ liệu.
    """

    success: bool = True

    schema_errors: list = field(default_factory=list)

    reference_errors: list = field(default_factory=list)

    dependency_errors: list = field(default_factory=list)

    variable_errors: list = field(default_factory=list)

    warnings: list = field(default_factory=list)

    def has_errors(self) -> bool:

        return not self.success

    @property
    def total_errors(self):

        return (
            len(self.schema_errors)
            + len(self.reference_errors)
            + len(self.dependency_errors)
            + len(self.variable_errors)
        )

    def summary(self):

        return {

            "success": self.success,

            "schema": len(self.schema_errors),

            "reference": len(self.reference_errors),

            "dependency": len(self.dependency_errors),

            "variable": len(self.variable_errors),

            "warnings": len(self.warnings),

            "total": self.total_errors

        }


class IntegrityChecker:
    """
    Điều phối toàn bộ checker.
    """

    def __init__(
        self,
        validator=None,
        dependency_checker=None,
        reference_checker=None,
        variable_checker=None
    ):

        self.validator = validator

        self.dependency_checker = dependency_checker

        self.reference_checker = reference_checker

        self.variable_checker = variable_checker

    def validate_schema(
        self,
        rows,
        schema_name
    ):

        report = IntegrityReport()

        if self.validator is None:
            return report

        for index, row in enumerate(rows):

            errors = self.validator.validate(
                row,
                schema_name
            )

            if errors:

                report.success = False

                report.schema_errors.append({

                    "row": index + 1,

                    "errors": [
                        err.message
                        for err in errors
                    ]

                })

        return report

    def validate_reference(
        self,
        source_rows,
        source_field,
        target_rows,
        target_field
    ):

        report = IntegrityReport()

        if self.reference_checker is None:
            return report

        ok = self.reference_checker.check_reference(
            source_rows,
            source_field,
            target_rows,
            target_field
        )

        if not ok:

            report.success = False

            report.reference_errors = (
                self.reference_checker.get_errors()
            )

        return report

    def validate_dependency(self):

        report = IntegrityReport()

        if self.dependency_checker is None:
            return report

        try:

            self.dependency_checker.validate()

        except Exception as ex:

            report.success = False

            report.dependency_errors.append(str(ex))

        return report

    def validate_variables(self, rows):

        report = IntegrityReport()

        if self.variable_checker is None:
            return report

        ok = self.variable_checker.validate_rows(rows)

        if not ok:

            report.success = False

            report.variable_errors = (
                self.variable_checker.errors
            )

        return report

    @staticmethod
    def merge(*reports):

        result = IntegrityReport()

        for report in reports:

            if not report.success:
                result.success = False

            result.schema_errors.extend(report.schema_errors)

            result.reference_errors.extend(report.reference_errors)

            result.dependency_errors.extend(report.dependency_errors)

            result.variable_errors.extend(report.variable_errors)

            result.warnings.extend(report.warnings)

        return result
