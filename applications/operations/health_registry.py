"""Operational health registry.

Defines Service, Pipeline, Dependency, and Overall health contracts.
Does not add HTTP endpoints and does not execute probes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

from applications.operations.operations_status import (
    ComponentStatus,
    HealthLevel,
    OperationsStatus,
)
from applications.operations.service_catalog import SERVICE_CATALOG

HealthDomain = Literal["service", "pipeline", "dependency", "overall"]


@dataclass(slots=True, frozen=True)
class HealthCheckContract:
    """Named health concern. No probe implementation."""

    check_id: str
    domain: HealthDomain
    description: str
    default_level: HealthLevel = "unknown"


SERVICE_HEALTH_CHECKS: Final[tuple[HealthCheckContract, ...]] = tuple(
    HealthCheckContract(
        check_id=f"service.{item.service_id}",
        domain="service",
        description=f"{item.display_name} process/probe ({item.health_probe})",
        default_level="unknown" if item.reserved else "healthy",
    )
    for item in SERVICE_CATALOG
)

PIPELINE_HEALTH_CHECKS: Final[tuple[HealthCheckContract, ...]] = (
    HealthCheckContract("pipeline.analysis", "pipeline", "Canonical analysis pipeline binding"),
    HealthCheckContract("pipeline.decision", "pipeline", "Canonical decision pipeline binding"),
    HealthCheckContract("pipeline.luck", "pipeline", "Canonical luck pipeline binding"),
    HealthCheckContract("pipeline.interpretation", "pipeline", "Canonical interpretation pipeline binding"),
    HealthCheckContract("pipeline.report", "pipeline", "Canonical report pipeline binding"),
)

DEPENDENCY_HEALTH_CHECKS: Final[tuple[HealthCheckContract, ...]] = (
    HealthCheckContract("dependency.storage", "dependency", "Application storage backend"),
    HealthCheckContract("dependency.filesystem", "dependency", "Log, report, and backup volumes"),
    HealthCheckContract("dependency.secrets", "dependency", "Runtime secret/env availability"),
)

OVERALL_HEALTH_CHECK: Final[HealthCheckContract] = HealthCheckContract(
    check_id="overall.platform",
    domain="overall",
    description="Aggregate of critical services, pipelines, and dependencies",
)

ALL_HEALTH_CHECKS: Final[tuple[HealthCheckContract, ...]] = (
    SERVICE_HEALTH_CHECKS
    + PIPELINE_HEALTH_CHECKS
    + DEPENDENCY_HEALTH_CHECKS
    + (OVERALL_HEALTH_CHECK,)
)


class HealthRegistry:
    """In-memory catalog of operational health contracts."""

    def __init__(self, checks: tuple[HealthCheckContract, ...] = ALL_HEALTH_CHECKS) -> None:
        self._checks = {item.check_id: item for item in checks}

    def get(self, check_id: str) -> HealthCheckContract | None:
        """Return one health contract."""
        return self._checks.get(check_id)

    def by_domain(self, domain: HealthDomain) -> tuple[HealthCheckContract, ...]:
        """Return contracts for a health domain."""
        return tuple(item for item in self._checks.values() if item.domain == domain)

    def snapshot(self) -> OperationsStatus:
        """Return a contract snapshot. Does not probe live systems."""
        components = tuple(
            ComponentStatus(
                name=item.check_id,
                level=item.default_level,
                kind="service"
                if item.domain == "service"
                else "pipeline"
                if item.domain == "pipeline"
                else "dependency",
                detail=item.description,
            )
            for item in self._checks.values()
            if item.domain != "overall"
        )
        return OperationsStatus(overall="unknown", components=components)

    def check_ids(self) -> tuple[str, ...]:
        """Return registered health check identifiers."""
        return tuple(self._checks.keys())
