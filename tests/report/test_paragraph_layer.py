"""WP7B — Paragraph Layer unit tests."""

from __future__ import annotations

import importlib

from engines.report_engine.content.models import ContentContext

_paragraph = importlib.import_module("engines.report_engine.content.02_paragraph")
ParagraphBuilder = _paragraph.ParagraphBuilder
ParagraphContext = _paragraph.ParagraphContext
SentenceMerger = _paragraph.SentenceMerger
ParagraphSplitter = _paragraph.ParagraphSplitter
SentenceUnit = _paragraph.SentenceUnit


def _sample_content() -> ContentContext:
    return ContentContext(
        section_scores={"summary": 80.0, "career": 70.0, "wealth": 60.0},
        important_sections=["summary", "career", "wealth"],
        keywords=[
            {"keyword": "nghiep", "count": 3},
            {"keyword": "than", "count": 2},
            {"keyword": "tai", "count": 2},
        ],
        grouped_rules={
            "summary": [
                {
                    "rule_id": "S1",
                    "description": "Tong quan than vuong on dinh.",
                    "polarity": "positive",
                    "priority": 90,
                }
            ],
            "career": [
                {
                    "rule_id": "C1",
                    "description": "Su nghiep thuan loi khi than duoc dung.",
                    "polarity": "positive",
                    "priority": 80,
                },
                {
                    "rule_id": "C2",
                    "description": "Su nghiep tot neu dung than dung cach.",
                    "polarity": "positive",
                    "priority": 75,
                },
                {
                    "rule_id": "C3",
                    "description": "Su nghiep bat loi khi xung pha.",
                    "polarity": "negative",
                    "priority": 50,
                },
            ],
            "wealth": [
                {
                    "rule_id": "W1",
                    "description": "Tai van on dinh nho than bao ve.",
                    "polarity": "positive",
                    "priority": 70,
                }
            ],
        },
        repeated_topics=[
            {
                "topic": "than",
                "sections": ["summary", "career", "wealth"],
                "section_count": 3,
                "total_count": 3,
            }
        ],
        suggested_order=["summary", "career", "wealth"],
        metadata={"rule_count": 5},
    )


def test_paragraph_builder_returns_paragraph_context():
    result = ParagraphBuilder().build(_sample_content())
    assert isinstance(result, ParagraphContext)
    assert result.paragraphs
    assert result.ordered_sentences
    assert result.paragraph_scores
    assert isinstance(result.transitions, list)


def test_paragraph_context_to_dict_keys():
    payload = ParagraphBuilder().build(_sample_content()).to_dict()
    for key in ("paragraphs", "ordered_sentences", "transitions", "paragraph_scores"):
        assert key in payload


def test_no_cross_section_merge():
    result = ParagraphBuilder().build(_sample_content())
    for paragraph in result.paragraphs:
        sections = {sentence.section for sentence in paragraph.sentences}
        assert len(sections) == 1


def test_different_polarity_not_merged():
    result = ParagraphBuilder().build(_sample_content())
    career_paragraphs = [p for p in result.paragraphs if p.section == "career"]
    polarities = {p.polarity for p in career_paragraphs}
    assert "positive" in polarities
    assert "negative" in polarities
    for paragraph in career_paragraphs:
        assert len({s.polarity for s in paragraph.sentences}) == 1


def test_same_topic_positive_career_can_merge():
    result = ParagraphBuilder().build(_sample_content())
    positive_career = [
        p
        for p in result.paragraphs
        if p.section == "career" and p.polarity == "positive"
    ]
    assert positive_career
    assert any(len(p.sentences) >= 2 for p in positive_career)


def test_transitions_only_between_paragraphs():
    result = ParagraphBuilder().build(_sample_content())
    assert len(result.transitions) == max(0, len(result.paragraphs) - 1)
    paragraph_ids = [p.paragraph_id for p in result.paragraphs]
    for index, transition in enumerate(result.transitions):
        assert transition.after_paragraph_id == paragraph_ids[index]
        assert transition.before_paragraph_id == paragraph_ids[index + 1]


def test_transition_does_not_invent_sentence_text():
    result = ParagraphBuilder().build(_sample_content())
    for transition in result.transitions:
        payload = transition.to_dict()
        assert "text" not in payload
        assert "sentence" not in payload


def test_sentence_merger_never_mixes_sections():
    units = [
        SentenceUnit(
            "A tot.", "career", polarity="positive", topic_key="nghiep", priority=10
        ),
        SentenceUnit(
            "B tot.", "wealth", polarity="positive", topic_key="nghiep", priority=9
        ),
    ]
    groups = SentenceMerger().merge(units)
    assert len(groups) == 2


def test_paragraph_splitter_separates_polarity():
    units = [
        SentenceUnit("tot", "career", polarity="positive", topic_key="x", priority=1),
        SentenceUnit("xau", "career", polarity="negative", topic_key="x", priority=1),
    ]
    split = ParagraphSplitter().split([units])
    assert len(split) == 2


def test_accepts_content_context_dict():
    payload = _sample_content().to_dict()
    result = ParagraphBuilder().build(payload)
    assert isinstance(result, ParagraphContext)
    assert result.paragraphs
