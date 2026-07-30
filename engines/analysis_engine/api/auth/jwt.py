"""JWT-ready auth primitives for Analysis Engine API."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass
from typing import Any

from engines.analysis_engine.api.config import settings
from engines.analysis_engine.api.exceptions import AuthenticationError


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


@dataclass(slots=True, frozen=True)
class TokenPair:
    """Access token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 0


class JWTManager:
    """HS256 JWT manager (stdlib only — JWT ready)."""

    def create_access_token(
        self,
        *,
        subject: str,
        role: str,
        username: str,
        extra_claims: dict[str, Any] | None = None,
    ) -> TokenPair:
        """Issue a signed access token."""
        now = int(time.time())
        ttl = settings.access_token_expire_minutes * 60
        header = {"alg": settings.jwt_algorithm, "typ": "JWT"}
        payload: dict[str, Any] = {
            "sub": subject,
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "iat": now,
            "exp": now + ttl,
            "jti": str(uuid.uuid4()),
            "type": "access",
            "role": role,
            "username": username,
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
        return TokenPair(
            access_token=f"{header_part}.{payload_part}.{signature}",
            expires_in=ttl,
        )

    def decode_access_token(self, token: str) -> dict[str, Any]:
        """Validate and decode an access token."""
        try:
            header_b64, payload_b64, signature = token.split(".")
        except ValueError as exc:
            raise AuthenticationError("Malformed token") from exc

        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected_sig = _sign(signing_input)
        if not hmac.compare_digest(expected_sig, signature):
            raise AuthenticationError("Invalid signature")

        try:
            payload = json.loads(_b64url_decode(payload_b64))
        except (json.JSONDecodeError, ValueError) as exc:
            raise AuthenticationError("Invalid payload") from exc

        if payload.get("iss") != settings.jwt_issuer:
            raise AuthenticationError("Invalid issuer")
        if payload.get("aud") != settings.jwt_audience:
            raise AuthenticationError("Invalid audience")
        exp = payload.get("exp")
        if not isinstance(exp, int) or exp < int(time.time()):
            raise AuthenticationError("Token expired")
        if payload.get("type") != "access":
            raise AuthenticationError("Expected access token")
        if not payload.get("sub"):
            raise AuthenticationError("Missing subject")
        return payload
