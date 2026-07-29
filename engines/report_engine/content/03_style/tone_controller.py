"""Resolve document tone from paragraph polarities + Sentence Library tones."""

from __future__ import annotations

import importlib
from collections import Counter
from typing import Iterable

from .style_models import StyleKnowledge

_paragraph = importlib.import_module(
    "engines.report_engine.content.02_paragraph.paragraph_models"
)
Paragraph = _paragraph.Paragraph


class ToneController:
    """Pick a schema-allowed document tone without rewriting meaning."""

    def __init__(self, knowledge: StyleKnowledge) -> None:
        self.knowledge = knowledge

    def resolve(self, paragraphs: Iterable[Paragraph]) -> str:
        """
        Dominant tone from polarities, constrained to Sentence Library tones.
        """
        allowed = set(self.knowledge.tones) or {"neutral"}
        counts: Counter[str] = Counter()
        for paragraph in paragraphs:
            mapped = self._map_polarity(paragraph.polarity)
            if mapped in allowed:
                counts[mapped] += 1
            elif "neutral" in allowed:
                counts["neutral"] += 1
        if not counts:
            return "neutral" if "neutral" in allowed else next(iter(allowed))
        return counts.most_common(1)[0][0]

    @staticmethod
    def _map_polarity(polarity: str) -> str:
        raw = (polarity or "neutral").lower()
        if raw in {"positive", "pos", "+"}:
            return "positive"
        if raw in {"negative", "neg", "-", "warning", "warn"}:
            return "serious"
        return "neutral"
