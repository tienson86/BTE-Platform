"""HTML Report V1 renderer — consumes ReportInputV1 via shared presentation."""

from __future__ import annotations

from html import escape
from pathlib import Path

from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.rendering.report_sections_v1 import (
    PresentedReportV1,
    PresentedSection,
    build_presented_report,
)

_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates" / "v1"


class HtmlReportV1Renderer:
    """Render Report V1 HTML from ReportInputV1."""

    def __init__(
        self,
        *,
        template_dir: Path | None = None,
    ) -> None:
        self._template_dir = template_dir or _TEMPLATE_DIR

    def render(self, report_input: ReportInputV1) -> str:
        """Return a complete UTF-8 HTML document."""
        template = (self._template_dir / "report_v1.html").read_text(encoding="utf-8")
        css = (self._template_dir / "report_v1.css").read_text(encoding="utf-8")
        presented = build_presented_report(report_input)
        return (
            template.replace("{{TITLE}}", escape(presented.document_title))
            .replace("{{CSS}}", css)
            .replace("{{CONTENT}}", _render_content(presented))
        )


def render_html(report_input: ReportInputV1) -> str:
    """Render HTML Report V1 (module-level API)."""
    return HtmlReportV1Renderer().render(report_input)


def _render_content(presented: PresentedReportV1) -> str:
    parts: list[str] = [
        '<header class="report-v1__header">'
        f'<h1 class="report-v1__title">{escape(presented.heading)}</h1>'
        f'<p class="report-v1__subtitle">{escape(presented.subtitle)}</p>'
        "</header>"
    ]
    parts.extend(_render_section(section) for section in presented.sections)
    parts.append(
        f'<footer class="report-v1__footer">{escape(presented.footer)}</footer>'
    )
    return "".join(parts)


def _render_section(section: PresentedSection) -> str:
    body: list[str] = []
    if section.meta_rows:
        body.append(_meta_grid(section.meta_rows))
    if section.pillars:
        cards = "".join(_pillar_card(pillar.label, pillar.lines) for pillar in section.pillars)
        body.append(f'<div class="report-v1__pillars">{cards}</div>')
    elif section.table is not None:
        body.append(_table(section.table.headers, section.table.rows))
    body.extend(f"<p>{escape(paragraph)}</p>" for paragraph in section.paragraphs)
    if section.list_items:
        items = "".join(f"<li>{escape(item)}</li>" for item in section.list_items)
        body.append(f'<ul class="report-v1__list">{items}</ul>')
    has_primary = bool(
        section.meta_rows
        or section.pillars
        or section.table
        or section.paragraphs
        or section.list_items
    )
    if section.fallback and not has_primary:
        body.append(f'<p class="report-v1__fallback">{escape(section.fallback)}</p>')
    body.extend(
        f'<p class="report-v1__fallback">{escape(note)}</p>' for note in section.notes
    )
    return (
        f'<section class="report-v1__section" id="{escape(section.id)}">'
        f'<h2 class="report-v1__section-title">{escape(section.title)}</h2>'
        f'<div class="report-v1__section-body">{"".join(body)}</div>'
        "</section>"
    )


def _meta_grid(rows: list[tuple[str, str]]) -> str:
    parts = ['<dl class="report-v1__meta-grid">']
    for label, value in rows:
        parts.append(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>")
    parts.append("</dl>")
    return "".join(parts)


def _pillar_card(label: str, lines: list[tuple[str, str]]) -> str:
    details = "".join(
        f"<p><strong>{escape(name)}:</strong> {escape(value)}</p>" for name, value in lines
    )
    return (
        f'<article class="report-v1__pillar-card">'
        f"<h3>{escape(label)}</h3>"
        f"{details}"
        "</article>"
    )


def _table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return (
        '<table class="report-v1__table"><thead><tr>'
        f"{head}</tr></thead><tbody>{body}</tbody></table>"
    )
