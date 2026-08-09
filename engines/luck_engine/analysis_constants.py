"""Constants for Luck Analysis Engine (LE-2)."""

from __future__ import annotations

ANALYSIS_VERSION = "1.0.0"
ANALYSIS_ENGINE_ID = "luck_analysis_engine"
REQUIRED_TIMELINE_VERSION = "1.0.0"
REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_SCHEMA_VERSION = "2.0.0"

STAGE_SEASONAL = "seasonal_impact"
STAGE_STRENGTH = "strength_impact"
STAGE_TEMPERATURE = "temperature_impact"
STAGE_PATTERN = "pattern_impact"
STAGE_PATTERN_EVALUATION = "pattern_evaluation_impact"
STAGE_USEFUL_GOD = "useful_god_impact"

CANONICAL_IMPACT_ORDER: tuple[str, ...] = (
    STAGE_SEASONAL,
    STAGE_STRENGTH,
    STAGE_TEMPERATURE,
    STAGE_PATTERN,
    STAGE_PATTERN_EVALUATION,
    STAGE_USEFUL_GOD,
)

PUBLISHED_OUTPUTS: tuple[str, ...] = (
    STAGE_SEASONAL,
    STAGE_STRENGTH,
    STAGE_TEMPERATURE,
    STAGE_PATTERN,
    STAGE_PATTERN_EVALUATION,
    STAGE_USEFUL_GOD,
    "overall_analysis_impact",
    "analysis_trace",
    "analysis_diagnostics",
    "analysis_version",
)

DIRECTION_AMPLIFYING = "amplifying"
DIRECTION_DAMPENING = "dampening"
DIRECTION_NEUTRAL = "neutral"
DIRECTION_UNRESOLVED = "unresolved"

CONFIDENCE_HIGH = "high"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_LOW = "low"
CONFIDENCE_NONE = "none"

DIAG_TIMELINE_MISSING = "TIMELINE-MISSING"
DIAG_ANALYSIS_MISSING = "ANALYSIS-MISSING"
DIAG_DECISION_MISSING = "DECISION-MISSING"
DIAG_DEP_VIOLATION = "DEP-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_OUT_DUPLICATE = "OUT-DUPLICATE"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"

FORBIDDEN_FORTUNE_FIELDS: tuple[str, ...] = (
    "auspicious",
    "inauspicious",
    "fortune_quality",
    "risk",
    "luck_quality",
)
