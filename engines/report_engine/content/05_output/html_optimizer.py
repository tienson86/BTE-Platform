"""Normalize ConsistentParagraphContext into HTML-ready markup."""

from __future__ import annotations

from typing import Any

from ._helpers import (
    collapse_blank_lines,
    escape_html,
    iter_paragraphs,
    paragraph_section,
    paragraph_text,
    section_heading,
)


class HtmlOptimizer:
    """
    Build HTML from existing paragraph texts.

    Escapes markup characters; does not invent sentences.
    """

    def optimize(
        self,
        context: Any,
        *,
        title: str = "",
    ) -> str:
        """Return a minimal HTML document string."""
        parts: list[str] = ["<html>", "<head>", "<meta charset=\"utf-8\"/>"]
        if title:
            parts.append(f"<title>{escape_html(title)}</title>")
        parts.append("</head>")
        parts.append("<body>")
        if title:
            parts.append(f"<h1>{escape_html(title)}</h1>")

        last_section = ""
        for paragraph in iter_paragraphs(context):
            section = paragraph_section(paragraph)
            text = paragraph_text(paragraph)
            if not text:
                continue
            if section and section != last_section:
                parts.append(f"<h2>{escape_html(section_heading(section))}</h2>")
                last_section = section
            # Preserve paragraph text; only escape for HTML safety
            parts.append(f"<p>{escape_html(text)}</p>")

        parts.extend(["</body>", "</html>"])
        return collapse_blank_lines("\n".join(parts))
