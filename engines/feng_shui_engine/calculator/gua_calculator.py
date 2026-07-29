"""Cung Phi / Mệnh Quái calculator (V1 — year + gender only)."""

from __future__ import annotations

from engines.feng_shui_engine.data import load_json
from engines.feng_shui_engine.exceptions import FengShuiValidationError


def _reduce_to_single_digit(value: int) -> int:
    """Reduce a non-negative integer to a single digit 1–9 (0 → 9)."""
    n = abs(int(value))
    while n > 9:
        n = sum(int(ch) for ch in str(n))
    return 9 if n == 0 else n


def _normalize_gender(gender: str | None) -> str:
    if gender is None or str(gender).strip() == "":
        raise FengShuiValidationError("gender is required for Cung Phi calculation")
    key = str(gender).strip().lower()
    if key in {"male", "nam", "m", "man", "boy"}:
        return "male"
    if key in {"female", "nu", "nữ", "f", "woman", "girl"}:
        return "female"
    raise FengShuiValidationError(f"unsupported gender: {gender!r}")


def year_digit_sum(year: int) -> int:
    """Sum the last two digits of ``year`` down to 1–9."""
    if year < 1:
        raise FengShuiValidationError(f"invalid birth year: {year}")
    return _reduce_to_single_digit(year % 100)


def calculate_gua_number(*, year: int, gender: str | None) -> int:
    """
    Compute Mệnh Quái number (1–9, never 5) from birth year and gender.

    Uses the common Bát Trạch digit method with pre-/post-2000 branches.
    """
    sex = _normalize_gender(gender)
    digit = year_digit_sum(year)
    table = load_json("gua_table.json")
    male_five = int(table.get("male_five_maps_to", 2))
    female_five = int(table.get("female_five_maps_to", 8))

    if year < 2000:
        if sex == "male":
            gua = 10 - digit
        else:
            gua = _reduce_to_single_digit(5 + digit)
    else:
        if sex == "male":
            gua = 9 - digit
            if gua == 0:
                gua = 9
        else:
            gua = _reduce_to_single_digit(6 + digit)

    if gua == 5:
        gua = male_five if sex == "male" else female_five
    if gua not in {1, 2, 3, 4, 6, 7, 8, 9}:
        raise FengShuiValidationError(f"invalid gua number computed: {gua}")
    return gua


def gua_name_for_number(gua_number: int) -> str:
    """Look up gua display name from data table."""
    table = load_json("gua_table.json")
    entry = (table.get("guas") or {}).get(str(gua_number))
    if not entry or not entry.get("name"):
        raise FengShuiValidationError(f"unknown gua number: {gua_number}")
    return str(entry["name"])
