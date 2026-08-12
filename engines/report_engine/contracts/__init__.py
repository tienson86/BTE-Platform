"""Report Foundation contracts (RE-1)."""

from engines.report_engine.contracts.report_contracts import (
    CanonicalReportResult,
    ReportAsset,
    ReportBlock,
    ReportContext,
    ReportDocument,
    ReportMetadata,
    ReportSection,
    empty_report_result,
    report_foundation_contract,
)
from engines.report_engine.contracts.report_export_result_v1 import (
    MEDIA_TYPE_DOCX,
    MEDIA_TYPE_PDF,
    ReportExportResultV1,
)
from engines.report_engine.contracts.report_input_v1 import (
    REPORT_INPUT_VERSION,
    ReportInputV1,
    missing_data_message,
)

__all__ = [
    "CanonicalReportResult",
    "REPORT_INPUT_VERSION",
    "ReportAsset",
    "ReportBlock",
    "ReportContext",
    "ReportDocument",
    "MEDIA_TYPE_DOCX",
    "MEDIA_TYPE_PDF",
    "ReportExportResultV1",
    "ReportInputV1",
    "ReportMetadata",
    "ReportSection",
    "empty_report_result",
    "missing_data_message",
    "report_foundation_contract",
]
