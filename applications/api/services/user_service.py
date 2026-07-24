"""User service over in-memory store (no customer management)."""

from __future__ import annotations

from applications.api.auth.store import InMemoryUserStore, UserRecord
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
