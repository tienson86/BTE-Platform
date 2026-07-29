"""Build ParagraphContext from ContentContext."""

from __future__ import annotations

from typing import Any, Mapping

from engines.report_engine.content.models import ContentContext

from ._text_utils import (
    detect_polarity,
    extract_text,
    priority_of,
    topic_key,
)
from .paragraph_models import Paragraph, ParagraphContext, SentenceUnit
from .paragraph_splitter import ParagraphSplitter
from .sentence_merger import SentenceMerger
from .transition_selector import TransitionSelector


class ParagraphBuilder:
    """
    ContentContext → ParagraphContext

    1. Extract sentences per section (suggested_order)
    2. Assign polarity + topic
    3. Merge same topic (same section + polarity)
    4. Split mixed polarity (defensive)
    5. Score paragraphs
    6. Select transitions between paragraphs only
    """

    def __init__(self) -> None:
        self.merger = SentenceMerger()
        self.splitter = ParagraphSplitter()
        self.transitions = TransitionSelector()

    def build(self, content: ContentContext | Mapping[str, Any]) -> ParagraphContext:
        """Compose ParagraphContext without inventing new sentences."""
        ctx = self._as_content(content)
        keyword_list = [
            str(item.get("keyword") or "")
            for item in (ctx.keywords or [])
            if isinstance(item, Mapping) and item.get("keyword")
        ]

        units = self._extract_units(ctx, keyword_list)
        merged = self.merger.merge(units)
        pure_groups = self.splitter.split(merged)

        paragraphs: list[Paragraph] = []
        scores: dict[str, float] = {}
        for index, group in enumerate(pure_groups, start=1):
            paragraph = self._to_paragraph(index, group, ctx.section_scores)
            paragraphs.append(paragraph)
            scores[paragraph.paragraph_id] = paragraph.score

        # Keep section order aligned with suggested_order
        paragraphs = self._order_paragraphs(paragraphs, ctx.suggested_order)

        # Re-id after ordering for stable transition references
        for index, paragraph in enumerate(paragraphs, start=1):
            paragraph.paragraph_id = f"P{index:03d}"
            scores[paragraph.paragraph_id] = paragraph.score

        transition_list = self.transitions.select(
            paragraphs,
            repeated_topics=ctx.repeated_topics,
        )
        ordered_sentences = [
            sentence
            for paragraph in paragraphs
            for sentence in paragraph.sentences
        ]

        return ParagraphContext(
            paragraphs=paragraphs,
            ordered_sentences=ordered_sentences,
            transitions=transition_list,
            paragraph_scores={
                paragraph.paragraph_id: paragraph.score for paragraph in paragraphs
            },
            metadata={
                "section_count": len({item.section for item in paragraphs}),
                "paragraph_count": len(paragraphs),
                "sentence_count": len(ordered_sentences),
                "transition_count": len(transition_list),
            },
        )

    def _extract_units(
        self,
        ctx: ContentContext,
        keywords: list[str],
    ) -> list[SentenceUnit]:
        order = list(ctx.suggested_order) or list(ctx.grouped_rules.keys())
        seen_sections = set(order)
        for section in ctx.grouped_rules:
            if section not in seen_sections:
                order.append(section)

        units: list[SentenceUnit] = []
        for section in order:
            rules = ctx.grouped_rules.get(section) or []
            for rule in rules:
                if not isinstance(rule, Mapping):
                    continue
                text = extract_text(rule)
                if not text:
                    continue
                polarity = detect_polarity(rule, text)
                units.append(
                    SentenceUnit(
                        text=text,
                        section=section,
                        polarity=polarity,
                        topic_key=topic_key(text, keywords),
                        priority=priority_of(rule),
                        rule_id=str(rule.get("rule_id") or ""),
                        source=dict(rule),
                    )
                )
        return units

    def _to_paragraph(
        self,
        index: int,
        group: list[SentenceUnit],
        section_scores: Mapping[str, float],
    ) -> Paragraph:
        section = group[0].section
        polarity = group[0].polarity
        topic = group[0].topic_key
        # Join existing sentences only — no newly authored clauses
        text = " ".join(self._ensure_terminal(unit.text) for unit in group)
        base = float(section_scores.get(section, 0.0))
        avg_priority = sum(unit.priority for unit in group) / max(1, len(group))
        score = round(min(100.0, base * 0.6 + avg_priority * 0.4 + len(group)), 2)
        return Paragraph(
            paragraph_id=f"P{index:03d}",
            section=section,
            polarity=polarity,
            topic_key=topic,
            sentences=list(group),
            text=text,
            score=score,
        )

    @staticmethod
    def _order_paragraphs(
        paragraphs: list[Paragraph],
        suggested_order: list[str],
    ) -> list[Paragraph]:
        rank = {name: index for index, name in enumerate(suggested_order)}

        def _key(paragraph: Paragraph) -> tuple[int, float, str]:
            return (
                rank.get(paragraph.section, len(rank) + 1),
                -paragraph.score,
                paragraph.paragraph_id,
            )

        return sorted(paragraphs, key=_key)

    @staticmethod
    def _as_content(content: ContentContext | Mapping[str, Any]) -> ContentContext:
        if isinstance(content, ContentContext):
            return content
        return ContentContext(
            section_scores=dict(content.get("section_scores") or {}),
            important_sections=list(content.get("important_sections") or []),
            keywords=list(content.get("keywords") or []),
            grouped_rules={
                str(key): [dict(item) for item in (value or [])]
                for key, value in (content.get("grouped_rules") or {}).items()
            },
            repeated_topics=list(content.get("repeated_topics") or []),
            suggested_order=list(content.get("suggested_order") or []),
            metadata=dict(content.get("metadata") or {}),
        )

    @staticmethod
    def _ensure_terminal(text: str) -> str:
        stripped = text.strip()
        if not stripped:
            return stripped
        if stripped[-1] in ".!?…。！？":
            return stripped
        return stripped + "."
