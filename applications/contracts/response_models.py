"""Canonical public success response models.

Every success response contains status, data, metadata, request_id,
timestamp, and api_version. Engine objects are never exposed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from applications.contracts.metadata_models import RequestIdentifiers, ResponseMetadata
from applications.versioning.api_versions import CURRENT_API_VERSION


class PublicSuccessResponse(BaseModel):
    """Standard public success envelope."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["success"] = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    metadata: ResponseMetadata
    request_id: str
    timestamp: datetime
    api_version: str = CURRENT_API_VERSION


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def build_success_response(
    *,
    data: dict[str, Any],
    service: str,
    operation: str,
    request_id: str,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    pipeline: str | None = None,
    api_version: str = CURRENT_API_VERSION,
    timestamp: datetime | None = None,
) -> PublicSuccessResponse:
    """Build a consistent public success envelope."""
    stamp = timestamp or utc_now()
    identifiers = RequestIdentifiers(
        request_id=request_id,
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
    )
    return PublicSuccessResponse(
        data=data,
        metadata=ResponseMetadata(
            service=service,
            operation=operation,
            pipeline=pipeline,
            identifiers=identifiers,
        ),
        request_id=request_id,
        timestamp=stamp,
        api_version=api_version,
    )
