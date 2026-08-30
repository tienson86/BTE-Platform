"""Executive Summary Formula tests (N-IMP-06)."""

from __future__ import annotations

from engines.narrative_v2.summary.summary_formula import (
    CORE_SEMANTIC_PRIORITY,
    headline_from_insight,
    join_sentences,
    split_sentences,
    word_count,
)
from engines.narrative_v2.summary.summary_model import HEADLINE_WORD_LIMIT


def test_formula_priority_is_stable() -> None:
    assert CORE_SEMANTIC_PRIORITY[0] == "core.pattern_context"
    assert "core.pattern_ten_gods_relation" in CORE_SEMANTIC_PRIORITY


def test_split_and_join_preserve_units() -> None:
    text = "Bạn có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung."
    parts = split_sentences(text)
    assert len(parts) == 2
    assert join_sentences(parts) == text


def test_headline_rejects_overlong_sentence() -> None:
    words = " ".join(["word"] * (HEADLINE_WORD_LIMIT + 1))
    sentence = f"{words}."
    assert word_count(sentence) > HEADLINE_WORD_LIMIT
    assert headline_from_insight(sentence) is None


def test_headline_takes_first_sentence_only() -> None:
    text = "Bạn có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung."
    headline = headline_from_insight(text)
    assert headline == "Bạn có chỗ dưỡng, chịu được việc cần nền."
    assert word_count(headline) <= HEADLINE_WORD_LIMIT
