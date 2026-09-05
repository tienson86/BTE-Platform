"""Deterministic serialization helpers for MC-01."""

from __future__ import annotations

import hashlib
import json
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, Mapping


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses, enums, and tuples to JSON-safe values."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {item.name: to_jsonable(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return str(value)


def compute_content_hash(payload: Mapping[str, Any]) -> str:
    """SHA-256 of canonical JSON."""
    canonical = json.dumps(
        to_jsonable(payload),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def clamp_score(score: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Bound a 0..100 score."""
    return max(minimum, min(maximum, round(float(score), 2)))


def clamp_confidence(value: float) -> float:
    """Bound confidence to 0..1."""
    return max(0.0, min(1.0, round(float(value), 4)))


def band_for_score(score: float, bands: tuple[tuple[float, str], ...]) -> str:
    """Map a score onto descending (minimum, label) bands."""
    for minimum, label in bands:
        if score >= minimum:
            return label
    return bands[-1][1]
