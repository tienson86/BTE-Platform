"""Normalize ConsistentParagraphContext into PDF-ready line payload."""

from __future__ import annotations

from typing import Any

from ._helpers import (
    iter_paragraphs,
    paragraph_section,
    paragraph_text,
    section_heading,
)


class PdfOptimizer:
    """
    Prepare a PDF writer payload (title + plain lines).

    Does not invent sentences; wraps existing texts as printable lines.
    """

    def optimize(
        self,
        context: Any,
        *,
        title: str = "",
    ) -> dict[str, Any]:
        """
        Return ``{title, lines}`` suitable for ``write_simple_pdf``.
        """
        lines: list[str] = []
        doc_title = title or "BTE Content"
        lines.append(doc_title)
        lines.append("=" * min(40, max(8, len(doc_title))))

        last_section = ""
        for paragraph in iter_paragraphs(context):
            section = paragraph_section(paragraph)
            text = paragraph_text(paragraph)
            if not text:
                continue
            if section and section != last_section:
                lines.append("")
                lines.append(section_heading(section))
                lines.append("-" * min(20, max(4, len(section))))
                last_section = section
            # Keep original paragraph text; split only on existing newlines
            lines.extend(text.splitlines() or [text])

        return {
            "title": doc_title,
            "lines": lines,
            "format": "pdf_lines_v1",
        }
