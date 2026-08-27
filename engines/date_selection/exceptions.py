"""Date Selection Engine exceptions."""

from __future__ import annotations


class DateSelectionError(Exception):
    """Base error for Date Selection Engine."""


class DateSelectionValidationError(DateSelectionError):
    """Invalid input for Date Selection."""
