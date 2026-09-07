"""Assessment-layer Golden signature. Does not rewrite Decision Golden."""

from __future__ import annotations

from typing import Any

from consulting.marriage.assessment.projector import project_marriage_assessment
from consulting.marriage.models.result import MarriageDecisionResult


def assessment_signature(decision: MarriageDecisionResult) -> dict[str, Any]:
    """Freeze public Assessment cards. Omits Decision evidence and score."""
    if decision.assessment is None:
        decision.assessment = project_marriage_assessment(decision)
    assessment = decision.assessment
    return {
        "question_set_id": assessment.question_set_id,
        "version": assessment.version,
        "cards": [
            {
                "question_id": card.question_id,
                "question": card.question,
                "answer": card.answer,
                "supporting_facts": list(card.supporting_facts),
                "confidence": card.confidence,
                "semantic_key": card.semantic_key,
            }
            for card in assessment.cards
        ],
    }
