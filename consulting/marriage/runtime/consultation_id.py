"""Consultation ID generation. Stable for one runtime execution."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone

_CONSULTATION_PREFIX = "MC"
_TOKEN_LENGTH = 6
_TOKEN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_consultation_id(moment: datetime | None = None) -> str:
    """Return a consultation id in the form MC-YYYYMMDD-XXXXXX."""
    stamp = moment or datetime.now(timezone.utc)
    date_part = stamp.strftime("%Y%m%d")
    token = "".join(secrets.choice(_TOKEN_ALPHABET) for _ in range(_TOKEN_LENGTH))
    return f"{_CONSULTATION_PREFIX}-{date_part}-{token}"


def is_consultation_id(value: str) -> bool:
    """Return True when value matches MC-YYYYMMDD-XXXXXX."""
    parts = value.split("-")
    if len(parts) != 3:
        return False
    prefix, date_part, token = parts
    if prefix != _CONSULTATION_PREFIX:
        return False
    if len(date_part) != 8 or not date_part.isdigit():
        return False
    if len(token) != _TOKEN_LENGTH:
        return False
    return all(character in _TOKEN_ALPHABET for character in token)
