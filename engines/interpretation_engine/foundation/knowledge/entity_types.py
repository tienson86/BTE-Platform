"""Canonical knowledge entity types and engine inventories."""

from __future__ import annotations

from typing import Final

KNOWLEDGE_ENTITY_TYPE_STATE: Final[str] = "state"
KNOWLEDGE_ENTITY_TYPE_PATTERN: Final[str] = "pattern"
KNOWLEDGE_ENTITY_TYPE_TEN_GOD: Final[str] = "ten_god"
KNOWLEDGE_ENTITY_TYPE_SHEN_SHA: Final[str] = "shen_sha"

CANONICAL_KNOWLEDGE_ENTITY_TYPES: Final[tuple[str, ...]] = (
    "stem",
    "role",
    "element",
    "state",
    "pattern",
    "ten_god",
    "shen_sha",
)

# Strength Engine V2 level rules (database/12_strength/06_priority_rules.csv).
# Engine inventory is strong | balanced | weak. very_strong / very_weak are not emitted.
STRENGTH_STATE_KEYS: Final[tuple[str, ...]] = (
    "strong",
    "balanced",
    "weak",
)

# Heavenly stems produced as Useful God values by season/temperature/flow rules.
USEFUL_GOD_STEM_KEYS: Final[tuple[str, ...]] = (
    "Giáp",
    "Ất",
    "Bính",
    "Đinh",
    "Mậu",
    "Kỷ",
    "Canh",
    "Tân",
    "Nhâm",
    "Quý",
)

# Ten-god role names produced as Useful God / Hỷ / Kỵ by strength and special rules.
# Engine candidate_type for these values is ``ten_god``; knowledge entity_type is ``role``.
USEFUL_GOD_ROLE_KEYS: Final[tuple[str, ...]] = (
    "Thực Thần",
    "Thương Quan",
    "Tỷ Kiên",
    "Kiếp Tài",
    "Chính Tài",
    "Thiên Tài",
    "Chính Quan",
    "Thất Sát",
    "Chính Ấn",
    "Thiên Ấn",
)

ENGINE_CANDIDATE_TYPES: Final[tuple[str, ...]] = (
    "stem",
    "ten_god",
)

KNOWLEDGE_READINESS_READY = "READY"
KNOWLEDGE_READINESS_PARTIAL = "PARTIAL"

# Pattern Engine V2 codes from database/14_pattern/*.csv — do not guess extra labels.
PATTERN_MAIN_KEYS: Final[tuple[str, ...]] = (
    "chinh_quan",
    "that_sat",
    "chinh_tai",
    "thien_tai",
    "thuc_than",
    "thuong_quan",
    "chinh_an",
    "thien_an",
    "ty_kien",
    "kiep_tai",
)
PATTERN_SPECIAL_KEYS: Final[tuple[str, ...]] = (
    "khuc_truc",
    "viem_thuong",
    "nhuan_ha",
    "gia_sac",
    "jia_wang",
)
PATTERN_FOLLOW_KEYS: Final[tuple[str, ...]] = (
    "tong_vuong",
    "tong_tai",
    "tong_sat",
    "tong_quan",
    "tong_nhi",
    "tong_an",
)
PATTERN_COMBINATION_KEYS: Final[tuple[str, ...]] = (
    "quan_an",
    "sat_an",
    "thuc_than_sinh_tai",
    "thuong_quan_phoi_an",
    "tai_quan_song_my",
)
PATTERN_KEYS: Final[tuple[str, ...]] = (
    *PATTERN_MAIN_KEYS,
    *PATTERN_SPECIAL_KEYS,
    *PATTERN_FOLLOW_KEYS,
    *PATTERN_COMBINATION_KEYS,
)

# Ten Gods Engine labels from engines/ten_gods_engine/constants.py.
# The 10 classic gods plus Nhật Chủ (god_id=day_master) which the engine emits
# when a stem equals the day master. Do not guess extra aliases.
TEN_GOD_ROLE_KEYS: Final[tuple[str, ...]] = (
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
TEN_GOD_DAY_MASTER_KEY: Final[str] = "Nhật Chủ"
TEN_GOD_KEYS: Final[tuple[str, ...]] = (
    *TEN_GOD_ROLE_KEYS,
    TEN_GOD_DAY_MASTER_KEY,
)
TEN_GOD_PILLAR_KEYS: Final[tuple[str, ...]] = ("year", "month", "day", "hour")

# Production ShenShaService catalog (engines/bazi_engine/shensha/service.py).
# Closed list of names the production engine can emit. Do not add analysis-CSV extras.
SHEN_SHA_KEYS: Final[tuple[str, ...]] = (
    "Thiên Ất Quý Nhân",
    "Thiên Ất",
    "Văn Xương",
    "Lộc Thần",
    "Hồng Loan",
    "Thiên Hỷ",
    "Hoa Cái",
    "Dương Nhẫn",
    "Thiên Đức",
    "Thiên Đức Quý Nhân",
    "Nguyệt Đức",
    "Nguyệt Đức Quý Nhân",
)
