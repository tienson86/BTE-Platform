"""Analysis Runtime constants."""

from __future__ import annotations

RUNTIME_VERSION: str = "1.0.0"

CANONICAL_STAGES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "luck",
    "summary",
)

# Default data dependencies by pipeline position (append-only prerequisites).
DEFAULT_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "strength": (),
    "temperature": ("strength",),
    "pattern": ("strength", "temperature"),
    "useful_god": ("strength", "temperature", "pattern"),
    "ten_gods": ("strength", "temperature", "pattern", "useful_god"),
    "combination": (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
    ),
    "shensha": (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
        "combination",
    ),
    "luck": (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
        "combination",
        "shensha",
    ),
    "summary": (
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "ten_gods",
        "combination",
        "shensha",
        "luck",
    ),
}

STAGE_RESULT_ATTR: dict[str, str] = {
    "strength": "strength_result",
    "temperature": "temperature_result",
    "pattern": "pattern_result",
    "useful_god": "useful_god_result",
    "ten_gods": "ten_gods_result",
    "combination": "combination_result",
    "shensha": "shensha_result",
    "luck": "luck_result",
    "summary": "summary_result",
}
