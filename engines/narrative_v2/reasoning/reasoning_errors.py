"""Narrative V2 Reasoning error model.

N-IMP-03: graph construction and validation failures only.
"""

from __future__ import annotations


class ReasoningError(Exception):
    """Base error for Reasoning Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ReasoningValidationError(ReasoningError):
    """Reasoning contract validation failed."""
