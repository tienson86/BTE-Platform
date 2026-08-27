"""PACK 06 Date Selection report foundation and presentation (P6-01 / P6-02).

Public surface: models, adapter, validation, render tree. No PDF/DOCX export.
"""

from engines.date_selection_report.adapter import DateSelectionReportAdapter
from engines.date_selection_report.contracts import (
    CanonicalSearchResult,
    RENDER_CONTRACT,
    REPORT_FOUNDATION_CONTRACT,
)
from engines.date_selection_report.exceptions import (
    DateSelectionReportError,
    DateSelectionReportTemplateError,
    DateSelectionReportValidationError,
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
    "DateSelectionReportError",
    "DateSelectionReportModel",
    "DateSelectionReportTemplateError",
    "DateSelectionReportValidationError",
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
    "build_render_tree",
    "create_render_context",
    "load_date_selection_template_package",
    "validate_render_tree",
    "validate_report_model",
    "validate_search_result",
]
