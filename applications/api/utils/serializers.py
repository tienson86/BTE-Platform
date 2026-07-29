"""Serialize engine results for JSON API responses."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def to_jsonable(value: Any) -> Any:
    """Best-effort conversion of engine objects to JSON-serializable data."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
        try:
            return to_jsonable(value.to_dict())
        except Exception:
            pass
    if is_dataclass(value):
        try:
            return to_jsonable(asdict(value))
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        raw = {
            key: item
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
        if raw:
            return to_jsonable(raw)
    return str(value)
