"""Constants for Temperature Interpreter business logic."""

from __future__ import annotations

TEMPERATURE_MODULE_IDS: tuple[str, ...] = (
    "temperature",
    "temperature_engine",
    "11_temperature",
)

TEMPERATURE_SECTION_TYPE = "temperature"
TEMPERATURE_INTERPRETER_ID = "temperature_interpreter"
TEMPERATURE_INTERPRETER_VERSION = "1.0.0"

COLD_KEYS: tuple[str, ...] = (
    "cold",
    "cold_score",
    "han_score",
)
HOT_KEYS: tuple[str, ...] = (
    "hot",
    "hot_score",
    "warm_score",
    "nhiet_score",
)
DRY_KEYS: tuple[str, ...] = (
    "dry",
    "dry_score",
    "dryness_score",
    "tao_score",
)
WET_KEYS: tuple[str, ...] = (
    "wet",
    "wet_score",
    "humid_score",
    "humidity_score",
    "tham_score",
)
BALANCE_KEYS: tuple[str, ...] = (
    "balance",
    "balance_score",
)
LEVEL_KEYS: tuple[str, ...] = (
    "temperature_level",
    "classification",
    "level",
)
SCORE_KEYS: tuple[str, ...] = (
    "temperature_score",
    "score",
)
DRYNESS_LEVEL_KEYS: tuple[str, ...] = (
    "dryness_level",
    "dry_level",
)
HUMIDITY_LEVEL_KEYS: tuple[str, ...] = (
    "humidity_level",
    "wet_level",
    "humid_level",
)
