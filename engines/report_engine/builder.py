"""
BTE Platform
Report Engine

File: builder.py
Version: 1.0
"""

from __future__ import annotations

from typing import Any

from .report import (
    Report,
    ReportMetadata,
    ReportSummary,
    ReportStatus,
)

from .section import (
    ReportSection,
    SectionType,
)


class ReportBuilder:
    """
    Xây dựng Report từ dữ liệu Interpretation.
    """

    def __init__(self) -> None:

        self._report = Report()

    # =====================================================
    # Basic
    # =====================================================

    def reset(self) -> "ReportBuilder":
        """
        Khởi tạo Report mới.
        """

        self._report = Report()

        return self

    def build(self) -> Report:
        """
        Trả về Report hoàn chỉnh.
        """

        self._report.status = ReportStatus.COMPLETED

        return self._report

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(
        self,
        metadata: ReportMetadata,
    ) -> "ReportBuilder":

        self._report.metadata = metadata

        return self

    # =====================================================
    # Summary
    # =====================================================

    def summary(
        self,
        summary: ReportSummary,
    ) -> "ReportBuilder":

        self._report.summary = summary

        return self

    # =====================================================
    # Section
    # =====================================================

    def add_section(
        self,
        section: ReportSection,
    ) -> "ReportBuilder":

        self._report.sections.append(section)

        return self

    def add_sections(
        self,
        sections: list[ReportSection],
    ) -> "ReportBuilder":

        self._report.sections.extend(sections)

        return self

    # =====================================================
    # Recommendation
    # =====================================================

    def add_recommendation(
        self,
        recommendation,
    ) -> "ReportBuilder":

        self._report.recommendations.append(
            recommendation
        )

        return self

    # =====================================================
    # Score
    # =====================================================

    def set_score(
        self,
        score: dict[str, Any],
    ) -> "ReportBuilder":

        self._report.score = score

        return self

    # =====================================================
    # Appendix
    # =====================================================

    def set_appendix(
        self,
        appendix: dict[str, Any],
    ) -> "ReportBuilder":

        self._report.appendix = appendix

        return self

    # =====================================================
    # Auto Build
    # =====================================================

    def from_interpretation(
        self,
        interpretation: dict[str, Any],
    ) -> "ReportBuilder":
        """
        Sinh Report từ InterpretationResult.
        """

        if "summary" in interpretation:

            self.summary(

                ReportSummary(

                    title="Tổng quan",

                    content=interpretation["summary"],

                )

            )

        if "sections" in interpretation:

            for index, item in enumerate(

                interpretation["sections"]

            ):

                section = ReportSection(

                    id=f"section_{index+1}",

                    title=item.get(

                        "title",

                        f"Section {index+1}",

                    ),

                    type=SectionType.INTERPRETATION,

                    content=item.get(

                        "content",

                        "",

                    ),

                    order=index + 1,

                )

                self.add_section(section)

        if "score" in interpretation:

            self.set_score(

                interpretation["score"]

            )

        return self
