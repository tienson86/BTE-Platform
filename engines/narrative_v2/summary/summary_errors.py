"""Narrative V2 Summary error model.

N-IMP-06: assembly and validation failures only.
"""

from __future__ import annotations


class SummaryError(Exception):
    """Base error for Summary Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class SummaryValidationError(SummaryError):
    """Summary contract validation failed."""
