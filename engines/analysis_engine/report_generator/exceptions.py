"""Report Generator exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class ReportGeneratorError(AnalysisRuntimeError):
    """Base error for Report Generator."""

    error_class = "ReportGeneratorError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "report_generator",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class ReportValidationError(ReportGeneratorError, ValidationError):
    """Invalid ReportAssemblyContext or result schema."""

    error_class = "ValidationError"


class ReportPrerequisiteError(ReportGeneratorError, PrerequisiteError):
    """Missing InterpretationResult or required AnalysisResult."""

    error_class = "PrerequisiteError"


class ReportFormatProfileError(ReportGeneratorError, ValidationError):
    """Invalid or unsupported format profile."""

    error_class = "FormatProfileError"


class ReportBindingError(ReportGeneratorError, ValidationError):
    """Unresolvable section or structured data binding."""

    error_class = "BindingError"


class ReportSerializationError(ReportGeneratorError, StageExecutionError):
    """Format serializer failure."""

    error_class = "SerializationError"
    retryable = True


class ReportSchemaError(ReportGeneratorError, ValidationError):
    """StructuredReport or artifact schema mismatch."""

    error_class = "SchemaError"


class ReportExecutionError(ReportGeneratorError, StageExecutionError):
    """Internal assembly failure."""

    error_class = "ExecutionError"
    retryable = True
