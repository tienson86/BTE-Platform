"""Constants for Scoring Interpreter business logic."""

from __future__ import annotations

SCORING_MODULE_IDS: tuple[str, ...] = (
    "scoring",
    "score",
    "score_engine",
    "final_score",
    "09_final_score",
)

SCORING_SECTION_TYPE = "scoring"
SCORING_INTERPRETER_ID = "scoring_interpreter"
SCORING_INTERPRETER_VERSION = "1.0.0"

OVERALL_KEYS: tuple[str, ...] = (
    "overall_score",
    "final_score",
    "total_score",
    "score",
)
DIMENSION_KEYS: tuple[str, ...] = (
    "dimensions",
    "dimension_scores",
    "scores",
    "module_scores",
)
CONFIDENCE_KEYS: tuple[str, ...] = (
    "confidence",
    "confidence_score",
    "confidence_value",
)
QUALITY_KEYS: tuple[str, ...] = (
    "quality",
    "grade",
    "rating",
    "quality_level",
)

# Map common Pack 02 / AnalysisScore dimension aliases to Pack 01 module codes.
DIMENSION_ALIASES: dict[str, str] = {
    "wuxing": "WUXING",
    "ngu_hanh": "WUXING",
    "wuxing_score": "WUXING",
    "strength": "STRENGTH",
    "than_vuong": "STRENGTH",
    "strength_score": "STRENGTH",
    "ten_gods": "TEN_GODS",
    "ten_god": "TEN_GODS",
    "thap_than": "TEN_GODS",
    "ten_god_score": "TEN_GODS",
    "pattern": "PATTERN",
    "cach_cuc": "PATTERN",
    "pattern_score": "PATTERN",
    "useful_god": "USEFUL_GOD",
    "dung_than": "USEFUL_GOD",
    "useful_god_score": "USEFUL_GOD",
    "shensha": "SHENSHA",
    "than_sat": "SHENSHA",
    "shensha_score": "SHENSHA",
    "luck": "LUCK",
    "dai_van": "LUCK",
    "dayun": "LUCK",
    "luck_score": "LUCK",
    "overall": "OVERALL",
    "final": "OVERALL",
    "total": "OVERALL",
}
