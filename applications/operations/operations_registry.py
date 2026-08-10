"""Composition root for the operational platform contracts."""

from __future__ import annotations

from dataclasses import dataclass

from applications.operations.health_registry import HealthRegistry
from applications.operations.operations_context import OperationsContext
from applications.operations.service_catalog import SERVICE_CATALOG, CatalogService


@dataclass(slots=True)
class OperationsRegistry:
    """Registers operable services and health contracts. No control plane."""

    context: OperationsContext
    health: HealthRegistry
    services: tuple[CatalogService, ...] = SERVICE_CATALOG

    @classmethod
    def create_default(
        cls,
        context: OperationsContext | None = None,
    ) -> OperationsRegistry:
        """Create the default operational registry."""
        return cls(
            context=context
            or OperationsContext(environment="development", node_role="ops"),
            health=HealthRegistry(),
        )

    def service_ids(self) -> tuple[str, ...]:
        """Return catalogued service identifiers."""
        return tuple(item.service_id for item in self.services)

    def describe(self) -> dict[str, object]:
        """Return a JSON-safe registry summary."""
        return {
            "environment": self.context.environment,
            "node_role": self.context.node_role,
            "services": list(self.service_ids()),
            "health_checks": list(self.health.check_ids()),
            "maintenance": self.context.maintenance,
            "read_only": self.context.read_only,
            "draining": self.context.draining,
        }


def get_operations_registry() -> OperationsRegistry:
    """Return the default operational registry instance."""
    return OperationsRegistry.create_default()
