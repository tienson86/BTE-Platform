"""Auth routes: login, logout, refresh, me, api-key."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from applications.api.auth.dependencies import CurrentUser, get_auth_service
from applications.api.schemas.auth import (
    APIKeyCreateRequest,
    APIKeyCreateResponse,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    TokenResponse,
)
from applications.api.schemas.common import APIResponse
from applications.api.schemas.user import UserProfile
from applications.api.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Issue JWT access + refresh tokens."""
    user, tokens = auth_service.login(body.username, body.password)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
        expires_in=tokens.expires_in,
        user=user.to_public_dict(),
    )


@router.post("/logout", response_model=APIResponse)
def logout(
    request: Request,
    body: LogoutRequest | None = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> APIResponse:
    """Revoke access/refresh token ids when provided."""
    payload = body or LogoutRequest()
    access = payload.access_token
    if not access:
        authorization = request.headers.get("Authorization") or ""
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer":
            access = token.strip() or None
    auth_service.logout(
        access_token=access,
        refresh_token=payload.refresh_token,
    )
    return APIResponse(
        success=True,
        message="Logged out",
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    body: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Exchange refresh token for a new token pair."""
    tokens = auth_service.refresh(body.refresh_token)
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type=tokens.token_type,
        expires_in=tokens.expires_in,
    )


@router.get("/me", response_model=UserProfile)
def me(user: CurrentUser) -> UserProfile:
    """Return the authenticated user profile."""
    return UserProfile(**user.to_public_dict())


@router.post("/api-key", response_model=APIKeyCreateResponse)
def create_api_key(
    body: APIKeyCreateRequest,
    user: CurrentUser,
    auth_service: AuthService = Depends(get_auth_service),
) -> APIKeyCreateResponse:
    """Create an API key for the current authenticated user."""
    created = auth_service.create_api_key(user, name=body.name)
    return APIKeyCreateResponse(**created)
