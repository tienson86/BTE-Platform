"""Report Generator package.

Importable implementation of Analysis Engine stage 10 (Report Generator).

Architecture documentation lives in:
``engines/analysis_engine/10_report_generator/``

Consumes InterpretationResult (+ optional AnalysisResult) and publishes
ReportGeneratorResult with HTML / Markdown / PDF / JSON artifacts.
"""

from __future__ import annotations

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
from engines.analysis_engine.report_generator.template_loader import TemplateLoader
from engines.analysis_engine.report_generator.theme import ThemeRegistry

__all__ = [
    "FULL_PUBLICATION_FORMATS",
    "SUPPORTED_FORMATS",
    "FormatHints",
    "FormatProfile",
    "HtmlReportArtifact",
    "JsonReportArtifact",
    "LayoutTemplate",
    "MarkdownReportArtifact",
    "PdfReportArtifact",
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
    "StructuredDataBlock",
    "StructuredReport",
    "TemplateLoader",
    "ThemeRegistry",
]

__version__ = "1.0.0"
