"""Shared coerce helpers for Pack 07 frozen dataclasses.

No interpretation logic.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping, TypeVar

E = TypeVar("E", bound=Enum)


def as_str(value: Any, default: str = "") -> str:
    """Coerce a JSON scalar to str."""
    if value is None:
        return default
    return str(value)


def as_optional_str(value: Any) -> str | None:
    """Coerce empty JSON values to None."""
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def as_float(value: Any, default: float | None = None) -> float | None:
    """Coerce a JSON number to float, preserving None."""
    if value is None or value == "":
        return default
    return float(value)


def as_str_tuple(value: Any) -> tuple[str, ...]:
    """Coerce a JSON list to a string tuple."""
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def as_str_dict(value: Any) -> dict[str, str]:
    """Coerce a JSON object to str→str."""
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}


def as_enum(enum_cls: type[E], value: Any, default: E) -> E:
    """Coerce a JSON string to a frozen enum, defaulting when empty."""
    if value is None or value == "":
        return default
    if isinstance(value, enum_cls):
        return value
    return enum_cls(str(value))
