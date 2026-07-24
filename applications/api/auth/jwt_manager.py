"""JWT access / refresh token manager (HS256, stdlib)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Literal

from applications.api.config import settings

TokenType = Literal["access", "refresh"]


class JWTError(Exception):
    """Raised when a token is invalid or expired."""


@dataclass(slots=True)
class TokenPair:
    """Access + refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 0


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def _sign(message: bytes) -> str:
    digest = hmac.new(
        settings.jwt_secret.encode("utf-8"),
        message,
        hashlib.sha256,
    ).digest()
    return _b64url_encode(digest)


def create_token(
    *,
    subject: str,
    token_type: TokenType,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT for ``subject``."""
    now = int(time.time())
    if token_type == "access":
        ttl = settings.access_token_expire_minutes * 60
    else:
        ttl = settings.refresh_token_expire_days * 24 * 60 * 60

    header = {"alg": settings.jwt_algorithm, "typ": "JWT"}
    payload: dict[str, Any] = {
        "sub": subject,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": now,
        "exp": now + ttl,
        "jti": str(uuid.uuid4()),
        "type": token_type,
    }
    if extra_claims:
        payload.update(extra_claims)

    header_part = _b64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode()
    )
    payload_part = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    )
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    signature = _sign(signing_input)
    return f"{header_part}.{payload_part}.{signature}"


def decode_token(
    token: str,
    *,
    expected_type: TokenType | None = None,
) -> dict[str, Any]:
    """Validate and decode a JWT; raise ``JWTError`` on failure."""
    try:
        header_b64, payload_b64, signature = token.split(".")
    except ValueError as exc:
        raise JWTError("Malformed token") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_sig = _sign(signing_input)
    if not hmac.compare_digest(expected_sig, signature):
        raise JWTError("Invalid signature")

    try:
        payload = json.loads(_b64url_decode(payload_b64))
    except (json.JSONDecodeError, ValueError) as exc:
        raise JWTError("Invalid payload") from exc

    if payload.get("iss") != settings.jwt_issuer:
        raise JWTError("Invalid issuer")
    if payload.get("aud") != settings.jwt_audience:
        raise JWTError("Invalid audience")

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise JWTError("Token expired")

    token_type = payload.get("type")
    if expected_type is not None and token_type != expected_type:
        raise JWTError(f"Expected {expected_type} token")

    if not payload.get("sub"):
        raise JWTError("Missing subject")

    return payload


def create_token_pair(
    *,
    subject: str,
    role: str,
    username: str,
) -> TokenPair:
    """Issue access + refresh tokens for a user."""
    claims = {"role": role, "username": username}
    access = create_token(
        subject=subject,
        token_type="access",
        extra_claims=claims,
    )
    refresh = create_token(
        subject=subject,
        token_type="refresh",
        extra_claims=claims,
    )
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings.access_token_expire_minutes * 60,
    )


class JWTManager:
    """Facade used by services / dependencies."""

    def create_pair(
        self,
        *,
        subject: str,
        role: str,
        username: str,
    ) -> TokenPair:
        """Create access/refresh pair."""
        return create_token_pair(
            subject=subject,
            role=role,
            username=username,
        )

    def decode(
        self,
        token: str,
        *,
        expected_type: TokenType | None = None,
    ) -> dict[str, Any]:
        """Decode and validate token."""
        return decode_token(token, expected_type=expected_type)
