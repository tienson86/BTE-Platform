"""RE-2 Layout & Theme Composition Engine."""

from engines.report_engine.layout.layout_context import (
    LAYOUT_VERSION,
    LayoutContext,
    build_layout_context,
)
from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.layout.layout_registry import LayoutRegistry
from engines.report_engine.layout.layout_result import CanonicalReportLayout, LayoutAudit, LayoutTrace

__all__ = [
    "LAYOUT_VERSION",
    "CanonicalReportLayout",
    "LayoutAudit",
    "LayoutContext",
    "LayoutRegistry",
    "LayoutTrace",
    "ReportLayoutEngine",
    "build_layout_context",
]
