"""Paragraph Builder — assemble coherent paragraphs per section."""

from __future__ import annotations

from .models import NarrativeParagraph, NarrativeUnit


class ParagraphBuilder:
    """
    Group units into readable paragraphs.

    Default: one paragraph per section to avoid fragmented one-liners.
    """

    def __init__(self, *, max_sentences_per_paragraph: int = 8) -> None:
        self.max_sentences_per_paragraph = max(1, max_sentences_per_paragraph)

    def build(self, units: list[NarrativeUnit]) -> list[NarrativeParagraph]:
        """Build one coherent paragraph per section (avoids fragmented blocks)."""
        order: list[str] = []
        buckets: dict[str, list[NarrativeUnit]] = {}
        for unit in units:
            if unit.is_transition:
                continue
            if unit.section_id not in buckets:
                order.append(unit.section_id)
                buckets[unit.section_id] = []
            buckets[unit.section_id].append(unit)

        paragraphs: list[NarrativeParagraph] = []
        for section_id in order:
            group = buckets[section_id]
            title = group[0].section_title if group else section_id
            # Lead with higher priority, then remaining in original relative order
            ranked = sorted(group, key=lambda u: u.priority, reverse=True)
            texts = [self._ensure_terminal(item.text.strip()) for item in ranked if item.text.strip()]
            if not texts:
                continue
            # Soft join: keep as one paragraph unless very long → split by cap
            for chunk_texts in self._split_long(texts):
                joined = " ".join(chunk_texts)
                paragraphs.append(
                    NarrativeParagraph(
                        section_id=section_id,
                        section_title=title,
                        text=joined,
                        tone=ranked[0].tone if ranked else "neutral",
                        unit_count=len(chunk_texts),
                        is_transition=False,
                    )
                )
        return paragraphs

    def _split_long(self, texts: list[str]) -> list[list[str]]:
        """Split only when exceeding sentence budget; keep section continuity."""
        if len(texts) <= self.max_sentences_per_paragraph:
            return [texts]
        chunks: list[list[str]] = []
        current: list[str] = []
        for text in texts:
            current.append(text)
            if len(current) >= self.max_sentences_per_paragraph:
                chunks.append(current)
                current = []
        if current:
            chunks.append(current)
        return chunks

    @staticmethod
    def _ensure_terminal(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return stripped
        if stripped[-1] in ".!?…。！？":
            return stripped
        return stripped + "."
