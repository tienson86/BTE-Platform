"""Frozen Narrative Composer V2 constants."""

from __future__ import annotations

from typing import Final, Mapping

BUNDLE_KIND_DECISION: Final[str] = "decision"
BUNDLE_KIND_STATE: Final[str] = "state"
BUNDLE_KIND_RELATIONSHIP: Final[str] = "relationship"
BUNDLE_KIND_KNOWLEDGE: Final[str] = "knowledge"

CANONICAL_BUNDLE_KINDS: Final[tuple[str, ...]] = (
    BUNDLE_KIND_DECISION,
    BUNDLE_KIND_STATE,
    BUNDLE_KIND_RELATIONSHIP,
    BUNDLE_KIND_KNOWLEDGE,
)

CUSTOMER_DOMAIN_CAREER: Final[str] = "Career"
CUSTOMER_DOMAIN_FINANCE: Final[str] = "Finance"
CUSTOMER_DOMAIN_RELATIONSHIP: Final[str] = "Relationship"
CUSTOMER_DOMAIN_HEALTH: Final[str] = "Health"
CUSTOMER_DOMAIN_LEARNING: Final[str] = "Learning"
CUSTOMER_DOMAIN_DECISION_MAKING: Final[str] = "Decision Making"
CUSTOMER_DOMAIN_ENVIRONMENT: Final[str] = "Environment"

CUSTOMER_DOMAINS: Final[tuple[str, ...]] = (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_LEARNING,
    CUSTOMER_DOMAIN_DECISION_MAKING,
    CUSTOMER_DOMAIN_ENVIRONMENT,
)

CUSTOMER_DOMAIN_ALIASES: Final[Mapping[str, str]] = {
    "career": CUSTOMER_DOMAIN_CAREER,
    "wealth": CUSTOMER_DOMAIN_FINANCE,
    "finance": CUSTOMER_DOMAIN_FINANCE,
    "relationships": CUSTOMER_DOMAIN_RELATIONSHIP,
    "relationship": CUSTOMER_DOMAIN_RELATIONSHIP,
    "health": CUSTOMER_DOMAIN_HEALTH,
    "learning": CUSTOMER_DOMAIN_LEARNING,
    "learning_growth": CUSTOMER_DOMAIN_LEARNING,
    "decision_making": CUSTOMER_DOMAIN_DECISION_MAKING,
    "decision making": CUSTOMER_DOMAIN_DECISION_MAKING,
    "environment": CUSTOMER_DOMAIN_ENVIRONMENT,
    "supportive_environments": CUSTOMER_DOMAIN_ENVIRONMENT,
    "decision_guidance": CUSTOMER_DOMAIN_DECISION_MAKING,
}

SECTION_EXECUTIVE_SUMMARY: Final[str] = "Executive Summary"
SECTION_OBSERVATION: Final[str] = "Observation"
SECTION_REASONING: Final[str] = "Reasoning"
SECTION_IMPACT: Final[str] = "Impact"
SECTION_RECOMMENDATION: Final[str] = "Recommendation"
SECTION_WARNING: Final[str] = "Warning"
SECTION_CONCLUSION: Final[str] = "Conclusion"

NARRATIVE_SECTIONS: Final[tuple[str, ...]] = (
    SECTION_EXECUTIVE_SUMMARY,
    SECTION_OBSERVATION,
    SECTION_REASONING,
    SECTION_IMPACT,
    SECTION_RECOMMENDATION,
    SECTION_WARNING,
    SECTION_CONCLUSION,
)

KIND_FACT: Final[str] = "fact"
KIND_EVIDENCE: Final[str] = "evidence"
KIND_REASON: Final[str] = "reason"
KIND_CONCLUSION: Final[str] = "conclusion"
KIND_APPLICATION: Final[str] = "application"
KIND_RECOMMENDATION: Final[str] = "recommendation"
KIND_WARNING: Final[str] = "warning"

SLOT_SUMMARY: Final[str] = "summary"
SLOT_OBSERVATION: Final[str] = "observation"
SLOT_REASONING: Final[str] = "reasoning"
SLOT_IMPACT: Final[str] = "impact"
SLOT_RECOMMENDATION: Final[str] = "recommendation"
SLOT_WARNING: Final[str] = "warning"
SLOT_CONCLUSION: Final[str] = "conclusion"

SLOT_TO_SECTION: Final[Mapping[str, str]] = {
    SLOT_SUMMARY: SECTION_EXECUTIVE_SUMMARY,
    SLOT_OBSERVATION: SECTION_OBSERVATION,
    SLOT_REASONING: SECTION_REASONING,
    SLOT_IMPACT: SECTION_IMPACT,
    SLOT_RECOMMENDATION: SECTION_RECOMMENDATION,
    SLOT_WARNING: SECTION_WARNING,
    SLOT_CONCLUSION: SECTION_CONCLUSION,
}

DOMAIN_PRIORITY: Final[Mapping[str, int]] = {
    "UsefulGod": 100,
    "Strength": 80,
    "Pattern": 70,
    "TenGods": 60,
    "ShenSha": 50,
}

KIND_IMPORTANCE: Final[Mapping[str, float]] = {
    BUNDLE_KIND_DECISION: 1.0,
    BUNDLE_KIND_STATE: 0.85,
    BUNDLE_KIND_RELATIONSHIP: 0.7,
    BUNDLE_KIND_KNOWLEDGE: 0.6,
}

SCORE_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {"score", "total_score", "component_score"}
)
