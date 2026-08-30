"""Golden Dataset errors. Eligibility and immutability only."""

from __future__ import annotations


class GoldenError(Exception):
    """Base error for the Narrative V2 Golden Dataset."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class GoldenEligibilityError(GoldenError):
    """Case is not CERTIFIED and cannot enter the Golden Dataset."""


class GoldenImmutabilityError(GoldenError):
    """Attempted to overwrite a frozen Golden Case version."""


class GoldenValidationError(GoldenError):
    """Golden Case payload failed structural checks."""
