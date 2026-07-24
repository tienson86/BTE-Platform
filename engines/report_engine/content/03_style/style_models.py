"""Style Layer models (WP7C)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StyledSentence:
    """Sentence after style pass (same meaning, possibly rewritten expression)."""

    original: str
    rewritten: str
    section: str
    paragraph_id: str = ""
    polarity: str = "neutral"
    emphasis: str = "normal"
    rule_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize styled sentence."""
        return {
            "original": self.original,
            "rewritten": self.rewritten,
            "section": self.section,
            "paragraph_id": self.paragraph_id,
            "polarity": self.polarity,
            "emphasis": self.emphasis,
            "rule_id": self.rule_id,
        }


@dataclass(slots=True)
class StyledParagraph:
    """Paragraph after redundancy / rewrite / emphasis / tone alignment."""

    paragraph_id: str
    section: str
    polarity: str
    text: str
    original_text: str
    emphasis: str = "normal"
    score: float = 0.0
    sentences: list[StyledSentence] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize styled paragraph."""
        return {
            "paragraph_id": self.paragraph_id,
            "section": self.section,
            "polarity": self.polarity,
            "text": self.text,
            "original_text": self.original_text,
            "emphasis": self.emphasis,
            "score": self.score,
            "sentences": [item.to_dict() for item in self.sentences],
        }


@dataclass(slots=True)
class StyledParagraphContext:
    """
    WP7C output from ParagraphContext.

    styled_paragraphs:
        Paragraphs after style processing.
    rewritten_sentences:
        Flat list of rewritten sentence records.
    emphasis_levels:
        paragraph_id → emphasis level.
    tone:
        Document-level tone (from Sentence Library schema).
    removed_duplicates:
        Texts removed by redundancy reducer.
    """

    styled_paragraphs: list[StyledParagraph] = field(default_factory=list)
    rewritten_sentences: list[StyledSentence] = field(default_factory=list)
    emphasis_levels: dict[str, str] = field(default_factory=dict)
    tone: str = "neutral"
    removed_duplicates: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize StyledParagraphContext."""
        return {
            "styled_paragraphs": [item.to_dict() for item in self.styled_paragraphs],
            "rewritten_sentences": [item.to_dict() for item in self.rewritten_sentences],
            "emphasis_levels": dict(self.emphasis_levels),
            "tone": self.tone,
            "removed_duplicates": list(self.removed_duplicates),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class StyleKnowledge:
    """Read-only style assets loaded from Knowledge."""

    protected_terms: tuple[str, ...] = ()
    synonym_map: dict[str, str] = field(default_factory=dict)
    tones: tuple[str, ...] = ("neutral",)
    emphasis_label: str = "emphasis"
    warning_label: str = "warning"
    positive_label: str = "positive"
