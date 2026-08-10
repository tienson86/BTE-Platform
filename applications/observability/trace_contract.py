"""Observability identifier contract.

No distributed tracing implementation. Field definitions only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

REQUEST_ID_HEADER: Final[str] = "Request-ID"
CORRELATION_ID_HEADER: Final[str] = "Correlation-ID"
TRACE_ID_HEADER: Final[str] = "Trace-ID"
OPERATION_ID_FIELD: Final[str] = "operation_id"
PIPELINE_ID_FIELD: Final[str] = "pipeline_id"


@dataclass(slots=True, frozen=True)
class TraceIdentifiers:
    """Pass-through observability identifiers."""

    request_id: str
    correlation_id: str | None = None
    trace_id: str | None = None
    operation_id: str | None = None
    pipeline_id: str | None = None

    def reserved_trace_enabled(self) -> bool:
        """Trace-ID is reserved. Always False in Beta-3."""
        return False
