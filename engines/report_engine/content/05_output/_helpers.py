"""Shared helpers for output normalization (no content invention)."""

from __future__ import annotations

import re
from typing import Any, Iterable


def paragraph_text(paragraph: Any) -> str:
    """Extract existing paragraph text without modification beyond strip."""
    return str(getattr(paragraph, "text", "") or "").strip()


def paragraph_section(paragraph: Any) -> str:
    """Section id/title source already present on the paragraph."""
    return str(getattr(paragraph, "section", "") or "").strip()


def paragraph_id(paragraph: Any) -> str:
    """Paragraph identifier."""
    return str(getattr(paragraph, "paragraph_id", "") or "").strip()


def escape_html(text: str) -> str:
    """Escape HTML special characters (format normalization only)."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def collapse_blank_lines(text: str) -> str:
    """Normalize consecutive blank lines for stable document layout."""
    return re.sub(r"\n{3,}", "\n\n", text).strip() + ("\n" if text.strip() else "")


def iter_paragraphs(context: Any) -> list[Any]:
    """List checked paragraphs from ConsistentParagraphContext or mapping."""
    if isinstance(context, dict):
        return list(context.get("checked_paragraphs") or [])
    return list(getattr(context, "checked_paragraphs", None) or [])


def section_heading(section: str) -> str:
    """Use section key as heading — no new narrative wording."""
    return section
