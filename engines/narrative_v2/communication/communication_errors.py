"""Commercial Communication error model.

N-IMP-07B: consulting-style failures only. Does not rewrite Meaning.
"""

from __future__ import annotations


class CommunicationError(Exception):
    """Base error for Commercial Communication."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ConsultingStyleError(CommunicationError):
    """Consulting Style contract failure."""


class ConsultingStyleValidationError(ConsultingStyleError):
    """Consulting Style validation failed."""
