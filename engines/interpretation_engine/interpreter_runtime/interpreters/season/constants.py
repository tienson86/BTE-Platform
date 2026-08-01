"""Constants for Season Interpreter business logic."""

from __future__ import annotations

SEASON_MODULE_IDS: tuple[str, ...] = (
    "season",
    "temperature",
    "temperature_engine",
    "11_temperature",
    "strength",
)

SEASON_SECTION_TYPE = "season"
SEASON_INTERPRETER_ID = "season_interpreter"
SEASON_INTERPRETER_VERSION = "1.0.0"

SEASON_KEYS: tuple[str, ...] = (
    "season",
    "season_type",
    "final_season",
)
QI_STAGE_KEYS: tuple[str, ...] = (
    "qi_stage",
    "season_phase",
    "phase",
)
MONTH_BRANCH_KEYS: tuple[str, ...] = (
    "month_branch",
    "month_zhi",
    "tháng_chi",
)
CLIMATE_KEYS: tuple[str, ...] = (
    "climate",
    "climate_type",
    "temperature_type",
)
TEMPERATURE_LEVEL_KEYS: tuple[str, ...] = (
    "temperature_level",
    "climate_level",
    "classification",
    "level",
)
SEASON_SCORE_KEYS: tuple[str, ...] = (
    "season_score",
    "season_strength",
    "month_strength",
)
TEMPERATURE_SCORE_KEYS: tuple[str, ...] = (
    "temperature_score",
    "score",
)

VN_SEASON_MAP: dict[str, str] = {
    "xuân": "spring",
    "xuan": "spring",
    "hạ": "summer",
    "ha": "summer",
    "thu": "autumn",
    "đông": "winter",
    "dong": "winter",
}
