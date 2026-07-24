"""Normalize ConsistentParagraphContext into Markdown-ready text."""

from __future__ import annotations

from typing import Any

from ._helpers import (
    collapse_blank_lines,
    iter_paragraphs,
    paragraph_section,
    paragraph_text,
    section_heading,
)


class MarkdownOptimizer:
    """
    Build Markdown from existing paragraph texts.

    Uses section keys as headings; does not invent narrative content.
    """

    def optimize(
        self,
        context: Any,
        *,
        title: str = "",
    ) -> str:
        """Return Markdown document string."""
        lines: list[str] = []
        if title:
            lines.append(f"# {title}")
            lines.append("")

        last_section = ""
        for paragraph in iter_paragraphs(context):
            section = paragraph_section(paragraph)
            text = paragraph_text(paragraph)
            if not text:
                continue
            if section and section != last_section:
                lines.append(f"## {section_heading(section)}")
                lines.append("")
                last_section = section
            lines.append(text)
            lines.append("")

        return collapse_blank_lines("\n".join(lines))
