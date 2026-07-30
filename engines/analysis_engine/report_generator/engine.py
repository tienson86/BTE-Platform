"""Report Generator — multi-format assembly from InterpretationResult."""

from __future__ import annotations

import logging
import time
from pathlib import Path

from engines.analysis_engine.report_generator.html_serializer import HtmlSerializer
from engines.analysis_engine.report_generator.json_serializer import JsonSerializer
from engines.analysis_engine.report_generator.markdown_serializer import (
    MarkdownSerializer,
)
from engines.analysis_engine.report_generator.models import (
    ReportAssemblyContext,
    ReportGeneratorResult,
)
from engines.analysis_engine.report_generator.pdf_serializer import PdfSerializer
from engines.analysis_engine.report_generator.report_builder import ReportBuilder
from engines.analysis_engine.report_generator.template_loader import TemplateLoader
from engines.analysis_engine.report_generator.theme import ThemeRegistry
from engines.analysis_engine.report_generator.validators import (
    validate_context,
    validate_format_profile,
    validate_prerequisites,
    validate_result,
    validate_structured_report,
)
from engines.analysis_engine.runtime.models import DiagnosticInfo, ExecutionMetadata

logger = logging.getLogger(__name__)

MODULE_VERSION = "1.0.0"


class ReportGenerator:
    """Assemble InterpretationResult into multi-format report artifacts.

    Public contract:
        assemble(context: ReportAssemblyContext) -> ReportGeneratorResult

    Supports HTML, Markdown, PDF, and JSON. Uses Report Builder, Section
    Builder, Theme, and Template Loader. Does not interpret or recompute.
    """

    version: str = MODULE_VERSION

    def __init__(
        self,
        *,
        report_builder: ReportBuilder | None = None,
        theme_registry: ThemeRegistry | None = None,
        template_loader: TemplateLoader | None = None,
        html_serializer: HtmlSerializer | None = None,
        markdown_serializer: MarkdownSerializer | None = None,
        json_serializer: JsonSerializer | None = None,
        pdf_serializer: PdfSerializer | None = None,
        version: str | None = None,
        pdf_output_dir: str | Path | None = None,
    ) -> None:
        self.version = version or MODULE_VERSION
        self._report_builder = report_builder or ReportBuilder()
        self._themes = theme_registry or ThemeRegistry()
        self._templates = template_loader or TemplateLoader()
        self._html = html_serializer or HtmlSerializer()
        self._markdown = markdown_serializer or MarkdownSerializer()
        self._json = json_serializer or JsonSerializer()
        self._pdf = pdf_serializer or PdfSerializer()
        self._pdf_output_dir = Path(pdf_output_dir) if pdf_output_dir else None

    def assemble(self, context: ReportAssemblyContext) -> ReportGeneratorResult:
        """Assemble and serialize report artifacts from assembly context."""
        started = time.perf_counter()
        validate_context(context)
        validate_format_profile(context.format_profile)
        validate_prerequisites(context)

        profile = context.format_profile
        theme = self._themes.get(profile.theme_id)
        template = self._templates.load(profile.template_id)

        structured = self._report_builder.build(
            context,
            theme=theme,
            module_version=self.version,
        )
        validate_structured_report(structured)

        html = None
        markdown = None
        json_artifact = None
        pdf = None
        requested = set(profile.formats)

        if "html" in requested:
            html = self._html.serialize(
                structured,
                theme=theme,
                template=template,
            )
        if "markdown" in requested:
            markdown = self._markdown.serialize(structured, template=template)
        if "json" in requested:
            json_artifact = self._json.serialize(structured)
        if "pdf" in requested:
            pdf_path = None
            if self._pdf_output_dir is not None:
                pdf_path = self._pdf_output_dir / f"{context.request_id}.pdf"
            pdf = self._pdf.serialize(structured, output_path=pdf_path)

        finished = time.perf_counter()
        diagnostics = (
            DiagnosticInfo(
                code="report_generator.assembled",
                message="ReportGeneratorResult assembled",
                level="info",
                stage_id="report_generator",
                details={
                    "formats": list(profile.formats),
                    "section_count": len(structured.sections),
                    "data_block_count": len(structured.data_blocks),
                },
            ),
        )
        result = ReportGeneratorResult(
            structured_report=structured,
            html=html,
            pdf=pdf,
            json=json_artifact,
            markdown=markdown,
            diagnostics=diagnostics,
            execution_metadata=ExecutionMetadata(
                request_id=context.request_id,
                runtime_version=self.version,
                stage_id="report_generator",
                module_version=self.version,
                started_at=started,
                finished_at=finished,
                duration_ms=(finished - started) * 1000.0,
                status="success",
            ),
            module_version=self.version,
            summary={
                "formats": list(profile.formats),
                "section_count": len(structured.sections),
                "data_block_count": len(structured.data_blocks),
                "theme_id": theme.theme_id,
                "template_id": template.template_id,
            },
        )
        validate_result(result, profile=profile)
        logger.info(
            "report_assembled",
            extra={
                "request_id": context.request_id,
                "formats": list(profile.formats),
                "section_count": len(structured.sections),
            },
        )
        return result

    def generate(self, context: ReportAssemblyContext) -> ReportGeneratorResult:
        """Alias of :meth:`assemble` for Report Engine naming."""
        return self.assemble(context)


# Compatibility alias matching user-facing "Report Engine" naming.
ReportEngine = ReportGenerator
