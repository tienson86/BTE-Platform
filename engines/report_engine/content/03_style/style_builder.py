"""Style Layer (WP7C) — ParagraphContext → StyledParagraphContext."""

from __future__ import annotations

import importlib
from typing import Any, Mapping

from ._knowledge_loader import StyleKnowledgeLoader
from .emphasis_controller import EmphasisController
from .redundancy_reducer import RedundancyReducer
from .style_models import (
    StyledParagraph,
    StyledParagraphContext,
    StyledSentence,
    StyleKnowledge,
)
from .synonym_rewriter import SynonymRewriter
from .tone_controller import ToneController

_paragraph = importlib.import_module(
    "engines.report_engine.content.02_paragraph.paragraph_models"
)
Paragraph = _paragraph.Paragraph
ParagraphContext = _paragraph.ParagraphContext
SentenceUnit = _paragraph.SentenceUnit


class StyleBuilder:
    """
    Independent Style Layer entry point.

    Pipeline
    --------
    ParagraphContext
      → redundancy reduce
      → synonym rewrite (Dictionary/Terminology)
      → emphasis levels (Sentence Library labels)
      → tone resolve (Sentence Library tones)
      → StyledParagraphContext
    """

    def __init__(
        self,
        knowledge: StyleKnowledge | None = None,
        *,
        knowledge_root: str | None = None,
    ) -> None:
        self.knowledge = knowledge or StyleKnowledgeLoader(knowledge_root).load()
        self.reducer = RedundancyReducer()
        self.rewriter = SynonymRewriter(self.knowledge)
        self.emphasis = EmphasisController(self.knowledge)
        self.tone = ToneController(self.knowledge)

    def apply(
        self,
        paragraph_context: ParagraphContext | Mapping[str, Any],
    ) -> StyledParagraphContext:
        """Run full style pass."""
        ctx = self._as_paragraph_context(paragraph_context)
        reduced, removed = self.reducer.reduce(ctx.paragraphs)

        styled_paragraphs: list[StyledParagraph] = []
        rewritten_sentences: list[StyledSentence] = []
        emphasis_levels: dict[str, str] = {}

        for paragraph in reduced:
            level = self.emphasis.level_for(paragraph)
            emphasis_levels[paragraph.paragraph_id] = level
            styled_sentences: list[StyledSentence] = []
            for sentence in paragraph.sentences:
                rewritten = self.rewriter.rewrite(sentence.text)
                styled = StyledSentence(
                    original=sentence.text,
                    rewritten=rewritten,
                    section=paragraph.section,
                    paragraph_id=paragraph.paragraph_id,
                    polarity=sentence.polarity,
                    emphasis=level,
                    rule_id=sentence.rule_id,
                )
                styled_sentences.append(styled)
                rewritten_sentences.append(styled)

            body = " ".join(
                self._terminal(item.rewritten) for item in styled_sentences
            )
            marked = self.emphasis.apply_marker(body, level, paragraph.polarity)
            styled_paragraphs.append(
                StyledParagraph(
                    paragraph_id=paragraph.paragraph_id,
                    section=paragraph.section,
                    polarity=paragraph.polarity,
                    text=marked,
                    original_text=paragraph.text,
                    emphasis=level,
                    score=paragraph.score,
                    sentences=styled_sentences,
                )
            )

        document_tone = self.tone.resolve(reduced)
        return StyledParagraphContext(
            styled_paragraphs=styled_paragraphs,
            rewritten_sentences=rewritten_sentences,
            emphasis_levels=emphasis_levels,
            tone=document_tone,
            removed_duplicates=removed,
            metadata={
                "protected_term_count": len(self.knowledge.protected_terms),
                "synonym_count": len(self.knowledge.synonym_map),
                "paragraph_count": len(styled_paragraphs),
                "removed_count": len(removed),
            },
        )

    def _as_paragraph_context(
        self,
        value: ParagraphContext | Mapping[str, Any],
    ) -> ParagraphContext:
        if isinstance(value, ParagraphContext):
            return value
        paragraphs: list[Paragraph] = []
        for row in value.get("paragraphs") or []:
            if not isinstance(row, Mapping):
                continue
            sentences = [
                SentenceUnit(
                    text=str(item.get("text") or ""),
                    section=str(item.get("section") or row.get("section") or ""),
                    polarity=str(item.get("polarity") or "neutral"),
                    topic_key=str(item.get("topic_key") or ""),
                    priority=float(item.get("priority") or 0),
                    rule_id=str(item.get("rule_id") or ""),
                )
                for item in (row.get("sentences") or [])
                if isinstance(item, Mapping)
            ]
            paragraphs.append(
                Paragraph(
                    paragraph_id=str(row.get("paragraph_id") or ""),
                    section=str(row.get("section") or ""),
                    polarity=str(row.get("polarity") or "neutral"),
                    topic_key=str(row.get("topic_key") or ""),
                    sentences=sentences,
                    text=str(row.get("text") or ""),
                    score=float(row.get("score") or 0),
                )
            )
        return ParagraphContext(
            paragraphs=paragraphs,
            ordered_sentences=[],
            transitions=[],
            paragraph_scores=dict(value.get("paragraph_scores") or {}),
            metadata=dict(value.get("metadata") or {}),
        )

    @staticmethod
    def _terminal(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return stripped
        if stripped[-1] in ".!?…。！？":
            return stripped
        return stripped + "."
