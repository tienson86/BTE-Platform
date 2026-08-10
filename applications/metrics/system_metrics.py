"""Host and container system metrics. No collectors."""

from __future__ import annotations

from typing import Final

from applications.metrics.metric_contract import MetricDefinition

SYSTEM_METRICS: Final[tuple[MetricDefinition, ...]] = (
    MetricDefinition(
        name="cpu",
        domain="system",
        kind="gauge",
        unit="percent",
        description="CPU utilization of the service container or node.",
    ),
    MetricDefinition(
        name="memory",
        domain="system",
        kind="gauge",
        unit="bytes",
        description="Resident memory used by the service.",
    ),
    MetricDefinition(
        name="disk",
        domain="system",
        kind="gauge",
        unit="bytes",
        description="Disk used on log, data, and backup volumes.",
    ),
    MetricDefinition(
        name="network",
        domain="system",
        kind="gauge",
        unit="bytes",
        description="Network bytes in/out (catalog placeholder).",
    ),
)
