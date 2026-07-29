"""
BTE Platform
Report Engine

File: service.py
Version: 2.0 — WP6
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builder import ReportBuilder
from .coverage import TemplateCoverageAnalyzer
from .exporter import ReportExporter
from .formatter import ReportFormatter
from .report import Report, ReportFormat, ReportModel
from .simple_pdf import report_lines_from_model, write_simple_pdf
from .template_loader import TemplateLoader


class ReportService:
    """Dịch vụ tạo và xuất ReportModel."""

    def __init__(
        self,
        template_dir: str | Path = "templates",
        knowledge_templates_root: str | Path | None = None,
    ) -> None:
        self.builder = ReportBuilder(templates_root=knowledge_templates_root)
        self.formatter = ReportFormatter()
        self.exporter = ReportExporter()
        self.template_loader = TemplateLoader(template_dir=template_dir)
        self.coverage_analyzer = TemplateCoverageAnalyzer(self.builder.loader)

    def build(self, interpretation: Any) -> ReportModel:
        """Tạo ReportModel từ InterpretationResult."""
        return self.builder.reset().from_interpretation(interpretation).build()

    def build_full(
        self,
        interpretation: Any,
        *,
        pdf_output: str | Path | None = None,
    ) -> ReportModel:
        """
        InterpretationResult → ReportModel → HTML → Markdown → PDF.
        """
        report = self.build(interpretation)
        report.markdown = self.formatter.to_markdown(report)
        report.html = self.formatter.to_html(report)
        report.format = ReportFormat.HTML

        target = Path(pdf_output) if pdf_output else Path("reports") / "wp6_report.pdf"
        report.pdf_path = str(
            write_simple_pdf(
                report_lines_from_model(report),
                target,
                title=report.metadata.title or "BTE Report",
            )
        )
        report.status = report.status
        return report

    def format(self, report: Report, fmt: ReportFormat) -> str:
        """Chuyển Report thành chuỗi (text/md/html/json)."""
        if fmt == ReportFormat.PDF:
            raise ValueError("Use export(..., ReportFormat.PDF) for PDF files.")
        return self.formatter.format(report, fmt)

    def to_html(self, report: Report) -> str:
        """Render HTML."""
        return self.formatter.to_html(report)

    def to_markdown(self, report: Report) -> str:
        """Render Markdown."""
        return self.formatter.to_markdown(report)

    def to_pdf(self, report: Report, output: str | Path) -> Path:
        """Render PDF file."""
        return write_simple_pdf(
            report_lines_from_model(report),
            output,
            title=getattr(report.metadata, "title", None) or "BTE Report",
        )

    def export(
        self,
        report: Report,
        output: str | Path,
        fmt: ReportFormat,
    ) -> Path:
        """Xuất Report ra file."""
        return self.exporter.export(report=report, output=output, fmt=fmt)

    def build_and_format(
        self,
        interpretation: Any,
        fmt: ReportFormat,
    ) -> str:
        """Tạo Report và trả về chuỗi."""
        report = self.build(interpretation)
        return self.format(report, fmt)

    def build_and_export(
        self,
        interpretation: Any,
        output: str | Path,
        fmt: ReportFormat,
    ) -> Path:
        """Tạo Report và xuất ra file."""
        report = self.build(interpretation)
        return self.export(report=report, output=output, fmt=fmt)

    def template_coverage(self, report: ReportModel) -> dict[str, Any]:
        """Return coverage payload already attached or recompute."""
        if report.template_coverage:
            return report.template_coverage
        # Recompute from appendix if needed
        return dict(report.appendix.get("template_coverage") or {})

    def write_coverage_report(
        self,
        report: ReportModel,
        output_dir: str | Path,
    ) -> dict[str, Path]:
        """Write used/unused template coverage files."""
        from .coverage import TemplateCoverageReport

        payload = self.template_coverage(report)
        coverage = TemplateCoverageReport(
            templates_used=list(payload.get("templates_used") or report.templates_used),
            templates_unused=list(payload.get("templates_unused") or report.templates_unused),
            modules_covered=list(payload.get("modules_covered") or []),
            modules_missing=list(payload.get("modules_missing") or []),
            coverage_ratio=float(payload.get("coverage_ratio") or 0.0),
            notes=list(payload.get("notes") or []),
        )
        return self.coverage_analyzer.write_report(coverage, output_dir)

    def load_template(self, name: str) -> str:
        """Đọc local markdown template (legacy)."""
        return self.template_loader.load(name)

    def list_templates(self) -> list[str]:
        """Danh sách local markdown templates (legacy)."""
        return self.template_loader.list_templates()

    def save_template(self, name: str, content: str) -> None:
        """Lưu local markdown template (legacy)."""
        self.template_loader.save(name=name, content=content)

    def delete_template(self, name: str) -> bool:
        """Xóa local markdown template (legacy)."""
        return self.template_loader.delete(name)
