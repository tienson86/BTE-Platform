"""Customer-safe and internal serializers. Separate on purpose."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation


def serialize_customer(presentation: NarrativeV2Presentation) -> dict[str, Any]:
    """JSON-safe public dict. No traces, ids, or runtime internals."""
    payload = _to_plain(presentation)
    if not isinstance(payload, dict):
        raise TypeError("Presentation serialization must be an object")
    return payload


def serialize_internal(presentation: NarrativeV2Presentation) -> dict[str, Any]:
    """Diagnostic copy of the public object only. Still no Evidence/Knowledge."""
    return serialize_customer(presentation)


def _to_plain(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, tuple):
        return [_to_plain(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        return {key: _to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _to_plain(item) for key, item in value.items()}
    return str(value)
