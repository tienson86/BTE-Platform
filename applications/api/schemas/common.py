"""Shared request / response envelopes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BirthRequest(BaseModel):
    """Birth datetime payload shared by engine endpoints.

    Customer fields (``full_name``, ``birth_place``, ``customer_id``, ``metadata``)
    are presentation / profile metadata. They are echoed in API responses and are
    never passed into Calendar / Bazi / Pattern engines.
    """

    year: int = Field(..., ge=1, le=9999, examples=[1990])
    month: int = Field(..., ge=1, le=12, examples=[5])
    day: int = Field(..., ge=1, le=31, examples=[15])
    hour: int = Field(0, ge=0, le=23, examples=[10])
    minute: int = Field(0, ge=0, le=59, examples=[30])
    gender: str | None = Field(None, examples=["male"])
    timezone: str = Field("Asia/Ho_Chi_Minh", examples=["Asia/Ho_Chi_Minh"])
    full_name: str | None = Field(None, examples=["Nguyễn Văn A"])
    birth_place: str | None = Field(None, examples=["Hà Nội"])
    customer_id: str | None = Field(
        None,
        description="Optional link to a future Customer Profile record.",
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Opaque customer/chart metadata for presentation layers.",
    )


class DiscussionRequest(BirthRequest):
    """Additive Discussion / Knowledge Expert request (Epic 03 Milestone 10)."""

    question: str | None = Field(
        None,
        description="Single discussion question (Why/How/Evidence/...).",
        examples=["Why is Suitable Career favored?"],
    )
    questions: list[str] | None = Field(
        default=None,
        description="Optional multi-turn question list for converse mode.",
    )
    show_citations: bool = Field(
        False,
        description="When true, include visible bibliography in prompt grounding.",
    )


class APIResponse(BaseModel):
    """Standard JSON envelope."""

    success: bool = True
    message: str = "OK"
    data: dict[str, Any] = Field(default_factory=dict)
    request_id: str | None = None


# Backward-compatible aliases used by older WP8 clients / tests.
ReportRequest = BirthRequest
ReportResponse = APIResponse
