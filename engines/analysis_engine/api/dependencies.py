"""FastAPI dependency providers."""

from __future__ import annotations

from functools import lru_cache

from engines.analysis_engine.api.services.analysis_service import AnalysisService
from engines.analysis_engine.api.services.chart_service import ChartService
from engines.analysis_engine.api.services.interpretation_service import (
    InterpretationService,
)
from engines.analysis_engine.api.services.report_service import ReportService
from engines.analysis_engine.api.services.store import ResourceStore, get_store


@lru_cache(maxsize=1)
def get_resource_store() -> ResourceStore:
    """Process-wide resource store."""
    return get_store()


def get_chart_service() -> ChartService:
    """Chart service provider."""
    return ChartService(get_resource_store())


def get_analysis_service() -> AnalysisService:
    """Analysis service provider."""
    return AnalysisService(get_resource_store())


def get_interpretation_service() -> InterpretationService:
    """Interpretation service provider."""
    return InterpretationService(get_resource_store())


def get_report_service() -> ReportService:
    """Report service provider."""
    return ReportService(get_resource_store())
