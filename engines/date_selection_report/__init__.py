"""PACK 06 Date Selection report foundation (P6-01).

Public surface: models, adapter, validation. No rendering or export.
"""

from engines.date_selection_report.adapter import DateSelectionReportAdapter
from engines.date_selection_report.contracts import (
    CanonicalSearchResult,
    REPORT_FOUNDATION_CONTRACT,
)
from engines.date_selection_report.exceptions import (
    DateSelectionReportError,
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
from engines.date_selection_report.validators import (
    validate_report_model,
    validate_search_result,
)

__all__ = [
    "CanonicalSearchResult",
    "CompatibleHourReportData",
    "DateSelectionReportAdapter",
    "DateSelectionReportError",
    "DateSelectionReportModel",
    "DateSelectionReportValidationError",
    "GuidanceItem",
    "GuidanceReportData",
    "Metadata",
    "PersonReportData",
    "PositiveKeReportData",
    "Provenance",
    "ProvenanceData",
    "REPORT_FOUNDATION_CONTRACT",
    "RecommendedDateReportData",
    "SearchPeriodReportData",
    "validate_report_model",
    "validate_search_result",
]
