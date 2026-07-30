"""Registry statistics aggregation."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from services.registry_constants import ALLOWED_STATUSES
from services.registry_loader import RegistryLoader
from services.registry_models import StatisticsSnapshot

logger = logging.getLogger(__name__)


class RegistryStatistics:
    """Compute aggregate statistics across registry catalogs."""

    def __init__(self, loader: RegistryLoader) -> None:
        """Initialize statistics service."""
        self.loader = loader

    def compute(self) -> StatisticsSnapshot:
        """Compute current statistics from loaded catalogs."""
        by_registry: dict[str, int] = {}
        by_status: dict[str, int] = {status: 0 for status in sorted(ALLOWED_STATUSES)}
        by_namespace: dict[str, int] = {}
        total = 0

        for catalog in self.loader.load_all_catalogs():
            by_registry.setdefault(catalog.name, 0)
            for record in catalog.records:
                total += 1
                by_registry[catalog.name] += 1
                identity = record.get("identity", {})
                metadata = record.get("metadata", {})
                namespace = (
                    str(identity.get("namespace", ""))
                    if isinstance(identity, dict)
                    else ""
                )
                status = (
                    str(metadata.get("status", ""))
                    if isinstance(metadata, dict)
                    else ""
                )
                if namespace:
                    by_namespace[namespace] = by_namespace.get(namespace, 0) + 1
                if status:
                    by_status[status] = by_status.get(status, 0) + 1

        snapshot = StatisticsSnapshot(
            total_records=total,
            by_registry=by_registry,
            by_status=by_status,
            by_namespace=by_namespace,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
        logger.debug("Computed registry statistics: %s records", total)
        return snapshot

    def to_dict(self, snapshot: StatisticsSnapshot | None = None) -> dict[str, Any]:
        """Serialize a statistics snapshot to the on-disk JSON shape."""
        snap = snapshot or self.compute()
        return {
            "version": "1.0.0",
            "generated_at": snap.generated_at,
            "description": (
                "Aggregate statistics across all Registry domains."
            ),
            "statistics": {
                "total_records": snap.total_records,
                "by_registry": snap.by_registry,
                "by_status": snap.by_status,
                "by_namespace": snap.by_namespace,
            },
        }
