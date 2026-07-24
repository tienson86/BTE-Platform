"""BTE Report Engine — public API (WP6)."""

from .coverage import TemplateCoverageAnalyzer, TemplateCoverageReport
from .engine import ReportEngine
from .knowledge_template_loader import KnowledgeTemplateLoader
from .report import (
    Report,
    ReportFormat,
    ReportMetadata,
    ReportModel,
    ReportRecommendation,
    ReportStatus,
    ReportSummary,
)
from .section import ReportSection, SectionType
from .section_builders import SectionBuilderRegistry
from .service import ReportService

__all__ = [
    "KnowledgeTemplateLoader",
    "Report",
    "ReportEngine",
    "ReportFormat",
    "ReportMetadata",
    "ReportModel",
    "ReportRecommendation",
    "ReportSection",
    "ReportService",
    "ReportStatus",
    "ReportSummary",
    "SectionBuilderRegistry",
    "SectionType",
    "TemplateCoverageAnalyzer",
    "TemplateCoverageReport",
]
