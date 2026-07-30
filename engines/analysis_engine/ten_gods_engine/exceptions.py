"""Ten Gods Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class TenGodsEngineError(AnalysisRuntimeError):
    """Base error for Ten Gods Engine."""

    error_class = "TenGodsEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "ten_gods",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class TenGodsValidationError(TenGodsEngineError, ValidationError):
    """Invalid AnalysisContext or chart facts."""

    error_class = "ValidationError"


class TenGodsPrerequisiteError(TenGodsEngineError, PrerequisiteError):
    """Missing required upstream stage results."""

    error_class = "PrerequisiteError"


class TenGodsKnowledgeError(TenGodsEngineError, KnowledgeError):
    """Knowledge SDK access failure for ten_gods_knowledge."""

    error_class = "KnowledgeError"
    retryable = True


class TenGodsExecutionError(TenGodsEngineError, StageExecutionError):
    """Internal evaluation failure."""

    error_class = "ExecutionError"
    retryable = True


class TenGodsConflictResolutionError(TenGodsEngineError):
    """Unable to deterministically resolve required conflicts."""

    error_class = "ConflictResolutionError"
