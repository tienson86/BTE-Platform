"""
section_builder.py
==================

Section Builder

Chịu trách nhiệm:

- Gom RuleResult theo Section
- Sắp xếp theo Priority
- Gọi ParagraphBuilder xây dựng nội dung
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Optional

from ..models.context import InterpretationContext
from ..models.rule_result import RuleResult
from ..models.report import ReportSection

from .paragraph_builder import ParagraphBuilder


class SectionBuilder:
    """
    Xây dựng từng Section của báo cáo.
    """

    def __init__(
        self,
        paragraph_builder: Optional[ParagraphBuilder] = None,
    ) -> None:

        self.paragraph_builder = (
            paragraph_builder
            or ParagraphBuilder()
        )

    # ======================================================
    # Public API
    # ======================================================

    def build(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> List[ReportSection]:

        groups = self.group_results(results)

        sections: List[ReportSection] = []

        for section_name, items in groups.items():

            items.sort(
                key=lambda r: (
                    r.priority,
                    r.score,
                ),
                reverse=True,
            )

            paragraphs = self.paragraph_builder.build(
                context=context,
                results=items,
            )

            section = ReportSection(

                title=section_name,

                paragraphs=paragraphs,

                rule_count=len(items),

            )

            sections.append(section)

        sections.sort(
            key=lambda s: s.title
        )

        return sections

    # ======================================================
    # Group
    # ======================================================

    def group_results(
        self,
        results: Iterable[RuleResult],
    ) -> Dict[str, List[RuleResult]]:

        groups: Dict[
            str,
            List[RuleResult]
        ] = defaultdict(list)

        for result in results:

            if not result.matched:
                continue

            section = self.get_section(result)

            groups[section].append(result)

        return groups

    # ======================================================
    # Resolve Section
    # ======================================================

    def get_section(
        self,
        result: RuleResult,
    ) -> str:
        """
        Xác định Section của Rule.

        Ưu tiên:

        Rule.section

        nếu không có

        -> "Tổng quan"
        """

        if result.rule.section:

            return result.rule.section

        return "Tổng quan"
