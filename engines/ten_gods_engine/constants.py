"""Ten Gods Engine constants."""

from __future__ import annotations

ENGINE_VERSION = "1.0.0"

VISIBLE_STEM_WEIGHT = 1.0
DOMINANCE_MARGIN = 0.05
SECONDARY_WEIGHT_RATIO = 0.5

TEN_GOD_LABELS: tuple[str, ...] = (
    "Tỷ Kiên",
    "Kiếp Tài",
    "Thực Thần",
    "Thương Quan",
    "Thiên Tài",
    "Chính Tài",
    "Thất Sát",
    "Chính Quan",
    "Thiên Ấn",
    "Chính Ấn",
)

LABEL_TO_GOD_ID: dict[str, str] = {
    "Tỷ Kiên": "bi_jian",
    "Kiếp Tài": "jie_cai",
    "Thực Thần": "shi_shen",
    "Thương Quan": "shang_guan",
    "Thiên Tài": "pian_cai",
    "Chính Tài": "zheng_cai",
    "Thất Sát": "qi_sha",
    "Chính Quan": "zheng_guan",
    "Thiên Ấn": "pian_yin",
    "Chính Ấn": "zheng_yin",
}

GOD_ID_TO_LABEL: dict[str, str] = {
    god_id: label for label, god_id in LABEL_TO_GOD_ID.items()
}

TEN_GOD_IDS: tuple[str, ...] = tuple(LABEL_TO_GOD_ID[label] for label in TEN_GOD_LABELS)

# Structural family grouping (relative to Day Master).
GOD_ID_TO_FAMILY: dict[str, str] = {
    "bi_jian": "companion",
    "jie_cai": "companion",
    "shi_shen": "output",
    "shang_guan": "output",
    "pian_cai": "wealth",
    "zheng_cai": "wealth",
    "qi_sha": "officer",
    "zheng_guan": "officer",
    "pian_yin": "resource",
    "zheng_yin": "resource",
}

DAY_MASTER_GOD_ID = "day_master"
DAY_MASTER_LABEL = "Nhật Chủ"

PILLAR_ORDER: tuple[str, ...] = ("year", "month", "day", "hour")

HIDDEN_POSITION_NAMES: tuple[str, ...] = ("primary", "secondary", "tertiary")

# Family-level generation cycle: source → target.
FAMILY_GENERATES: tuple[tuple[str, str], ...] = (
    ("resource", "companion"),
    ("companion", "output"),
    ("output", "wealth"),
    ("wealth", "officer"),
    ("officer", "resource"),
)

# Family-level control cycle: controller → controlled.
FAMILY_CONTROLS: tuple[tuple[str, str], ...] = (
    ("officer", "companion"),
    ("companion", "wealth"),
    ("wealth", "resource"),
    ("resource", "output"),
    ("output", "officer"),
)

HIDDEN_STEMS_CSV = "09_hidden_stems/hidden_stems.csv"
