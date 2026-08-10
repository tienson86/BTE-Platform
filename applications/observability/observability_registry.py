"""Registry of observability contracts. No tracer SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from applications.observability.trace_contract import (
    CORRELATION_ID_HEADER,
    OPERATION_ID_FIELD,
    PIPELINE_ID_FIELD,
    REQUEST_ID_HEADER,
    TRACE_ID_HEADER,
)

OBSERVABILITY_FIELDS: Final[tuple[str, ...]] = (
    REQUEST_ID_HEADER,
    CORRELATION_ID_HEADER,
    TRACE_ID_HEADER,
    OPERATION_ID_FIELD,
    PIPELINE_ID_FIELD,
)


@dataclass(slots=True, frozen=True)
class ObservabilityField:
    """One observability identifier and its Beta-3 status."""

    name: str
    required: bool
    status: str
    description: str


FIELD_CATALOG: Final[tuple[ObservabilityField, ...]] = (
    ObservabilityField(REQUEST_ID_HEADER, True, "active", "Per-request identifier"),
    ObservabilityField(CORRELATION_ID_HEADER, False, "active", "Cross-service correlation"),
    ObservabilityField(TRACE_ID_HEADER, False, "reserved", "Distributed trace id"),
    ObservabilityField(OPERATION_ID_FIELD, False, "active", "Service operation name"),
    ObservabilityField(PIPELINE_ID_FIELD, False, "active", "Canonical pipeline name"),
)


class ObservabilityRegistry:
    """Catalog of observability identifiers."""

    def fields(self) -> tuple[ObservabilityField, ...]:
        """Return all observability field contracts."""
        return FIELD_CATALOG

    def reserved_fields(self) -> tuple[ObservabilityField, ...]:
        """Return fields that must not be implemented as a tracer yet."""
        return tuple(item for item in FIELD_CATALOG if item.status == "reserved")

    def describe(self) -> dict[str, object]:
        """Return a JSON-safe observability summary."""
        return {
            "distributed_tracing": False,
            "fields": [
                {
                    "name": item.name,
                    "required": item.required,
                    "status": item.status,
                    "description": item.description,
                }
                for item in FIELD_CATALOG
            ],
        }
