"""TV-01 Marriage Assessment models. Question-driven projection. Not Decision."""

from __future__ import annotations

from dataclasses import dataclass, field


QUESTION_SET_ID = "TV-01-QSET-1.0"
ASSESSMENT_MODEL_VERSION = "1.0.0"

Q1_OVERALL_COMPATIBILITY = "Q1"
Q2_MUTUAL_SUPPORT = "Q2"
Q3_PERSONALITY_BALANCE = "Q3"
Q4_MARRIAGE_STABILITY = "Q4"
Q5_CHILDREN = "Q5"
Q6_OVERALL_MARRIAGE = "Q6"

QUESTION_ORDER = (
    Q1_OVERALL_COMPATIBILITY,
    Q2_MUTUAL_SUPPORT,
    Q3_PERSONALITY_BALANCE,
    Q4_MARRIAGE_STABILITY,
    Q5_CHILDREN,
    Q6_OVERALL_MARRIAGE,
)

CUSTOMER_QUESTIONS = {
    Q1_OVERALL_COMPATIBILITY: "Hai người có hợp nhau không?",
    Q2_MUTUAL_SUPPORT: "Ai bổ trợ cho ai?",
    Q3_PERSONALITY_BALANCE: "Hai người có hợp tính cách không?",
    Q4_MARRIAGE_STABILITY: "Cuộc hôn nhân có ổn định không?",
    Q5_CHILDREN: "Khả năng nuôi dạy con chung thế nào?",
    Q6_OVERALL_MARRIAGE: "Có nên tiến tới hôn nhân không?",
}


@dataclass(slots=True)
class MarriageAssessmentCard:
    """One customer Assessment card. Object, not an essay."""

    question_id: str
    question: str
    answer: str
    supporting_facts: list[str]
    confidence: str
    limitations: list[str] = field(default_factory=list)
    semantic_key: str = ""
    finding_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    fact_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class MarriageAssessmentResult:
    """Six-question Marriage Assessment. Sibling of Recommendation."""

    assessment_id: str
    consultation_id: str
    question_set_id: str
    version: str
    cards: list[MarriageAssessmentCard]
    source_decision_id: str
