"""Map HTTP traffic to audit event types."""

from __future__ import annotations

from applications.audit.audit_log import AuditLog, get_audit_log


class ActivityLogger:
    """Derive audit events from request metadata."""

    def __init__(self, audit_log: AuditLog | None = None) -> None:
        self.audit_log = audit_log or get_audit_log()

    def record_from_request(
        self,
        *,
        method: str,
        path: str,
        status_code: int,
        user_id: str | None = None,
        username: str | None = None,
    ) -> None:
        """Record an audit event when the path matches a known activity."""
        event_type = self._classify(method, path)
        if event_type is None:
            return
        # Only successful mutating/auth flows (and exports) are audited.
        if status_code >= 400 and event_type not in {"login", "logout"}:
            return
        if event_type == "login" and status_code >= 400:
            self.audit_log.create(
                "login_failed",
                actor_username=username,
                resource=path,
                status_code=status_code,
            )
            return
        self.audit_log.create(
            event_type,
            actor_id=user_id,
            actor_username=username,
            resource=path,
            status_code=status_code,
        )

    @staticmethod
    def _classify(method: str, path: str) -> str | None:
        method = method.upper()
        if method == "POST" and path.endswith("/analyze"):
            return "analyze"
        if method == "GET" and "/export" in path and path.startswith("/api/v1/cases"):
            return "export"
        if method == "POST" and path == "/api/v1/auth/login":
            return "login"
        if method == "POST" and path == "/api/v1/auth/logout":
            return "logout"
        if method == "POST" and path == "/api/v1/customers":
            return "create_customer"
        if method == "PUT" and path.startswith("/api/v1/customers/"):
            return "update_customer"
        if method == "DELETE" and path.startswith("/api/v1/customers/"):
            return "delete_customer"
        if method == "POST" and path == "/api/v1/analyze":
            return "analyze"
        return None


_LOGGER = ActivityLogger()


def get_activity_logger() -> ActivityLogger:
    """Process-wide activity logger."""
    return _LOGGER
