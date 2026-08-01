"""Constants for Pattern Interpreter business logic."""

from __future__ import annotations

PATTERN_MODULE_IDS: tuple[str, ...] = (
    "pattern",
    "pattern_engine",
    "14_pattern",
)

PATTERN_SECTION_TYPE = "pattern"
PATTERN_INTERPRETER_ID = "pattern_interpreter"
PATTERN_INTERPRETER_VERSION = "1.0.0"

PATTERN_KEYS: tuple[str, ...] = (
    "pattern",
    "main_pattern",
    "final_pattern",
    "main",
    "name",
    "pattern_name",
    "cach_cuc",
)
STATUS_KEYS: tuple[str, ...] = (
    "status",
    "pattern_status",
)
FOLLOW_KEYS: tuple[str, ...] = (
    "follow_type",
    "follow",
    "tong_cach",
)
SCORE_KEYS: tuple[str, ...] = (
    "score",
    "pattern_score",
)
PRIORITY_KEYS: tuple[str, ...] = (
    "priority",
    "pattern_priority",
)
MONTH_BRANCH_TEN_GOD_KEYS: tuple[str, ...] = (
    "month_branch_ten_god",
    "month_ten_god",
)
STRENGTH_LEVEL_KEYS: tuple[str, ...] = (
    "strength_level",
    "than_vuong_nhuoc",
)
