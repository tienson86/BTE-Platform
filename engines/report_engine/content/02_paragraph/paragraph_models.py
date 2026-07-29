"""Paragraph Layer models (WP7B)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SentenceUnit:
    """One source sentence extracted from ContentContext.grouped_rules."""

    text: str
    section: str
    polarity: str = "neutral"
    topic_key: str = ""
    priority: float = 0.0
    rule_id: str = ""
    source: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize sentence unit."""
        return {
            "text": self.text,
            "section": self.section,
            "polarity": self.polarity,
            "topic_key": self.topic_key,
            "priority": self.priority,
            "rule_id": self.rule_id,
        }


@dataclass(slots=True)
class Paragraph:
    """Merged paragraph confined to a single section and polarity."""

    paragraph_id: str
    section: str
    polarity: str
    topic_key: str
    sentences: list[SentenceUnit] = field(default_factory=list)
    text: str = ""
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize paragraph."""
        return {
            "paragraph_id": self.paragraph_id,
            "section": self.section,
            "polarity": self.polarity,
            "topic_key": self.topic_key,
            "sentences": [item.to_dict() for item in self.sentences],
            "text": self.text,
            "score": self.score,
        }


@dataclass(slots=True)
class Transition:
    """
    Structural transition placed between two paragraphs.

    Does not invent narrative prose — only selects existing topic anchors
    from ContentContext when available.
    """

    transition_id: str
    after_paragraph_id: str
    before_paragraph_id: str
    from_section: str
    to_section: str
    kind: str = "section_boundary"
    anchor_topic: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize transition metadata."""
        return {
            "transition_id": self.transition_id,
            "after_paragraph_id": self.after_paragraph_id,
            "before_paragraph_id": self.before_paragraph_id,
            "from_section": self.from_section,
            "to_section": self.to_section,
            "kind": self.kind,
            "anchor_topic": self.anchor_topic,
        }


@dataclass(slots=True)
class ParagraphContext:
    """
    WP7B output built from ContentContext.

    paragraphs:
        Ordered paragraph objects.
    ordered_sentences:
        Flattened sentence units in final paragraph order.
    transitions:
        Transitions inserted only between paragraphs.
    paragraph_scores:
        paragraph_id → score.
    """

    paragraphs: list[Paragraph] = field(default_factory=list)
    ordered_sentences: list[SentenceUnit] = field(default_factory=list)
    transitions: list[Transition] = field(default_factory=list)
    paragraph_scores: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize ParagraphContext."""
        return {
            "paragraphs": [item.to_dict() for item in self.paragraphs],
            "ordered_sentences": [item.to_dict() for item in self.ordered_sentences],
            "transitions": [item.to_dict() for item in self.transitions],
            "paragraph_scores": dict(self.paragraph_scores),
            "metadata": dict(self.metadata),
        }
