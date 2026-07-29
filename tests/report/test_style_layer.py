"""WP7C — Style Layer unit tests (runs independently)."""

from __future__ import annotations

import importlib

_paragraph = importlib.import_module(
    "engines.report_engine.content.02_paragraph.paragraph_models"
)
Paragraph = _paragraph.Paragraph
ParagraphContext = _paragraph.ParagraphContext
SentenceUnit = _paragraph.SentenceUnit

_style = importlib.import_module("engines.report_engine.content.03_style")
StyleBuilder = _style.StyleBuilder
StyledParagraphContext = _style.StyledParagraphContext
SynonymRewriter = _style.SynonymRewriter
RedundancyReducer = _style.RedundancyReducer
StyleKnowledge = _style.StyleKnowledge


def _sample_paragraph_context() -> ParagraphContext:
    return ParagraphContext(
        paragraphs=[
            Paragraph(
                paragraph_id="P001",
                section="summary",
                polarity="positive",
                topic_key="nhat",
                sentences=[
                    SentenceUnit(
                        text="Day Master manh, BaZi on dinh.",
                        section="summary",
                        polarity="positive",
                        topic_key="nhat",
                        priority=90,
                        rule_id="S1",
                    ),
                    SentenceUnit(
                        text="Day Master manh, BaZi on dinh.",
                        section="summary",
                        polarity="positive",
                        topic_key="nhat",
                        priority=80,
                        rule_id="S2",
                    ),
                ],
                text="Day Master manh, BaZi on dinh. Day Master manh, BaZi on dinh.",
                score=88.0,
            ),
            Paragraph(
                paragraph_id="P002",
                section="career",
                polarity="negative",
                topic_key="nghiep",
                sentences=[
                    SentenceUnit(
                        text="Su nghiep gap Weak Day Master kho khan.",
                        section="career",
                        polarity="negative",
                        topic_key="nghiep",
                        priority=55,
                        rule_id="C1",
                    )
                ],
                text="Su nghiep gap Weak Day Master kho khan.",
                score=50.0,
            ),
        ],
        ordered_sentences=[],
        transitions=[],
        paragraph_scores={"P001": 88.0, "P002": 50.0},
        metadata={},
    )


def test_style_builder_returns_styled_context():
    result = StyleBuilder().apply(_sample_paragraph_context())
    assert isinstance(result, StyledParagraphContext)
    assert result.styled_paragraphs
    assert result.rewritten_sentences
    assert result.emphasis_levels
    assert result.tone
    assert isinstance(result.removed_duplicates, list)


def test_style_context_to_dict_keys():
    payload = StyleBuilder().apply(_sample_paragraph_context()).to_dict()
    for key in (
        "styled_paragraphs",
        "rewritten_sentences",
        "emphasis_levels",
        "tone",
        "removed_duplicates",
    ):
        assert key in payload


def test_redundancy_removes_duplicate_sentence():
    result = StyleBuilder().apply(_sample_paragraph_context())
    assert result.removed_duplicates
    summary = next(p for p in result.styled_paragraphs if p.section == "summary")
    assert len(summary.sentences) == 1


def test_synonym_rewriter_uses_kb_aliases():
    knowledge = StyleKnowledge(
        protected_terms=("Nhật Chủ", "Day Master", "Bát Tự", "BaZi"),
        synonym_map={
            "Day Master": "Nhật Chủ",
            "BaZi": "Bát Tự",
            "Weak Day Master": "Thân Nhược",
        },
        tones=("neutral", "positive", "serious"),
    )
    text = SynonymRewriter(knowledge).rewrite("Day Master and BaZi / Weak Day Master")
    assert "Nhật Chủ" in text
    assert "Bát Tự" in text
    assert "Thân Nhược" in text
    assert "Day Master" not in text


def test_protected_canonical_not_invented_away():
    """Canonical terms remain as KB canonical after rewrite."""
    result = StyleBuilder().apply(_sample_paragraph_context())
    joined = " ".join(p.text for p in result.styled_paragraphs)
    # After rewrite, aliases become canonical Vietnamese terms from KB
    assert "Day Master" not in joined or "Nhật Chủ" in joined


def test_tone_is_from_sentence_library_set():
    result = StyleBuilder().apply(_sample_paragraph_context())
    knowledge = StyleBuilder().knowledge
    assert result.tone in set(knowledge.tones)


def test_emphasis_levels_assigned():
    result = StyleBuilder().apply(_sample_paragraph_context())
    assert "P001" in result.emphasis_levels or any(
        p.paragraph_id in result.emphasis_levels for p in result.styled_paragraphs
    )
    assert all(
        level in {"high", "medium", "normal"}
        for level in result.emphasis_levels.values()
    )


def test_accepts_paragraph_context_dict():
    payload = _sample_paragraph_context().to_dict()
    result = StyleBuilder().apply(payload)
    assert isinstance(result, StyledParagraphContext)
    assert result.styled_paragraphs


def test_style_layer_runs_independently_without_content_engine():
    """No ContentEngine / Narrative / Report Engine required."""
    reducer = RedundancyReducer()
    paragraphs, removed = reducer.reduce(_sample_paragraph_context().paragraphs)
    assert paragraphs
    assert removed
    styled = StyleBuilder().apply(
        ParagraphContext(
            paragraphs=paragraphs,
            paragraph_scores={p.paragraph_id: p.score for p in paragraphs},
        )
    )
    assert styled.styled_paragraphs
