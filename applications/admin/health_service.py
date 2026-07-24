"""Admin health checks for storage / repository / api / config."""

from __future__ import annotations

from typing import Any

from applications.storage.factory import RepositoryFactory, StorageConfig


class HealthService:
    """Operational health probes (no Prometheus)."""

    def __init__(self, storage_config: StorageConfig | None = None) -> None:
        self.storage_config = storage_config or StorageConfig.from_env()

    def check(self) -> dict[str, Any]:
        """Run health checks and return overall status."""
        from applications.api.config import settings

        checks: dict[str, Any] = {}
        overall = "ok"

        # config
        try:
            _ = settings.app_version
            checks["config"] = {"status": "ok"}
        except Exception as exc:
            checks["config"] = {"status": "error", "detail": str(exc)}
            overall = "degraded"

        # storage + repository
        try:
            bundle = RepositoryFactory.create(self.storage_config)
            _ = bundle.customers.list()
            _ = bundle.cases.list()
            checks["storage"] = {
                "status": "ok",
                "backend": bundle.backend,
            }
            checks["repository"] = {"status": "ok"}
        except Exception as exc:
            checks["storage"] = {"status": "error", "detail": str(exc)}
            checks["repository"] = {"status": "error", "detail": str(exc)}
            overall = "error"

        checks["api"] = {"status": "ok"}
        return {"status": overall, "checks": checks}
