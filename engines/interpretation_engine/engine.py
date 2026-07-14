"""
engine.py
=========

Interpretation Engine

Điểm vào chính của Interpretation Engine.

Pipeline:

InterpretationContext
        │
        ▼
InterpretationEngine
        │
        ▼
InterpretationService
        │
        ▼
InterpretationReport
        │
        ▼
ReportService
        │
        ▼
ExportService
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models.context import InterpretationContext
from .models.report import InterpretationReport
from .models.rule import Rule

from .services.interpretation_service import InterpretationService
from .services.report_service import ReportService
from .services.export_service import ExportService


class InterpretationEngine:
    """
    Engine chính của Interpretation Engine.

    Đây là API mà các module khác sử dụng.
    """

    def __init__(
        self,
        interpretation_service: InterpretationService | None = None,
        report_service: ReportService | None = None,
        export_service: ExportService | None = None,
    ) -> None:

        self.interpretation_service = (
            interpretation_service
            or InterpretationService()
        )

        self.report_service = (
            report_service
            or ReportService()
        )

        self.export_service = (
            export_service
            or ExportService(
                self.report_service
            )
        )

    # =====================================================
    # Interpretation
    # =====================================================

    def interpret(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> InterpretationReport:
        """
        Chạy diễn giải từ danh sách Rule.
        """

        return self.interpretation_service.run(
            context=context,
            rules=rules,
        )

    # =====================================================
    # Database
    # =====================================================

    def interpret_database(
        self,
        context: InterpretationContext,
        database: str | Path,
    ) -> InterpretationReport:
        """
        Chạy diễn giải từ Rule Database.
        """

        return self.interpretation_service.run_from_database(
            context=context,
            database_path=database,
        )

    # =====================================================
    # Markdown
    # =====================================================

    def to_markdown(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.report_service.to_markdown(
            report
        )

    # =====================================================
    # HTML
    # =====================================================

    def to_html(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.report_service.to_html(
            report
        )

    # =====================================================
    # TEXT
    # =====================================================

    def to_text(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.report_service.to_text(
            report
        )

    # =====================================================
    # JSON
    # =====================================================

    def to_json(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.report_service.to_json(
            report
        )

    # =====================================================
    # Export
    # =====================================================

    def export(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.export_service.export(
            report,
            output,
        )

    def export_all(
        self,
        report: InterpretationReport,
        output_dir: str | Path,
        prefix: str = "report",
    ) -> list[Path]:

        return self.export_service.export_all(
            report=report,
            output_dir=output_dir,
            prefix=prefix,
        )

    # =====================================================
    # Shortcut
    # =====================================================

    def run(
        self,
        context: InterpretationContext,
        database: str | Path,
    ) -> InterpretationReport:
        """
        API rút gọn.

        Đây sẽ là hàm được gọi nhiều nhất.
        """

        return self.interpret_database(
            context=context,
            database=database,
        )
