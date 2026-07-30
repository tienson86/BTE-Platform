"""Paragraph Builder — group bound sentences into section paragraphs."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    InterpretationParagraph,
)
from engines.analysis_engine.interpretation_engine.phrase_library import PhraseLibrary
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    KnowledgeSession,
)


class ParagraphBuilder:
    """Build paragraphs from bound sentences without rewriting core text."""

    def __init__(self, *, phrase_library: PhraseLibrary | None = None) -> None:
        self._phrases = phrase_library or PhraseLibrary()

    def build(
        self,
        sentences: tuple[BoundSentence, ...],
        *,
        section_order: tuple[str, ...],
        session: KnowledgeSession | None = None,
        apply_phrases: bool = True,
    ) -> tuple[InterpretationParagraph, ...]:
        """Group sentences by section_id preserving selection order.

        When ``session`` is provided and ``apply_phrases`` is true, prepends a
        deterministic opening phrase from the Phrase Library.
        """
        buckets: dict[str, list[BoundSentence]] = {
            section_id: [] for section_id in section_order
        }
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
            paragraphs.append(
                self._make_paragraph(
                    section_id,
                    items,
                    session=session,
                    apply_phrases=apply_phrases,
                )
            )

        for section_id in sorted(extras):
            items = extras[section_id]
            paragraphs.append(
                self._make_paragraph(
                    section_id,
                    items,
                    session=session,
                    apply_phrases=apply_phrases,
                )
            )
        return tuple(paragraphs)

    def _make_paragraph(
        self,
        section_id: str,
        items: list[BoundSentence],
        *,
        session: KnowledgeSession | None,
        apply_phrases: bool,
    ) -> InterpretationParagraph:
        body = " ".join(item.text.strip() for item in items if item.text.strip())
        if apply_phrases and session is not None and body:
            _phrase_id, phrase_text = self._phrases.opening_for_section(
                section_id,
                session=session,
            )
            if phrase_text:
                body = f"{phrase_text} {body}"
        return InterpretationParagraph(
            section_id=section_id,
            sentences=tuple(items),
            text=body,
        )
