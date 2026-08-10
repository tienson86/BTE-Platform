"""Combined metric catalog for the operational platform."""

from __future__ import annotations

from typing import Final

from applications.metrics.metric_contract import MetricDefinition
from applications.metrics.pipeline_metrics import PIPELINE_METRICS
from applications.metrics.service_metrics import SERVICE_METRICS
from applications.metrics.system_metrics import SYSTEM_METRICS

METRIC_CATALOG: Final[tuple[MetricDefinition, ...]] = (
    SERVICE_METRICS + PIPELINE_METRICS + SYSTEM_METRICS
)

REQUIRED_METRIC_NAMES: Final[tuple[str, ...]] = (
    "request_count",
    "request_latency",
    "error_rate",
    "availability",
    "analysis_duration",
    "decision_duration",
    "luck_duration",
    "interpretation_duration",
    "report_duration",
    "cpu",
    "memory",
    "disk",
    "network",
)


def all_metric_names() -> tuple[str, ...]:
    """Return catalogued metric names in stable order."""
    return tuple(item.name for item in METRIC_CATALOG)


def is_catalog_complete() -> bool:
    """Return True when every required Beta-3 metric is catalogued."""
    return set(REQUIRED_METRIC_NAMES).issubset(set(all_metric_names()))
