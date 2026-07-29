"""
formatter.py
============

Formatter

Chuyển InterpretationReport thành:

- Plain Text
- Markdown
- HTML
"""

from __future__ import annotations

from html import escape

from ..models.report import InterpretationReport


class Formatter:
    """
    Formatter cho InterpretationReport.
    """

    # =====================================================
    # Plain Text
    # =====================================================

    def to_text(
        self,
        report: InterpretationReport,
    ) -> str:

        lines: list[str] = []

        if getattr(report, "title", ""):
            lines.append(report.title)
            lines.append("=" * len(report.title))
            lines.append("")

        if getattr(report, "summary", ""):
            lines.append(report.summary)
            lines.append("")

        for section in report.sections:

            lines.append(section.title.upper())
            lines.append("-" * len(section.title))

            for paragraph in section.paragraphs:

                if paragraph.title:
                    lines.append(paragraph.title + ":")

                for sentence in paragraph.sentences:
                    lines.append(f"• {sentence}")

                lines.append("")

        return "\n".join(lines)

    # =====================================================
    # Markdown
    # =====================================================

    def to_markdown(
        self,
        report: InterpretationReport,
    ) -> str:

        md: list[str] = []

        if getattr(report, "title", ""):
            md.append(f"# {report.title}")
            md.append("")

        if getattr(report, "subtitle", ""):
            md.append(f"## {report.subtitle}")
            md.append("")

        if getattr(report, "summary", ""):
            md.append(report.summary)
            md.append("")

        for section in report.sections:

            md.append(f"## {section.title}")
            md.append("")

            for paragraph in section.paragraphs:

                if paragraph.title:
                    md.append(f"### {paragraph.title}")

                for sentence in paragraph.sentences:
                    md.append(f"- {sentence}")

                md.append("")

        return "\n".join(md)

    # =====================================================
    # HTML
    # =====================================================

    def to_html(
        self,
        report: InterpretationReport,
    ) -> str:

        html = []

        html.append("<html>")
        html.append("<body>")

        if getattr(report, "title", ""):
            html.append(f"<h1>{escape(report.title)}</h1>")

        if getattr(report, "subtitle", ""):
            html.append(f"<h2>{escape(report.subtitle)}</h2>")

        if getattr(report, "summary", ""):
            html.append(f"<p>{escape(report.summary)}</p>")

        for section in report.sections:

            html.append(f"<h2>{escape(section.title)}</h2>")

            for paragraph in section.paragraphs:

                if paragraph.title:
                    html.append(f"<h3>{escape(paragraph.title)}</h3>")

                html.append("<ul>")

                for sentence in paragraph.sentences:
                    html.append(
                        f"<li>{escape(sentence)}</li>"
                    )

                html.append("</ul>")

        html.append("</body>")
        html.append("</html>")

        return "\n".join(html)
