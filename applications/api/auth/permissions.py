"""Permission catalog and role → permission map."""

from __future__ import annotations

from enum import Enum

from applications.api.auth.roles import Role


class Permission(str, Enum):
    """Fine-grained permissions (WP10)."""

    CALENDAR_READ = "calendar.read"
    CALENDAR_EXECUTE = "calendar.execute"
    BAZI_EXECUTE = "bazi.execute"
    PATTERN_EXECUTE = "pattern.execute"
    SCORE_EXECUTE = "score.execute"
    INTERPRETATION_EXECUTE = "interpretation.execute"
    REPORT_GENERATE = "report.generate"
    NARRATIVE_GENERATE = "narrative.generate"
    CUSTOMER_READ = "customer.read"
    CUSTOMER_WRITE = "customer.write"
    ADMIN_FULL = "admin.full"


ALL_PERMISSIONS: frozenset[Permission] = frozenset(Permission)

ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset({Permission.ADMIN_FULL}),
    Role.SYSTEM: frozenset(
        {
            Permission.CALENDAR_READ,
            Permission.CALENDAR_EXECUTE,
            Permission.BAZI_EXECUTE,
            Permission.PATTERN_EXECUTE,
            Permission.SCORE_EXECUTE,
            Permission.INTERPRETATION_EXECUTE,
            Permission.REPORT_GENERATE,
            Permission.NARRATIVE_GENERATE,
            Permission.CUSTOMER_READ,
            Permission.CUSTOMER_WRITE,
        }
    ),
    Role.STAFF: frozenset(
        {
            Permission.CALENDAR_READ,
            Permission.CALENDAR_EXECUTE,
            Permission.BAZI_EXECUTE,
            Permission.PATTERN_EXECUTE,
            Permission.SCORE_EXECUTE,
            Permission.INTERPRETATION_EXECUTE,
            Permission.REPORT_GENERATE,
            Permission.NARRATIVE_GENERATE,
            Permission.CUSTOMER_READ,
            Permission.CUSTOMER_WRITE,
        }
    ),
    Role.CONSULTANT: frozenset(
        {
            Permission.CALENDAR_READ,
            Permission.CALENDAR_EXECUTE,
            Permission.BAZI_EXECUTE,
            Permission.PATTERN_EXECUTE,
            Permission.SCORE_EXECUTE,
            Permission.INTERPRETATION_EXECUTE,
            Permission.REPORT_GENERATE,
            Permission.NARRATIVE_GENERATE,
            Permission.CUSTOMER_READ,
        }
    ),
    Role.CUSTOMER: frozenset(
        {
            Permission.CALENDAR_READ,
            Permission.REPORT_GENERATE,
            Permission.NARRATIVE_GENERATE,
        }
    ),
}


def permissions_for_role(role: Role | str) -> frozenset[Permission]:
    """Return permissions granted to a role."""
    role_value = Role(role) if not isinstance(role, Role) else role
    return ROLE_PERMISSIONS.get(role_value, frozenset())


def has_permission(
    role: Role | str,
    permission: Permission | str,
) -> bool:
    """True if role grants permission (ADMIN_FULL implies all)."""
    role_perms = permissions_for_role(role)
    if Permission.ADMIN_FULL in role_perms:
        return True
    needed = (
        permission
        if isinstance(permission, Permission)
        else Permission(permission)
    )
    return needed in role_perms
