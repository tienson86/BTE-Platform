"""User routes (WP10 — profile only, no customer management)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from applications.api.auth.dependencies import (
    CurrentUser,
    require_permission,
    require_role,
)
from applications.api.auth.permissions import Permission
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.schemas.user import UserProfile

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfile)
def current_user_profile(user: CurrentUser) -> UserProfile:
    """Return current user profile (alias of /auth/me)."""
    return UserProfile(**user.to_public_dict())


@router.get(
    "/admin-check",
    response_model=UserProfile,
    summary="RBAC demo: ADMIN role required",
)
def admin_check(
    user: UserRecord = Depends(require_role(Role.ADMIN)),
) -> UserProfile:
    """Demo endpoint protected by ``require_role(ADMIN)``."""
    return UserProfile(**user.to_public_dict())


@router.get(
    "/permission-check",
    response_model=UserProfile,
    summary="RBAC demo: report.generate required",
)
def permission_check(
    user: UserRecord = Depends(
        require_permission(Permission.REPORT_GENERATE)
    ),
) -> UserProfile:
    """Demo endpoint protected by ``require_permission``."""
    return UserProfile(**user.to_public_dict())
