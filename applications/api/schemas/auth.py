"""Auth request / response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Username / password login."""

    username: str = Field(..., min_length=1, examples=["admin"])
    password: str = Field(..., min_length=1, examples=["admin123"])


class RefreshRequest(BaseModel):
    """Refresh token exchange."""

    refresh_token: str = Field(..., min_length=1)


class LogoutRequest(BaseModel):
    """Optional tokens to revoke on logout."""

    access_token: str | None = None
    refresh_token: str | None = None


class TokenResponse(BaseModel):
    """JWT token pair response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict[str, Any] = Field(default_factory=dict)


class APIKeyCreateRequest(BaseModel):
    """Create API key for current user."""

    name: str = Field("default", min_length=1, max_length=64)


class APIKeyCreateResponse(BaseModel):
    """API key created (plaintext shown once)."""

    key_id: str
    api_key: str
    name: str
    user_id: str
