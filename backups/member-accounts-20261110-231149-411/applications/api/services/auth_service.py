"""Authentication service (login / refresh / logout / API keys)."""

from __future__ import annotations

from typing import Any

from fastapi import Request

from applications.api.auth.api_key_manager import APIKeyManager
from applications.api.auth.jwt_manager import JWTError, JWTManager, TokenPair
from applications.api.auth.password_hasher import verify_password
from applications.api.auth.store import APIKeyRecord, InMemoryUserStore, UserRecord
from applications.api.config import settings
from applications.api.exceptions import ApplicationsAPIError


class AuthServiceError(ApplicationsAPIError):
    """Auth domain error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 401,
        code: str = "auth_error",
    ) -> None:
        super().__init__(message, status_code=status_code, code=code)


class AuthService:
    """Orchestrates JWT + API key authentication against in-memory store."""

    def __init__(
        self,
        store: InMemoryUserStore,
        *,
        jwt_manager: JWTManager | None = None,
        api_key_manager: APIKeyManager | None = None,
    ) -> None:
        self.store = store
        self.jwt = jwt_manager or JWTManager()
        self.api_keys = api_key_manager or APIKeyManager()

    def login(self, username: str, password: str) -> tuple[UserRecord, TokenPair]:
        """Authenticate username/password and issue tokens."""
        user = self.store.get_by_username(username)
        if user is None or not user.is_active:
            raise AuthServiceError("Invalid username or password")
        if not verify_password(password, user.password_hash):
            raise AuthServiceError("Invalid username or password")
        tokens = self.jwt.create_pair(
            subject=user.user_id,
            role=user.role.value,
            username=user.username,
        )
        return user, tokens

    def refresh(self, refresh_token: str) -> TokenPair:
        """Issue a new token pair from a valid refresh token."""
        try:
            payload = self.jwt.decode(refresh_token, expected_type="refresh")
        except JWTError as exc:
            raise AuthServiceError(str(exc)) from exc

        jti = payload.get("jti")
        if self.store.is_jti_revoked(jti):
            raise AuthServiceError("Refresh token revoked")

        user = self.store.get_by_id(str(payload["sub"]))
        if user is None or not user.is_active:
            raise AuthServiceError("User not found or inactive")

        if jti:
            self.store.revoke_jti(str(jti))

        return self.jwt.create_pair(
            subject=user.user_id,
            role=user.role.value,
            username=user.username,
        )

    def logout(self, *, access_token: str | None, refresh_token: str | None) -> None:
        """Revoke provided token ids (best-effort)."""
        for token, expected in (
            (access_token, "access"),
            (refresh_token, "refresh"),
        ):
            if not token:
                continue
            try:
                payload = self.jwt.decode(token, expected_type=expected)  # type: ignore[arg-type]
            except JWTError:
                continue
            jti = payload.get("jti")
            if jti:
                self.store.revoke_jti(str(jti))

    def create_api_key(
        self,
        user: UserRecord,
        *,
        name: str = "default",
    ) -> dict[str, Any]:
        """Generate API key for user; plaintext returned once."""
        generated = self.api_keys.generate()
        self.store.add_api_key(
            APIKeyRecord(
                key_id=generated.key_id,
                user_id=user.user_id,
                key_hash=generated.key_hash,
                name=name,
            )
        )
        return {
            "key_id": generated.key_id,
            "api_key": generated.api_key,
            "name": name,
            "user_id": user.user_id,
        }

    def resolve_user_from_headers(
        self,
        *,
        authorization: str | None,
        api_key: str | None,
    ) -> UserRecord | None:
        """Resolve user from Bearer JWT or API key header values."""
        if api_key:
            user = self._user_from_api_key(api_key)
            if user is not None:
                return user

        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() == "bearer" and token.strip():
                return self._user_from_access_token(token.strip())
        return None

    def resolve_user_from_request(self, request: Request) -> UserRecord | None:
        """Resolve user from request headers."""
        authorization = request.headers.get("Authorization")
        api_key = request.headers.get(settings.api_key_header)
        return self.resolve_user_from_headers(
            authorization=authorization,
            api_key=api_key,
        )

    def _user_from_access_token(self, token: str) -> UserRecord | None:
        try:
            payload = self.jwt.decode(token, expected_type="access")
        except JWTError:
            return None
        jti = payload.get("jti")
        if self.store.is_jti_revoked(jti):
            return None
        user = self.store.get_by_id(str(payload["sub"]))
        if user is None or not user.is_active:
            return None
        return user

    def _user_from_api_key(self, api_key: str) -> UserRecord | None:
        key_hash = self.api_keys.hash(api_key)
        record = self.store.find_api_key_by_hash(key_hash)
        if record is None:
            return None
        user = self.store.get_by_id(record.user_id)
        if user is None or not user.is_active:
            return None
        return user
