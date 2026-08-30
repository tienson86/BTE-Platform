"""Narrative V2 Rewrite error model.

N-IMP-05: unit rewrite and validation failures only.
"""

from __future__ import annotations


class RewriteError(Exception):
    """Base error for Commercial Rewrite Engine."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class RewriteValidationError(RewriteError):
    """Rewrite contract validation failed."""
