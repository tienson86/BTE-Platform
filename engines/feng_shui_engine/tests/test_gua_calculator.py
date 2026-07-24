"""Unit tests for gua_calculator."""

from __future__ import annotations

import pytest

from engines.feng_shui_engine.calculator.gua_calculator import (
    calculate_gua_number,
    gua_name_for_number,
    year_digit_sum,
)
from engines.feng_shui_engine.exceptions import FengShuiValidationError


def test_year_digit_sum_basic() -> None:
    assert year_digit_sum(1990) == 9
    assert year_digit_sum(1985) == 4
    assert year_digit_sum(2000) == 9


@pytest.mark.parametrize(
    ("year", "gender", "expected"),
    [
        (1990, "male", 1),
        (1990, "female", 8),
        (1985, "male", 6),
        (1985, "female", 9),
        (2000, "male", 9),
        (2000, "female", 6),
        (1992, "male", 8),
        (1992, "female", 7),
    ],
)
def test_calculate_gua_number_known_cases(year: int, gender: str, expected: int) -> None:
    assert calculate_gua_number(year=year, gender=gender) == expected


def test_gua_name_for_number() -> None:
    assert gua_name_for_number(1) == "Khảm"
    assert gua_name_for_number(6) == "Càn"
    assert gua_name_for_number(9) == "Ly"


def test_gender_aliases() -> None:
    assert calculate_gua_number(year=1990, gender="nam") == 1
    assert calculate_gua_number(year=1990, gender="nữ") == 8


def test_missing_gender_raises() -> None:
    with pytest.raises(FengShuiValidationError):
        calculate_gua_number(year=1990, gender=None)
