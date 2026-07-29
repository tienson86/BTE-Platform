"""
Portal-facing ReportView / NarrativeView serialization.

Sole producer of the commercial ``title`` / ``markdown`` / ``html`` JSON shape
used by AnalysisResult.report / narrative and Portal.
"""

from __future__ import annotations

import html
from typing import Any

DEFAULT_REPORT_TITLE = "Bản luận Bát tự"


def _sections_from_interpretation(interpretation: Any) -> list[dict[str, str]]:
    """Extract portal interpretation sections from AnalysisResult.interpretation."""
    sections_attr = getattr(interpretation, "sections", None)
    if sections_attr is not None:
        rows: list[dict[str, str]] = []
        for item in sections_attr:
            if hasattr(item, "to_dict"):
                payload = item.to_dict()
            elif isinstance(item, dict):
                payload = item
            else:
                continue
            rows.append(
                {
                    "id": str(payload.get("id") or ""),
                    "title": str(payload.get("title") or ""),
                    "body": str(payload.get("body") or ""),
                }
            )
        return rows
    if isinstance(interpretation, dict):
        raw = interpretation.get("sections") or []
        if isinstance(raw, list):
            return [
                {
                    "id": str(item.get("id") or ""),
                    "title": str(item.get("title") or ""),
                    "body": str(item.get("body") or ""),
                }
                for item in raw
                if isinstance(item, dict)
            ]
    return []


def render_markdown_from_sections(sections: list[dict[str, str]], title: str) -> str:
    """Build a simple markdown document from sanitized interpretation sections."""
    blocks = [f"# {title}"]
    for section in sections:
        body = str(section.get("body") or "").strip()
        if not body:
            continue
        blocks.append(f"## {section['title']}")
        blocks.append(body)
    return "\n\n".join(blocks).strip()


def render_html_from_sections(sections: list[dict[str, str]], title: str) -> str:
    """Build basic HTML from sanitized interpretation sections."""
    parts = ["<html><body>", f"<h1>{html.escape(title)}</h1>"]
    for section in sections:
        body = str(section.get("body") or "").strip()
        if not body:
            continue
        parts.append(f"<h2>{html.escape(section['title'])}</h2>")
        for paragraph in body.split("\n\n"):
            para = paragraph.strip()
            if para:
                parts.append(f"<p>{html.escape(para)}</p>")
    parts.append("</body></html>")
    return "\n".join(parts)


def build_report_portal_dict(
    interpretation: Any,
    *,
    title: str = DEFAULT_REPORT_TITLE,
) -> dict[str, Any]:
    """Build portal-compatible report payload from authoritative interpretation."""
    sections = _sections_from_interpretation(interpretation)
    markdown = render_markdown_from_sections(sections, title)
    html_text = render_html_from_sections(sections, title)
    return {
        "title": title,
        "markdown": markdown,
        "html": html_text,
        "section_count": len(sections),
    }


def build_narrative_portal_dict(
    interpretation: Any,
    *,
    title: str = DEFAULT_REPORT_TITLE,
) -> dict[str, Any]:
    """Build portal-compatible narrative payload from authoritative interpretation."""
    payload = build_report_portal_dict(interpretation, title=title)
    return payload
