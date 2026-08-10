"""Request-level trace contract. No exporter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from applications.observability.trace_contract import TraceIdentifiers


@dataclass(slots=True)
class RequestTrace:
    """One HTTP or service request as an observability record."""

    identifiers: TraceIdentifiers
    method: str
    path: str
    started_at: datetime
    service_id: str = "api"
    status_code: int | None = None

    @classmethod
    def start(
        cls,
        *,
        request_id: str,
        method: str,
        path: str,
        correlation_id: str | None = None,
        operation_id: str | None = None,
        pipeline_id: str | None = None,
        service_id: str = "api",
    ) -> RequestTrace:
        """Build a request trace record without emitting spans."""
        return cls(
            identifiers=TraceIdentifiers(
                request_id=request_id,
                correlation_id=correlation_id,
                trace_id=None,
                operation_id=operation_id,
                pipeline_id=pipeline_id,
            ),
            method=method,
            path=path,
            started_at=datetime.now(timezone.utc),
            service_id=service_id,
        )
