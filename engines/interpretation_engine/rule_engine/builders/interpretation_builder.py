"""
interpretation_builder.py
=========================

Interpretation Builder

Điều phối toàn bộ quá trình xây dựng báo cáo diễn giải.

Pipeline:

RuleResult
    ↓
SectionBuilder
    ↓
ParagraphBuilder
    ↓
SentenceGenerator
    ↓
Formatter
    ↓
InterpretationReport
"""

from __future__ import annotations

from typing import Iterable, List, Optional

from ..models.context import InterpretationContext
from ..models.report import InterpretationReport
from ..models.rule_result import RuleResult

from .section_builder import SectionBuilder
from .formatter import Formatter


class InterpretationBuilder:
    """
    Builder cấp cao của Interpretation Engine.

    Chịu trách nhiệm:
        - Nhóm RuleResult theo Section
        - Xây dựng từng Section
        - Định dạng báo cáo cuối
    """

    def __init__(
        self,
        section_builder: Optional[SectionBuilder] = None,
        formatter: Optional[Formatter] = None,
    ) -> None:

        self.section_builder = section_builder or SectionBuilder()
        self.formatter = formatter or Formatter()

    # ==========================================================
    # Public API
    # ==========================================================

    def build(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> InterpretationReport:
        """
        Xây dựng báo cáo hoàn chỉnh.
        """

        report = InterpretationReport()

        report.sections = self.section_builder.build(
            context=context,
            results=list(results),
        )

        return report

    # ==========================================================
    # Markdown
    # ==========================================================

    def build_markdown(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> str:

        report = self.build(context, results)

        return self.formatter.to_markdown(report)

    # ==========================================================
    # HTML
    # ==========================================================

    def build_html(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> str:

        report = self.build(context, results)

        return self.formatter.to_html(report)

    # ==========================================================
    # Plain Text
    # ==========================================================

    def build_text(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> str:

        report = self.build(context, results)

        return self.formatter.to_text(report)
