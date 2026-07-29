"""Thập thần lookup from Nhật Chủ stem to another heavenly stem."""

from __future__ import annotations

STEM_META: dict[str, tuple[str, str]] = {
    "Giáp": ("Mộc", "Dương"),
    "Ất": ("Mộc", "Âm"),
    "Bính": ("Hỏa", "Dương"),
    "Đinh": ("Hỏa", "Âm"),
    "Mậu": ("Thổ", "Dương"),
    "Kỷ": ("Thổ", "Âm"),
    "Canh": ("Kim", "Dương"),
    "Tân": ("Kim", "Âm"),
    "Nhâm": ("Thủy", "Dương"),
    "Quý": ("Thủy", "Âm"),
}

GENERATES: dict[str, str] = {
    "Mộc": "Hỏa",
    "Hỏa": "Thổ",
    "Thổ": "Kim",
    "Kim": "Thủy",
    "Thủy": "Mộc",
}

CONTROLS: dict[str, str] = {
    "Mộc": "Thổ",
    "Hỏa": "Kim",
    "Thổ": "Thủy",
    "Kim": "Mộc",
    "Thủy": "Hỏa",
}


def ten_god_name(day_master: str, other_stem: str) -> str:
    """Resolve Thập thần label from day master stem to another stem."""
    dm = STEM_META.get(day_master)
    other = STEM_META.get(other_stem)
    if not dm or not other:
        return ""
    dm_el, dm_pol = dm
    other_el, other_pol = other
    same = dm_pol == other_pol
    if dm_el == other_el:
        return "Tỷ Kiên" if same else "Kiếp Tài"
    if GENERATES[other_el] == dm_el:
        return "Thiên Ấn" if same else "Chính Ấn"
    if GENERATES[dm_el] == other_el:
        return "Thực Thần" if same else "Thương Quan"
    if CONTROLS[dm_el] == other_el:
        return "Thiên Tài" if same else "Chính Tài"
    if CONTROLS[other_el] == dm_el:
        return "Thất Sát" if same else "Chính Quan"
    return ""


def day_master_element(stem: str) -> str:
    """Ngũ hành của Nhật Chủ."""
    meta = STEM_META.get(stem)
    return meta[0] if meta else ""


def day_master_yin_yang(stem: str) -> str:
    """Âm Dương của Nhật Chủ."""
    meta = STEM_META.get(stem)
    return meta[1] if meta else ""
