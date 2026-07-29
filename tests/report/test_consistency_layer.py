"""WP7D — Consistency Layer unit tests (runs independently)."""

from __future__ import annotations

import importlib

_style = importlib.import_module("engines.report_engine.content.03_style.style_models")
StyledParagraph = _style.StyledParagraph
StyledParagraphContext = _style.StyledParagraphContext
StyledSentence = _style.StyledSentence

_consistency = importlib.import_module(
    "engines.report_engine.content.04_consistency"
)
ConsistencyBuilder = _consistency.ConsistencyBuilder
ConsistentParagraphContext = _consistency.ConsistentParagraphContext
DuplicateChecker = _consistency.DuplicateChecker
PolarityChecker = _consistency.PolarityChecker
ContradictionChecker = _consistency.ContradictionChecker
CoherenceChecker = _consistency.CoherenceChecker


def _para(
    pid: str,
    section: str,
    text: str,
    *,
    polarity: str = "neutral",
    score: float = 50.0,
) -> StyledParagraph:
    return StyledParagraph(
        paragraph_id=pid,
        section=section,
        polarity=polarity,
        text=text,
        original_text=text,
        emphasis="normal",
        score=score,
        sentences=[
            StyledSentence(
                original=text,
                rewritten=text,
                section=section,
                paragraph_id=pid,
                polarity=polarity,
            )
        ],
    )


def _sample_styled() -> StyledParagraphContext:
    return StyledParagraphContext(
        styled_paragraphs=[
            _para(
                "P001",
                "career",
                "Su nghiep thuan loi manh.",
                polarity="positive",
                score=90,
            ),
            _para(
                "P002",
                "career",
                "Su nghiep thuan loi manh.",
                polarity="positive",
                score=40,
            ),
            _para(
                "P003",
                "career",
                "Su nghiep bat loi yeu.",
                polarity="negative",
                score=30,
            ),
            _para(
                "P004",
                "wealth",
                "Tai van on dinh.",
                polarity="positive",
                score=70,
            ),
            _para("P005", "health", "OK", polarity="neutral", score=10),
        ],
        emphasis_levels={
            "P001": "high",
            "P002": "normal",
            "P003": "high",
            "P004": "medium",
            "P005": "normal",
        },
        tone="neutral",
        removed_duplicates=[],
    )


def test_consistency_builder_returns_context():
    result = ConsistencyBuilder().apply(_sample_styled())
    assert isinstance(result, ConsistentParagraphContext)
    assert result.checked_paragraphs
    assert isinstance(result.removed_duplicates, list)
    assert isinstance(result.contradiction_report, list)
    assert isinstance(result.coherence_report, list)
    assert isinstance(result.warnings, list)


def test_to_dict_keys():
    payload = ConsistencyBuilder().apply(_sample_styled()).to_dict()
    for key in (
        "checked_paragraphs",
        "removed_duplicates",
        "contradiction_report",
        "coherence_report",
        "warnings",
    ):
        assert key in payload


def test_duplicate_keeps_higher_score():
    result = ConsistencyBuilder().apply(_sample_styled())
    ids = [p.paragraph_id for p in result.checked_paragraphs]
    assert "P001" in ids
    assert "P002" not in ids
    assert any("thuan loi manh" in text for text in result.removed_duplicates)


def test_polarity_conflict_keeps_higher_priority():
    result = ConsistencyBuilder().apply(_sample_styled())
    career = [p for p in result.checked_paragraphs if p.section == "career"]
    # P001 positive score 90 wins over P003 negative score 30
    assert len(career) == 1
    assert career[0].paragraph_id == "P001"
    assert result.contradiction_report


def test_does_not_rewrite_kept_content():
    original = _sample_styled()
    kept_text = next(p.text for p in original.styled_paragraphs if p.paragraph_id == "P001")
    result = ConsistencyBuilder().apply(original)
    survivor = next(p for p in result.checked_paragraphs if p.paragraph_id == "P001")
    assert survivor.text == kept_text


def test_coherence_warns_short_paragraph():
    issues = CoherenceChecker(min_chars=8).check(
        [_para("P005", "health", "OK", score=10)]
    )
    assert any(issue.kind == "coherence" for issue in issues)


def test_accepts_dict_input():
    payload = _sample_styled().to_dict()
    result = ConsistencyBuilder().apply(payload)
    assert isinstance(result, ConsistentParagraphContext)
    assert result.checked_paragraphs


def test_runs_independently_without_style_builder():
    """No StyleBuilder / Narrative / Report Engine required."""
    paragraphs = [
        _para("A", "career", "Su nghiep tot manh.", polarity="positive", score=80),
        _para("B", "career", "Su nghiep xau yeu.", polarity="negative", score=20),
    ]
    kept, issues = ContradictionChecker().check(paragraphs)
    assert len(kept) == 1
    assert kept[0].paragraph_id == "A"
    assert issues
    styled = StyledParagraphContext(styled_paragraphs=paragraphs, tone="neutral")
    result = ConsistencyBuilder().apply(styled)
    assert result.checked_paragraphs
