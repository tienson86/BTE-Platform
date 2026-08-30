"""Presentation errors."""

from __future__ import annotations


class PresentationError(Exception):
    """Base error for Presentation Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class PresentationValidationError(PresentationError):
    """Presentation contract validation failed."""
