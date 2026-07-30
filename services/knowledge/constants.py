"""Constants for Knowledge infrastructure."""

from __future__ import annotations

from typing import Final

DEFAULT_CANON_ROOT_RELATIVE: Final[str] = "knowledge/knowledge_canon"
DEFAULT_SCHEMA_ROOT_RELATIVE: Final[str] = "knowledge/schema"

DOMAIN_SCHEMA_MAP: Final[dict[str, str]] = {
    "01_five_elements": "five_element.schema.json",
    "02_heavenly_stems": "heavenly_stem.schema.json",
    "03_earthly_branches": "earthly_branch.schema.json",
    "04_hidden_stems": "hidden_stem.schema.json",
    "05_yin_yang": "yin_yang.schema.json",
    "06_ten_gods": "ten_god.schema.json",
    "07_strength": "strength.schema.json",
    "08_patterns": "pattern.schema.json",
    "09_useful_gods": "useful_god.schema.json",
    "10_combinations": "combination.schema.json",
    "11_clashes": "clash.schema.json",
    "12_punishments": "punishment.schema.json",
    "13_harms": "harm.schema.json",
    "14_transformations": "transformation.schema.json",
    "15_seasonal_qi": "seasonal_qi.schema.json",
    "16_temperature": "temperature.schema.json",
    "17_shensha": "shensha.schema.json",
    "18_luck_cycles": "luck_cycle.schema.json",
    "19_special_cases": "special_case.schema.json",
}

DOMAIN_CONST_MAP: Final[dict[str, str]] = {
    "01_five_elements": "five_elements",
    "02_heavenly_stems": "heavenly_stems",
    "03_earthly_branches": "earthly_branches",
    "04_hidden_stems": "hidden_stems",
    "05_yin_yang": "yin_yang",
    "06_ten_gods": "ten_gods",
    "07_strength": "strength",
    "08_patterns": "patterns",
    "09_useful_gods": "useful_gods",
    "10_combinations": "combinations",
    "11_clashes": "clashes",
    "12_punishments": "punishments",
    "13_harms": "harms",
    "14_transformations": "transformations",
    "15_seasonal_qi": "seasonal_qi",
    "16_temperature": "temperature",
    "17_shensha": "shensha",
    "18_luck_cycles": "luck_cycles",
    "19_special_cases": "special_cases",
}

KNOWLEDGE_ID_PATTERN: Final[str] = r"^KNO-[0-9]{6}$"
RECORD_FILENAME_SUFFIX: Final[str] = ".json"
SCHEMA_FILENAME_SUFFIX: Final[str] = ".schema.json"
