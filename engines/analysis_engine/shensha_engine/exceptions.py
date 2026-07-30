"""ShenSha Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class ShenShaEngineError(AnalysisRuntimeError):
    """Base error for ShenSha Engine."""

    error_class = "ShenShaEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "shensha",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class ShenShaValidationError(ShenShaEngineError, ValidationError):
    """Invalid AnalysisContext or chart facts."""

    error_class = "ValidationError"


class ShenShaPrerequisiteError(ShenShaEngineError, PrerequisiteError):
    """Missing required upstream stage results."""

    error_class = "PrerequisiteError"


class ShenShaKnowledgeError(ShenShaEngineError, KnowledgeError):
    """Knowledge SDK access failure for shensha_knowledge."""

    error_class = "KnowledgeError"
    retryable = True


class ShenShaExecutionError(ShenShaEngineError, StageExecutionError):
    """Internal evaluation failure."""

    error_class = "ExecutionError"
    retryable = True


class ShenShaConflictResolutionError(ShenShaEngineError):
    """Unable to deterministically resolve required conflicts."""

    error_class = "ConflictResolutionError"
