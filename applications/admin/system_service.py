"""System information service."""

from __future__ import annotations

import platform
import sys
from typing import Any

from applications.monitoring.metrics import get_metrics
from applications.storage.factory import StorageConfig


class SystemService:
    """Runtime / platform system snapshot."""

    def build(self) -> dict[str, Any]:
        """Return system information for admins."""
        from applications.api.config import settings

        storage = StorageConfig.from_env()
        metrics = get_metrics().snapshot()
        return {
            "app_name": settings.app_name,
            "api_version": settings.app_version,
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "storage_backend": storage.backend,
            "data_dir": storage.data_dir,
            "uptime_seconds": metrics["uptime_seconds"],
        }
