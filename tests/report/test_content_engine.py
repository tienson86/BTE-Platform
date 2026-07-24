"""WP7A — Content Analysis Layer tests."""

from __future__ import annotations

from engines.interpretation_engine.legacy_builder import (
    InterpretationResult,
    InterpretationSection,
)
from engines.report_engine.content import ContentContext, ContentEngine


def _sample_interpretation() -> InterpretationResult:
    return InterpretationResult(
        summary="Tong quan la so Canh than vuong.",
        confidence=72.0,
        matched_rule_count=5,
        resolved_rule_count=4,
        rules_used=["R1", "R2", "R3"],
        sentences=[
            {
                "section": "career",
                "rule_id": "C1",
                "sentence": "Su nghiep thuan loi khi dung than duoc dung.",
                "priority": 80,
            },
            {
                "section": "wealth",
                "rule_id": "W1",
                "sentence": "Tai van on dinh neu dung than duoc bao ve.",
                "priority": 70,
            },
            {
                "section": "career",
                "rule_id": "C2",
                "sentence": "Su nghiep can than trong nam xung.",
                "priority": 60,
            },
        ],
        sections={
            "summary": InterpretationSection(
                name="summary",
                rules=[
                    {
                        "rule_id": "S1",
                        "description": "Tong quan canh than vuong.",
                        "priority": 90,
                    }
                ],
                score=10,
            ),
            "career": InterpretationSection(
                name="career",
                rules=[
                    {
                        "rule_id": "C1",
                        "description": "Su nghiep thuan loi khi dung than duoc dung.",
                        "priority": 80,
                    }
                ],
                score=8,
            ),
            "wealth": InterpretationSection(
                name="wealth",
                rules=[
                    {
                        "rule_id": "W1",
                        "description": "Tai van on dinh neu dung than duoc bao ve.",
                        "priority": 70,
                    }
                ],
                score=7,
            ),
            "pattern": InterpretationSection(
                name="pattern",
                rules=[
                    {
                        "rule_id": "P1",
                        "description": "Cach cuc chinh quan.",
                        "priority": 85,
                    }
                ],
                score=12,
            ),
        },
    )


def test_content_engine_returns_content_context():
    """ContentEngine.analyze must produce ContentContext."""
    engine = ContentEngine()
    result = engine.analyze(_sample_interpretation())

    assert isinstance(result, ContentContext)
    assert result.section_scores
    assert result.important_sections
    assert result.grouped_rules
    assert result.suggested_order
    assert isinstance(result.keywords, list)
    assert isinstance(result.repeated_topics, list)


def test_content_context_to_dict_has_required_keys():
    """ContentContext.to_dict exposes the WP7A contract fields."""
    payload = ContentEngine().analyze_to_dict(_sample_interpretation())

    for key in (
        "section_scores",
        "important_sections",
        "keywords",
        "grouped_rules",
        "repeated_topics",
        "suggested_order",
    ):
        assert key in payload


def test_suggested_order_prefers_canonical_spine():
    """Summary/pattern should appear before late sections when present."""
    context = ContentEngine().analyze(_sample_interpretation())
    order = context.suggested_order

    assert "summary" in order
    assert "pattern" in order
    assert "career" in order
    assert order.index("summary") < order.index("career")
    assert order.index("pattern") < order.index("wealth")


def test_repeated_topics_detect_cross_section_keywords():
    """Shared tokens like dung/than should surface as repeated topics."""
    context = ContentEngine().analyze(_sample_interpretation())
    topics = {item["topic"] for item in context.repeated_topics}
    # Folded tokens from "dung than" appear in career + wealth sentences
    assert topics.intersection({"dung", "than", "duoc"})


def test_content_engine_accepts_plain_dict():
    """Analysis Layer accepts dict-shaped InterpretationResult."""
    payload = {
        "summary": "Hello",
        "confidence": 10,
        "sections": {
            "summary": {
                "name": "summary",
                "rules": [{"rule_id": "A", "description": "Alpha beta gamma", "priority": 50}],
                "score": 1,
            }
        },
        "sentences": [],
    }
    context = ContentEngine().analyze(payload)
    assert isinstance(context, ContentContext)
    assert "summary" in context.grouped_rules
    assert context.suggested_order
