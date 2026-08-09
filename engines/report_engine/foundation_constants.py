"""Deterministic constants for the Report Foundation (RE-1)."""

from __future__ import annotations

ENGINE_ID = "report_engine"
REPORT_VERSION = "1.0.0"
REPORT_CONTRACT_ID = "bte.report.foundation.v1"
REQUIRED_SCHEMA_VERSION = "2.0.0"
FOUNDATION_VERSION = "1.0.0"

REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_LUCK_PIPELINE_VERSION = "1.0.0"
REQUIRED_INTERPRETATION_PIPELINE_VERSION = "1.0.0"

MODULE_COVER = "cover"
MODULE_OVERVIEW = "overview"
MODULE_CHART = "chart"
MODULE_ANALYSIS = "analysis"
MODULE_DECISION = "decision"
MODULE_LUCK = "luck"
MODULE_INTERPRETATION = "interpretation"
MODULE_APPENDIX = "appendix"
MODULE_SUMMARY = "summary"

CANONICAL_MODULE_ORDER: tuple[str, ...] = (
    MODULE_COVER,
    MODULE_OVERVIEW,
    MODULE_CHART,
    MODULE_ANALYSIS,
    MODULE_DECISION,
    MODULE_LUCK,
    MODULE_INTERPRETATION,
    MODULE_APPENDIX,
    MODULE_SUMMARY,
)

MODULE_STATUS_REGISTERED = "registered"
MODULE_STATUS_UNIMPLEMENTED = "unimplemented"

CONTEXT_STATUS_READY = "ready"
RESULT_STATUS_EMPTY = "empty"
PLACEHOLDER_STATUS_UNBOUND = "unbound"

PUBLISHED_CONTEXT_INPUTS: tuple[str, ...] = (
    "canonical_analysis_result",
    "canonical_decision_result",
    "canonical_luck_result",
    "canonical_interpretation_result",
)

PUBLISHED_CONTRACTS: tuple[str, ...] = (
    "ReportContext",
    "ReportDocument",
    "ReportSection",
    "ReportBlock",
    "ReportMetadata",
    "ReportAsset",
    "CanonicalReportResult",
)

PUBLISHED_MODELS: tuple[str, ...] = (
    "DocumentModel",
    "SectionModel",
    "BlockModel",
    "AssetModel",
    "PlaceholderModel",
    "MetadataModel",
    "ResultModel",
)

FORBIDDEN_RENDER_FIELDS: tuple[str, ...] = (
    "pdf",
    "docx",
    "html",
    "markdown",
    "css",
    "stylesheet",
    "rendered_html",
    "export_bytes",
    "binary_content",
    "narrative",
    "sentence",
    "report_text",
    "consultant_copy",
    "template_body",
    "generated_text",
    "layout_css",
    "page_style",
)
