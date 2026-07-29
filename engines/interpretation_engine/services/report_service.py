"""
report_service.py
=================

Report Service

Chịu trách nhiệm:

- Xuất báo cáo
- Markdown
- HTML
- Text
- JSON

Không xử lý Rule Engine.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ..builders.formatter import Formatter
from ..models.report import InterpretationReport


class ReportService:
    """
    Dịch vụ xuất báo cáo.
    """

    def __init__(
        self,
        formatter: Formatter | None = None,
    ) -> None:

        self.formatter = formatter or Formatter()

    # ======================================================
    # TEXT
    # ======================================================

    def to_text(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.formatter.to_text(report)

    # ======================================================
    # MARKDOWN
    # ======================================================

    def to_markdown(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.formatter.to_markdown(report)

    # ======================================================
    # HTML
    # ======================================================

    def to_html(
        self,
        report: InterpretationReport,
    ) -> str:

        return self.formatter.to_html(report)

    # ======================================================
    # JSON
    # ======================================================

    def to_json(
        self,
        report: InterpretationReport,
        *,
        indent: int = 2,
        ensure_ascii: bool = False,
    ) -> str:

        return json.dumps(
            asdict(report),
            indent=indent,
            ensure_ascii=ensure_ascii,
            default=str,
        )

    # ======================================================
    # SAVE
    # ======================================================

    def save(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        output = Path(output)

        suffix = output.suffix.lower()

        if suffix == ".md":

            content = self.to_markdown(report)

        elif suffix == ".html":

            content = self.to_html(report)

        elif suffix == ".txt":

            content = self.to_text(report)

        elif suffix == ".json":

            content = self.to_json(report)

        else:

            raise ValueError(
                f"Không hỗ trợ định dạng: {suffix}"
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            content,
            encoding="utf-8",
        )

        return output

    # ======================================================
    # EXPORT
    # ======================================================

    def export_markdown(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.save(report, output)

    def export_html(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.save(report, output)

    def export_text(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.save(report, output)

    def export_json(
        self,
        report: InterpretationReport,
        output: str | Path,
    ) -> Path:

        return self.save(report, output)
