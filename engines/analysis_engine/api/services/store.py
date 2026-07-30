"""In-memory resource store for Analysis Engine API."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from engines.analysis_engine.api.exceptions import NotFoundError


def new_id(prefix: str) -> str:
    """Allocate a prefixed resource id."""
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(slots=True)
class ChartRecord:
    """Stored natal chart snapshot."""

    chart_id: str
    chart: dict[str, Any]
    calendar: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisRecord:
    """Stored AnalysisResult serialization + chart link."""

    analysis_id: str
    chart_id: str
    request_id: str
    payload: dict[str, Any]
    stage_payloads: dict[str, dict[str, Any]]


@dataclass(slots=True)
class InterpretationRecord:
    """Stored InterpretationResult serialization."""

    interpretation_id: str
    analysis_id: str
    chart_id: str
    request_id: str
    payload: dict[str, Any]


@dataclass(slots=True)
class ReportRecord:
    """Stored ReportGeneratorResult serialization."""

    report_id: str
    interpretation_id: str
    analysis_id: str
    chart_id: str
    request_id: str
    payload: dict[str, Any]


class ResourceStore:
    """Thread-safe in-memory store (stateless engine, request-scoped resources)."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.charts: dict[str, ChartRecord] = {}
        self.analyses: dict[str, AnalysisRecord] = {}
        self.interpretations: dict[str, InterpretationRecord] = {}
        self.reports: dict[str, ReportRecord] = {}

    def put_chart(self, record: ChartRecord) -> ChartRecord:
        with self._lock:
            self.charts[record.chart_id] = record
            return record

    def get_chart(self, chart_id: str) -> ChartRecord:
        with self._lock:
            record = self.charts.get(chart_id)
            if record is None:
                raise NotFoundError(
                    f"Chart not found: {chart_id}",
                    details={"chart_id": chart_id},
                )
            return record

    def put_analysis(self, record: AnalysisRecord) -> AnalysisRecord:
        with self._lock:
            self.analyses[record.analysis_id] = record
            return record

    def get_analysis(self, analysis_id: str) -> AnalysisRecord:
        with self._lock:
            record = self.analyses.get(analysis_id)
            if record is None:
                raise NotFoundError(
                    f"Analysis not found: {analysis_id}",
                    details={"analysis_id": analysis_id},
                )
            return record

    def put_interpretation(self, record: InterpretationRecord) -> InterpretationRecord:
        with self._lock:
            self.interpretations[record.interpretation_id] = record
            return record

    def get_interpretation(self, interpretation_id: str) -> InterpretationRecord:
        with self._lock:
            record = self.interpretations.get(interpretation_id)
            if record is None:
                raise NotFoundError(
                    f"Interpretation not found: {interpretation_id}",
                    details={"interpretation_id": interpretation_id},
                )
            return record

    def put_report(self, record: ReportRecord) -> ReportRecord:
        with self._lock:
            self.reports[record.report_id] = record
            return record

    def get_report(self, report_id: str) -> ReportRecord:
        with self._lock:
            record = self.reports.get(report_id)
            if record is None:
                raise NotFoundError(
                    f"Report not found: {report_id}",
                    details={"report_id": report_id},
                )
            return record

    def clear(self) -> None:
        """Clear all resources (tests)."""
        with self._lock:
            self.charts.clear()
            self.analyses.clear()
            self.interpretations.clear()
            self.reports.clear()


_STORE = ResourceStore()


def get_store() -> ResourceStore:
    """Return process-wide resource store."""
    return _STORE
