"""Request and response metadata contracts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RequestIdentifiers(BaseModel):
    """Pass-through request identifiers. No persistence in this layer."""

    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(..., description="Request-ID header or generated value.")
    correlation_id: str | None = Field(
        default=None,
        description="Correlation-ID header for distributed tracing.",
    )
    idempotency_key: str | None = Field(
        default=None,
        description="Idempotency-Key header. Pass-through only.",
    )


class ResponseMetadata(BaseModel):
    """Service-layer metadata. Must not contain engine objects."""

    model_config = ConfigDict(extra="forbid")

    service: str = Field(..., description="Public service name.")
    operation: str = Field(..., description="Service operation name.")
    pipeline: str | None = Field(
        default=None,
        description="Canonical pipeline name when a pipeline call is intended.",
    )
    identifiers: RequestIdentifiers = Field(..., description="Request identifiers.")
