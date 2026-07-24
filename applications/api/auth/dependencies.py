"""Auth FastAPI dependencies: current user, roles, permissions."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Request

from applications.api.auth.permissions import Permission, has_permission
from applications.api.auth.roles import Role
from applications.api.auth.store import UserRecord
from applications.api.exceptions import ApplicationsAPIError
from applications.api.services.auth_service import AuthService
from applications.api.services.user_service import UserService


class AuthenticationError(ApplicationsAPIError):
    """Missing or invalid credentials."""

    def __init__(self, message: str = "Not authenticated") -> None:
        super().__init__(message, status_code=401, code="unauthorized")


class AuthorizationError(ApplicationsAPIError):
    """Authenticated but missing role/permission."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, status_code=403, code="forbidden")


def get_auth_service() -> AuthService:
    """Resolve auth service singleton."""
    from applications.api.dependencies import get_auth_service as _get

    return _get()


def get_user_service() -> UserService:
    """Resolve user service singleton."""
    from applications.api.dependencies import get_user_service as _get

    return _get()


def _user_from_request(request: Request) -> UserRecord | None:
    user = getattr(request.state, "user", None)
    return user if isinstance(user, UserRecord) else None


def get_current_user_optional(request: Request) -> UserRecord | None:
    """Return authenticated user when present; otherwise ``None``."""
    return _user_from_request(request)


def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserRecord:
    """
    Require an authenticated user.

    Prefers ``request.state.user`` (middleware); falls back to header parse.
    """
    user = _user_from_request(request)
    if user is not None:
        return user

    user = auth_service.resolve_user_from_request(request)
    if user is None:
        raise AuthenticationError()
    request.state.user = user
    return user


CurrentUser = Annotated[UserRecord, Depends(get_current_user)]
OptionalUser = Annotated[UserRecord | None, Depends(get_current_user_optional)]


def require_role(*roles: Role | str) -> Callable[..., UserRecord]:
    """Dependency factory: user must have one of the given roles."""
    allowed = {Role(r) if not isinstance(r, Role) else r for r in roles}

    def dependency(user: CurrentUser) -> UserRecord:
        if user.role not in allowed and user.role != Role.ADMIN:
            raise AuthorizationError(
                f"Requires role: {', '.join(sorted(r.value for r in allowed))}"
            )
        return user

    return dependency


def require_permission(
    *permissions: Permission | str,
) -> Callable[..., UserRecord]:
    """Dependency factory: user must have all listed permissions."""

    def dependency(user: CurrentUser) -> UserRecord:
        for permission in permissions:
            if not has_permission(user.role, permission):
                needed = (
                    permission.value
                    if isinstance(permission, Permission)
                    else str(permission)
                )
                raise AuthorizationError(f"Missing permission: {needed}")
        return user

    return dependency
