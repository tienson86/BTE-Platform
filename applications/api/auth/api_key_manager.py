"""API key generation and verification (in-memory friendly hashes)."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass


@dataclass(slots=True)
class GeneratedAPIKey:
    """Plain key returned once + hash for storage."""

    key_id: str
    api_key: str
    key_hash: str
    prefix: str


def generate_api_key(*, prefix: str = "bte") -> GeneratedAPIKey:
    """Create a random API key; store only ``key_hash``."""
    key_id = secrets.token_hex(8)
    secret = secrets.token_urlsafe(32)
    api_key = f"{prefix}_{key_id}_{secret}"
    return GeneratedAPIKey(
        key_id=key_id,
        api_key=api_key,
        key_hash=hash_api_key(api_key),
        prefix=prefix,
    )


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage (SHA-256 hex)."""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """Constant-time compare of key against stored hash."""
    return hmac.compare_digest(hash_api_key(api_key), key_hash)


class APIKeyManager:
    """Facade for API key operations."""

    def generate(self, *, prefix: str = "bte") -> GeneratedAPIKey:
        """Generate a new API key."""
        return generate_api_key(prefix=prefix)

    def hash(self, api_key: str) -> str:
        """Hash an API key."""
        return hash_api_key(api_key)

    def verify(self, api_key: str, key_hash: str) -> bool:
        """Verify an API key against its hash."""
        return verify_api_key(api_key, key_hash)
