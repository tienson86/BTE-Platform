"""Combination Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class CombinationEngineError(AnalysisRuntimeError):
    """Base error for Combination Engine."""

    error_class = "CombinationEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "combination",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class CombinationValidationError(CombinationEngineError, ValidationError):
    """Invalid AnalysisContext or chart facts."""

    error_class = "ValidationError"


class CombinationPrerequisiteError(CombinationEngineError, PrerequisiteError):
    """Missing required upstream stage results."""

    error_class = "PrerequisiteError"


class CombinationKnowledgeError(CombinationEngineError, KnowledgeError):
    """Knowledge SDK access failure for combination_knowledge."""

    error_class = "KnowledgeError"
    retryable = True


class CombinationExecutionError(CombinationEngineError, StageExecutionError):
    """Internal evaluation failure."""

    error_class = "ExecutionError"
    retryable = True


class CombinationConflictResolutionError(CombinationEngineError):
    """Unable to deterministically resolve required conflicts."""

    error_class = "ConflictResolutionError"
