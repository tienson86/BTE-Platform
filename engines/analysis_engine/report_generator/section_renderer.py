"""Section Renderer — render ReportSection components."""

from __future__ import annotations

import html

from engines.analysis_engine.report_generator.models import ReportSection


class SectionRenderer:
    """Render bound report sections for HTML and Markdown."""

    def render_html(self, section: ReportSection) -> str:
        """Render one section as an HTML block."""
        return (
            f'  <section class="report-section" id="{html.escape(section.section_id)}">\n'
            f"    <h2>{html.escape(section.title)}</h2>\n"
            f"    <p>{html.escape(section.body)}</p>\n"
            f"  </section>"
        )

    def render_markdown(self, section: ReportSection) -> str:
        """Render one section as Markdown."""
        return f"## {section.title}\n\n{section.body}\n"

    def render_many_html(self, sections: tuple[ReportSection, ...]) -> str:
        """Render ordered sections as HTML."""
        return "\n".join(self.render_html(section) for section in sections)

    def render_many_markdown(self, sections: tuple[ReportSection, ...]) -> str:
        """Render ordered sections as Markdown."""
        parts = [self.render_markdown(section) for section in sections]
        return "\n".join(parts).rstrip() + "\n"
