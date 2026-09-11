"""Layer 1–2 parser: raw digits and gua/modifier classification."""

from __future__ import annotations

from engines.number_energy.constants import (
    DIGIT_PROFILES,
    MAX_INPUT_DIGITS,
    is_ascii_digit_string,
)
from engines.number_energy.exceptions import NumberEnergyValidationError
from engines.number_energy.types import ClassifiedDigit, ParsedNumber


def parse_number_string(number: str) -> ParsedNumber:
    """Parse a digit string into classified gua and modifier digits.

    V1 accepts a string of digits ``0-9`` only. Non-digit input is rejected
    rather than interpreted.
    """
    if not isinstance(number, str):
        raise NumberEnergyValidationError("number input must be a string")

    raw = number.strip()
    if not raw:
        raise NumberEnergyValidationError("number input must not be empty")
    if not is_ascii_digit_string(raw):
        raise NumberEnergyValidationError(
            "number input must contain digits 0-9 only"
        )
    if len(raw) > MAX_INPUT_DIGITS:
        raise NumberEnergyValidationError(
            f"number input must not exceed {MAX_INPUT_DIGITS} digits"
        )

    raw_digits = tuple(int(ch) for ch in raw)
    classified = tuple(
        _classify_digit(index=index, digit=digit)
        for index, digit in enumerate(raw_digits)
    )
    return ParsedNumber(
        input_raw=raw,
        raw_digits=raw_digits,
        classified_digits=classified,
    )


def _classify_digit(*, index: int, digit: int) -> ClassifiedDigit:
    """Classify one digit from the frozen digit profile table."""
    profile = DIGIT_PROFILES[digit]
    return ClassifiedDigit(
        index=index,
        digit=digit,
        internal_type=str(profile["internal_type"]),
        gua_or_field=str(profile["gua_or_field"]),
        direction=str(profile["direction"]),
        element=profile["element"],
        group=str(profile["group"]),
        pair_role=str(profile["pair_role"]),
    )
