"""In-memory user / API-key store for WP10 development."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from applications.api.auth.password_hasher import hash_password
from applications.api.auth.permissions import permissions_for_role
from applications.api.auth.roles import Role


@dataclass(slots=True)
class UserRecord:
    """Stored user (no plaintext password)."""

    user_id: str
    username: str
    password_hash: str
    role: Role
    is_active: bool = True
    display_name: str = ""

    def permission_values(self) -> list[str]:
        """Resolved permission strings for this user's role."""
        return sorted(p.value for p in permissions_for_role(self.role))

    def to_public_dict(self) -> dict[str, Any]:
        """JSON-safe public profile."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role.value,
            "display_name": self.display_name or self.username,
            "is_active": self.is_active,
            "permissions": self.permission_values(),
        }


@dataclass(slots=True)
class APIKeyRecord:
    """Stored API key hash bound to a user."""

    key_id: str
    user_id: str
    key_hash: str
    name: str = "default"
    is_active: bool = True


@dataclass
class InMemoryUserStore:
    """Dev-only store — not a database / ORM."""

    users_by_id: dict[str, UserRecord] = field(default_factory=dict)
    users_by_username: dict[str, UserRecord] = field(default_factory=dict)
    api_keys_by_id: dict[str, APIKeyRecord] = field(default_factory=dict)
    revoked_jtis: set[str] = field(default_factory=set)

    def add_user(self, user: UserRecord) -> UserRecord:
        """Insert or replace a user."""
        self.users_by_id[user.user_id] = user
        self.users_by_username[user.username.lower()] = user
        return user

    def get_by_id(self, user_id: str) -> UserRecord | None:
        """Lookup by user id."""
        return self.users_by_id.get(user_id)

    def get_by_username(self, username: str) -> UserRecord | None:
        """Lookup by username (case-insensitive)."""
        return self.users_by_username.get(username.lower())

    def add_api_key(self, record: APIKeyRecord) -> APIKeyRecord:
        """Store an API key record."""
        self.api_keys_by_id[record.key_id] = record
        return record

    def find_api_key_by_hash(self, key_hash: str) -> APIKeyRecord | None:
        """Find active API key by hash."""
        for record in self.api_keys_by_id.values():
            if record.is_active and record.key_hash == key_hash:
                return record
        return None

    def revoke_jti(self, jti: str) -> None:
        """Mark a JWT id as revoked (logout / refresh rotation)."""
        if jti:
            self.revoked_jtis.add(jti)

    def is_jti_revoked(self, jti: str | None) -> bool:
        """True if token id was revoked."""
        return bool(jti) and jti in self.revoked_jtis


def seed_dev_store() -> InMemoryUserStore:
    """Seed demo users for local development / tests."""
    store = InMemoryUserStore()
    seeds = [
        ("u-admin", "admin", "admin123", Role.ADMIN, "Admin User"),
        ("u-system", "system", "system123", Role.SYSTEM, "System User"),
        ("u-staff", "staff", "staff123", Role.STAFF, "Staff User"),
        (
            "u-consultant",
            "consultant",
            "consultant123",
            Role.CONSULTANT,
            "Consultant User",
        ),
        (
            "u-customer",
            "customer",
            "customer123",
            Role.CUSTOMER,
            "Customer User",
        ),
    ]
    for user_id, username, password, role, display_name in seeds:
        store.add_user(
            UserRecord(
                user_id=user_id,
                username=username,
                password_hash=hash_password(password),
                role=role,
                display_name=display_name,
            )
        )
    return store
