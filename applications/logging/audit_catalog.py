"""Audit event catalog. No audit emitter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

AuditSeverity = Literal["info", "notice", "warning"]


@dataclass(slots=True, frozen=True)
class AuditEventContract:
    """One auditable operational or security event type."""

    event_id: str
    description: str
    severity: AuditSeverity
    stream: str = "audit"


AUDIT_CATALOG: Final[tuple[AuditEventContract, ...]] = (
    AuditEventContract("auth.login_placeholder", "Auth attempt recorded (placeholder)", "info"),
    AuditEventContract("auth.api_key_reserved", "API key header present (reserved)", "info"),
    AuditEventContract("ops.maintenance_enter", "Maintenance mode announced", "notice"),
    AuditEventContract("ops.maintenance_exit", "Maintenance mode cleared", "notice"),
    AuditEventContract("ops.read_only_enter", "Read-only mode announced", "notice"),
    AuditEventContract("ops.drain_enter", "Drain mode announced", "notice"),
    AuditEventContract("ops.backup_run", "Backup job started or finished", "info"),
    AuditEventContract("ops.restore_run", "Restore procedure started", "warning"),
    AuditEventContract("ops.deploy", "Release deploy or rollback", "notice"),
    AuditEventContract("security.denied_reserved", "Authorization denial (reserved)", "warning"),
)
