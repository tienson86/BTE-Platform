"""Analysis Runtime exception hierarchy."""

from __future__ import annotations

from typing import Any


class AnalysisRuntimeError(Exception):
    """Base exception for Analysis Runtime failures."""

    error_class: str = "AnalysisRuntimeError"
    retryable: bool = False

    def __init__(
        self,
        message: str,
        *,
        stage_id: str | None = None,
        details: dict[str, Any] | None = None,
        retryable: bool | None = None,
    ) -> None:
        self.message = message
        self.stage_id = stage_id
        self.details = details or {}
        if retryable is not None:
            self.retryable = retryable
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """Serialize error surface for logging and API boundaries."""
        return {
            "error_class": self.error_class,
            "message": self.message,
            "stage_id": self.stage_id,
            "retryable": self.retryable,
            "details": dict(self.details),
        }


class AdmissionError(AnalysisRuntimeError):
    """Invalid input AnalysisContext."""

    error_class = "AdmissionError"


class KnowledgeError(AnalysisRuntimeError):
    """Knowledge session bind / SDK failure."""

    error_class = "KnowledgeError"
    retryable = True


class CompatibilityError(AnalysisRuntimeError):
    """Incompatible knowledge / engine set."""

    error_class = "CompatibilityError"


class IntegrityError(AnalysisRuntimeError):
    """Integrity failure."""

    error_class = "IntegrityError"


class PrerequisiteError(AnalysisRuntimeError):
    """Missing prior StageResult."""

    error_class = "PrerequisiteError"


class StageExecutionError(AnalysisRuntimeError):
    """Module evaluate failure."""

    error_class = "StageExecutionError"
    retryable = True


class ValidationError(AnalysisRuntimeError):
    """Pre/post/final validation failure."""

    error_class = "ValidationError"


class CacheError(AnalysisRuntimeError):
    """Runtime cache corruption / revalidation failure."""

    error_class = "CacheError"


class StateError(AnalysisRuntimeError):
    """Illegal lifecycle or order violation."""

    error_class = "StateError"


class AbortedError(AnalysisRuntimeError):
    """Governed abort."""

    error_class = "AbortedError"


class RegistrationError(AnalysisRuntimeError):
    """Module registration failure."""

    error_class = "RegistrationError"
