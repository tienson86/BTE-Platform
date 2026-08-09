"""BTE Report Engine — public API (WP6 + RE-1 foundation)."""

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
from .contracts.report_contracts import (
    CanonicalReportResult,
    report_foundation_contract,
)
from .context.canonical_report_context import (
    CanonicalReportContext,
    build_report_context,
)
from .foundation_constants import REPORT_VERSION
from .registry.module_registry import ReportModuleRegistry

__all__ = [
    "CanonicalReportContext",
    "CanonicalReportResult",
    "KnowledgeTemplateLoader",
    "REPORT_VERSION",
    "Report",
    "ReportEngine",
    "ReportFormat",
    "ReportMetadata",
    "ReportModel",
    "ReportModuleRegistry",
    "ReportRecommendation",
    "ReportSection",
    "ReportService",
    "ReportStatus",
    "ReportSummary",
    "SectionBuilderRegistry",
    "SectionType",
    "TemplateCoverageAnalyzer",
    "TemplateCoverageReport",
    "build_report_context",
    "report_foundation_contract",
]
