"""Role-ready RBAC for Analysis Engine API."""

from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    """API roles (role-ready catalog)."""

    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


class Permission(str, Enum):
    """Fine-grained permissions."""

    CHART_CREATE = "chart.create"
    CHART_READ = "chart.read"
    ANALYSIS_EXECUTE = "analysis.execute"
    ANALYSIS_READ = "analysis.read"
    INTERPRETATION_EXECUTE = "interpretation.execute"
    INTERPRETATION_READ = "interpretation.read"
    REPORT_GENERATE = "report.generate"
    REPORT_READ = "report.read"
    TOKEN_ISSUE = "token.issue"
    ADMIN_FULL = "admin.full"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset({Permission.ADMIN_FULL}),
    Role.ANALYST: frozenset(
        {
            Permission.CHART_CREATE,
            Permission.CHART_READ,
            Permission.ANALYSIS_EXECUTE,
            Permission.ANALYSIS_READ,
            Permission.INTERPRETATION_EXECUTE,
            Permission.INTERPRETATION_READ,
            Permission.REPORT_GENERATE,
            Permission.REPORT_READ,
            Permission.TOKEN_ISSUE,
        }
    ),
    Role.VIEWER: frozenset(
        {
            Permission.CHART_READ,
            Permission.ANALYSIS_READ,
            Permission.INTERPRETATION_READ,
            Permission.REPORT_READ,
        }
    ),
}


def permissions_for_role(role: Role | str) -> frozenset[Permission]:
    """Return permissions granted to a role."""
    role_value = Role(role) if not isinstance(role, Role) else role
    return ROLE_PERMISSIONS.get(role_value, frozenset())


def has_permission(role: Role | str, permission: Permission | str) -> bool:
    """True if role grants permission (ADMIN_FULL implies all)."""
    role_perms = permissions_for_role(role)
    if Permission.ADMIN_FULL in role_perms:
        return True
    needed = (
        permission if isinstance(permission, Permission) else Permission(permission)
    )
    return needed in role_perms
