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


RELATION_SAME = "Đồng hành"
RELATION_DM_GENERATES = "Nhật Chủ sinh"
RELATION_OTHER_GENERATES = "Đối tượng sinh"
RELATION_DM_CONTROLS = "Nhật Chủ khắc"
RELATION_OTHER_CONTROLS = "Đối tượng khắc"
POLARITY_SAME = "Cùng âm dương"
POLARITY_DIFF = "Khác âm dương"


def stem_element(stem: str) -> str:
    """Ngũ hành of a heavenly stem."""
    meta = STEM_META.get(stem)
    return meta[0] if meta else ""


def stem_yin_yang(stem: str) -> str:
    """Âm Dương of a heavenly stem."""
    meta = STEM_META.get(stem)
    return meta[1] if meta else ""


def element_relation(day_master: str, other_stem: str) -> str:
    """Ngũ hành relation of target stem versus Day Master."""
    dm_el = stem_element(day_master)
    other_el = stem_element(other_stem)
    if not dm_el or not other_el:
        return ""
    if dm_el == other_el:
        return RELATION_SAME
    if GENERATES[other_el] == dm_el:
        return RELATION_OTHER_GENERATES
    if GENERATES[dm_el] == other_el:
        return RELATION_DM_GENERATES
    if CONTROLS[dm_el] == other_el:
        return RELATION_DM_CONTROLS
    if CONTROLS[other_el] == dm_el:
        return RELATION_OTHER_CONTROLS
    return ""


def polarity_relation(day_master: str, other_stem: str) -> str:
    """Yin/yang relation of target stem versus Day Master."""
    dm_pol = stem_yin_yang(day_master)
    other_pol = stem_yin_yang(other_stem)
    if not dm_pol or not other_pol:
        return ""
    return POLARITY_SAME if dm_pol == other_pol else POLARITY_DIFF


def stem_mapping_facts(day_master: str, other_stem: str) -> dict[str, str]:
    """Evidence facts for one Day Master × stem pair. Does not overlay Nhật Chủ."""
    return {
        "element": stem_element(other_stem),
        "yin_yang": stem_yin_yang(other_stem),
        "element_relation": element_relation(day_master, other_stem),
        "polarity_relation": polarity_relation(day_master, other_stem),
        "ten_god": ten_god_name(day_master, other_stem),
    }


def ten_god_name(day_master: str, other_stem: str) -> str:
    """Resolve Thập thần label from day master stem to another stem."""
    relation = element_relation(day_master, other_stem)
    polarity = polarity_relation(day_master, other_stem)
    same = polarity == POLARITY_SAME
    if relation == RELATION_SAME:
        return "Tỷ Kiên" if same else "Kiếp Tài"
    if relation == RELATION_OTHER_GENERATES:
        return "Thiên Ấn" if same else "Chính Ấn"
    if relation == RELATION_DM_GENERATES:
        return "Thực Thần" if same else "Thương Quan"
    if relation == RELATION_DM_CONTROLS:
        return "Thiên Tài" if same else "Chính Tài"
    if relation == RELATION_OTHER_CONTROLS:
        return "Thất Sát" if same else "Chính Quan"
    return ""


def day_master_element(stem: str) -> str:
    """Ngũ hành của Nhật Chủ."""
    return stem_element(stem)


def day_master_yin_yang(stem: str) -> str:
    """Âm Dương của Nhật Chủ."""
    return stem_yin_yang(stem)
