"""Constants for Strength Interpreter business logic."""

from __future__ import annotations

STRENGTH_MODULE_IDS: tuple[str, ...] = (
    "strength",
    "strength_engine",
    "01_strength",
)

STRENGTH_SECTION_TYPE = "strength"
STRENGTH_INTERPRETER_ID = "strength_interpreter"
STRENGTH_INTERPRETER_VERSION = "1.0.0"

# Payload / score key aliases (Pack 02 FinalResult shapes vary).
BODY_KEYS: tuple[str, ...] = (
    "body_strength",
    "body_score",
    "strength_score",
    "score",
)
SEASON_KEYS: tuple[str, ...] = (
    "season_strength",
    "season_score",
    "month_strength",
    "month_score",
)
ROOT_KEYS: tuple[str, ...] = (
    "root_strength",
    "root_score",
)
STEM_KEYS: tuple[str, ...] = (
    "stem_strength",
    "stem_score",
    "stem_support_score",
)
SUPPORT_KEYS: tuple[str, ...] = (
    "support_score",
    "support_strength",
)
DRAIN_KEYS: tuple[str, ...] = (
    "drain_score",
    "drain_strength",
    "flow_score",
)
BALANCE_KEYS: tuple[str, ...] = (
    "balance_score",
    "balance_strength",
)
FINAL_LEVEL_KEYS: tuple[str, ...] = (
    "final_strength",
    "strength_level",
    "classification",
    "level",
)
FINAL_SCORE_KEYS: tuple[str, ...] = (
    "final_strength_score",
    "strength_score",
    "score",
)

STEM_SUPPORT_TYPE = "Thiên Can trợ lực"
STEM_SUPPORT_RULE_CODES: frozenset[str] = frozenset(
    {"STEM_SUPPORT", "sup_003", "SP003"}
)
