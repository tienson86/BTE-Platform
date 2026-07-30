"""HTML serializer for StructuredReport."""

from __future__ import annotations

import html

from engines.analysis_engine.report_generator.component_renderer import (
    ComponentRenderer,
)
from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    HtmlReportArtifact,
    LayoutTemplate,
    ReportTheme,
    StructuredReport,
)
from engines.analysis_engine.report_generator.theme import ThemeManager


class HtmlSerializer:
    """Serialize StructuredReport to HTML using layout template + theme."""

    def __init__(
        self,
        *,
        component_renderer: ComponentRenderer | None = None,
        theme_manager: ThemeManager | None = None,
    ) -> None:
        self._components = component_renderer or ComponentRenderer()
        self._themes = theme_manager or ThemeManager()

    def serialize(
        self,
        report: StructuredReport,
        *,
        theme: ReportTheme,
        template: LayoutTemplate,
    ) -> HtmlReportArtifact:
        """Render deterministic HTML artifact."""
        try:
            sections_html = self._components.render_sections_html(report.sections)
            data_html = self._components.render_data_blocks_html(report.data_blocks)
            print_css = self._themes.print_css(theme.theme_id)
            format_kwargs = {
                "title": html.escape(report.metadata.title),
                "overview": html.escape(report.overview),
                "theme_css": theme.css_block(),
                "font_family": html.escape(theme.font_family),
                "sections": sections_html,
                "data_blocks": data_html,
            }
            if "{print_css}" in template.html_shell:
                format_kwargs["print_css"] = print_css
            content = template.html_shell.format(**format_kwargs)
        except (KeyError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "HTML serialization failed",
                details={"error": str(exc)},
            ) from exc
        return HtmlReportArtifact(content=content)
