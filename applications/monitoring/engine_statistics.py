"""Engine endpoint usage statistics (from request paths)."""

from __future__ import annotations

from typing import Any

from applications.monitoring.metrics import MetricsCollector, get_metrics

_ENGINE_PREFIXES = (
    "/api/v1/calendar",
    "/api/v1/bazi",
    "/api/v1/pattern",
    "/api/v1/score",
    "/api/v1/interpretation",
    "/api/v1/report",
    "/api/v1/narrative",
    "/api/v1/analyze",
)


def engine_statistics(
    collector: MetricsCollector | None = None,
) -> dict[str, Any]:
    """Count hits to engine orchestration endpoints."""
    snap = (collector or get_metrics()).snapshot()
    usage = snap["endpoint_usage"]
    by_engine: dict[str, int] = {}
    for key, count in usage.items():
        path = key.split(" ", 1)[-1]
        for prefix in _ENGINE_PREFIXES:
            if path == prefix or path.startswith(prefix + "/"):
                name = prefix.rsplit("/", 1)[-1]
                by_engine[name] = by_engine.get(name, 0) + int(count)
                break
    return {
        "engine_endpoint_hits": by_engine,
        "total_engine_hits": sum(by_engine.values()),
    }
