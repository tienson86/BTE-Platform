"""
BTE Platform
Report Engine

File: engine.py
Version: 1.0
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from engines.base.base_engine import BaseEngine
from engines.base.context import EngineContext
from engines.base.result import EngineResult

from .report import ReportFormat
from .service import ReportService


class ReportEngine(BaseEngine):
    """
    Report Engine.

    Chuyển InterpretationResult thành Report.
    """

    stage = "report"

    def __init__(self) -> None:

        super().__init__()

        self.service = ReportService()

    # ==========================================================
    # Legacy API
    # ==========================================================

    def generate(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Tạo báo cáo (API tương thích tests / pipeline cũ).
        """

        if "interpretation" in kwargs:

            raw = kwargs["interpretation"]

        elif not args:

            raw = {}

        elif len(args) == 1:

            raw = args[0]

        else:

            raw = args[-1]

        if isinstance(raw, dict):

            interpretation = raw

        else:

            interpretation = {}

            text = getattr(raw, "text", None)

            if isinstance(text, str) and text:

                interpretation["summary"] = text

            sections = getattr(raw, "sections", None)

            if sections:

                interpretation["sections"] = sections

            score = getattr(raw, "score", None)

            if score is not None:

                interpretation["score"] = score

        report = self.service.build(interpretation)

        content = self.service.format(
            report,
            ReportFormat.TEXT,
        )

        return SimpleNamespace(
            success=True,
            content=content,
        )

    # ==========================================================
    # Validate
    # ==========================================================

    def validate(
        self,
        context: EngineContext,
    ) -> None:
        """
        Kiểm tra dữ liệu đầu vào.
        """

        interpretation = context.get("interpretation")

        if interpretation is None:

            raise ValueError(
                "InterpretationResult not found."
            )

    # ==========================================================
    # Run
    # ==========================================================

    def run(
        self,
        context: EngineContext,
    ) -> EngineResult:
        """
        Sinh Report.
        """

        interpretation = context.get(
            "interpretation"
        )

        report = self.service.build(
            interpretation
        )

        context.set(
            "report",
            report,
        )

        return EngineResult(
            success=True,
            data=report,
            message="Report generated successfully.",
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def export(
        self,
        context: EngineContext,
        output: str,
        fmt: ReportFormat,
    ) -> None:
        """
        Xuất Report.
        """

        report = context.get("report")

        if report is None:

            raise ValueError(
                "Report not found."
            )

        self.service.export(
            report=report,
            output=output,
            fmt=fmt,
        )

    def format(
        self,
        context: EngineContext,
        fmt: ReportFormat,
    ) -> str:
        """
        Chuyển Report thành chuỗi.
        """

        report = context.get("report")

        if report is None:

            raise ValueError(
                "Report not found."
            )

        return self.service.format(
            report=report,
            fmt=fmt,
        )
