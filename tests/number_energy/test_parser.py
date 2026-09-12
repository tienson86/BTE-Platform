"""Parser tests for Number Energy Engine V1."""

from __future__ import annotations

import pytest

from engines.number_energy.constants import MAX_INPUT_DIGITS
from engines.number_energy.exceptions import NumberEnergyValidationError
from engines.number_energy.parser import parse_number_string
from engines.number_energy.plate_input import normalize_plate_input


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


@pytest.mark.parametrize("raw", ["", "   ", "12a", "12-13", "+84123", "１２３", "١٠٣"])
def test_reject_non_digit_input(raw: str) -> None:
    with pytest.raises(NumberEnergyValidationError):
        parse_number_string(raw)


def test_reject_overlong_digit_string() -> None:
    with pytest.raises(NumberEnergyValidationError):
        parse_number_string("1" * (MAX_INPUT_DIGITS + 1))


def test_accepts_ascii_digits_with_surrounding_space() -> None:
    parsed = parse_number_string(" 103 ")
    assert parsed.input_raw == "103"
    assert parsed.raw_digits == (1, 0, 3)


def test_normalize_plate_letters_to_english_alphabet_positions() -> None:
    assert normalize_plate_input("30A-123.45") == "30112345"
    assert normalize_plate_input("30F-058.11") == "30605811"
    assert normalize_plate_input("30F05811") == "30605811"
    assert normalize_plate_input("30F-05811") == "30605811"
    assert normalize_plate_input("30A1-05811") == "301105811"
    assert normalize_plate_input("30AM-05811") == "3011305811"
    assert normalize_plate_input("29X1-123.45") == "2924112345"
    assert normalize_plate_input("A B C Z") == "12326"


@pytest.mark.parametrize("raw", ["30Á-123", "30@123", "１２A"])
def test_reject_invalid_plate_characters(raw: str) -> None:
    with pytest.raises(NumberEnergyValidationError):
        normalize_plate_input(raw)
