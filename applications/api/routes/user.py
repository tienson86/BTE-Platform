"""User routes (WP10 — profile only, no customer management)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from applications.api.auth.dependencies import (
    CurrentUser,
    get_user_service,
    require_permission,
    require_role,
)
from applications.api.auth.permissions import Permission
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.schemas.user import AdminUserCreate, AdminUserUpdate, UserProfile, UserQuotaUpdate
from applications.api.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserProfile])
def list_users(
    _admin: UserRecord = Depends(require_role(Role.ADMIN)),
    users: UserService = Depends(get_user_service),
) -> list[UserProfile]:
    return [UserProfile(**item.to_public_dict()) for item in users.list_users()]


@router.post("", response_model=UserProfile, status_code=201)
def create_user(
    body: AdminUserCreate,
    _admin: UserRecord = Depends(require_role(Role.ADMIN)),
    users: UserService = Depends(get_user_service),
) -> UserProfile:
    return UserProfile(**users.create_user(body.username, body.password, body.display_name, body.analysis_limit).to_public_dict())


@router.patch("/{username}", response_model=UserProfile)
def update_user(
    username: str,
    body: AdminUserUpdate,
    _admin: UserRecord = Depends(require_role(Role.ADMIN)),
    users: UserService = Depends(get_user_service),
) -> UserProfile:
    return UserProfile(**users.update_user(username, **body.model_dump(exclude_unset=True)).to_public_dict())


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


@router.put("/{username}/quota", response_model=UserProfile)
def update_user_quota(
    username: str,
    body: UserQuotaUpdate,
    _admin: UserRecord = Depends(require_role(Role.ADMIN)),
    users: UserService = Depends(get_user_service),
) -> UserProfile:
    """Admin only: set the maximum analyses and optionally reset usage."""
    user = users.update_quota(
        username,
        analysis_limit=body.analysis_limit,
        analyses_used=body.analyses_used,
    )
    return UserProfile(**user.to_public_dict())
