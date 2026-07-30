"""Interpretation Engine exceptions."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AnalysisRuntimeError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    ValidationError,
)


class InterpretationEngineError(AnalysisRuntimeError):
    """Base error for Interpretation Engine."""

    error_class = "InterpretationEngineError"

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = "interpretation",
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        super().__init__(
            message,
            stage_id=stage_id,
            details=details,
            retryable=retryable,
        )


class InterpretationValidationError(InterpretationEngineError, ValidationError):
    """Invalid InterpretationContext or binding failure."""

    error_class = "ValidationError"


class InterpretationPrerequisiteError(InterpretationEngineError, PrerequisiteError):
    """Missing AnalysisResult or required stage results."""

    error_class = "PrerequisiteError"


class InterpretationKnowledgeError(InterpretationEngineError, KnowledgeError):
    """Knowledge SDK access failure for interpretation_knowledge."""

    error_class = "KnowledgeError"
    retryable = True


class InterpretationExecutionError(InterpretationEngineError, StageExecutionError):
    """Internal pipeline failure."""

    error_class = "ExecutionError"
    retryable = True


class InterpretationBindingError(InterpretationEngineError, ValidationError):
    """Unresolved required placeholder or template binding failure."""

    error_class = "BindingError"
