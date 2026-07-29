"""Customer API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CustomerCreateRequest(BaseModel):
    """Create customer payload."""

    full_name: str = Field(..., min_length=1, examples=["Nguyen Van A"])
    gender: str | None = Field(None, examples=["male"])
    birth_datetime: str | None = Field(
        None,
        examples=["1990-05-15T10:30:00"],
    )
    timezone: str = Field("Asia/Ho_Chi_Minh")
    language: str = Field("vi")
    phone: str | None = Field(None, examples=["+84901234567"])
    email: str | None = Field(None, examples=["a@example.com"])
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)


class CustomerUpdateRequest(BaseModel):
    """Partial customer update."""

    full_name: str | None = None
    gender: str | None = None
    birth_datetime: str | None = None
    timezone: str | None = None
    language: str | None = None
    phone: str | None = None
    email: str | None = None
    notes: str | None = None
    tags: list[str] | None = None


class CustomerAnalyzeRequest(BaseModel):
    """Optional overrides when analyzing a customer."""

    year: int | None = Field(None, ge=1, le=9999)
    month: int | None = Field(None, ge=1, le=12)
    day: int | None = Field(None, ge=1, le=31)
    hour: int | None = Field(None, ge=0, le=23)
    minute: int | None = Field(None, ge=0, le=59)
    gender: str | None = None
    timezone: str | None = None
