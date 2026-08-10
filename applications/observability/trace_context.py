"""Trace context placeholder.

Distributed tracing (W3C / OpenTelemetry) is reserved. This module
defines the field layout only and never starts a tracer.
"""

from __future__ import annotations

from dataclasses import dataclass

from applications.observability.trace_contract import TraceIdentifiers

TRACE_PARENT_HEADER = "traceparent"
TRACE_STATE_HEADER = "tracestate"


@dataclass(slots=True, frozen=True)
class TraceContext:
    """Reserved W3C-style trace context. Not propagated in Beta-3."""

    identifiers: TraceIdentifiers
    traceparent: str | None = None
    tracestate: str | None = None
    implemented: bool = False

    @classmethod
    def reserved(cls, request_id: str) -> TraceContext:
        """Return an unimplemented trace context bound to Request-ID."""
        return cls(
            identifiers=TraceIdentifiers(request_id=request_id, trace_id=None),
            implemented=False,
        )
