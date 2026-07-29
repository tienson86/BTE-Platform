"""
export_service.py
=================

Export Service

Chịu trách nhiệm:

- Xuất báo cáo ra nhiều định dạng
- Quản lý thư mục xuất
- Sinh tên file
- Gọi ReportService

Không chứa logic Rule Engine.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from ..models.report import InterpretationReport
from .report_service import ReportService


class ExportService:
    """
    Dịch vụ xuất báo cáo.
    """

    def __init__(
        self,
        report_service: ReportService | None = None,
    ) -> None:

        self.report_service = report_service or ReportService()

    # =====================================================
    # Utilities
    # =====================================================

    def create_filename(
        self,
        prefix: str = "report",
        timestamp: bool = True,
    ) -> str:

        if not timestamp:
            return prefix

        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"{prefix}_{now}"

    # =====================================================
    # Export Single
    # =====================================================

    def export(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.report_service.save(
            report,
            output,
        )

    # =====================================================
    # Export Multiple
    # =====================================================

    def export_all(
        self,
        report: InterpretationReport,
        output_dir: str | Path,
        prefix: str = "report",
    ) -> list[Path]:

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = self.create_filename(prefix)

        outputs = []

        for ext in (
            ".md",
            ".html",
            ".txt",
            ".json",
        ):

            path = output_dir / f"{filename}{ext}"

            self.report_service.save(
                report,
                path,
            )

            outputs.append(path)

        return outputs

    # =====================================================
    # Export Selected
    # =====================================================

    def export_formats(
        self,
        report: InterpretationReport,
        output_dir: str | Path,
        formats: Iterable[str],
        prefix: str = "report",
    ) -> list[Path]:

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = self.create_filename(prefix)

        outputs = []

        for fmt in formats:

            fmt = fmt.lower().lstrip(".")

            path = output_dir / f"{filename}.{fmt}"

            self.report_service.save(
                report,
                path,
            )

            outputs.append(path)

        return outputs

    # =====================================================
    # Exists
    # =====================================================

    @staticmethod
    def exists(
        path: str | Path,
    ) -> bool:

        return Path(path).exists()

    # =====================================================
    # Remove
    # =====================================================

    @staticmethod
    def remove(
        path: str | Path,
    ) -> None:

        file = Path(path)

        if file.exists():

            file.unlink()

    # =====================================================
    # Clean Directory
    # =====================================================

    @staticmethod
    def clean_directory(
        directory: str | Path,
    ) -> None:

        directory = Path(directory)

        if not directory.exists():
            return

        for file in directory.iterdir():

            if file.is_file():

                file.unlink()
