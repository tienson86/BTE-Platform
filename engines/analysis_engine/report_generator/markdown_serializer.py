"""Markdown serializer for StructuredReport."""

from __future__ import annotations

from engines.analysis_engine.report_generator.component_renderer import (
    ComponentRenderer,
)
from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    LayoutTemplate,
    MarkdownReportArtifact,
    StructuredReport,
)


class MarkdownSerializer:
    """Serialize StructuredReport to Markdown using layout template."""

    def __init__(
        self,
        *,
        component_renderer: ComponentRenderer | None = None,
    ) -> None:
        self._components = component_renderer or ComponentRenderer()

    def serialize(
        self,
        report: StructuredReport,
        *,
        template: LayoutTemplate,
    ) -> MarkdownReportArtifact:
        """Render deterministic Markdown artifact."""
        try:
            sections_md = self._components.render_sections_markdown(report.sections)
            data_md = self._components.render_data_blocks_markdown(report.data_blocks)
            content = template.markdown_shell.format(
                title=report.metadata.title,
                overview=report.overview,
                sections=sections_md,
                data_blocks=data_md,
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "Markdown serialization failed",
                details={"error": str(exc)},
            ) from exc
        return MarkdownReportArtifact(content=content)
