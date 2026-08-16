"""HTML renderer for Commercial Report V2."""

from __future__ import annotations

from html import escape
from pathlib import Path

from engines.report_engine.commercial.models import (
    CommercialChapter,
    CommercialCover,
    CommercialReport,
    CommercialSection,
)

_TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates" / "v1"


class CommercialHtmlRenderer:
    """Render Cover → Pack 05 canonical narrative → optional Appendix."""

    def __init__(self, *, template_dir: Path | None = None) -> None:
        self._template_dir = template_dir or _TEMPLATE_DIR

    def render(self, report: CommercialReport) -> str:
        """Return a complete UTF-8 HTML document."""
        template = (self._template_dir / "report_v1.html").read_text(encoding="utf-8")
        css = (self._template_dir / "report_v1.css").read_text(encoding="utf-8")
        commercial_css = _COMMERCIAL_CSS
        title = report.cover.heading
        if report.cover.client_name:
            title = f"{report.cover.heading} — {report.cover.client_name}"
        return (
            template.replace("{{TITLE}}", escape(title))
            .replace("{{CSS}}", css + commercial_css)
            .replace("{{CONTENT}}", _render_content(report))
        )


def render_commercial_html(report: CommercialReport) -> str:
    """Module-level commercial HTML helper."""
    return CommercialHtmlRenderer().render(report)


def _render_content(report: CommercialReport) -> str:
    parts = [_render_cover(report.cover)]
    for chapter in report.chapters:
        parts.append(_render_chapter(chapter))
    for chapter in report.supporting_chapters:
        if chapter.chapter_id == "career":
            parts.append(_render_chapter(chapter))
    if report.audience.value == "ADVISOR" and report.appendix:
        parts.append(_render_appendix(report.appendix))
    parts.append(f'<footer class="report-v1__footer">{escape(report.footer)}</footer>')
    return "".join(parts)


def _render_cover(cover: CommercialCover) -> str:
    meta = ""
    if cover.meta_rows:
        items = "".join(
            f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>"
            for label, value in cover.meta_rows
        )
        meta = f'<dl class="report-v1__meta-grid">{items}</dl>'
    class_line = ""
    if cover.consulting_class:
        class_line = (
            f'<p class="report-commercial__class">{escape(cover.consulting_class)}</p>'
        )
    return (
        '<header class="report-v1__header report-commercial__cover">'
        f'<p class="report-commercial__kicker">BTE Consulting</p>'
        f'<h1 class="report-v1__title">{escape(cover.heading)}</h1>'
        f"{class_line}"
        f'<p class="report-v1__subtitle">{escape(cover.subtitle)}</p>'
        f"{meta}"
        "</header>"
    )


def _render_chapter(chapter: CommercialChapter) -> str:
    body = "".join(_render_section(section) for section in chapter.sections)
    return (
        f'<section class="report-v1__section report-commercial__chapter" '
        f'id="{escape(chapter.chapter_id)}">'
        f'<h2 class="report-v1__section-title">{escape(chapter.title)}</h2>'
        f"{body}"
        "</section>"
    )


def _render_section(section: CommercialSection) -> str:
    paragraphs = "".join(f"<p>{escape(item)}</p>" for item in section.paragraphs)
    return (
        f'<article class="report-commercial__section" id="{escape(section.section_id)}">'
        f"<h3>{escape(section.title)}</h3>"
        f"{paragraphs}"
        "</article>"
    )


def _render_appendix(sections: list[CommercialSection]) -> str:
    body = "".join(_render_section(section) for section in sections)
    return (
        '<section class="report-v1__section report-commercial__appendix" id="appendix">'
        '<h2 class="report-v1__section-title">Phụ lục cố vấn</h2>'
        f"{body}"
        "</section>"
    )


_COMMERCIAL_CSS = """
.report-commercial__kicker {
  color: var(--report-accent);
  font-size: 12px;
  letter-spacing: 0.12em;
  margin: 0 0 8px;
  text-transform: uppercase;
}
.report-commercial__class {
  color: var(--report-accent);
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
}
.report-commercial__cover .report-v1__meta-grid {
  margin-top: 16px;
}
.report-commercial__section {
  margin: 0 0 16px;
}
.report-commercial__section h3 {
  color: var(--report-text);
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px;
}
.report-commercial__appendix {
  border-top: 1px dashed var(--report-border);
  margin-top: 32px;
  padding-top: 16px;
}
"""
