"""Luck Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class LuckEngineError(AnalysisRuntimeError):
    """Base error for Luck Engine."""

    error_class = "LuckEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "luck",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class LuckValidationError(LuckEngineError, ValidationError):
    """Invalid AnalysisContext or luck timeline facts."""

    error_class = "ValidationError"


class LuckPrerequisiteError(LuckEngineError, PrerequisiteError):
    """Missing required upstream stage results."""

    error_class = "PrerequisiteError"


class LuckKnowledgeError(LuckEngineError, KnowledgeError):
    """Knowledge SDK access failure for luck_knowledge."""

    error_class = "KnowledgeError"
    retryable = True


class LuckExecutionError(LuckEngineError, StageExecutionError):
    """Internal evaluation failure."""

    error_class = "ExecutionError"
    retryable = True


class LuckConflictResolutionError(LuckEngineError):
    """Unable to deterministically resolve required conflicts."""

    error_class = "ConflictResolutionError"
