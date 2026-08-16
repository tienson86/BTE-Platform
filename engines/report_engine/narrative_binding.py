"""Bind Pack 05 NarrativeResult into report/PDF structures — no prose rewrite."""

from __future__ import annotations

from typing import Any

from engines.report_engine.portal_view import (
    DEFAULT_REPORT_TITLE,
    render_html_from_sections,
    render_markdown_from_sections,
)

CANONICAL_SECTION_IDS: tuple[str, ...] = (
    "sec-executive_summary",
    "sec-observation",
    "sec-reasoning",
    "sec-impact",
    "sec-recommendation",
    "sec-warning",
    "sec-conclusion",
)

CANONICAL_INTENT_ORDER: tuple[str, ...] = (
    "overview",
    "observation",
    "reasoning",
    "impact",
    "priority",
    "warning",
    "closing",
)

NARRATIVE_SOURCE = "pack05_narrative_result_v1"
MISSING_NARRATIVE_DIAGNOSTIC = "canonical_narrative_missing"


def is_usable_narrative_result(payload: Any) -> bool:
    """True when Pack 05 NarrativeResult can be the customer spine."""
    if not isinstance(payload, dict):
        return False
    sections = payload.get("sections")
    if not isinstance(sections, list) or not sections:
        return False
    contract = str(payload.get("contract") or "")
    if contract and contract != NARRATIVE_SOURCE:
        return False
    return True


def extract_canonical_sections(payload: dict[str, Any]) -> list[dict[str, str]]:
    """Return the seven Pack 05 sections in canonical order, content unchanged."""
    raw = [item for item in (payload.get("sections") or []) if isinstance(item, dict)]
    by_id = {str(item.get("id") or ""): item for item in raw}
    ordered: list[dict[str, Any]] = []
    for section_id in CANONICAL_SECTION_IDS:
        if section_id in by_id:
            ordered.append(by_id[section_id])
    if len(ordered) < len(CANONICAL_SECTION_IDS):
        by_intent = {str(item.get("intent") or ""): item for item in raw}
        for intent in CANONICAL_INTENT_ORDER:
            item = by_intent.get(intent)
            if item is None or item in ordered:
                continue
            ordered.append(item)
    if len(ordered) < len(raw):
        for item in raw:
            if item not in ordered:
                ordered.append(item)

    sections: list[dict[str, str]] = []
    for item in ordered:
        paragraphs = _paragraphs_from_section(item)
        if not paragraphs:
            continue
        sections.append(
            {
                "id": str(item.get("id") or ""),
                "title": str(item.get("title") or item.get("intent") or ""),
                "body": "\n\n".join(paragraphs),
            }
        )
    return sections


def build_report_dict_from_narrative(
    payload: dict[str, Any],
    *,
    title: str = DEFAULT_REPORT_TITLE,
) -> dict[str, Any]:
    """Render HTML/Markdown from NarrativeResult sections. Structured data stays source."""
    sections = extract_canonical_sections(payload)
    return {
        "title": title,
        "markdown": render_markdown_from_sections(sections, title),
        "html": render_html_from_sections(sections, title),
        "section_count": len(sections),
    }


def missing_narrative_report(*, title: str = DEFAULT_REPORT_TITLE) -> dict[str, Any]:
    """Diagnostic report when NarrativeResult is required but absent — no legacy dump."""
    return {
        "title": title,
        "markdown": "",
        "html": "",
        "section_count": 0,
    }


def _paragraphs_from_section(section: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for paragraph in section.get("paragraphs") or []:
        if isinstance(paragraph, dict):
            text = str(paragraph.get("text") or "").strip()
        else:
            text = str(paragraph or "").strip()
        if text:
            lines.append(text)
    if lines:
        return lines
    for recommendation in section.get("recommendations") or []:
        if not isinstance(recommendation, dict):
            continue
        action = str(recommendation.get("action") or "").strip()
        if action:
            lines.append(action)
    return lines
