"""Auth package exports."""

from __future__ import annotations

from engines.analysis_engine.api.auth.dependencies import (
    CurrentPrincipal,
    Principal,
    get_current_principal,
    get_jwt_manager,
    require_permission,
    require_role,
)
from engines.analysis_engine.api.auth.jwt import JWTManager, TokenPair
from engines.analysis_engine.api.auth.roles import Permission, Role, has_permission

__all__ = [
    "CurrentPrincipal",
    "JWTManager",
    "Permission",
    "Principal",
    "Role",
    "TokenPair",
    "get_current_principal",
    "get_jwt_manager",
    "has_permission",
    "require_permission",
    "require_role",
]
