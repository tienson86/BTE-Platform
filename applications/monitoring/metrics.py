"""In-memory metrics collector for operations monitoring."""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricsCollector:
    """Thread-safe process metrics (no Prometheus)."""

    started_at: float = field(default_factory=time.time)
    request_count: int = 0
    error_count: int = 0
    total_response_ms: float = 0.0
    endpoint_counts: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    active_users: set[str] = field(default_factory=set)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record_request(
        self,
        *,
        method: str,
        path: str,
        status_code: int,
        elapsed_ms: float,
        user_id: str | None = None,
    ) -> None:
        """Record one HTTP request sample."""
        key = f"{method} {path}"
        with self._lock:
            self.request_count += 1
            self.total_response_ms += max(elapsed_ms, 0.0)
            self.endpoint_counts[key] += 1
            if status_code >= 400:
                self.error_count += 1
            if user_id:
                self.active_users.add(user_id)

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-friendly metrics snapshot."""
        with self._lock:
            avg = (
                self.total_response_ms / self.request_count
                if self.request_count
                else 0.0
            )
            endpoints = dict(
                sorted(
                    self.endpoint_counts.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )[:50]
            )
            return {
                "request_count": self.request_count,
                "error_count": self.error_count,
                "average_response_ms": round(avg, 2),
                "endpoint_usage": endpoints,
                "active_users": len(self.active_users),
                "uptime_seconds": round(time.time() - self.started_at, 2),
            }

    def reset(self) -> None:
        """Clear counters (tests)."""
        with self._lock:
            self.request_count = 0
            self.error_count = 0
            self.total_response_ms = 0.0
            self.endpoint_counts.clear()
            self.active_users.clear()
            self.started_at = time.time()


_METRICS = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Return the process-wide metrics collector."""
    return _METRICS
