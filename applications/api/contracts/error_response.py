"""Canonical API error response contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetails(BaseModel):
    """Structured error details contract."""

    model_config = ConfigDict(extra="forbid")

    field: str | None = Field(default=None, description="Related field name.")
    reason: str | None = Field(default=None, description="Error reason.")
    context: list[str] = Field(default_factory=list, description="Additional context entries.")


class ApiError(BaseModel):
    """Structured API error payload."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")
    details: ErrorDetails | None = Field(
        default=None,
        description="Optional structured error details.",
    )
    request_id: str | None = Field(
        default=None,
        description="Correlation identifier for the failed request.",
    )
    timestamp: datetime = Field(
        ...,
        description="UTC timestamp when the error was produced.",
    )


class ErrorResponse(BaseModel):
    """Canonical API error response."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(
        ...,
        description="Always false for error responses.",
    )
    error: ApiError = Field(
        ...,
        description="Structured API error payload.",
    )
