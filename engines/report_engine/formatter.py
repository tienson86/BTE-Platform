"""
BTE Platform
Report Engine

File: formatter.py
Version: 1.0
"""

from __future__ import annotations

import json

from .report import (
    Report,
    ReportFormat,
)


def _escape(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class ReportFormatter:
    """
    Formatter của Report.

    Chuyển Report thành các định dạng
    Text / Markdown / HTML / JSON.
    """

    # =====================================================
    # Main
    # =====================================================

    def format(
        self,
        report: Report,
        fmt: ReportFormat,
    ) -> str:

        if fmt == ReportFormat.TEXT:
            return self.to_text(report)

        if fmt == ReportFormat.MARKDOWN:
            return self.to_markdown(report)

        if fmt == ReportFormat.HTML:
            return self.to_html(report)

        if fmt == ReportFormat.JSON:
            return self.to_json(report)

        raise ValueError(
            f"Unsupported format: {fmt}"
        )

    # =====================================================
    # TEXT
    # =====================================================

    def to_text(
        self,
        report: Report,
    ) -> str:

        lines: list[str] = []

        lines.append(report.metadata.title)

        lines.append("=" * 60)

        lines.append("")

        if report.summary.title:

            lines.append(report.summary.title)

            lines.append("-" * len(report.summary.title))

            lines.append(report.summary.content)

            lines.append("")

        for section in sorted(
            report.sections,
            key=lambda x: x.order,
        ):

            if not section.visible:
                continue

            lines.append(section.title)

            lines.append("-" * len(section.title))

            lines.append(section.content)

            lines.append("")

        return "\n".join(lines)

    # =====================================================
    # MARKDOWN
    # =====================================================

    def to_markdown(
        self,
        report: Report,
    ) -> str:

        lines: list[str] = []

        lines.append(f"# {report.metadata.title}")

        lines.append("")

        if report.summary.content:

            lines.append(f"## {report.summary.title or 'summary'}")

            lines.append("")

            lines.append(report.summary.content)

            lines.append("")

        for section in sorted(
            report.sections,
            key=lambda x: x.order,
        ):

            if not section.visible:
                continue

            lines.append(f"## {section.title}")

            lines.append("")

            lines.append(section.content)

            lines.append("")

        if report.recommendations:

            rec_title = "recommendation"
            for section in report.sections:
                meta = getattr(section, "metadata", None) or {}
                if meta.get("module_id") == "01_summary":
                    rec_title = section.title
                    break
            # Prefer appendix label if present
            labels = (report.appendix or {}).get("recommendation_label")
            if labels:
                rec_title = str(labels)

            lines.append(f"## {rec_title}")

            lines.append("")

            for item in report.recommendations:

                lines.append(
                    f"- {item.title}: {item.content}"
                )

            lines.append("")

        return "\n".join(lines)

    # =====================================================
    # HTML
    # =====================================================

    def to_html(
        self,
        report: Report,
    ) -> str:

        html = []

        html.append("<html>")

        html.append("<body>")

        html.append(
            f"<h1>{_escape(report.metadata.title)}</h1>"
        )

        if report.summary.content:

            html.append(
                f"<h2>{_escape(report.summary.title or 'summary')}</h2>"
            )

            for paragraph in str(report.summary.content).split("\n\n"):
                if paragraph.strip():
                    html.append(f"<p>{_escape(paragraph.strip())}</p>")

        for section in sorted(
            report.sections,
            key=lambda x: x.order,
        ):

            if not section.visible:
                continue

            html.append(
                f"<h2>{_escape(section.title)}</h2>"
            )

            for paragraph in str(section.content).split("\n\n"):
                if paragraph.strip():
                    html.append(f"<p>{_escape(paragraph.strip())}</p>")

        html.append("</body>")

        html.append("</html>")

        return "\n".join(html)

    # =====================================================
    # JSON
    # =====================================================

    def to_json(
        self,
        report: Report,
    ) -> str:

        return json.dumps(

            report.to_dict(),

            ensure_ascii=False,

            indent=2,

        )
