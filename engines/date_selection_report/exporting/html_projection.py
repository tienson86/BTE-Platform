"""Project DateSelectionRenderTree onto PACK 05 HTML with commercial print CSS.

Read-only. Does not mutate the render tree.
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
COMMERCIAL_CSS_PATH = Path(__file__).resolve().parent / "commercial_report.css"
PDF_DOCUMENT_TITLE = "Báo cáo Chọn ngày tốt"
PDF_AUTHOR = "BTE Platform"
PDF_SUBJECT = "Date Selection"

_ELEMENT_PILL_CLASS: dict[str, str] = {
    "Mộc": "ds-pill-moc",
    "Hỏa": "ds-pill-hoa",
    "Thổ": "ds-pill-tho",
    "Kim": "ds-pill-kim",
    "Thủy": "ds-pill-thuy",
}


def project_render_tree_to_html(tree: DateSelectionRenderTree) -> str:
    """Fill PACK 05 report_v1.html with RenderTree content and commercial CSS."""
    template = (PACK05_TEMPLATE_DIR / "report_v1.html").read_text(encoding="utf-8")
    css = (PACK05_TEMPLATE_DIR / "report_v1.css").read_text(encoding="utf-8")
    css += COMMERCIAL_CSS_PATH.read_text(encoding="utf-8")
    html = (
        template.replace("{{TITLE}}", escape(PDF_DOCUMENT_TITLE))
        .replace("{{CSS}}", css)
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
        '<header class="ds-cover" id="ds-header">'
        f"<h1>{escape(tree.header.title)}</h1>"
        f'<p class="ds-brand">{escape(tree.header.subtitle)}</p>'
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
        body=_kv_rows([(row.label, row.value) for row in tree.person.rows]),
    )


def _search(tree: DateSelectionRenderTree) -> str:
    period = tree.search_period
    body = (
        '<div class="ds-summary">'
        + _summary_item(period.month_label, period.month_display)
        + _summary_item(period.recommendation_count_label, period.recommendation_count)
        + "</div>"
    )
    if period.explanation:
        body += f'<p class="ds-caption">{escape(period.explanation)}</p>'
    return _section(section_id="search_period", title=period.title, body=body)


def _summary_item(label: str, value: str) -> str:
    return (
        '<div class="ds-summary-item">'
        f'<span class="ds-label">{escape(label)}</span>'
        f'<span class="ds-value">{escape(value)}</span>'
        "</div>"
    )


def _recommendations(tree: DateSelectionRenderTree) -> str:
    if tree.empty_state is not None:
        body = f'<p class="ds-caption">{escape(tree.empty_state.message)}</p>'
        return _section(
            section_id="recommendations",
            title=tree.recommendations_title,
            body=body,
            allow_break=True,
            card=False,
        )
    blocks = "".join(_recommendation(node) for node in tree.recommendations)
    return _section(
        section_id="recommendations",
        title=tree.recommendations_title,
        body=blocks,
        allow_break=True,
        card=False,
    )


def _recommendation(node: RecommendationNode) -> str:
    header = node.date_header
    date_day = (
        '<div class="ds-date-day">'
        f'<p class="ds-solar">{escape(header.solar_date)}</p>'
        f'<p class="ds-lunar">{escape(header.lunar_display)}</p>'
        f'<p class="ds-result">{escape(header.day_result)}</p>'
        "</div>"
    )
    info = (
        '<div class="ds-day-info">'
        + _kv_rows([(row.label, row.value) for row in node.day_information.rows])
        + "</div>"
    )
    hours = (
        '<div class="ds-hours">'
        f"<h3>{escape(node.compatible_hours.title)}</h3>"
        + _list([row.display for row in node.compatible_hours.rows])
        + "</div>"
    )
    groups = "".join(_positive_group(group.label, group.items) for group in node.positive_times.groups)
    positive = (
        f'<div class="ds-positive-times" id="positive-times-{node.rank}">'
        f"<h3>{escape(node.positive_times.title)}</h3>"
        f"{groups}"
        "</div>"
    )
    return (
        f'<article class="ds-recommendation" id="recommendation-{node.rank}">'
        f"{date_day}{info}{hours}{positive}"
        "</article>"
    )


def _positive_group(label: str, items: tuple) -> str:
    lines = [f"{item.branch_display} · {item.time_range}" for item in items]
    return f'<div class="ds-ke-group"><h4>{escape(label)}</h4>{_list(lines)}</div>'


def _guidance(tree: DateSelectionRenderTree) -> str:
    items = "".join(
        f"<h3>{escape(item.label)}</h3><p>{escape(item.text)}</p>" for item in tree.guidance.items
    )
    return _section(section_id="guidance", title=tree.guidance.title, body=items)


def _footer(tree: DateSelectionRenderTree) -> str:
    footer = tree.footer
    text = f"{footer.generator} · {footer.product} · {footer.report_version}"
    return f'<footer class="ds-footer" id="ds-footer">{escape(text)}</footer>'


def _section(
    *,
    section_id: str,
    title: str,
    body: str,
    allow_break: bool = False,
    card: bool = True,
) -> str:
    classes = ["report-v1__section"]
    if allow_break:
        classes.append("report-v1__section--flow")
    if card:
        classes.append("ds-card")
    return (
        f'<section class="{" ".join(classes)}" id="{escape(section_id)}">'
        f'<h2 class="report-v1__section-title">{escape(title)}</h2>'
        f'<div class="report-v1__section-body">{body}</div>'
        "</section>"
    )


def _kv_rows(rows: list[tuple[str, str]]) -> str:
    parts = ['<div class="ds-kv">']
    for label, value in rows:
        parts.append(
            '<div class="ds-kv-row">'
            f'<span class="ds-label">{escape(label)}</span>'
            f'<span class="ds-value">{_format_value(value)}</span>'
            "</div>"
        )
    parts.append("</div>")
    return "".join(parts)


def _format_value(value: str) -> str:
    if value in _ELEMENT_PILL_CLASS:
        return _pill(value)
    for element, css_class in _ELEMENT_PILL_CLASS.items():
        if value.endswith(f"({element})") and "·" not in value:
            return f'<span class="ds-pill {css_class}">{escape(value)}</span>'
    return escape(value)


def _pill(element: str) -> str:
    return f'<span class="ds-pill {_ELEMENT_PILL_CLASS[element]}">{escape(element)}</span>'


def _list(items: list[str]) -> str:
    rows = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f'<ul class="report-v1__list">{rows}</ul>'
