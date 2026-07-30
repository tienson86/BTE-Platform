"""Auth FastAPI dependencies (JWT ready + role ready)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request

from engines.analysis_engine.api.auth.jwt import JWTManager
from engines.analysis_engine.api.auth.roles import Permission, Role, has_permission
from engines.analysis_engine.api.config import settings
from engines.analysis_engine.api.exceptions import (
    AuthenticationError,
    AuthorizationError,
)


@dataclass(slots=True, frozen=True)
class Principal:
    """Authenticated (or anonymous) caller identity."""

    subject: str
    username: str
    role: Role
    authenticated: bool


def get_jwt_manager() -> JWTManager:
    """Resolve JWT manager."""
    return JWTManager()


def get_current_principal(
    request: Request,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
) -> Principal:
    """Resolve caller from Bearer JWT or anonymous default role."""
    auth = request.headers.get("Authorization") or ""
    if auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
        claims = jwt_manager.decode_access_token(token)
        role_raw = str(claims.get("role") or settings.default_anonymous_role)
        try:
            role = Role(role_raw)
        except ValueError as exc:
            raise AuthenticationError(f"Unknown role in token: {role_raw}") from exc
        return Principal(
            subject=str(claims["sub"]),
            username=str(claims.get("username") or claims["sub"]),
            role=role,
            authenticated=True,
        )

    if settings.auth_required:
        raise AuthenticationError("Bearer token required")

    return Principal(
        subject="anonymous",
        username="anonymous",
        role=Role(settings.default_anonymous_role),
        authenticated=False,
    )


CurrentPrincipal = Annotated[Principal, Depends(get_current_principal)]


def require_permission(
    *permissions: Permission | str,
) -> Callable[..., Principal]:
    """Dependency factory: principal must hold all listed permissions."""

    def dependency(principal: CurrentPrincipal) -> Principal:
        for permission in permissions:
            if not has_permission(principal.role, permission):
                needed = (
                    permission.value
                    if isinstance(permission, Permission)
                    else str(permission)
                )
                raise AuthorizationError(f"Missing permission: {needed}")
        return principal

    return dependency


def require_role(*roles: Role | str) -> Callable[..., Principal]:
    """Dependency factory: principal must have one of the given roles."""
    allowed = {Role(r) if not isinstance(r, Role) else r for r in roles}

    def dependency(principal: CurrentPrincipal) -> Principal:
        if principal.role not in allowed and principal.role != Role.ADMIN:
            raise AuthorizationError(
                f"Requires role: {', '.join(sorted(r.value for r in allowed))}"
            )
        return principal

    return dependency
