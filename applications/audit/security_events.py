"""Security-oriented audit event helpers."""

from __future__ import annotations

from typing import Any

from applications.audit.audit_log import AuditLog, get_audit_log

_SECURITY_TYPES = frozenset(
    {
        "login",
        "login_failed",
        "logout",
    }
)


def list_security_events(
    audit_log: AuditLog | None = None,
    *,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Return recent security-related audit events."""
    log = audit_log or get_audit_log()
    events = log.list(limit=max(limit * 3, limit))
    return [e for e in events if e.get("event_type") in _SECURITY_TYPES][:limit]
