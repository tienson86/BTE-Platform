"""Canonical ShenSha identity, aliases, and display labels.

Published V1.0 names are the Quý Nhân forms plus independent stars.
Legacy short names stay as aliases and are never a second logical star.
"""

from __future__ import annotations

from typing import Final, Mapping

PILLAR_KEYS: Final[tuple[str, ...]] = ("year", "month", "day", "hour")

PILLAR_LABELS_VI: Final[Mapping[str, str]] = {
    "year": "Năm",
    "month": "Tháng",
    "day": "Ngày",
    "hour": "Giờ",
}

SOURCE_LABELS_VI: Final[Mapping[str, str]] = {
    "day_stem": "Nhật can",
    "year_branch": "Niên chi",
    "day_branch": "Nhật chi",
    "month_branch": "Nguyệt chi",
}

LOCATION_STEM: Final[str] = "stem"
LOCATION_BRANCH: Final[str] = "branch"
TARGET_BRANCH: Final[str] = "earthly_branch"
TARGET_STEM: Final[str] = "heavenly_stem"
TARGET_STEM_OR_BRANCH: Final[str] = "stem_or_branch"

ID_TIAN_YI: Final[str] = "tian_yi"
ID_WEN_CHANG: Final[str] = "wen_chang"
ID_LU_SHEN: Final[str] = "lu_shen"
ID_HONG_LUAN: Final[str] = "hong_luan"
ID_TIAN_XI: Final[str] = "tian_xi"
ID_HUA_GAI: Final[str] = "hua_gai"
ID_YANG_REN: Final[str] = "yang_ren"
ID_TIAN_DE: Final[str] = "tian_de"
ID_YUE_DE: Final[str] = "yue_de"

NAME_TIAN_YI: Final[str] = "Thiên Ất Quý Nhân"
NAME_WEN_CHANG: Final[str] = "Văn Xương"
NAME_LU_SHEN: Final[str] = "Lộc Thần"
NAME_HONG_LUAN: Final[str] = "Hồng Loan"
NAME_TIAN_XI: Final[str] = "Thiên Hỷ"
NAME_HUA_GAI: Final[str] = "Hoa Cái"
NAME_YANG_REN: Final[str] = "Dương Nhẫn"
NAME_TIAN_DE: Final[str] = "Thiên Đức Quý Nhân"
NAME_YUE_DE: Final[str] = "Nguyệt Đức Quý Nhân"

ALIAS_TIAN_YI: Final[str] = "Thiên Ất"
ALIAS_TIAN_DE: Final[str] = "Thiên Đức"
ALIAS_YUE_DE: Final[str] = "Nguyệt Đức"

CANONICAL_NAMES: Final[Mapping[str, str]] = {
    ID_TIAN_YI: NAME_TIAN_YI,
    ID_WEN_CHANG: NAME_WEN_CHANG,
    ID_LU_SHEN: NAME_LU_SHEN,
    ID_HONG_LUAN: NAME_HONG_LUAN,
    ID_TIAN_XI: NAME_TIAN_XI,
    ID_HUA_GAI: NAME_HUA_GAI,
    ID_YANG_REN: NAME_YANG_REN,
    ID_TIAN_DE: NAME_TIAN_DE,
    ID_YUE_DE: NAME_YUE_DE,
}

CANONICAL_ALIASES: Final[Mapping[str, tuple[str, ...]]] = {
    ID_TIAN_YI: (ALIAS_TIAN_YI,),
    ID_TIAN_DE: (ALIAS_TIAN_DE,),
    ID_YUE_DE: (ALIAS_YUE_DE,),
}

PUBLISHED_NAMES: Final[tuple[str, ...]] = (
    NAME_TIAN_YI,
    NAME_WEN_CHANG,
    NAME_LU_SHEN,
    NAME_HONG_LUAN,
    NAME_TIAN_XI,
    NAME_HUA_GAI,
    NAME_YANG_REN,
    NAME_TIAN_DE,
    NAME_YUE_DE,
)

LEGACY_ALIAS_NAMES: Final[tuple[str, ...]] = (
    ALIAS_TIAN_YI,
    ALIAS_TIAN_DE,
    ALIAS_YUE_DE,
)

ALIAS_TO_CANONICAL: Final[Mapping[str, str]] = {
    ALIAS_TIAN_YI: NAME_TIAN_YI,
    ALIAS_TIAN_DE: NAME_TIAN_DE,
    ALIAS_YUE_DE: NAME_YUE_DE,
}

RULE_TIAN_YI: Final[str] = "signal_maps.TIAN_YI_BRANCHES"
RULE_WEN_CHANG: Final[str] = "signal_maps.WEN_CHANG_BRANCH"
RULE_LU_SHEN: Final[str] = "signal_maps.LU_SHEN_BRANCH"
RULE_HONG_LUAN: Final[str] = "signal_maps.HONG_LUAN_OPPOSITE"
RULE_TIAN_XI: Final[str] = "signal_maps.TIAN_XI_BRANCH"
RULE_HUA_GAI: Final[str] = "signal_maps.HUA_GAI_BRANCHES"
RULE_YANG_REN: Final[str] = "signal_maps.YANG_REN_BRANCH"
RULE_TIAN_DE: Final[str] = "signal_maps.TIAN_DE_BRANCH"
RULE_YUE_DE: Final[str] = "signal_maps.YUE_DE_STEM"


def aliases_for(star_id: str) -> tuple[str, ...]:
    """Return legacy aliases for a canonical star id."""
    return CANONICAL_ALIASES.get(star_id, ())


def canonical_name_for(star_id: str) -> str:
    """Return the published V1.0 display name for a star id."""
    return CANONICAL_NAMES[star_id]
