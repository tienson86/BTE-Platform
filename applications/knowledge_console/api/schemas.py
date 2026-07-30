"""API request/response schemas for Knowledge Console."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

AssetType = Literal["rule", "sentence", "phrase", "terminology"]
WorkflowAction = Literal["submit", "approve", "reject", "release"]


class APIEnvelope(BaseModel):
    """Standard API envelope."""

    success: bool
    message: str
    data: Any = None
    request_id: str | None = None


class CreateAssetRequest(BaseModel):
    """Create knowledge asset."""

    asset_type: AssetType
    title: str = Field(..., min_length=1)
    content: dict[str, Any]
    actor: str = "editor"
    metadata: dict[str, Any] = Field(default_factory=dict)


class UpdateAssetRequest(BaseModel):
    """Update knowledge asset."""

    title: str | None = None
    content: dict[str, Any] | None = None
    actor: str = "editor"
    note: str = "Edited"


class WorkflowRequest(BaseModel):
    """Approval workflow transition."""

    action: WorkflowAction
    actor: str = "reviewer"
    message: str = ""
