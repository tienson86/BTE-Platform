"""Project DateSelectionRenderTree onto PACK 05 HTML Report V1.

Read-only. Does not mutate the render tree. Does not invent a theme.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import engines.report_engine as report_engine
from engines.date_selection_report.exceptions import DateSelectionReportExportError
from engines.date_selection_report.rendering.labels import FORBIDDEN_PUBLIC_TERMS
from engines.date_selection_report.rendering.nodes import (
    DateSelectionRenderTree,
    RecommendationNode,
)

PACK05_TEMPLATE_DIR = Path(report_engine.__file__).resolve().parent / "templates" / "v1"
PDF_DOCUMENT_TITLE = "Báo cáo Chọn ngày tốt"
PDF_AUTHOR = "BTE Platform"
PDF_SUBJECT = "Date Selection"

# Pagination hints only. Colors and type scale stay on PACK 05 tokens.
_PAGINATION_CSS = """
.ds-recommendation {
  border-top: 1px solid var(--report-border);
  margin: 16px 0 0;
  padding-top: 12px;
  break-inside: avoid;
  page-break-inside: avoid;
}
.ds-date-day {
  break-inside: avoid;
  page-break-inside: avoid;
}
.ds-solar {
  color: var(--report-accent);
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 4px;
}
.ds-result {
  color: var(--report-accent);
  font-size: 16px;
  font-weight: 700;
  margin: 4px 0 10px;
}
.ds-positive-times h4 {
  color: var(--report-accent);
  font-size: 14px;
  margin: 12px 0 6px;
}
.ds-meta {
  color: var(--report-muted);
  font-size: 12px;
  margin: 8px 0 0;
}
"""


def project_render_tree_to_html(tree: DateSelectionRenderTree) -> str:
    """Fill PACK 05 report_v1.html with RenderTree content."""
    template = (PACK05_TEMPLATE_DIR / "report_v1.html").read_text(encoding="utf-8")
    css = (PACK05_TEMPLATE_DIR / "report_v1.css").read_text(encoding="utf-8")
    html = (
        template.replace("{{TITLE}}", escape(PDF_DOCUMENT_TITLE))
        .replace("{{CSS}}", css + _PAGINATION_CSS)
        .replace("{{CONTENT}}", _render_content(tree))
    )
    html = _inject_document_meta(html)
    _assert_exportable_html(html)
    return html


def _inject_document_meta(html: str) -> str:
    meta = (
        f'<meta name="author" content="{escape(PDF_AUTHOR)}" />'
        f'<meta name="subject" content="{escape(PDF_SUBJECT)}" />'
    )
    return html.replace("<title>", meta + "<title>", 1)


def _assert_exportable_html(html: str) -> None:
    if "{{" in html or "}}" in html:
        raise DateSelectionReportExportError("unresolved placeholders remain")
    for term in FORBIDDEN_PUBLIC_TERMS:
        if term in html:
            raise DateSelectionReportExportError(f"forbidden public term: {term}")


def _render_content(tree: DateSelectionRenderTree) -> str:
    parts = [
        _header(tree),
        _person(tree),
        _search(tree),
        _recommendations(tree),
        '<div id="ds-last">',
        _guidance(tree),
        _footer(tree),
        "</div>",
    ]
    return "".join(parts)


def _header(tree: DateSelectionRenderTree) -> str:
    generated = _format_generated_at(tree.header.generated_at)
    return (
        '<header class="report-v1__header" id="ds-header">'
        f'<h1 class="report-v1__title">{escape(tree.header.title)}</h1>'
        f'<p class="report-v1__subtitle">{escape(tree.header.subtitle)}</p>'
        f'<p class="ds-meta">{escape(generated)}</p>'
        "</header>"
    )


def _format_generated_at(value: str) -> str:
    date_part = value.split("T", 1)[0]
    pieces = date_part.split("-")
    if len(pieces) == 3:
        year, month, day = pieces
        return f"{day}/{month}/{year}"
    return value


def _person(tree: DateSelectionRenderTree) -> str:
    return _section(
        section_id="person",
        title=tree.person.title,
        body=_meta_grid([(row.label, row.value) for row in tree.person.rows]),
    )


def _search(tree: DateSelectionRenderTree) -> str:
    period = tree.search_period
    rows = [
        (period.month_label, period.month_display),
        (period.recommendation_count_label, period.recommendation_count),
    ]
    body = _meta_grid(rows)
    if period.explanation:
        body += f"<p>{escape(period.explanation)}</p>"
    return _section(section_id="search_period", title=period.title, body=body)


def _recommendations(tree: DateSelectionRenderTree) -> str:
    if tree.empty_state is not None:
        body = f'<p class="report-v1__fallback">{escape(tree.empty_state.message)}</p>'
        return _section(
            section_id="recommendations",
            title=tree.recommendations_title,
            body=body,
            allow_break=True,
        )
    blocks = "".join(_recommendation(node) for node in tree.recommendations)
    return _section(
        section_id="recommendations",
        title=tree.recommendations_title,
        body=blocks,
        allow_break=True,
    )


def _recommendation(node: RecommendationNode) -> str:
    header = node.date_header
    date_day = (
        '<div class="ds-date-day">'
        f'<p class="ds-solar">{escape(header.solar_date)}</p>'
        f'<p class="report-v1__subtitle">{escape(header.lunar_display)}</p>'
        f'<p class="ds-result">{escape(header.day_result)}</p>'
        + _meta_grid([(row.label, row.value) for row in node.day_information.rows])
        + "</div>"
    )
    hours = (
        f"<h3>{escape(node.compatible_hours.title)}</h3>"
        + _list([row.display for row in node.compatible_hours.rows])
    )
    groups = [_positive_group(group.label, group.items) for group in node.positive_times.groups]
    positive = (
        f'<div class="ds-positive-times" id="positive-times-{node.rank}">'
        f"<h3>{escape(node.positive_times.title)}</h3>"
        f"{''.join(groups)}"
        "</div>"
    )
    return (
        f'<article class="ds-recommendation" id="recommendation-{node.rank}">'
        f"{date_day}{hours}{positive}"
        "</article>"
    )


def _positive_group(label: str, items: tuple) -> str:
    lines = [f"{item.branch_display} · {item.time_range}" for item in items]
    return f"<h4>{escape(label)}</h4>" + _list(lines)


def _guidance(tree: DateSelectionRenderTree) -> str:
    items = "".join(
        f"<h3>{escape(item.label)}</h3><p>{escape(item.text)}</p>" for item in tree.guidance.items
    )
    return _section(section_id="guidance", title=tree.guidance.title, body=items)


def _footer(tree: DateSelectionRenderTree) -> str:
    footer = tree.footer
    text = (
        f"{footer.generated_by_label} {footer.generator}"
        f" · {footer.product}"
        f" · {footer.report_version}"
    )
    return f'<footer class="report-v1__footer" id="ds-footer">{escape(text)}</footer>'


def _section(*, section_id: str, title: str, body: str, allow_break: bool = False) -> str:
    flow = " report-v1__section--flow" if allow_break else ""
    return (
        f'<section class="report-v1__section{flow}" id="{escape(section_id)}">'
        f'<h2 class="report-v1__section-title">{escape(title)}</h2>'
        f'<div class="report-v1__section-body">{body}</div>'
        "</section>"
    )


def _meta_grid(rows: list[tuple[str, str]]) -> str:
    parts = ['<dl class="report-v1__meta-grid">']
    for label, value in rows:
        parts.append(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>")
    parts.append("</dl>")
    return "".join(parts)


def _list(items: list[str]) -> str:
    rows = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f'<ul class="report-v1__list">{rows}</ul>'
