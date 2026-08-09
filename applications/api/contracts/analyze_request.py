"""Canonical analyze request contract."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AnalyzeOptions(BaseModel):
    """Extensible analyze request options."""

    model_config = ConfigDict(extra="allow")


class ChartInput(BaseModel):
    """Extensible chart input contract."""

    model_config = ConfigDict(extra="allow")


class AnalyzeRequest(BaseModel):
    """Canonical API analyze request."""

    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(..., description="Client or gateway correlation identifier.")
    api_version: str = Field(..., description="Requested API contract version.")
    language: str = Field(..., description="Preferred response language code.")
    chart: ChartInput = Field(..., description="Birth chart input payload.")
    report_template: str = Field(..., description="Report template identifier.")
    options: AnalyzeOptions = Field(
        default_factory=AnalyzeOptions,
        description="Extensible runtime options.",
    )
