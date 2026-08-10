"""API / service metric catalog. No counters are emitted."""

from __future__ import annotations

from typing import Final

from applications.metrics.metric_contract import MetricDefinition

SERVICE_METRICS: Final[tuple[MetricDefinition, ...]] = (
    MetricDefinition(
        name="request_count",
        domain="api",
        kind="counter",
        unit="1",
        description="Count of HTTP requests received by the public API.",
    ),
    MetricDefinition(
        name="request_latency",
        domain="api",
        kind="histogram",
        unit="ms",
        description="End-to-end HTTP request latency.",
    ),
    MetricDefinition(
        name="error_rate",
        domain="api",
        kind="ratio",
        unit="1",
        description="Ratio of 5xx responses to total requests.",
    ),
    MetricDefinition(
        name="availability",
        domain="api",
        kind="gauge",
        unit="1",
        description="Successful health probes over the SLO window.",
    ),
)
