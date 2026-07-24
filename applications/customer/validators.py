"""Customer input validators."""

from __future__ import annotations

import re
from datetime import datetime

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^[\d\s+\-().]{6,32}$")


class CustomerValidationError(ValueError):
    """Invalid customer payload."""


def validate_full_name(full_name: str) -> str:
    """Require a non-empty trimmed name."""
    name = (full_name or "").strip()
    if not name:
        raise CustomerValidationError("full_name is required")
    if len(name) > 200:
        raise CustomerValidationError("full_name is too long")
    return name


def validate_email(email: str | None) -> str | None:
    """Optional email format check."""
    if email is None or email == "":
        return None
    value = email.strip()
    if not _EMAIL_RE.match(value):
        raise CustomerValidationError("invalid email")
    return value


def validate_phone(phone: str | None) -> str | None:
    """Optional phone format check."""
    if phone is None or phone == "":
        return None
    value = phone.strip()
    if not _PHONE_RE.match(value):
        raise CustomerValidationError("invalid phone")
    return value


def validate_birth_datetime(birth_datetime: str | None) -> str | None:
    """Accept ISO-8601 datetime strings (or None)."""
    if birth_datetime is None or birth_datetime == "":
        return None
    value = birth_datetime.strip()
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CustomerValidationError(
            "birth_datetime must be ISO-8601"
        ) from exc
    return value


def validate_tags(tags: list[str] | None) -> list[str]:
    """Normalize tag list."""
    if not tags:
        return []
    cleaned: list[str] = []
    for tag in tags:
        item = str(tag).strip()
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned
