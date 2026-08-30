"""Narrative V2 Evidence error model.

N-IMP-02: extraction and validation failures only. No astrology logic.
"""

from __future__ import annotations


class EvidenceError(Exception):
    """Base error for Evidence Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class EvidenceValidationError(EvidenceError):
    """Evidence contract validation failed."""
