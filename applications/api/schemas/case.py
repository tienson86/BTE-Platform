"""Case API schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CaseCreateRequest(BaseModel):
    """Manually create a case shell (rarely used; prefer analyze)."""

    customer_id: str
    engine_version: str | None = None
    input_snapshot: dict[str, Any] = Field(default_factory=dict)
    calendar_result: dict[str, Any] = Field(default_factory=dict)
    bazi_result: dict[str, Any] = Field(default_factory=dict)
    pattern_result: dict[str, Any] = Field(default_factory=dict)
    score_result: dict[str, Any] = Field(default_factory=dict)
    interpretation_result: dict[str, Any] = Field(default_factory=dict)
    report_result: dict[str, Any] = Field(default_factory=dict)
    narrative_result: dict[str, Any] = Field(default_factory=dict)
