"""
BTE Platform
Report Engine

File: engine.py
Version: 2.0 — WP6
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from engines.base.base_engine import BaseEngine
from engines.base.context import EngineContext
from engines.base.result import EngineResult

from .report import ReportFormat, ReportModel
from .service import ReportService


class ReportEngine(BaseEngine):
    """
    Report Engine.

    InterpretationResult → ReportModel → HTML / Markdown / PDF.
    Templates: knowledge/06_report_templates only.
    """

    stage = "report"

    def __init__(self) -> None:
        super().__init__()
        self.service = ReportService()

    def generate(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Tạo báo cáo (API tương thích tests / pipeline cũ)."""
        if "interpretation" in kwargs:
            raw = kwargs["interpretation"]
        elif not args:
            raw = {}
        elif len(args) == 1:
            raw = args[0]
        else:
            raw = args[-1]

        report = self.service.build(raw)
        content = self.service.format(report, ReportFormat.TEXT)
        return SimpleNamespace(success=True, content=content, report=report)

    def render(
        self,
        interpretation: Any,
        *,
        pdf_output: str | Path | None = None,
    ) -> ReportModel:
        """
        WP6 full pipeline:

        InterpretationResult → ReportModel → HTML → Markdown → PDF
        """
        return self.service.build_full(interpretation, pdf_output=pdf_output)

    def validate(self, context: EngineContext) -> None:
        """Kiểm tra dữ liệu đầu vào."""
        interpretation = context.get("interpretation")
        if interpretation is None:
            raise ValueError("InterpretationResult not found.")

    def run(self, context: EngineContext) -> EngineResult:
        """Sinh ReportModel (with optional HTML/MD/PDF in context)."""
        interpretation = context.get("interpretation")
        pdf_output = context.get("pdf_output")
        report = self.service.build_full(interpretation, pdf_output=pdf_output)
        context.set("report", report)
        context.set("report_html", report.html)
        context.set("report_markdown", report.markdown)
        context.set("report_pdf", report.pdf_path)
        return EngineResult(
            success=True,
            data=report,
            message="Report generated successfully.",
        )

    def export(
        self,
        context: EngineContext,
        output: str,
        fmt: ReportFormat,
    ) -> None:
        """Xuất Report."""
        report = context.get("report")
        if report is None:
            raise ValueError("Report not found.")
        self.service.export(report=report, output=output, fmt=fmt)

    def format(
        self,
        context: EngineContext,
        fmt: ReportFormat,
    ) -> str:
        """Chuyển Report thành chuỗi."""
        report = context.get("report")
        if report is None:
            raise ValueError("Report not found.")
        return self.service.format(report=report, fmt=fmt)
