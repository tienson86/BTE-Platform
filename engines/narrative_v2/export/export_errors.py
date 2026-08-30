"""Export-layer errors. Shadow Presentation consumers only."""

from __future__ import annotations


class ExportError(Exception):
    """Base error for the Presentation Export Layer."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ExportValidationError(ExportError):
    """Export contract failed. No silent fallback composition."""


class IncompatiblePresentationVersion(ExportValidationError):
    """Consumer rejected a Presentation that is not v2.1."""
