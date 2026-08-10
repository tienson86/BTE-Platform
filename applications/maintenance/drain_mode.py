"""Drain mode contract. No connection draining implementation."""

from __future__ import annotations

from applications.maintenance.maintenance_contract import MaintenanceState

DRAIN_STATE = MaintenanceState(
    mode="drain",
    accepts_traffic=False,
    accepts_writes=False,
    draining=True,
    message="Stop new traffic. Finish in-flight requests, then shut down.",
)


def describe_drain_mode() -> MaintenanceState:
    """Return the drain-mode contract."""
    return DRAIN_STATE
