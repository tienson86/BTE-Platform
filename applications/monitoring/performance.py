"""Performance helpers derived from metrics."""

from __future__ import annotations

from typing import Any

from applications.monitoring.metrics import MetricsCollector, get_metrics


def performance_summary(
    collector: MetricsCollector | None = None,
) -> dict[str, Any]:
    """Summarize latency and error rate."""
    snap = (collector or get_metrics()).snapshot()
    requests = snap["request_count"]
    errors = snap["error_count"]
    return {
        "average_response_ms": snap["average_response_ms"],
        "error_rate": round(errors / requests, 4) if requests else 0.0,
        "uptime_seconds": snap["uptime_seconds"],
    }
