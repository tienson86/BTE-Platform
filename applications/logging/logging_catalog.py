"""Standard log stream catalog."""

from __future__ import annotations

from typing import Final

from applications.logging.logging_contract import LogStreamContract

LOGGING_CATALOG: Final[tuple[LogStreamContract, ...]] = (
    LogStreamContract(
        kind="application",
        name="Application Log",
        owner="api-owner",
        destination="bte-logs/app.log + stdout",
    ),
    LogStreamContract(
        kind="access",
        name="Access Log",
        owner="edge-owner",
        destination="nginx access.log",
    ),
    LogStreamContract(
        kind="error",
        name="Error Log",
        owner="api-owner",
        destination="nginx error.log + app stderr",
    ),
    LogStreamContract(
        kind="audit",
        name="Audit Log",
        owner="security-owner",
        destination="bte-logs/audit.log (logical stream)",
    ),
    LogStreamContract(
        kind="security",
        name="Security Log",
        owner="security-owner",
        destination="bte-logs/security.log (logical stream)",
    ),
    LogStreamContract(
        kind="operational",
        name="Operational Log",
        owner="platform-ops",
        destination="bte-logs/ops.log + compose events",
    ),
)

REQUIRED_LOG_KINDS: Final[tuple[str, ...]] = (
    "application",
    "access",
    "error",
    "audit",
    "security",
    "operational",
)


def log_kinds() -> tuple[str, ...]:
    """Return catalogued log kinds."""
    return tuple(item.kind for item in LOGGING_CATALOG)
