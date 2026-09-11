"""Phone-number input shaping for V1.1. Does not invent Du Niên pairs."""

from __future__ import annotations


def split_phone_input(number: str) -> tuple[str, bool]:
    """Strip a single leading ``0`` as VN prefix; keep the body for Du Niên.

    Returns ``(analyzed_digits, had_leading_zero)``.
    """
    if number.startswith("0") and len(number) > 1:
        return number[1:], True
    return number, False


def has_interior_zero(analyzed_digits: str) -> bool:
    """Return True when ``0`` remains inside the analyzed phone body."""
    return "0" in analyzed_digits
