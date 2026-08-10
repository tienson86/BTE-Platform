"""Canonical public error contract models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetails(BaseModel):
    """Safe, non-sensitive error detail payload."""

    model_config = ConfigDict(extra="forbid")

    field: str | None = Field(default=None, description="Related request field.")
    reason: str | None = Field(default=None, description="Machine-safe reason.")
    context: list[str] = Field(default_factory=list, description="Additional safe context.")
    extra: dict[str, Any] | None = Field(
        default=None,
        description="Optional structured details. Must not include secrets or traces.",
    )


class CanonicalError(BaseModel):
    """Public error body. Never includes stack traces or filesystem paths."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(..., description="Stable machine-readable error code.")
    message: str = Field(..., description="Safe human-readable message.")
    details: ErrorDetails | None = Field(default=None, description="Optional safe details.")
    request_id: str = Field(..., description="Request identifier for support correlation.")
    timestamp: datetime = Field(..., description="UTC timestamp when the error was produced.")
