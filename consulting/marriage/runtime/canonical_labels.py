"""Map Canonical labels onto TV-01 contract enums. No calculation."""

from __future__ import annotations

from consulting.marriage.exceptions import MarriageCanonicalContractError
from consulting.marriage.models.enums import FiveElement, YinYang

_ELEMENT_TOKENS: dict[str, FiveElement] = {
    "wood": FiveElement.WOOD,
    "moc": FiveElement.WOOD,
    "mộc": FiveElement.WOOD,
    "fire": FiveElement.FIRE,
    "hoa": FiveElement.FIRE,
    "hỏa": FiveElement.FIRE,
    "earth": FiveElement.EARTH,
    "tho": FiveElement.EARTH,
    "thổ": FiveElement.EARTH,
    "metal": FiveElement.METAL,
    "kim": FiveElement.METAL,
    "water": FiveElement.WATER,
    "thuy": FiveElement.WATER,
    "thủy": FiveElement.WATER,
}

_YIN_YANG_TOKENS: dict[str, YinYang] = {
    "yin": YinYang.YIN,
    "am": YinYang.YIN,
    "âm": YinYang.YIN,
    "yang": YinYang.YANG,
    "duong": YinYang.YANG,
    "dương": YinYang.YANG,
}


def map_five_element(token: str | None) -> FiveElement:
    """Map a Canonical element label onto FiveElement."""
    key = str(token or "").strip().lower()
    element = _ELEMENT_TOKENS.get(key)
    if element is None:
        raise MarriageCanonicalContractError(f"invalid_five_element:{token}")
    return element


def try_map_five_element(token: str | None) -> FiveElement | None:
    """Return a FiveElement when the token is recognized."""
    key = str(token or "").strip().lower()
    if not key:
        return None
    return _ELEMENT_TOKENS.get(key)


def map_yin_yang(token: str | None) -> YinYang:
    """Map a Canonical yin/yang label onto YinYang."""
    key = str(token or "").strip().lower()
    value = _YIN_YANG_TOKENS.get(key)
    if value is None:
        raise MarriageCanonicalContractError(f"invalid_yin_yang:{token}")
    return value
