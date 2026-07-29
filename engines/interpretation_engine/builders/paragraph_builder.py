"""
paragraph_builder.py
====================

Paragraph Builder

Chịu trách nhiệm:

- Gom RuleResult theo Topic
- Sắp xếp Rule
- Sinh đoạn văn
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Optional

from ..models.context import InterpretationContext
from ..models.rule_result import RuleResult
from ..models.report import ReportParagraph

from .sentence_generator import SentenceGenerator


class ParagraphBuilder:
    """
    Xây dựng Paragraph từ RuleResult.
    """

    def __init__(
        self,
        sentence_generator: Optional[SentenceGenerator] = None,
    ) -> None:

        self.sentence_generator = (
            sentence_generator
            or SentenceGenerator()
        )

    # =====================================================
    # Public API
    # =====================================================

    def build(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> List[ReportParagraph]:

        groups = self.group_results(results)

        paragraphs: List[ReportParagraph] = []

        for topic, items in groups.items():

            items.sort(
                key=lambda r: (
                    getattr(r.rule, "order", 0),
                    r.priority,
                    r.score,
                ),
                reverse=True,
            )

            sentences = []

            for result in items:

                sentence = self.sentence_generator.generate(
                    context=context,
                    result=result,
                )

                if sentence:
                    sentences.append(sentence)

            paragraph = ReportParagraph(
                title=topic,
                sentences=sentences,
                rule_count=len(items),
            )

            paragraphs.append(paragraph)

        paragraphs.sort(key=lambda p: p.title)

        return paragraphs

    # =====================================================
    # Group
    # =====================================================

    def group_results(
        self,
        results: Iterable[RuleResult],
    ) -> Dict[str, List[RuleResult]]:

        groups: Dict[str, List[RuleResult]] = defaultdict(list)

        for result in results:

            if not result.matched:
                continue

            topic = self.get_topic(result)

            groups[topic].append(result)

        return groups

    # =====================================================
    # Resolve Topic
    # =====================================================

    def get_topic(
        self,
        result: RuleResult,
    ) -> str:

        if result.topic:
            return result.topic

        return "Chung"
