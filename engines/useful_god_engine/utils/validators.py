"""Validators for Useful God Engine."""

from __future__ import annotations

from typing import Any


REQUIRED_CONTEXT_FIELDS = (
    "day_master",
    "day_master_element",
    "month_branch",
    "month_branch_ten_god",
    "season",
    "temperature_type",
)


class UsefulGodValidationError(ValueError):
    """Raised when Useful God context/result is invalid."""


def validate_context(context: Any) -> None:
    missing = [name for name in REQUIRED_CONTEXT_FIELDS if getattr(context, name, None) in (None, "")]
    if missing:
        raise UsefulGodValidationError("Missing required context fields: " + ", ".join(missing))


def validate_result(result: Any) -> None:
    if not getattr(result, "success", False):
        return
    useful_god = getattr(result, "useful_god", None)
    if not useful_god:
        raise UsefulGodValidationError("UsefulGodResult.success=True but useful_god is empty")
