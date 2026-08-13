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

from .narrative_binding import (
    MISSING_NARRATIVE_DIAGNOSTIC,
    NARRATIVE_SOURCE,
    build_report_dict_from_narrative,
    is_usable_narrative_result,
    missing_narrative_report,
)
from .report import ReportFormat, ReportModel
from .result import ReportResult
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

    def render_from_analysis(
        self,
        analysis: Any,
        *,
        include_narrative: bool = False,
        narrative_result: Any = None,
    ) -> ReportResult:
        """
        Terminal pipeline entry: NarrativeResult → portal report (+ optional narrative).

        Interpretation remains on AnalysisResult as an upstream artifact.
        Customer narrative is Pack 05 NarrativeResult only.
        """
        interpretation = getattr(analysis, "interpretation", None)
        if interpretation is None:
            raise ValueError("AnalysisResult.interpretation is required for report.")

        payload = narrative_result
        if payload is None:
            payload = getattr(analysis, "narrative_result", None)

        if is_usable_narrative_result(payload):
            report = build_report_dict_from_narrative(payload)
            narrative = dict(report) if include_narrative else None
            return ReportResult(
                report=report,
                narrative=narrative,
                canonical_narrative=dict(payload),
                source=NARRATIVE_SOURCE,
                diagnostics={"narrative_source": NARRATIVE_SOURCE},
            )

        # Fallback path is diagnostic only — never dump InterpretationView as narrative.
        report = missing_narrative_report()
        narrative = dict(report) if include_narrative else None
        return ReportResult(
            report=report,
            narrative=narrative,
            canonical_narrative=None,
            source=MISSING_NARRATIVE_DIAGNOSTIC,
            diagnostics={
                "narrative_source": MISSING_NARRATIVE_DIAGNOSTIC,
                "interpretation_available": True,
            },
        )

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
