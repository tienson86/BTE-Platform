"""User service over in-memory store (no customer management)."""

from __future__ import annotations

from applications.api.auth.store import InMemoryUserStore, UserRecord
from applications.api.auth.password_hasher import hash_password
from applications.api.auth.roles import Role
from uuid import uuid4
from applications.api.exceptions import ApplicationsAPIError


class UserServiceError(ApplicationsAPIError):
    """User lookup error."""

    def __init__(self, message: str, *, status_code: int = 404) -> None:
        super().__init__(message, status_code=status_code, code="user_error")


class UserService:
    """Read-only user helpers for WP10 (no CRUD / billing)."""

    def __init__(self, store: InMemoryUserStore) -> None:
        self.store = store

    def get_by_id(self, user_id: str) -> UserRecord:
        """Return user or raise."""
        user = self.store.get_by_id(user_id)
        if user is None:
            raise UserServiceError(f"User not found: {user_id}")
        return user

    def get_by_username(self, username: str) -> UserRecord:
        """Return user by username or raise."""
        user = self.store.get_by_username(username)
        if user is None:
            raise UserServiceError(f"User not found: {username}")
        return user

    def update_quota(
        self,
        username: str,
        *,
        analysis_limit: int,
        analyses_used: int | None = None,
    ) -> UserRecord:
        """Set an account quota; optionally correct/reset its used count."""
        return self.update_user(username,analysis_limit=max(0,int(analysis_limit)),analyses_used=analyses_used)

    def list_users(self) -> list[UserRecord]:
        return sorted(self.store.users_by_id.values(), key=lambda item: item.username.lower())

    def create_user(self, username: str, password: str, display_name: str, analysis_limit: int, phone: str = "") -> UserRecord:
        if self.store.get_by_username(username):
            raise UserServiceError("Username đã tồn tại", status_code=409)
        return self.store.add_user(UserRecord(
            user_id="u-" + uuid4().hex, username=username.strip(), password_hash=hash_password(password),
            role=Role.CUSTOMER, display_name=display_name.strip(), analysis_limit=analysis_limit,
            phone=phone,
        ))

    def update_user(self, username: str, **changes: object) -> UserRecord:
        user = self.get_by_username(username)
        updates = {}
        if changes.get("phone") is not None:
            from applications.api.schemas.activity import normalize_phone
            updates["phone"] = normalize_phone(str(changes["phone"])) if changes["phone"] else ""
        if changes.get("display_name") is not None:
            updates["display_name"] = str(changes["display_name"]).strip()
        if changes.get("password"):
            updates["password_hash"] = hash_password(str(changes["password"]))
        if changes.get("is_active") is not None:
            updates["is_active"] = bool(changes["is_active"])
        if "analysis_limit" in changes:
            updates["analysis_limit"] = None if changes["analysis_limit"] is None else max(0, int(changes["analysis_limit"]))
        if changes.get("analyses_used") is not None:
            updates["analyses_used"] = max(0, int(changes["analyses_used"]))
        with self.store._lock:
            before = {key:getattr(user,key) for key in updates}
            try:
                for key,value in updates.items():setattr(user,key,value)
                self.store._after_change()
            except Exception:
                for key,value in before.items():setattr(user,key,value)
                raise
        return user
