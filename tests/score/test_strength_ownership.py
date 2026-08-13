"""ScoreEngine must not overwrite StrengthEngine classification."""

from __future__ import annotations

from engines.score_engine.engine import ScoreEngine
from engines.score_engine.result import ScoreResult


def test_append_score_does_not_overwrite_strength_level() -> None:
    """A. Score contribution must not remap canonical strength.level."""
    rule_context = {
        "strength": {"level": "strong", "score": 0.66, "reasoning": "Thân vượng"},
        "facts": {
            "strong_day_master": True,
            "strength_vuong": True,
            "balanced_day_master": False,
        },
        "score": {},
    }
    result = ScoreResult(success=True, strength_score=57.0, total_score=54.25, grade="D+")
    composed = ScoreEngine().append_score_to_rule_context(rule_context, result)

    assert composed["strength"]["level"] == "strong"
    assert composed["strength"]["score"] == 0.66
    assert composed["strength"]["reasoning"] == "Thân vượng"
    assert composed["score"]["strength_score"] == 57.0
    assert composed["facts"]["strong_day_master"] is True
    assert composed["facts"]["balanced_day_master"] is False
    assert rule_context["strength"]["level"] == "strong"


def test_append_score_keeps_weak_and_balanced_canonical() -> None:
    """Score must preserve every StrengthEngine class, not only strong."""
    engine = ScoreEngine()
    for level, score in (("weak", 0.22), ("balanced", 0.5), ("strong", 0.66)):
        context = {"strength": {"level": level, "score": score}, "score": {}}
        composed = engine.append_score_to_rule_context(
            context,
            ScoreResult(success=True, strength_score=57.0),
        )
        assert composed["strength"]["level"] == level
        assert composed["strength"]["score"] == score
