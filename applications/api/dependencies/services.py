"""Service dependency providers for the public API layer."""

from __future__ import annotations

from applications.api.adapters.analysis_adapter import AnalysisAdapter
from applications.api.adapters.interpretation_adapter import InterpretationAdapter
from applications.api.adapters.report_adapter import ReportAdapter
from applications.api.services.analysis_service import (
    AnalysisService,
    DefaultAnalysisService,
)
from applications.api.services.interpretation_service import (
    DefaultInterpretationService,
    InterpretationService,
)
from applications.api.services.report_service import DefaultReportService, ReportService


def get_analysis_service() -> AnalysisService:
    """Provide an AnalysisService wired to AnalysisAdapter."""
    return DefaultAnalysisService(adapter=AnalysisAdapter())


def get_interpretation_service() -> InterpretationService:
    """Provide an InterpretationService wired to InterpretationAdapter."""
    return DefaultInterpretationService(adapter=InterpretationAdapter())


def get_report_service() -> ReportService:
    """Provide a ReportService wired to ReportAdapter."""
    return DefaultReportService(adapter=ReportAdapter())
