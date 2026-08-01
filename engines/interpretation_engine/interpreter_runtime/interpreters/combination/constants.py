"""Constants for Combination Interpreter business logic."""

from __future__ import annotations

COMBINATION_MODULE_IDS: tuple[str, ...] = (
    "combination",
    "combination_engine",
    "06_combination",
)

COMBINATION_SECTION_TYPE = "combination"
COMBINATION_INTERPRETER_ID = "combination_interpreter"
COMBINATION_INTERPRETER_VERSION = "1.0.0"

STEM_KEYS: tuple[str, ...] = (
    "stem_combinations",
    "stem_combination",
    "thien_can_hop",
    "can_hop",
)
BRANCH_KEYS: tuple[str, ...] = (
    "branch_combinations",
    "branch_combination",
    "dia_chi_hop",
    "luc_hop",
    "tam_hop",
)
TRANSFORM_KEYS: tuple[str, ...] = (
    "transformations",
    "transformation",
    "hop_hoa",
    "hua",
)
SCORE_KEYS: tuple[str, ...] = (
    "combination_score",
    "score",
)

# Pack 01 score CSV combination_type mapped to interpreter domain.
STEM_SCORE_TYPES: frozenset[str] = frozenset({"TIAN_GAN_HE"})
BRANCH_SCORE_TYPES: frozenset[str] = frozenset(
    {"DI_ZHI_LIUHE", "TAM_HOP", "TAM_HOI", "BAN_HOP"}
)
TRANSFORM_SUCCESS_TYPE = "HUA_SUCCESS"
TRANSFORM_FAIL_TYPE = "HUA_FAIL"
