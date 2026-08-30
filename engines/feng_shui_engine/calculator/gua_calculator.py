"""Cung Phi / Mệnh Quái calculator — Gregorian digit-sum (Calendar SSOT)."""

from __future__ import annotations

from engines.calendar_engine.cung_phi import (
    calculate_cung_phi,
)
from engines.calendar_engine.exceptions import CalendarValidationError
from engines.feng_shui_engine.data import load_json
from engines.feng_shui_engine.exceptions import FengShuiValidationError


def _reduce_to_single_digit(value: int) -> int:
    """Reduce a non-negative integer to a single digit 1–9 (0 → 9)."""
    n = abs(int(value))
    while n > 9:
        n = sum(int(ch) for ch in str(n))
    return 9 if n == 0 else n


def year_digit_sum(year: int) -> int:
    """Sum the last two digits of ``year`` down to 1–9.

    Kept for callers that still inspect the legacy helper. Personal Cung Phi
    uses ``calculate_cung_phi`` (all Gregorian digits).
    """
    if year < 1:
        raise FengShuiValidationError(f"invalid birth year: {year}")
    return _reduce_to_single_digit(year % 100)


def calculate_gua_number(*, year: int, gender: str | None) -> int:
    """
    Compute Mệnh Quái Lo Shu number (1–9, never 5) from Gregorian year + gender.
    """
    try:
        return calculate_cung_phi(year=year, gender=gender).gua_number
    except CalendarValidationError as exc:
        raise FengShuiValidationError(str(exc)) from exc


def gua_name_for_number(gua_number: int) -> str:
    """Look up gua display name from data table."""
    table = load_json("gua_table.json")
    entry = (table.get("guas") or {}).get(str(gua_number))
    if not entry or not entry.get("name"):
        raise FengShuiValidationError(f"unknown gua number: {gua_number}")
    return str(entry["name"])
