"""API statistics derived from monitoring metrics."""

from __future__ import annotations

from typing import Any

from applications.monitoring.metrics import MetricsCollector, get_metrics
from applications.monitoring.request_statistics import request_statistics


def api_statistics(collector: MetricsCollector | None = None) -> dict[str, Any]:
    """API request / error / endpoint stats."""
    return request_statistics(collector or get_metrics())
