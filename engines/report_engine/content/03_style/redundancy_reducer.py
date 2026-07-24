"""Remove redundant sentences without inventing replacements."""

from __future__ import annotations

import importlib
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Iterable

_paragraph = importlib.import_module(
    "engines.report_engine.content.02_paragraph.paragraph_models"
)
Paragraph = _paragraph.Paragraph
SentenceUnit = _paragraph.SentenceUnit


def normalize(text: str) -> str:
    """Fold text for duplicate comparison."""
    decomposed = unicodedata.normalize("NFD", text.strip().lower())
    plain = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", plain).strip()


class RedundancyReducer:
    """Drop near-duplicate sentences; keep higher priority / longer text."""

    def __init__(self, *, similarity_threshold: float = 0.92) -> None:
        self.similarity_threshold = similarity_threshold

    def reduce(
        self,
        paragraphs: Iterable[Paragraph],
    ) -> tuple[list[Paragraph], list[str]]:
        """
        Return pruned paragraphs and list of removed original texts.
        """
        removed: list[str] = []
        kept_norms: list[str] = []
        result: list[Paragraph] = []

        for paragraph in paragraphs:
            kept_sentences: list[SentenceUnit] = []
            for sentence in paragraph.sentences:
                norm = normalize(sentence.text)
                if not norm:
                    removed.append(sentence.text)
                    continue
                if self._is_duplicate(norm, kept_norms):
                    removed.append(sentence.text)
                    continue
                kept_sentences.append(sentence)
                kept_norms.append(norm)

            if not kept_sentences:
                # Entire paragraph redundant
                if paragraph.text.strip():
                    removed.append(paragraph.text)
                continue

            text = " ".join(self._terminal(item.text) for item in kept_sentences)
            result.append(
                Paragraph(
                    paragraph_id=paragraph.paragraph_id,
                    section=paragraph.section,
                    polarity=paragraph.polarity,
                    topic_key=paragraph.topic_key,
                    sentences=kept_sentences,
                    text=text,
                    score=paragraph.score,
                )
            )
        return result, removed

    def _is_duplicate(self, norm: str, kept_norms: list[str]) -> bool:
        for other in kept_norms:
            if norm == other:
                return True
            if len(norm) >= 12 and len(other) >= 12:
                if norm in other or other in norm:
                    return True
            if SequenceMatcher(None, norm, other).ratio() >= self.similarity_threshold:
                return True
        return False

    @staticmethod
    def _terminal(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return stripped
        if stripped[-1] in ".!?…。！？":
            return stripped
        return stripped + "."
