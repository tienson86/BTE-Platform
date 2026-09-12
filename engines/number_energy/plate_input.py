"""Vehicle plate normalization for Number Energy.

Letters use the customer-provided English alphabet mapping:
A=1, B=2, ..., Z=26. Separators are ignored.
"""

from __future__ import annotations

import re

from engines.number_energy.constants import MAX_INPUT_DIGITS
from engines.number_energy.exceptions import NumberEnergyValidationError

PLATE_SEPARATORS_RE = re.compile(r"[.\s-]+")
PLATE_BODY_RE = re.compile(r"^[0-9A-Za-z]+$")


def normalize_plate_input(raw: str) -> str:
    """Convert a car/motorbike plate into the digit string used by the engine."""
    if not isinstance(raw, str):
        raise NumberEnergyValidationError("number input must be a string")
    compact = PLATE_SEPARATORS_RE.sub("", raw.strip())
    if not compact:
        raise NumberEnergyValidationError("plate input must not be empty")
    if not compact.isascii() or PLATE_BODY_RE.fullmatch(compact) is None:
        raise NumberEnergyValidationError(
            "plate input must contain ASCII letters A-Z, digits 0-9, and separators only"
        )
    digits = "".join(_plate_char_to_digits(ch) for ch in compact.upper())
    if len(digits) > MAX_INPUT_DIGITS:
        raise NumberEnergyValidationError(
            f"normalized plate input must not exceed {MAX_INPUT_DIGITS} digits"
        )
    return digits


def _plate_char_to_digits(ch: str) -> str:
    """Map one already-normalized plate character to digits."""
    if "A" <= ch <= "Z":
        return str(ord(ch) - ord("A") + 1)
    return ch
