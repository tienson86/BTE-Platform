"""Constants for Luck Decision Engine (LE-3)."""

from __future__ import annotations

DECISION_VERSION = "1.0.0"
DECISION_ENGINE_ID = "luck_decision_engine"
REQUIRED_TIMELINE_VERSION = "1.0.0"
REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_LUCK_ANALYSIS_VERSION = "1.0.0"

STAGE_OPPORTUNITY = "opportunity_evaluation"
STAGE_RISK = "risk_evaluation"
STAGE_CONFIDENCE = "confidence_evaluation"
STAGE_PRIORITY = "priority_resolution"
STAGE_PUBLICATION = "decision_publication"

CANONICAL_DECISION_ORDER: tuple[str, ...] = (
    STAGE_OPPORTUNITY,
    STAGE_RISK,
    STAGE_CONFIDENCE,
    STAGE_PRIORITY,
    STAGE_PUBLICATION,
)

OUTPUT_OPPORTUNITY = "opportunity_score"
OUTPUT_RISK = "risk_score"
OUTPUT_PRIORITY = "luck_priority"
OUTPUT_CONFIDENCE = "decision_confidence"
OUTPUT_REASONING = "decision_reasoning"
OUTPUT_TRACE = "decision_trace"
OUTPUT_AUDIT = "decision_audit"
OUTPUT_OVERALL = "overall_luck_decision"
OUTPUT_VERSION = "decision_version"

PUBLISHED_OUTPUTS: tuple[str, ...] = (
    OUTPUT_OPPORTUNITY,
    OUTPUT_RISK,
    OUTPUT_PRIORITY,
    OUTPUT_CONFIDENCE,
    OUTPUT_REASONING,
    OUTPUT_TRACE,
    OUTPUT_AUDIT,
    OUTPUT_OVERALL,
    OUTPUT_VERSION,
)

IMPACT_OUTPUT_KEYS: tuple[str, ...] = (
    "seasonal_impact",
    "strength_impact",
    "temperature_impact",
    "pattern_impact",
    "pattern_evaluation_impact",
    "useful_god_impact",
)

PRIORITY_OPPORTUNITY_FIRST = "opportunity_first"
PRIORITY_RISK_FIRST = "risk_first"
PRIORITY_BALANCED = "balanced"
PRIORITY_WITHHELD = "withheld"

PRIORITY_MARGIN = 5.0

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

REASON_OPP = "RC-LCK-OPP-001"
REASON_RSK = "RC-LCK-RSK-001"
REASON_CNF = "RC-LCK-CNF-001"
REASON_PRI = "RC-LCK-PRI-001"
REASON_PUB = "RC-LCK-PUB-001"

FORBIDDEN_INTERPRETATION_FIELDS: tuple[str, ...] = (
    "narrative",
    "interpretation",
    "report_text",
    "fortune_story",
    "consultant_copy",
)
