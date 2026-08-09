"""Deterministic constants for the Interpretation Foundation (IE-1)."""

from __future__ import annotations

ENGINE_ID = "interpretation_engine"
INTERPRETATION_VERSION = "1.0.0"
INTERPRETATION_CONTRACT_ID = "bte.interpretation.foundation.v1"
REQUIRED_SCHEMA_VERSION = "2.0.0"
FOUNDATION_VERSION = "1.0.0"

REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_LUCK_PIPELINE_VERSION = "1.0.0"

MODULE_OVERVIEW = "overview"
MODULE_PERSONALITY = "personality"
MODULE_CAREER = "career"
MODULE_WEALTH = "wealth"
MODULE_RELATIONSHIP = "relationship"
MODULE_HEALTH = "health"
MODULE_CHILDREN = "children"
MODULE_LUCK = "luck"
MODULE_SUMMARY = "summary"

CANONICAL_MODULE_ORDER: tuple[str, ...] = (
    MODULE_OVERVIEW,
    MODULE_PERSONALITY,
    MODULE_CAREER,
    MODULE_WEALTH,
    MODULE_RELATIONSHIP,
    MODULE_HEALTH,
    MODULE_CHILDREN,
    MODULE_LUCK,
    MODULE_SUMMARY,
)

MODULE_STATUS_REGISTERED = "registered"
MODULE_STATUS_UNIMPLEMENTED = "unimplemented"

CONTEXT_STATUS_READY = "ready"
RESULT_STATUS_EMPTY = "empty"
PLACEHOLDER_STATUS_UNBOUND = "unbound"

PUBLISHED_CONTEXT_INPUTS: tuple[str, ...] = (
    "canonical_analysis_result",
    "canonical_decision_result",
    "canonical_luck_result",
)

PUBLISHED_CONTRACTS: tuple[str, ...] = (
    "InterpretationContext",
    "InterpretationSection",
    "InterpretationChapter",
    "InterpretationParagraph",
    "InterpretationReference",
    "InterpretationMetadata",
    "CanonicalInterpretationResult",
)

PUBLISHED_MODELS: tuple[str, ...] = (
    "SectionModel",
    "ChapterModel",
    "ParagraphModel",
    "ReferenceModel",
    "PlaceholderModel",
    "MetadataModel",
    "ResultModel",
)

FORBIDDEN_TEXT_FIELDS: tuple[str, ...] = (
    "narrative",
    "sentence",
    "sentences",
    "report_text",
    "consultant_copy",
    "fortune_story",
    "template_body",
    "generated_text",
)
