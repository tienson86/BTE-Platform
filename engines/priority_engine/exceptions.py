"""Custom exceptions for the priority engine."""

from __future__ import annotations


class PriorityEngineError(Exception):
    """Base class for all priority engine errors."""


class PriorityDataNotFoundError(PriorityEngineError):
    """Raised when required priority data files cannot be found."""


class PriorityDataValidationError(PriorityEngineError):
    """Raised when priority data is malformed or internally inconsistent."""


class PriorityConditionError(PriorityEngineError):
    """Raised when a priority condition cannot be evaluated."""


class PriorityResolutionError(PriorityEngineError):
    """Raised when matched priority rules cannot be resolved."""
