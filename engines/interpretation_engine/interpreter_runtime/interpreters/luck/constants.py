"""Constants for Luck Interpreter business logic."""

from __future__ import annotations

LUCK_MODULE_IDS: tuple[str, ...] = (
    "luck",
    "luck_engine",
    "dai_van",
    "11_dai_van",
    "08_luck",
)

LUCK_SECTION_TYPE = "luck"
LUCK_INTERPRETER_ID = "luck_interpreter"
LUCK_INTERPRETER_VERSION = "1.0.0"

DAYUN_KEYS: tuple[str, ...] = (
    "da_yun",
    "dayun",
    "dai_van",
    "current_dayun",
    "current_dai_van",
)
LIUNIAN_KEYS: tuple[str, ...] = (
    "liu_nian",
    "liunian",
    "luu_nien",
    "tieu_van",
    "current_liunian",
    "current_luu_nien",
)
LIUYUE_KEYS: tuple[str, ...] = (
    "liu_yue",
    "liuyue",
    "luu_nguyet",
    "nguyet_van",
    "current_liuyue",
    "current_luu_nguyet",
)
INTERACTION_KEYS: tuple[str, ...] = (
    "interactions",
    "luck_interactions",
    "tuong_tac",
)
SCORE_KEYS: tuple[str, ...] = (
    "luck_score",
    "dai_van_score",
    "score",
)

FAVORABLE_TOKENS: frozenset[str] = frozenset(
    {
        "favorable",
        "support",
        "dung_than",
        "dụng",
        "hy_than",
        "hỷ",
        "cat",
        "cát",
        "good",
        "positive",
        "joy",
        "useful",
    }
)
UNFAVORABLE_TOKENS: frozenset[str] = frozenset(
    {
        "unfavorable",
        "attack",
        "ky_than",
        "kỵ",
        "hung",
        "bad",
        "negative",
        "clash",
        "destroy",
    }
)

SUPPORT_EFFECT_TOKENS: frozenset[str] = frozenset(
    {"support", "combine", "hop", "hợp", "assist", "sheng", "sinh"}
)
ATTACK_EFFECT_TOKENS: frozenset[str] = frozenset(
    {"attack", "clash", "xung", "hai", "hại", "pha", "phá", "destroy", "ke"}
)
