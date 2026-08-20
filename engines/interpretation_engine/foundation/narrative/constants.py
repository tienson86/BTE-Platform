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
CUSTOMER_DOMAIN_DECISION: Final[str] = "Decision"
CUSTOMER_DOMAIN_DECISION_MAKING: Final[str] = "Decision"
CUSTOMER_DOMAIN_ENVIRONMENT: Final[str] = "Environment"

CUSTOMER_DOMAINS: Final[tuple[str, ...]] = (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_LEARNING,
    CUSTOMER_DOMAIN_DECISION,
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
    "decision_making": CUSTOMER_DOMAIN_DECISION,
    "decision making": CUSTOMER_DOMAIN_DECISION,
    "decision": CUSTOMER_DOMAIN_DECISION,
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

MIN_CUSTOMER_PROSE_CHARS: Final[int] = 8
RANK_KEEP_RATIO: Final[float] = 0.65

DOMAIN_DEFAULT_TOPIC: Final[Mapping[str, str]] = {
    "UsefulGod": CUSTOMER_DOMAIN_DECISION,
    "Strength": CUSTOMER_DOMAIN_HEALTH,
    "Pattern": CUSTOMER_DOMAIN_CAREER,
    "TenGods": CUSTOMER_DOMAIN_DECISION,
    "ShenSha": CUSTOMER_DOMAIN_ENVIRONMENT,
}

CUSTOMER_DOMAIN_LABELS: Final[Mapping[str, str]] = {
    CUSTOMER_DOMAIN_CAREER: "Sự nghiệp",
    CUSTOMER_DOMAIN_FINANCE: "Tài chính",
    CUSTOMER_DOMAIN_RELATIONSHIP: "Quan hệ",
    CUSTOMER_DOMAIN_HEALTH: "Sức khỏe",
    CUSTOMER_DOMAIN_LEARNING: "Học hỏi",
    CUSTOMER_DOMAIN_DECISION: "Ra quyết định",
}

IMPACT_CUSTOMER_DOMAINS: Final[tuple[str, ...]] = (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    CUSTOMER_DOMAIN_HEALTH,
)

COMMERCIAL_OBSERVATION_LIMIT: Final[int] = 8
COMMERCIAL_OBSERVATION_MIN: Final[int] = 5
COMMERCIAL_SUMMARY_LIMIT: Final[int] = 6
COMMERCIAL_REASONING_LIMIT: Final[int] = 4
COMMERCIAL_IMPACT_PER_DOMAIN: Final[int] = 1
COMMERCIAL_RECOMMENDATION_LIMIT: Final[int] = 5
COMMERCIAL_WARNING_LIMIT: Final[int] = 3
COMMERCIAL_CONCLUSION_LIMIT: Final[int] = 2
COMMERCIAL_SHENSHA_LIMIT: Final[int] = 2
REASONING_DOMAIN_ORDER: Final[tuple[str, ...]] = (
    "Pattern",
    "Strength",
    "UsefulGod",
    "TenGods",
    "ShenSha",
)
GOVERNING_REASONING_DOMAINS: Final[tuple[str, ...]] = (
    "Pattern",
    "Strength",
    "UsefulGod",
)
RECOMMENDATION_DIRECTIVE_VERBS: Final[tuple[str, ...]] = (
    "Làm",
    "Tránh",
    "Xây",
    "Củng cố",
    "Giảm",
    "Dùng",
)
GOVERNING_APPLICATION_DOMAINS: Final[frozenset[str]] = frozenset(
    {"UsefulGod", "Strength", "Pattern"}
)
SHENSHA_CANONICAL_OVER_ALIAS: Final[Mapping[str, str]] = {
    "Thiên Ất": "Thiên Ất Quý Nhân",
    "Thiên Đức": "Thiên Đức Quý Nhân",
    "Nguyệt Đức": "Nguyệt Đức Quý Nhân",
}

PACK05_SECTION_MAP: Final[Mapping[str, tuple[str, str, str]]] = {
    SECTION_EXECUTIVE_SUMMARY: (
        "sec-executive_summary",
        "overview",
        "Tóm tắt điều hành",
    ),
    SECTION_OBSERVATION: ("sec-observation", "observation", "Quan sát"),
    SECTION_REASONING: ("sec-reasoning", "reasoning", "Lý giải"),
    SECTION_IMPACT: ("sec-impact", "impact", "Tác động"),
    SECTION_RECOMMENDATION: ("sec-recommendation", "priority", "Khuyến nghị"),
    SECTION_WARNING: ("sec-warning", "warning", "Lưu ý"),
    SECTION_CONCLUSION: ("sec-conclusion", "closing", "Kết luận"),
}

PACK05_SECTION_TONES: Final[Mapping[str, str]] = {
    SECTION_EXECUTIVE_SUMMARY: "briefing",
    SECTION_OBSERVATION: "neutral_factual",
    SECTION_REASONING: "explanatory",
    SECTION_IMPACT: "empathic_concrete",
    SECTION_RECOMMENDATION: "directive_supportive",
    SECTION_WARNING: "cautionary_calm",
    SECTION_CONCLUSION: "settling",
}

NARRATIVE_RESULT_V2_GENERATOR: Final[str] = "narrative_composer_v2"
PACK05_CONTRACT: Final[str] = "pack05_narrative_result_v1"

QUALITY_TRUTH_MARKERS: Final[tuple[str, ...]] = (
    ":selected",
    ":reason",
    "explain_rejected",
    ":rejected:",
    "favorable",
    "unfavorable",
    ":state",
    "pattern:selected",
    "preserve_hy",
)
