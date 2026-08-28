"""PACK 06 Date Selection report (P6-01 / P6-02 / P6-03 / P6-04).

Public surface: models, adapter, render tree, PDF and DOCX export. No portal.
"""

from engines.date_selection_report.adapter import DateSelectionReportAdapter
from engines.date_selection_report.contracts import (
    CanonicalSearchResult,
    EXPORT_CONTRACT,
    RENDER_CONTRACT,
    REPORT_FOUNDATION_CONTRACT,
)
from engines.date_selection_report.exceptions import (
    DateSelectionReportError,
    DateSelectionReportExportError,
    DateSelectionReportTemplateError,
    DateSelectionReportValidationError,
)
from engines.date_selection_report.exporting import (
    DateSelectionDocxExporter,
    DateSelectionPdfExporter,
    build_docx_filename,
    build_pdf_filename,
    export_docx,
    export_pdf,
    project_render_tree_to_html,
)
from engines.date_selection_report.models import (
    CompatibleHourReportData,
    DateSelectionReportModel,
    GuidanceItem,
    GuidanceReportData,
    Metadata,
    PersonReportData,
    PositiveKeReportData,
    Provenance,
    ProvenanceData,
    RecommendedDateReportData,
    SearchPeriodReportData,
)
from engines.date_selection_report.rendering import (
    CompatibleHoursSectionBuilder,
    DateSelectionRenderContext,
    DateSelectionRenderTree,
    DateSelectionRenderTreeBuilder,
    FooterSectionBuilder,
    GuidanceSectionBuilder,
    HeaderSectionBuilder,
    PersonSectionBuilder,
    PositiveTimesSectionBuilder,
    RecommendationSectionBuilder,
    SearchPeriodSectionBuilder,
    build_render_tree,
    create_render_context,
)
from engines.date_selection_report.templates import (
    DateSelectionTemplatePackage,
    load_date_selection_template_package,
    validate_render_tree,
)
from engines.date_selection_report.validators import (
    validate_report_model,
    validate_search_result,
)

__all__ = [
    "CanonicalSearchResult",
    "CompatibleHourReportData",
    "CompatibleHoursSectionBuilder",
    "DateSelectionRenderContext",
    "DateSelectionRenderTree",
    "DateSelectionRenderTreeBuilder",
    "DateSelectionReportAdapter",
    "DateSelectionDocxExporter",
    "DateSelectionPdfExporter",
    "DateSelectionReportError",
    "DateSelectionReportExportError",
    "DateSelectionReportModel",
    "DateSelectionReportTemplateError",
    "DateSelectionReportValidationError",
    "EXPORT_CONTRACT",
    "DateSelectionTemplatePackage",
    "FooterSectionBuilder",
    "GuidanceItem",
    "GuidanceReportData",
    "GuidanceSectionBuilder",
    "HeaderSectionBuilder",
    "Metadata",
    "PersonReportData",
    "PersonSectionBuilder",
    "PositiveKeReportData",
    "PositiveTimesSectionBuilder",
    "Provenance",
    "ProvenanceData",
    "RENDER_CONTRACT",
    "REPORT_FOUNDATION_CONTRACT",
    "RecommendationSectionBuilder",
    "RecommendedDateReportData",
    "SearchPeriodReportData",
    "SearchPeriodSectionBuilder",
    "build_docx_filename",
    "build_pdf_filename",
    "build_render_tree",
    "create_render_context",
    "export_docx",
    "export_pdf",
    "project_render_tree_to_html",
    "load_date_selection_template_package",
    "validate_render_tree",
    "validate_report_model",
    "validate_search_result",
]
