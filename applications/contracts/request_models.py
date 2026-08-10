"""Canonical public request models. Validation only. No business logic."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from applications.contracts.pagination_models import PaginationRequest


class BirthDataRequest(BaseModel):
    """Birth input accepted by the public analysis API."""

    model_config = ConfigDict(extra="forbid")

    year: int = Field(..., ge=1, le=9999, description="Birth year.")
    month: int = Field(..., ge=1, le=12, description="Birth month.")
    day: int = Field(..., ge=1, le=31, description="Birth day.")
    hour: int = Field(default=0, ge=0, le=23, description="Birth hour.")
    minute: int = Field(default=0, ge=0, le=59, description="Birth minute.")
    calendar_type: str = Field(default="solar", description="Calendar type identifier.")
    timezone: str = Field(default="Asia/Ho_Chi_Minh", description="IANA timezone.")
    gender: str | None = Field(default=None, description="Optional gender identifier.")


class CustomerRequest(BaseModel):
    """Optional customer reference. Not an engine model."""

    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, max_length=128)
    name: str | None = Field(default=None, max_length=256)


class AnalysisOptionsRequest(BaseModel):
    """Extensible analysis options. Unknown keys are rejected."""

    model_config = ConfigDict(extra="forbid")

    language: str = Field(default="vi", min_length=2, max_length=16)
    report_template: str | None = Field(default=None, max_length=128)


class AnalysisCreateRequest(BaseModel):
    """POST /api/v1/analysis body."""

    model_config = ConfigDict(extra="forbid")

    customer: CustomerRequest | None = None
    birth_data: BirthDataRequest
    options: AnalysisOptionsRequest = Field(default_factory=AnalysisOptionsRequest)
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Opaque client metadata. Never forwarded to engines by this layer.",
    )


class ResourceIdPath(BaseModel):
    """Shared path identifier contract."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1, max_length=128)


class AnalysisGetRequest(ResourceIdPath):
    """GET /api/v1/analysis/{id} path contract."""


class ReportGetRequest(ResourceIdPath):
    """GET /api/v1/report/{id} path contract."""


class KnowledgeGetRequest(ResourceIdPath):
    """GET /api/v1/knowledge/{id} path contract."""


class ListQueryRequest(PaginationRequest):
    """Reserved list query contract."""
