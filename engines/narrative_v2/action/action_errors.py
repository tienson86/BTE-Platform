"""Action Builder errors."""

from __future__ import annotations


class ActionError(Exception):
    """Base error for Action Builder."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ActionValidationError(ActionError):
    """Action contract validation failed."""
