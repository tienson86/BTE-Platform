"""Unit tests for permission helpers."""

from __future__ import annotations

from applications.api.auth.permissions import Permission, has_permission
from applications.api.auth.roles import Role


def test_permission_values() -> None:
    expected = {
        "calendar.read",
        "calendar.execute",
        "bazi.execute",
        "pattern.execute",
        "score.execute",
        "interpretation.execute",
        "report.generate",
        "narrative.generate",
        "customer.read",
        "customer.write",
        "admin.full",
    }
    assert {p.value for p in Permission} == expected


def test_has_permission_accepts_string_role() -> None:
    assert has_permission("STAFF", "score.execute")
    assert not has_permission("CUSTOMER", "score.execute")


def test_system_role_customer_write() -> None:
    assert has_permission(Role.SYSTEM, Permission.CUSTOMER_WRITE)
