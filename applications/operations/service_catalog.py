"""Operational service catalog. Documentation of runtime roles only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

ServiceCriticality = Literal["critical", "high", "medium", "reserved"]


@dataclass(slots=True, frozen=True)
class CatalogService:
    """One operable service in the production topology."""

    service_id: str
    display_name: str
    role: str
    criticality: ServiceCriticality
    health_probe: str
    owner: str = "platform-ops"
    scalable: bool = False
    reserved: bool = False


API_SERVICE: Final[CatalogService] = CatalogService(
    service_id="api",
    display_name="BTE Applications API",
    role="public and internal HTTP API",
    criticality="critical",
    health_probe="/health",
    scalable=False,
)
PORTAL_SERVICE: Final[CatalogService] = CatalogService(
    service_id="portal",
    display_name="Customer Portal",
    role="product UI host",
    criticality="critical",
    health_probe="/healthz",
    scalable=True,
)
NGINX_SERVICE: Final[CatalogService] = CatalogService(
    service_id="nginx",
    display_name="Edge Proxy",
    role="TLS termination and routing",
    criticality="critical",
    health_probe="/health",
    scalable=False,
)
WORKER_SERVICE: Final[CatalogService] = CatalogService(
    service_id="worker",
    display_name="Background Worker",
    role="async jobs",
    criticality="reserved",
    health_probe="reserved",
    reserved=True,
)
BACKUP_SERVICE: Final[CatalogService] = CatalogService(
    service_id="backup",
    display_name="Backup Job",
    role="scheduled backup and verify",
    criticality="high",
    health_probe="ops-job",
)

SERVICE_CATALOG: Final[tuple[CatalogService, ...]] = (
    API_SERVICE,
    PORTAL_SERVICE,
    NGINX_SERVICE,
    WORKER_SERVICE,
    BACKUP_SERVICE,
)


def get_service(service_id: str) -> CatalogService | None:
    """Return a catalog service by id."""
    for item in SERVICE_CATALOG:
        if item.service_id == service_id:
            return item
    return None


def critical_services() -> tuple[CatalogService, ...]:
    """Return services that affect overall availability."""
    return tuple(item for item in SERVICE_CATALOG if item.criticality == "critical")
