"""Summary Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class SummaryEngineError(AnalysisRuntimeError):
    """Base error for Summary Engine."""

    error_class = "SummaryEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "summary",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class SummaryValidationError(SummaryEngineError, ValidationError):
    """Invalid AnalysisContext or summary schema."""

    error_class = "ValidationError"


class SummaryPrerequisiteError(SummaryEngineError, PrerequisiteError):
    """Missing required upstream stage results."""

    error_class = "PrerequisiteError"


class SummaryConsistencyError(SummaryEngineError):
    """Blocking cross-stage inconsistency."""

    error_class = "ConsistencyError"


class SummaryExecutionError(SummaryEngineError, StageExecutionError):
    """Internal aggregation failure."""

    error_class = "ExecutionError"
    retryable = True
