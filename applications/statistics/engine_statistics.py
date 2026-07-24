"""Engine usage statistics (alias of monitoring engine stats)."""

from __future__ import annotations

from typing import Any

from applications.monitoring.engine_statistics import engine_statistics as _engine_stats
from applications.monitoring.metrics import MetricsCollector, get_metrics


def engine_statistics(collector: MetricsCollector | None = None) -> dict[str, Any]:
    """Engine endpoint hit statistics."""
    return _engine_stats(collector or get_metrics())
