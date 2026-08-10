"""Correlation context for logs and incidents. Pass-through only."""

from __future__ import annotations

from dataclasses import dataclass

from applications.observability.trace_contract import TraceIdentifiers


@dataclass(slots=True)
class CorrelationContext:
    """Links Request-ID, Correlation-ID, Operation-ID, and Pipeline-ID."""

    identifiers: TraceIdentifiers
    actor: str | None = None
    tenant: str | None = None

    def log_fields(self) -> dict[str, str]:
        """Return safe fields for structured logs. Omits empty values."""
        payload: dict[str, str] = {"request_id": self.identifiers.request_id}
        if self.identifiers.correlation_id:
            payload["correlation_id"] = self.identifiers.correlation_id
        if self.identifiers.operation_id:
            payload["operation_id"] = self.identifiers.operation_id
        if self.identifiers.pipeline_id:
            payload["pipeline_id"] = self.identifiers.pipeline_id
        if self.identifiers.trace_id:
            payload["trace_id"] = self.identifiers.trace_id
        if self.actor:
            payload["actor"] = self.actor
        return payload
