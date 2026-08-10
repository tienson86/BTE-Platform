"""Maintenance mode contract. No 503 switch implementation."""

from __future__ import annotations

from applications.maintenance.maintenance_contract import MaintenanceState

MAINTENANCE_STATE = MaintenanceState(
    mode="maintenance",
    accepts_traffic=False,
    accepts_writes=False,
    draining=False,
    message="Platform is in a planned maintenance window. Edge should serve 503.",
)


def describe_maintenance_mode() -> MaintenanceState:
    """Return the maintenance-mode contract."""
    return MAINTENANCE_STATE
