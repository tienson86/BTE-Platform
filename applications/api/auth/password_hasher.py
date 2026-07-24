"""Password hashing helpers (PBKDF2 — no plaintext storage)."""

from __future__ import annotations

import hashlib
import hmac
import secrets

from applications.api.config import settings

_HASH_PREFIX = "pbkdf2_sha256"


def hash_password(password: str) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256."""
    if not password:
        raise ValueError("password must not be empty")
    salt = secrets.token_bytes(settings.password_salt_bytes)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        settings.password_hash_iterations,
    )
    return (
        f"{_HASH_PREFIX}"
        f"${settings.password_hash_iterations}"
        f"${salt.hex()}"
        f"${digest.hex()}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    """Verify plaintext password against a stored hash."""
    try:
        algorithm, iterations_s, salt_hex, digest_hex = password_hash.split(
            "$", 3
        )
        if algorithm != _HASH_PREFIX:
            return False
        iterations = int(iterations_s)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except (ValueError, TypeError):
        return False

    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(candidate, expected)
