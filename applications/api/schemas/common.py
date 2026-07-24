"""Shared request / response envelopes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BirthRequest(BaseModel):
    """Birth datetime payload shared by engine endpoints."""

    year: int = Field(..., ge=1, le=9999, examples=[1990])
    month: int = Field(..., ge=1, le=12, examples=[5])
    day: int = Field(..., ge=1, le=31, examples=[15])
    hour: int = Field(0, ge=0, le=23, examples=[10])
    minute: int = Field(0, ge=0, le=59, examples=[30])
    gender: str | None = Field(None, examples=["male"])
    timezone: str = Field("Asia/Ho_Chi_Minh", examples=["Asia/Ho_Chi_Minh"])


class APIResponse(BaseModel):
    """Standard JSON envelope."""

    success: bool = True
    message: str = "OK"
    data: dict[str, Any] = Field(default_factory=dict)
    request_id: str | None = None


# Backward-compatible aliases used by older WP8 clients / tests.
ReportRequest = BirthRequest
ReportResponse = APIResponse
