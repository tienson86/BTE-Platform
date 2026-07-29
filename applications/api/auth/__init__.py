"""Authentication & authorization package (WP10)."""

from applications.api.auth.permissions import Permission
from applications.api.auth.roles import Role

__all__ = ["Permission", "Role"]
