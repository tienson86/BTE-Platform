"""Narrative V2 runtime error model.

N-IMP-01 defines the hierarchy only. No builder or narrative logic.
"""

from __future__ import annotations


class RuntimeError(Exception):
    """Base error for Narrative V2 runtime failures.

    Distinct from the builtin ``RuntimeError`` when imported from this module.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class PipelineError(RuntimeError):
    """Pipeline order or stage execution violation."""


class ValidationError(RuntimeError):
    """Runtime validation failed (ordering only in N-IMP-01)."""


class BuilderError(RuntimeError):
    """Builder registry error. No builder implementation in N-IMP-01."""
