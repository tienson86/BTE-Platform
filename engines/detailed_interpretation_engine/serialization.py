"""Serialize and deserialize Pack 07 frozen dataclasses."""

from __future__ import annotations

import hashlib
import json
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, Mapping

from engines.detailed_interpretation_engine.exceptions import (
    DetailedInterpretationContractError,
    DetailedInterpretationVersionError,
)
from engines.detailed_interpretation_engine.runtime import CanonicalRuntimeResult


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
    return value


def serialize_runtime_result(result: CanonicalRuntimeResult) -> dict[str, Any]:
    """Serialize CanonicalRuntimeResult to a JSON-safe mapping."""
    return to_jsonable(result)


def deserialize_runtime_result(payload: Mapping[str, Any] | None) -> CanonicalRuntimeResult:
    """Deserialize a mapping into CanonicalRuntimeResult."""
    if payload is None:
        raise DetailedInterpretationContractError("runtime payload is required")
    if not isinstance(payload, Mapping):
        raise DetailedInterpretationContractError("runtime payload must be an object")
    meta = payload.get("metadata")
    version = ""
    if isinstance(meta, Mapping):
        version = str(meta.get("contract_version") or "")
    if version and not version.startswith("bte.detailed_interpretation.runtime_contract"):
        raise DetailedInterpretationVersionError(f"unknown contract_version: {version}")
    return CanonicalRuntimeResult.from_dict(payload)


def dumps_runtime_result(result: CanonicalRuntimeResult) -> str:
    """Serialize CanonicalRuntimeResult to canonical JSON text."""
    return json.dumps(serialize_runtime_result(result), ensure_ascii=True, sort_keys=True)


def loads_runtime_result(raw: str) -> CanonicalRuntimeResult:
    """Deserialize CanonicalRuntimeResult from JSON text."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DetailedInterpretationContractError(f"invalid JSON: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise DetailedInterpretationContractError("runtime JSON must be an object")
    return deserialize_runtime_result(payload)


def _strip_created_at(payload: Any) -> Any:
    if isinstance(payload, Mapping):
        return {
            str(key): _strip_created_at(item)
            for key, item in payload.items()
            if not (key == "created_at")
        }
    if isinstance(payload, list):
        return [_strip_created_at(item) for item in payload]
    return payload


def compute_content_hash(payload: Mapping[str, Any]) -> str:
    """SHA-256 of canonical JSON with created_at excluded."""
    canonical = json.dumps(
        _strip_created_at(payload),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
