"""
BTE Platform
Report Engine

File: exporter.py
Version: 1.0
"""

from __future__ import annotations

import json
from pathlib import Path

from .formatter import ReportFormatter
from .report import Report, ReportFormat


class ReportExporter:
    """
    Xuất Report ra các định dạng khác nhau.
    """

    def __init__(self) -> None:

        self._formatter = ReportFormatter()

    # ==========================================================
    # Export
    # ==========================================================

    def export(
        self,
        report: Report,
        output: str | Path,
        fmt: ReportFormat,
    ) -> Path:
        """
        Xuất Report ra file.
        """

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if fmt == ReportFormat.JSON:

            self.export_json(report, output)

        elif fmt == ReportFormat.TEXT:

            self.export_text(report, output)

        elif fmt == ReportFormat.MARKDOWN:

            self.export_markdown(report, output)

        elif fmt == ReportFormat.HTML:

            self.export_html(report, output)

        else:

            raise ValueError(
                f"Unsupported format: {fmt}"
            )

        return output

    # ==========================================================
    # JSON
    # ==========================================================

    def export_json(
        self,
        report: Report,
        output: Path,
    ) -> None:

        output.write_text(

            json.dumps(

                report.to_dict(),

                ensure_ascii=False,

                indent=2,

            ),

            encoding="utf-8",

        )

    # ==========================================================
    # TEXT
    # ==========================================================

    def export_text(
        self,
        report: Report,
        output: Path,
    ) -> None:

        output.write_text(

            self._formatter.to_text(report),

            encoding="utf-8",

        )

    # ==========================================================
    # MARKDOWN
    # ==========================================================

    def export_markdown(
        self,
        report: Report,
        output: Path,
    ) -> None:

        output.write_text(

            self._formatter.to_markdown(report),

            encoding="utf-8",

        )

    # ==========================================================
    # HTML
    # ==========================================================

    def export_html(
        self,
        report: Report,
        output: Path,
    ) -> None:

        output.write_text(

            self._formatter.to_html(report),

            encoding="utf-8",

        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def export_default(
        self,
        report: Report,
        output: str | Path,
    ) -> Path:
        """
        Xuất theo format mặc định của Report.
        """

        return self.export(

            report=report,

            output=output,

            fmt=report.format,

        )
