"""Component Renderer — shared presentation helpers for report formats."""

from __future__ import annotations

from typing import Any, Mapping

from engines.analysis_engine.report_generator.models import (
    ReportSection,
    StructuredDataBlock,
)


class ComponentRenderer:
    """Base renderer coordinating section / table / chart components."""

    def __init__(
        self,
        *,
        section_renderer: Any | None = None,
        table_renderer: Any | None = None,
        chart_renderer: Any | None = None,
    ) -> None:
        # Late imports keep module import order simple for DI callers.
        from engines.analysis_engine.report_generator.chart_renderer import (
            ChartRenderer,
        )
        from engines.analysis_engine.report_generator.section_renderer import (
            SectionRenderer,
        )
        from engines.analysis_engine.report_generator.table_renderer import (
            TableRenderer,
        )

        self._sections = section_renderer or SectionRenderer()
        self._tables = table_renderer or TableRenderer()
        self._charts = chart_renderer or ChartRenderer()

    def render_sections_html(self, sections: tuple[ReportSection, ...]) -> str:
        """Render all sections as HTML."""
        return self._sections.render_many_html(sections)

    def render_sections_markdown(self, sections: tuple[ReportSection, ...]) -> str:
        """Render all sections as Markdown."""
        return self._sections.render_many_markdown(sections)

    def render_data_blocks_html(
        self,
        blocks: tuple[StructuredDataBlock, ...],
    ) -> str:
        """Render analytical data blocks as HTML tables/charts."""
        if not blocks:
            return ""
        parts = ['  <aside class="structured-data">', "    <h2>Analytical Data</h2>"]
        for block in blocks:
            parts.append(self._tables.render_html(block))
            chart = self._charts.render_html(block)
            if chart:
                parts.append(chart)
        parts.append("  </aside>")
        return "\n".join(parts)

    def render_data_blocks_markdown(
        self,
        blocks: tuple[StructuredDataBlock, ...],
    ) -> str:
        """Render analytical data blocks as Markdown tables/charts."""
        if not blocks:
            return ""
        lines = ["## Analytical Data", ""]
        for block in blocks:
            lines.append(self._tables.render_markdown(block))
            chart = self._charts.render_markdown(block)
            if chart:
                lines.append(chart)
                lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def flatten_payload(payload: Mapping[str, Any]) -> list[tuple[str, str]]:
        """Flatten a mapping into deterministic key/value rows."""
        rows: list[tuple[str, str]] = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, Mapping):
                rendered = ", ".join(
                    f"{child_key}={child_value}"
                    for child_key, child_value in sorted(value.items(), key=lambda i: str(i[0]))
                )
            elif isinstance(value, (list, tuple)):
                rendered = ", ".join(str(item) for item in value)
            else:
                rendered = str(value)
            rows.append((str(key), rendered))
        return rows
