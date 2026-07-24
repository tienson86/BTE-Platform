"""Admin dashboard aggregation service."""

from __future__ import annotations

from typing import Any

from applications.monitoring.metrics import MetricsCollector, get_metrics
from applications.statistics.case_statistics import case_statistics
from applications.statistics.customer_statistics import customer_statistics
from applications.storage.factory import RepositoryFactory, StorageConfig


class DashboardService:
    """Build admin dashboard payload."""

    def __init__(
        self,
        *,
        metrics: MetricsCollector | None = None,
        storage_config: StorageConfig | None = None,
    ) -> None:
        self.metrics = metrics or get_metrics()
        self.storage_config = storage_config or StorageConfig.from_env()

    def build(self) -> dict[str, Any]:
        """Return dashboard fields required by WP13."""
        from applications.api.config import settings

        bundle = RepositoryFactory.create(self.storage_config)
        cust = customer_statistics(bundle=bundle)
        cases = case_statistics(bundle=bundle)
        snap = self.metrics.snapshot()
        return {
            "customer_count": cust["customer_count"],
            "case_count": cases["case_count"],
            "request_count": snap["request_count"],
            "storage_backend": bundle.backend,
            "engine_version": settings.app_version,
            "uptime_seconds": snap["uptime_seconds"],
            "api_version": settings.app_version,
        }
