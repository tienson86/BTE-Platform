"""API request/response schemas for Validation Console."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

WorkflowAction = Literal["submit", "approve", "reject", "release"]


class APIEnvelope(BaseModel):
    """Standard API envelope."""

    success: bool
    message: str
    data: Any = None
    request_id: str | None = None


class CreateDatasetRequest(BaseModel):
    """Create a golden dataset."""

    name: str = Field(..., min_length=1)
    description: str = ""
    module: str = "general"
    cases: list[dict[str, Any]] = Field(default_factory=list)
    actor: str = "editor"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ImportDatasetRequest(BaseModel):
    """Import a dataset bundle."""

    name: str = Field(..., min_length=1)
    cases: list[dict[str, Any]] = Field(..., min_length=1)
    description: str = ""
    module: str = "general"
    actor: str = "editor"
    metadata: dict[str, Any] = Field(default_factory=dict)


class AddCaseRequest(BaseModel):
    """Add one case to a dataset."""

    case: dict[str, Any]
    actor: str = "editor"


class SetActualRequest(BaseModel):
    """Attach actual output for comparison."""

    actual_output: dict[str, Any]
    actor: str = "editor"


class WorkflowRequest(BaseModel):
    """Approval workflow transition."""

    action: WorkflowAction
    actor: str = "reviewer"
    message: str = ""


class RegressionRequest(BaseModel):
    """Run regression."""

    actor: str = "validator"
