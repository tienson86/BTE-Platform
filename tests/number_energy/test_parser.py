"""Parser tests for Number Energy Engine V1."""

from __future__ import annotations

import pytest

from engines.number_energy.exceptions import NumberEnergyValidationError
from engines.number_energy.parser import parse_number_string


def test_parse_keeps_raw_digit_order() -> None:
    parsed = parse_number_string("141319")
    assert parsed.input_raw == "141319"
    assert parsed.raw_digits == (1, 4, 1, 3, 1, 9)
    assert [item.digit for item in parsed.classified_digits] == [1, 4, 1, 3, 1, 9]


def test_classify_ordinary_gua_and_modifiers() -> None:
    parsed = parse_number_string("105")
    assert parsed.classified_digits[0].internal_type == "gua"
    assert parsed.classified_digits[0].pair_role == "normal pair digit"
    assert parsed.classified_digits[1].internal_type == "modifier"
    assert parsed.classified_digits[1].gua_or_field == "Âm trường / Trung cung Âm"
    assert parsed.classified_digits[2].internal_type == "modifier"
    assert parsed.classified_digits[2].gua_or_field == "Dương trường / Trung cung Dương"


@pytest.mark.parametrize("raw", ["", "   ", "12a", "12-13", "+84123"])
def test_reject_non_digit_input(raw: str) -> None:
    with pytest.raises(NumberEnergyValidationError):
        parse_number_string(raw)
