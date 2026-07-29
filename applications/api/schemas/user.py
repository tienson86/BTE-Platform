"""User profile schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Public user profile."""

    user_id: str
    username: str
    role: str
    display_name: str
    is_active: bool = True
    permissions: list[str] = Field(default_factory=list)
