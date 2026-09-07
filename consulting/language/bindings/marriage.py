"""TV-01 Language Pack binding seam. Not imported by Decision or Assessment."""

from __future__ import annotations

from typing import Final

# R02 Assessment.semantic_key → Language Pack key.
# LANG-01 records the map only. Projector must not consume it yet.
R02_SEMANTIC_TO_LANGUAGE_KEY: Final[dict[tuple[str, str], str]] = {
    ("Q1", "very_compatible"): "marriage.q1.supportive",
    ("Q1", "quite_compatible"): "marriage.q1.supportive",
    ("Q1", "average"): "marriage.q1.mixed",
    ("Q1", "high_pressure"): "marriage.q1.pressured",
    ("Q1", "needs_adjustment"): "marriage.q1.needs_adjustment",
    ("Q1", "insufficient"): "marriage.q1.insufficient",
    ("Q2", "mutual_support"): "marriage.q2.mutual_support",
    ("Q3", "similar"): "marriage.q3.similar_temperament",
    ("Q3", "complementary"): "marriage.q3.complementary",
    ("Q3", "balanced"): "marriage.q3.balanced",
    ("Q3", "conflict"): "marriage.q3.role_pressure",
    ("Q4", "stable_with_rescue"): "marriage.q4.stable_with_rescue",
    ("Q4", "stable_if_kept"): "marriage.q4.stable_if_kept",
    ("Q4", "needs_management"): "marriage.q4.needs_management",
    ("Q4", "maintainable"): "marriage.q4.mixed_with_conflict",
    ("Q4", "insufficient"): "marriage.q4.insufficient",
    ("Q5", "insufficient"): "marriage.q5.insufficient",
    ("Q5", "family_support"): "marriage.q5.parenting_support",
    ("Q6", "can_proceed"): "marriage.q6.can_progress",
    ("Q6", "learn_more"): "marriage.q6.needs_more_review",
    ("Q6", "resolve_first"): "marriage.q6.high_pressure",
    ("Q6", "good_foundation"): "marriage.q6.good_foundation",
}


def language_key_for(question_id: str, semantic_key: str) -> str | None:
    """Map a frozen R02 semantic_key onto a Language Pack key. Lookup only."""
    return R02_SEMANTIC_TO_LANGUAGE_KEY.get((question_id, semantic_key))
