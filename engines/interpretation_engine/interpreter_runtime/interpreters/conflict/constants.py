"""Constants for Conflict Interpreter business logic."""

from __future__ import annotations

CONFLICT_MODULE_IDS: tuple[str, ...] = (
    "conflict",
    "conflict_engine",
    "combination",
    "combination_engine",
    "06_combination",
)

CONFLICT_SECTION_TYPE = "conflict"
CONFLICT_INTERPRETER_ID = "conflict_interpreter"
CONFLICT_INTERPRETER_VERSION = "1.0.0"

CLASH_KEYS: tuple[str, ...] = (
    "clashes",
    "clash",
    "xung",
    "luc_xung",
)
PUNISHMENT_KEYS: tuple[str, ...] = (
    "punishments",
    "punishment",
    "hinh",
    "tuong_hinh",
    "xing",
)
HARM_KEYS: tuple[str, ...] = (
    "harms",
    "harm",
    "hai",
    "luc_hai",
    "tuong_hai",
)
DESTRUCTION_KEYS: tuple[str, ...] = (
    "destructions",
    "destruction",
    "pha",
    "tuong_pha",
    "po",
)
SCORE_KEYS: tuple[str, ...] = (
    "conflict_score",
    "clash_score",
    "score",
)

CLASH_SCORE_TYPES: frozenset[str] = frozenset({"LIU_CHONG", "TIAN_GAN_CHONG", "CHONG_HUA"})
PUNISHMENT_SCORE_TYPES: frozenset[str] = frozenset({"XING", "ZI_XING"})
HARM_SCORE_TYPES: frozenset[str] = frozenset({"LIU_HAI"})
DESTRUCTION_SCORE_TYPES: frozenset[str] = frozenset({"LIU_PO"})
