"""
BTE Platform
Report Engine

File: service.py
Version: 1.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builder import ReportBuilder
from .exporter import ReportExporter
from .formatter import ReportFormatter
from .report import Report, ReportFormat
from .template_loader import TemplateLoader


class ReportService:
    """
    Dịch vụ tạo và xuất Report.
    """

    def __init__(
        self,
        template_dir: str | Path = "templates",
    ) -> None:

        self.builder = ReportBuilder()

        self.formatter = ReportFormatter()

        self.exporter = ReportExporter()

        self.template_loader = TemplateLoader(
            template_dir=template_dir
        )

    # =====================================================
    # Build
    # =====================================================

    def build(
        self,
        interpretation: dict[str, Any],
    ) -> Report:
        """
        Tạo Report từ InterpretationResult.
        """

        return (
            self.builder
            .reset()
            .from_interpretation(
                interpretation
            )
            .build()
        )

    # =====================================================
    # Format
    # =====================================================

    def format(
        self,
        report: Report,
        fmt: ReportFormat,
    ) -> str:
        """
        Chuyển Report thành chuỗi.
        """

        return self.formatter.format(
            report,
            fmt,
        )

    # =====================================================
    # Export
    # =====================================================

    def export(
        self,
        report: Report,
        output: str | Path,
        fmt: ReportFormat,
    ) -> Path:
        """
        Xuất Report ra file.
        """

        return self.exporter.export(
            report=report,
            output=output,
            fmt=fmt,
        )

    # =====================================================
    # Build + Format
    # =====================================================

    def build_and_format(
        self,
        interpretation: dict[str, Any],
        fmt: ReportFormat,
    ) -> str:
        """
        Tạo Report và trả về chuỗi.
        """

        report = self.build(
            interpretation
        )

        return self.format(
            report,
            fmt,
        )

    # =====================================================
    # Build + Export
    # =====================================================

    def build_and_export(
        self,
        interpretation: dict[str, Any],
        output: str | Path,
        fmt: ReportFormat,
    ) -> Path:
        """
        Tạo Report và xuất ra file.
        """

        report = self.build(
            interpretation
        )

        return self.export(
            report=report,
            output=output,
            fmt=fmt,
        )

    # =====================================================
    # Template
    # =====================================================

    def load_template(
        self,
        name: str,
    ) -> str:
        """
        Đọc template.
        """

        return self.template_loader.load(
            name
        )

    def list_templates(
        self,
    ) -> list[str]:
        """
        Danh sách template.
        """

        return self.template_loader.list_templates()

    def save_template(
        self,
        name: str,
        content: str,
    ) -> None:
        """
        Lưu template.
        """

        self.template_loader.save(
            name=name,
            content=content,
        )

    def delete_template(
        self,
        name: str,
    ) -> bool:
        """
        Xóa template.
        """

        return self.template_loader.delete(
            name
        )
