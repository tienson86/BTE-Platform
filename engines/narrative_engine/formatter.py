"""Narrative formatters — HTML / Markdown / PDF (no Report Engine mutation)."""

from __future__ import annotations

from pathlib import Path

from .models import NarrativeReport


def _escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class NarrativeFormatter:
    """Render NarrativeReport to text formats."""

    def to_markdown(self, report: NarrativeReport) -> str:
        """Markdown body."""
        lines: list[str] = []
        if report.title:
            lines.append(f"# {report.title}")
            lines.append("")
        last_heading = ""
        for paragraph in report.paragraphs:
            if paragraph.is_transition:
                lines.append(f"*{paragraph.text}*")
                lines.append("")
                continue
            if paragraph.section_title and paragraph.section_title != last_heading:
                lines.append(f"## {paragraph.section_title}")
                lines.append("")
                last_heading = paragraph.section_title
            if paragraph.text:
                lines.append(paragraph.text)
                lines.append("")
        return "\n".join(lines).strip() + "\n"

    def to_html(self, report: NarrativeReport) -> str:
        """HTML body."""
        parts = ["<html>", "<body>"]
        if report.title:
            parts.append(f"<h1>{_escape(report.title)}</h1>")
        last_heading = ""
        for paragraph in report.paragraphs:
            if paragraph.is_transition:
                parts.append(
                    f'<p class="transition"><em>{_escape(paragraph.text)}</em></p>'
                )
                continue
            if paragraph.section_title and paragraph.section_title != last_heading:
                parts.append(f"<h2>{_escape(paragraph.section_title)}</h2>")
                last_heading = paragraph.section_title
            if paragraph.text:
                parts.append(f"<p>{_escape(paragraph.text)}</p>")
        parts.extend(["</body>", "</html>"])
        return "\n".join(parts)

    def to_pdf(self, report: NarrativeReport, output: str | Path) -> Path:
        """Write PDF via report_engine simple writer (read-only dependency)."""
        from engines.report_engine.simple_pdf import write_simple_pdf

        lines: list[str] = []
        if report.title:
            lines.append(report.title)
            lines.append("=" * 40)
        for paragraph in report.paragraphs:
            if paragraph.is_transition:
                lines.append(paragraph.text)
                lines.append("")
                continue
            if paragraph.section_title:
                lines.append(paragraph.section_title)
                lines.append("-" * 20)
            if paragraph.text:
                lines.extend(paragraph.text.splitlines())
            lines.append("")
        return write_simple_pdf(lines, output, title=report.title or "BTE Narrative")
