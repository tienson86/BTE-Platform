"""Print serializer — print-optimized HTML artifact."""

from __future__ import annotations

import html

from engines.analysis_engine.report_generator.component_renderer import (
    ComponentRenderer,
)
from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    LayoutTemplate,
    PrintReportArtifact,
    ReportTheme,
    StructuredReport,
)
from engines.analysis_engine.report_generator.theme import ThemeManager


class PrintSerializer:
    """Serialize StructuredReport to a print-ready HTML artifact."""

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
    ) -> PrintReportArtifact:
        """Render deterministic print HTML artifact."""
        try:
            print_css = self._themes.print_css(theme.theme_id)
            sections_html = self._components.render_sections_html(report.sections)
            data_html = self._components.render_data_blocks_html(report.data_blocks)
            shell = template.html_shell
            if "{print_css}" not in shell:
                # Fallback when a custom template omits print_css placeholder.
                content = shell.format(
                    title=html.escape(report.metadata.title),
                    overview=html.escape(report.overview),
                    theme_css=theme.css_block(),
                    font_family=html.escape(theme.font_family),
                    sections=sections_html,
                    data_blocks=data_html,
                )
            else:
                content = shell.format(
                    title=html.escape(report.metadata.title),
                    overview=html.escape(report.overview),
                    theme_css=theme.css_block(),
                    font_family=html.escape(theme.font_family),
                    print_css=print_css,
                    sections=sections_html,
                    data_blocks=data_html,
                )
        except (KeyError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "Print serialization failed",
                details={"error": str(exc)},
            ) from exc
        return PrintReportArtifact(content=content)
