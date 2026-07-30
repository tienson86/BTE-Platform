"""Pydantic request/response schemas for Analysis Engine API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class APIEnvelope(BaseModel):
    """Standard JSON envelope."""

    success: bool = True
    message: str = "OK"
    data: dict[str, Any] = Field(default_factory=dict)
    request_id: str | None = None


class CreateChartRequest(BaseModel):
    """Create Chart request."""

    day_master: str = Field(..., examples=["Giáp"])
    year: int | None = Field(None, ge=1, le=9999, examples=[1990])
    month: int | None = Field(None, ge=1, le=12, examples=[5])
    day: int | None = Field(None, ge=1, le=31, examples=[15])
    hour: int | None = Field(None, ge=0, le=23, examples=[10])
    minute: int | None = Field(0, ge=0, le=59, examples=[30])
    gender: str | None = Field(None, examples=["male"])
    timezone: str = Field("Asia/Ho_Chi_Minh")
    full_name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    luck: dict[str, Any] | None = Field(
        default=None,
        description="Optional chart.luck timeline; defaults applied when omitted.",
    )


class AnalysisRequest(BaseModel):
    """Run analysis for an existing chart."""

    chart_id: str = Field(..., examples=["cht_..."])


class InterpretationRequest(BaseModel):
    """Run interpretation for an existing analysis."""

    analysis_id: str = Field(..., examples=["anl_..."])


class ReportRequest(BaseModel):
    """Generate report from interpretation (+ analysis)."""

    interpretation_id: str = Field(..., examples=["int_..."])
    formats: list[str] = Field(
        default_factory=lambda: ["html", "markdown", "pdf", "json"],
        examples=[["html", "markdown", "pdf", "json"]],
    )
    include_structured_data: bool = True
    title: str = "BTE Analysis Report"


class TokenRequest(BaseModel):
    """Issue a development/access JWT (JWT-ready demo endpoint)."""

    subject: str = Field("user-1", examples=["user-1"])
    username: str = Field("analyst", examples=["analyst"])
    role: str = Field("ANALYST", examples=["ANALYST", "ADMIN", "VIEWER"])
