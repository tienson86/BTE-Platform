"""Unit tests for roles and role→permission mapping."""

from __future__ import annotations

from applications.api.auth.permissions import (
    Permission,
    has_permission,
    permissions_for_role,
)
from applications.api.auth.roles import Role


def test_all_roles_defined() -> None:
    assert {r.value for r in Role} == {
        "ADMIN",
        "SYSTEM",
        "STAFF",
        "CONSULTANT",
        "CUSTOMER",
    }


def test_admin_has_full_access() -> None:
    assert Permission.ADMIN_FULL in permissions_for_role(Role.ADMIN)
    assert has_permission(Role.ADMIN, Permission.REPORT_GENERATE)
    assert has_permission(Role.ADMIN, Permission.CUSTOMER_WRITE)


def test_customer_limited_permissions() -> None:
    perms = permissions_for_role(Role.CUSTOMER)
    assert Permission.CALENDAR_READ in perms
    assert Permission.REPORT_GENERATE in perms
    assert Permission.BAZI_EXECUTE not in perms
    assert not has_permission(Role.CUSTOMER, Permission.ADMIN_FULL)


def test_consultant_can_execute_engines() -> None:
    assert has_permission(Role.CONSULTANT, Permission.BAZI_EXECUTE)
    assert has_permission(Role.CONSULTANT, Permission.NARRATIVE_GENERATE)
    assert not has_permission(Role.CONSULTANT, Permission.CUSTOMER_WRITE)
