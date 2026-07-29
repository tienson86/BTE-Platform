"""
report_builder.py
=================

Report Builder

Ghép toàn bộ InterpretationReport.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..models.context import InterpretationContext
from ..models.report import InterpretationReport
from ..models.rule_result import RuleResult

from .section_builder import SectionBuilder


class ReportBuilder:
    """
    Xây dựng InterpretationReport.
    """

    VERSION = "1.0"

    def __init__(self):

        self.section_builder = SectionBuilder()

    # =====================================================
    # Build
    # =====================================================

    def build(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
        *,
        title: str = "BÁO CÁO PHÂN TÍCH BÁT TỰ",
        subtitle: str = "",
        summary: str = "",
    ) -> InterpretationReport:

        report = InterpretationReport()

        report.title = title

        report.subtitle = subtitle

        report.summary = summary

        report.sections = self.section_builder.build(
            context=context,
            results=list(results),
        )

        report.generated_at = datetime.now()

        report.version = self.VERSION

        report.statistics = {

            "matched_rules": sum(
                1
                for r in results
                if r.matched
            ),

            "total_sections": len(report.sections),

            "total_paragraphs": sum(
                len(s.paragraphs)
                for s in report.sections
            ),

            "total_sentences": sum(
                len(p.sentences)
                for s in report.sections
                for p in s.paragraphs
            ),
        }

        return report
