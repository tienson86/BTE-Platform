"""Report V1 localization package — single mapping used by HTML/PDF/DOCX."""

from engines.report_engine.localization.customer_text import (
    customer_paragraphs,
    customer_text,
    is_rule_engine_sentence,
)
from engines.report_engine.localization.display import display_text, localize, unwrap_display_object
from engines.report_engine.localization.labels_vi import (
    EXECUTIVE_SUMMARY_MISSING,
    FULL_LUCK_CYCLES_GAP_NOTE,
    RUNTIME_GAP_MESSAGE,
)
from engines.report_engine.localization.shensha_audit import audit_shensha_duplicates

__all__ = [
    "EXECUTIVE_SUMMARY_MISSING",
    "FULL_LUCK_CYCLES_GAP_NOTE",
    "RUNTIME_GAP_MESSAGE",
    "audit_shensha_duplicates",
    "customer_paragraphs",
    "customer_text",
    "display_text",
    "is_rule_engine_sentence",
    "localize",
    "unwrap_display_object",
]
