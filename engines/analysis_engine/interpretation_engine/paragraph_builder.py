"""Paragraph Builder — group bound sentences into section paragraphs."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    InterpretationParagraph,
)


class ParagraphBuilder:
    """Build paragraphs from bound sentences without rewriting text."""

    def build(
        self,
        sentences: tuple[BoundSentence, ...],
        *,
        section_order: tuple[str, ...],
    ) -> tuple[InterpretationParagraph, ...]:
        """Group sentences by section_id preserving selection order."""
        buckets: dict[str, list[BoundSentence]] = {section_id: [] for section_id in section_order}
        extras: dict[str, list[BoundSentence]] = {}

        for sentence in sentences:
            if sentence.section_id in buckets:
                buckets[sentence.section_id].append(sentence)
            else:
                extras.setdefault(sentence.section_id, []).append(sentence)

        paragraphs: list[InterpretationParagraph] = []
        for section_id in section_order:
            items = buckets.get(section_id) or []
            if not items:
                continue
            text = " ".join(item.text.strip() for item in items if item.text.strip())
            paragraphs.append(
                InterpretationParagraph(
                    section_id=section_id,
                    sentences=tuple(items),
                    text=text,
                )
            )

        for section_id in sorted(extras):
            items = extras[section_id]
            text = " ".join(item.text.strip() for item in items if item.text.strip())
            paragraphs.append(
                InterpretationParagraph(
                    section_id=section_id,
                    sentences=tuple(items),
                    text=text,
                )
            )
        return tuple(paragraphs)
