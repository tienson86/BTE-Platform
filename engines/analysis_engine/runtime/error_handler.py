"""Runtime error classification and recovery policy."""

from __future__ import annotations

import logging
from typing import Any

from engines.analysis_engine.runtime.exceptions import (
    AbortedError,
    AdmissionError,
    AnalysisRuntimeError,
    CacheError,
    CompatibilityError,
    IntegrityError,
    KnowledgeError,
    PrerequisiteError,
    StageExecutionError,
    StateError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Classify failures and apply fail-closed recovery policy."""

    def classify(
        self,
        exc: BaseException,
        *,
        stage_id: str | None = None,
    ) -> AnalysisRuntimeError:
        """Map an exception to a runtime error surface."""
        if isinstance(exc, AnalysisRuntimeError):
            if stage_id and exc.stage_id is None:
                exc.stage_id = stage_id
            return exc

        return StageExecutionError(
            str(exc) or exc.__class__.__name__,
            stage_id=stage_id,
            details={"exception_type": type(exc).__name__},
            retryable=True,
        )

    def handle(
        self,
        exc: BaseException,
        *,
        stage_id: str | None = None,
        request_id: str | None = None,
    ) -> AnalysisRuntimeError:
        """Classify, log, and return a runtime error (fail-closed)."""
        error = self.classify(exc, stage_id=stage_id)
        logger.error(
            "analysis_runtime_error",
            extra={
                "error_class": error.error_class,
                "stage_id": error.stage_id,
                "request_id": request_id,
                "retryable": error.retryable,
                "error_message": error.message,
                "details": error.details,
            },
        )
        return error

    def raise_handled(
        self,
        exc: BaseException,
        *,
        stage_id: str | None = None,
        request_id: str | None = None,
    ) -> None:
        """Classify and re-raise as AnalysisRuntimeError."""
        raise self.handle(exc, stage_id=stage_id, request_id=request_id)

    def is_retryable(self, error: AnalysisRuntimeError) -> bool:
        """Return whether a governed retry may be attempted."""
        return bool(error.retryable)

    def to_surface(self, error: AnalysisRuntimeError) -> dict[str, Any]:
        """Expose structured error surface."""
        return error.to_dict()

    @staticmethod
    def known_error_classes() -> tuple[type[AnalysisRuntimeError], ...]:
        """Return supported error classes."""
        return (
            AdmissionError,
            KnowledgeError,
            CompatibilityError,
            IntegrityError,
            PrerequisiteError,
            StageExecutionError,
            ValidationError,
            CacheError,
            StateError,
            AbortedError,
        )
