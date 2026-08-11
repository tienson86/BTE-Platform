"""ASCII helpers and constants for reference mapping (no inference)."""

from __future__ import annotations

SCHEMA_VERSION = "strength_profile_design_v0.1.0-candidate"

STEM_VI_TO_ASCII: dict[str, str] = {
    "Giáp": "giap",
    "Ất": "at",
    "Bính": "binh",
    "Đinh": "dinh",
    "Mậu": "mau",
    "Kỷ": "ky",
    "Canh": "canh",
    "Tân": "tan",
    "Nhâm": "nham",
    "Quý": "quy",
}

BRANCH_VI_TO_ASCII: dict[str, str] = {
    "Tý": "ty",
    "Sửu": "suu",
    "Dần": "dan",
    "Mão": "mao",
    "Thìn": "thin",
    "Tỵ": "ti",
    "Ngọ": "ngo",
    "Mùi": "mui",
    "Thân": "than",
    "Dậu": "dau",
    "Tuất": "tuat",
    "Hợi": "hoi",
}

ELEMENT_VI_TO_ASCII: dict[str, str] = {
    "Kim": "kim",
    "Mộc": "moc",
    "Thủy": "thuy",
    "Hỏa": "hoa",
    "Thổ": "tho",
}


def to_ascii_stem(value: str | None) -> str | None:
    """Map known stem labels to ASCII; pass through lowercase ascii; else None."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text in STEM_VI_TO_ASCII:
        return STEM_VI_TO_ASCII[text]
    lower = text.lower()
    if lower in STEM_VI_TO_ASCII.values():
        return lower
    return None


def to_ascii_branch(value: str | None) -> str | None:
    """Map known branch labels to ASCII."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text in BRANCH_VI_TO_ASCII:
        return BRANCH_VI_TO_ASCII[text]
    lower = text.lower()
    if lower in BRANCH_VI_TO_ASCII.values():
        return lower
    return None


def to_ascii_element(value: str | None) -> str | None:
    """Map known element labels to ASCII."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text in ELEMENT_VI_TO_ASCII:
        return ELEMENT_VI_TO_ASCII[text]
    lower = text.lower()
    if lower in ELEMENT_VI_TO_ASCII.values():
        return lower
    return None


def unknown() -> str:
    return "unknown"


def not_available() -> str:
    return "not_available"
