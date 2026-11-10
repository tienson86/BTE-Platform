"""User profile schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

def optional_phone(value):
    if not value:
        return value
    from applications.api.schemas.activity import normalize_phone
    return normalize_phone(value)


class UserProfile(BaseModel):
    """Public user profile."""

    user_id: str
    username: str
    role: str
    display_name: str
    phone: str = ""
    is_active: bool = True
    permissions: list[str] = Field(default_factory=list)
    analysis_limit: int | None = Field(default=None, ge=0)
    analyses_used: int = Field(default=0, ge=0)
    analyses_remaining: int | None = Field(default=None, ge=0)
    member_access: bool = True
    membership_status: str = "existing"
    membership_expires_at: str | None = None


class UserQuotaUpdate(BaseModel):
    """Admin-managed analysis allowance for one account."""

    analysis_limit: int = Field(..., ge=0, le=1_000_000)
    analyses_used: int | None = Field(default=None, ge=0)


class AdminUserCreate(BaseModel):
    phone: str = Field(default="", max_length=24)
    _phone = field_validator("phone")(optional_phone)
    username: str = Field(..., min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(..., min_length=8, max_length=128)
    display_name: str = Field(default="", max_length=120)
    analysis_limit: int | None = Field(default=50, ge=0, le=1_000_000)


class AdminUserUpdate(BaseModel):
    phone: str | None = Field(default=None, max_length=24)
    _phone = field_validator("phone")(optional_phone)
    display_name: str | None = Field(default=None, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None
    analysis_limit: int | None = Field(default=None, ge=0, le=1_000_000)
    analyses_used: int | None = Field(default=None, ge=0)
