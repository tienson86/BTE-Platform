"""In-memory user / API-key store for WP10 development."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
import os
import tempfile
import json
from pathlib import Path
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
    analysis_limit: int | None = None
    analyses_used: int = 0

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
            "analysis_limit": self.analysis_limit,
            "analyses_used": self.analyses_used,
            "analyses_remaining": None if self.analysis_limit is None else max(0, self.analysis_limit - self.analyses_used),
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
    _lock: RLock = field(default_factory=RLock, repr=False)

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

    def can_create_analysis(self, user_id: str) -> bool:
        user = self.get_by_id(user_id)
        return bool(user) and (user.analysis_limit is None or user.analyses_used < user.analysis_limit)

    def consume_analysis(self, user_id: str) -> bool:
        """Atomically consume one successful analysis from the account quota."""
        with self._lock:
            user = self.get_by_id(user_id)
            if user is None or not user.is_active:
                return False
            if user.analysis_limit is not None and user.analyses_used >= user.analysis_limit:
                return False
            user.analyses_used += 1
            self._after_change()
            return True

    def _after_change(self) -> None:
        """Persistence hook for durable stores."""


class JsonUserStore(InMemoryUserStore):
    """Durable account store used until production PostgreSQL is enabled."""

    def __init__(self, path: Path | str) -> None:
        super().__init__()
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self._load()

    def add_user(self, user: UserRecord) -> UserRecord:
        with self._lock:
            existing = self.users_by_username.get(user.username.lower())
            if existing is not None and existing.user_id != user.user_id:
                raise ValueError("Username already belongs to another account")
            for name, record in list(self.users_by_username.items()):
                if record.user_id == user.user_id and name != user.username.lower():
                    del self.users_by_username[name]
            saved = super().add_user(user)
            self._after_change()
            return saved

    def consume_analysis(self, user_id: str) -> bool:
        with self._lock:
            user = self.get_by_id(user_id)
            before = user.analyses_used if user is not None else None
            try:
                return super().consume_analysis(user_id)
            except Exception:
                if user is not None:
                    user.analyses_used = before
                raise

    def _load(self) -> None:
        payload = json.loads(self.path.read_text(encoding="utf-8") or "[]")
        for row in payload:
            super().add_user(UserRecord(
                user_id=str(row["user_id"]), username=str(row["username"]),
                password_hash=str(row["password_hash"]), role=Role(str(row["role"])),
                is_active=bool(row.get("is_active", True)), display_name=str(row.get("display_name", "")),
                analysis_limit=row.get("analysis_limit"), analyses_used=int(row.get("analyses_used", 0)),
            ))

    def _after_change(self) -> None:
        # One API process; serialize account writes inside that process.
        # Unique temp file + fsync + atomic replacement protects the previous file.
        with self._lock:
            rows = [{
                "user_id": u.user_id, "username": u.username, "password_hash": u.password_hash,
                "role": u.role.value, "is_active": u.is_active, "display_name": u.display_name,
                "analysis_limit": u.analysis_limit, "analyses_used": u.analyses_used,
            } for u in self.users_by_id.values()]
            name = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent,
                                                prefix=self.path.name+".", suffix=".tmp", delete=False) as handle:
                    name = handle.name
                    json.dump(rows, handle, ensure_ascii=False, indent=2)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(name, self.path)
                name = None
            finally:
                if name is not None:
                    Path(name).unlink(missing_ok=True)

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
                analysis_limit=None if role == Role.ADMIN else 100,
            )
        )
    return store


def load_persistent_store(path: Path | str) -> JsonUserStore:
    store = JsonUserStore(path)
    if store.users_by_id:
        return store
    seeded = seed_dev_store()
    for user in seeded.users_by_id.values():
        store.add_user(user)
    return store
