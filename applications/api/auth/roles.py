"""RBAC role definitions."""

from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    """Application roles (WP10)."""

    ADMIN = "ADMIN"
    SYSTEM = "SYSTEM"
    STAFF = "STAFF"
    CONSULTANT = "CONSULTANT"
    CUSTOMER = "CUSTOMER"
