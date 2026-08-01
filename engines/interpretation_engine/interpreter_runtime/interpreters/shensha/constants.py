"""Constants for Shensha Interpreter business logic."""

from __future__ import annotations

SHENSHA_MODULE_IDS: tuple[str, ...] = (
    "shensha",
    "shen_sha",
    "shensha_engine",
    "than_sat",
    "07_shensha",
)

SHENSHA_SECTION_TYPE = "shensha"
SHENSHA_INTERPRETER_ID = "shensha_interpreter"
SHENSHA_INTERPRETER_VERSION = "1.0.0"

PRESENCE_KEYS: tuple[str, ...] = (
    "presence",
    "shensha",
    "than_sat",
    "stars",
    "detected",
)
AUSPICIOUS_KEYS: tuple[str, ...] = (
    "auspicious",
    "cat_tinh",
    "positive",
)
INAUSPICIOUS_KEYS: tuple[str, ...] = (
    "inauspicious",
    "hung_tinh",
    "negative",
)
INTERACTION_KEYS: tuple[str, ...] = (
    "interactions",
    "xung_dot",
)
SCORE_KEYS: tuple[str, ...] = (
    "shensha_score",
    "than_sat_score",
    "score",
)

# Importance rank for muc_do / cap_do / loai tokens (higher = more important).
IMPORTANCE_RANK: dict[str, int] = {
    "dai_cat": 100,
    "dai_cát": 100,
    "rat_cat": 90,
    "rất_cát": 90,
    "cat": 80,
    "cát": 80,
    "cat_tinh": 80,
    "trung_binh": 50,
    "binh": 50,
    "binh_tinh": 50,
    "hung": 70,
    "hung_tinh": 70,
    "dai_hung": 95,
    "đại_hung": 95,
}

POSITIVE_LOAI: frozenset[str] = frozenset(
    {"cat_tinh", "cát_tinh", "cat", "cát", "auspicious", "positive"}
)
NEGATIVE_LOAI: frozenset[str] = frozenset(
    {"hung_tinh", "hung", "inauspicious", "negative"}
)
