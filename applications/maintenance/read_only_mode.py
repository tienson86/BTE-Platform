"""Read-only mode contract. No write blocking implementation."""

from __future__ import annotations

from applications.maintenance.maintenance_contract import MaintenanceState

READ_ONLY_STATE = MaintenanceState(
    mode="read_only",
    accepts_traffic=True,
    accepts_writes=False,
    draining=False,
    message="Reads allowed. Analysis POST and mutating admin actions must be rejected by a future gate.",
)


def describe_read_only_mode() -> MaintenanceState:
    """Return the read-only mode contract."""
    return READ_ONLY_STATE
