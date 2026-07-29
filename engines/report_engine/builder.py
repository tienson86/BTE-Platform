"""
BTE Platform
Report Engine

File: builder.py
Version: 2.0 — WP6 template-driven build
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .coverage import TemplateCoverageAnalyzer
from .interpretation_adapter import interpretation_to_dict
from .knowledge_template_loader import KnowledgeTemplateLoader
from .report import (
    ReportMetadata,
    ReportModel,
    ReportStatus,
    ReportSummary,
)
from .section import ReportSection, SectionType
from .section_builders import SectionBuilderRegistry


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ReportBuilder:
    """
    Xây dựng ReportModel từ InterpretationResult + 06_report_templates.
    """

    def __init__(
        self,
        templates_root: str | None = None,
    ) -> None:
        self.loader = KnowledgeTemplateLoader(templates_root)
        self.section_builders = SectionBuilderRegistry(self.loader)
        self.coverage_analyzer = TemplateCoverageAnalyzer(self.loader)
        self._report: ReportModel = ReportModel()
        self._built_sections: list[Any] = []

    def reset(self) -> "ReportBuilder":
        """Khởi tạo ReportModel mới."""
        self._report = ReportModel()
        self._built_sections = []
        return self

    def build(self) -> ReportModel:
        """Trả về ReportModel hoàn chỉnh."""
        self._report.status = ReportStatus.COMPLETED
        if self._report.metadata.generated_at is None:
            self._report.metadata.generated_at = _utc_now()
        return self._report

    def metadata(self, metadata: ReportMetadata) -> "ReportBuilder":
        self._report.metadata = metadata
        return self

    def summary(self, summary: ReportSummary) -> "ReportBuilder":
        self._report.summary = summary
        return self

    def add_section(self, section: ReportSection) -> "ReportBuilder":
        self._report.sections.append(section)
        return self

    def add_sections(self, sections: list[ReportSection]) -> "ReportBuilder":
        self._report.sections.extend(sections)
        return self

    def add_recommendation(self, recommendation) -> "ReportBuilder":
        self._report.recommendations.append(recommendation)
        return self

    def set_score(self, score: dict[str, Any]) -> "ReportBuilder":
        self._report.score = score
        return self

    def set_appendix(self, appendix: dict[str, Any]) -> "ReportBuilder":
        self._report.appendix = appendix
        return self

    def from_interpretation(
        self,
        interpretation: dict[str, Any] | Any,
    ) -> "ReportBuilder":
        """
        Sinh ReportModel từ InterpretationResult (object hoặc dict).

        Titles / structure come from ``06_report_templates``.
        Narrative text comes from Interpretation only.
        """
        data = interpretation_to_dict(interpretation)
        schema = self.loader.load_schema()

        self._report.metadata = ReportMetadata(
            title=str(schema.get("schema_name") or "BTE Report"),
            author="BTE Platform",
            version=str(schema.get("schema_version") or "1.0"),
            language=str(schema.get("language") or "vi"),
            generated_at=_utc_now(),
        )

        built = self.section_builders.build_all(data)
        self._built_sections = built
        self._report.sections = [item.section for item in built]

        # Summary block from 01_summary section content
        summary_section = next(
            (item.section for item in built if item.section.id == "summary"),
            None,
        )
        summary_module = self.loader.get_module("01_summary")
        summary_title = (
            summary_module.module_title if summary_module else "summary"
        )
        self._report.summary = ReportSummary(
            title=summary_title,
            content=(
                summary_section.content
                if summary_section is not None
                else str(data.get("summary") or "")
            ),
        )

        if "score" in data and isinstance(data["score"], dict):
            self._report.score = data["score"]

        coverage = self.coverage_analyzer.analyze(built)
        self._report.templates_used = coverage.templates_used
        self._report.templates_unused = coverage.templates_unused
        self._report.template_coverage = coverage.to_dict()
        self._report.appendix = {
            "template_coverage": coverage.to_dict(),
            "templates_root": str(self.loader.root),
        }

        # Backward-compatible path: also accept legacy list-shaped sections
        legacy_sections = data.get("sections")
        if isinstance(legacy_sections, list) and legacy_sections and not any(
            section.content for section in self._report.sections
        ):
            for index, item in enumerate(legacy_sections):
                if not isinstance(item, dict):
                    continue
                self.add_section(
                    ReportSection(
                        id=f"legacy_{index + 1}",
                        title=item.get("title", f"Section {index + 1}"),
                        type=SectionType.INTERPRETATION,
                        content=item.get("content", ""),
                        order=100 + index,
                    )
                )

        return self
