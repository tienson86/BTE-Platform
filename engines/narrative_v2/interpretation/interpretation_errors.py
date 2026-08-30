"""Narrative V2 Interpretation error model.

N-IMP-07: assembly and validation failures only.
"""

from __future__ import annotations


class InterpretationError(Exception):
    """Base error for Interpretation Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InterpretationValidationError(InterpretationError):
    """Interpretation contract validation failed."""
