"""Report Generator package.

Importable implementation of Analysis Engine stage 10 (Report Generator).

Architecture documentation lives in:
``engines/analysis_engine/10_report_generator/``

Consumes InterpretationResult (+ optional AnalysisResult) and publishes
ReportGeneratorResult with HTML / Markdown / PDF / JSON / Print artifacts.
"""

from __future__ import annotations

from engines.analysis_engine.report_generator.chart_renderer import ChartRenderer
from engines.analysis_engine.report_generator.component_renderer import (
    ComponentRenderer,
)
from engines.analysis_engine.report_generator.engine import (
    ReportEngine,
    ReportGenerator,
)
from engines.analysis_engine.report_generator.exceptions import (
    ReportBindingError,
    ReportExecutionError,
    ReportFormatProfileError,
    ReportGeneratorError,
    ReportPrerequisiteError,
    ReportSchemaError,
    ReportSerializationError,
    ReportValidationError,
)
from engines.analysis_engine.report_generator.models import (
    FULL_PUBLICATION_FORMATS,
    SUPPORTED_FORMATS,
    FormatHints,
    FormatProfile,
    HtmlReportArtifact,
    JsonReportArtifact,
    LayoutTemplate,
    MarkdownReportArtifact,
    PdfReportArtifact,
    PrintReportArtifact,
    ReportAssemblyContext,
    ReportGeneratorResult,
    ReportMetadata,
    ReportSection,
    ReportTheme,
    StructuredDataBlock,
    StructuredReport,
)
from engines.analysis_engine.report_generator.report_builder import ReportBuilder
from engines.analysis_engine.report_generator.section_builder import SectionBuilder
from engines.analysis_engine.report_generator.section_renderer import SectionRenderer
from engines.analysis_engine.report_generator.table_renderer import TableRenderer
from engines.analysis_engine.report_generator.template_loader import TemplateLoader
from engines.analysis_engine.report_generator.theme import (
    CATALOG_THEME_IDS,
    ThemeManager,
    ThemeRegistry,
)

__all__ = [
    "CATALOG_THEME_IDS",
    "FULL_PUBLICATION_FORMATS",
    "SUPPORTED_FORMATS",
    "ChartRenderer",
    "ComponentRenderer",
    "FormatHints",
    "FormatProfile",
    "HtmlReportArtifact",
    "JsonReportArtifact",
    "LayoutTemplate",
    "MarkdownReportArtifact",
    "PdfReportArtifact",
    "PrintReportArtifact",
    "ReportAssemblyContext",
    "ReportBindingError",
    "ReportBuilder",
    "ReportEngine",
    "ReportExecutionError",
    "ReportFormatProfileError",
    "ReportGenerator",
    "ReportGeneratorError",
    "ReportGeneratorResult",
    "ReportMetadata",
    "ReportPrerequisiteError",
    "ReportSchemaError",
    "ReportSection",
    "ReportSerializationError",
    "ReportTheme",
    "ReportValidationError",
    "SectionBuilder",
    "SectionRenderer",
    "StructuredDataBlock",
    "StructuredReport",
    "TableRenderer",
    "TemplateLoader",
    "ThemeManager",
    "ThemeRegistry",
]

__version__ = "1.0.0"
