"""HTTP request statistics views."""

from __future__ import annotations

from typing import Any

from applications.monitoring.metrics import MetricsCollector, get_metrics


def request_statistics(
    collector: MetricsCollector | None = None,
) -> dict[str, Any]:
    """Request-level monitoring snapshot."""
    snap = (collector or get_metrics()).snapshot()
    return {
        "request_count": snap["request_count"],
        "average_response_time_ms": snap["average_response_ms"],
        "endpoint_usage": snap["endpoint_usage"],
        "error_count": snap["error_count"],
        "active_users": snap["active_users"],
    }
