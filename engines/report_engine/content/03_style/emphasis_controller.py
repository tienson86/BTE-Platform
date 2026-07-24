"""Assign emphasis levels using Sentence Library labels + polarity/priority."""

from __future__ import annotations

import importlib
from typing import Iterable

from .style_models import StyleKnowledge

_paragraph = importlib.import_module(
    "engines.report_engine.content.02_paragraph.paragraph_models"
)
Paragraph = _paragraph.Paragraph

_EMPHASIS_HIGH = "high"
_EMPHASIS_MEDIUM = "medium"
_EMPHASIS_NORMAL = "normal"


class EmphasisController:
    """
    Compute emphasis levels; optionally prefix with Sentence Library emphasis label.

    Does not invent interpretation content — label text comes from KB only.
    """

    def __init__(self, knowledge: StyleKnowledge) -> None:
        self.knowledge = knowledge

    def level_for(self, paragraph: Paragraph) -> str:
        """Map paragraph signals to emphasis level."""
        if paragraph.polarity in {"negative", "warning"} and paragraph.score >= 40:
            return _EMPHASIS_HIGH
        if paragraph.polarity == "positive" and paragraph.score >= 70:
            return _EMPHASIS_HIGH
        avg_priority = 0.0
        if paragraph.sentences:
            avg_priority = sum(item.priority for item in paragraph.sentences) / len(
                paragraph.sentences
            )
        if avg_priority >= 85 or paragraph.score >= 80:
            return _EMPHASIS_HIGH
        if avg_priority >= 60 or paragraph.score >= 50:
            return _EMPHASIS_MEDIUM
        return _EMPHASIS_NORMAL

    def apply_marker(self, text: str, level: str, polarity: str) -> str:
        """
        Soft expression marker from Sentence Library labels.

        Only prefixes when high emphasis and label not already present.
        """
        if level != _EMPHASIS_HIGH or not text.strip():
            return text
        if polarity in {"negative", "warning"}:
            label = self.knowledge.warning_label
        elif polarity == "positive":
            label = self.knowledge.positive_label or self.knowledge.emphasis_label
        else:
            label = self.knowledge.emphasis_label
        if not label:
            return text
        if label.lower() in text.lower():
            return text
        return f"{label}: {text}"

    def map_levels(self, paragraphs: Iterable[Paragraph]) -> dict[str, str]:
        """paragraph_id → emphasis level."""
        return {
            paragraph.paragraph_id: self.level_for(paragraph)
            for paragraph in paragraphs
        }
