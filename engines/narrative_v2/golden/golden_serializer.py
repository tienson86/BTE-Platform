"""Canonical JSON and hashing for Golden Cases. Copy only."""

from __future__ import annotations

import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping

HASH_ALGORITHM = "sha256"


def freeze_mapping(value: object) -> object:
    """Return an immutable nested mapping/tuple copy."""
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): freeze_mapping(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze_mapping(item) for item in value)
    return value


def thaw_mapping(value: object) -> object:
    """Return a JSON-safe mutable copy of a frozen payload."""
    if isinstance(value, Mapping):
        return {str(key): thaw_mapping(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_mapping(item) for item in value]
    return value


def canonical_json(payload: object) -> str:
    """Deterministic JSON used for hashes and freeze files."""
    return json.dumps(
        thaw_mapping(payload),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def stable_hash(payload: object) -> str:
    """SHA-256 of canonical JSON."""
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def presentation_hash(presentation: Mapping[str, Any]) -> str:
    """Hash the certified Presentation baseline."""
    return stable_hash(dict(presentation))


def certification_hash(certification: Mapping[str, Any]) -> str:
    """Hash the CERTIFIED decision record."""
    return stable_hash(dict(certification))


def review_hash(certification: Mapping[str, Any]) -> str:
    """Hash reviewer metadata used at certification time."""
    return stable_hash(
        {
            "review_id": certification.get("review_id"),
            "reviewer": certification.get("reviewer"),
            "review_time": certification.get("review_time"),
            "review_comment": certification.get("review_comment"),
        }
    )


def narrative_hash(presentation: Mapping[str, Any]) -> str:
    """Hash customer-facing Narrative fields copied into Presentation."""
    return stable_hash(
        {
            "overview": presentation.get("overview"),
            "interpretation": presentation.get("interpretation"),
            "action_plan": presentation.get("action_plan"),
        }
    )


def canonical_payload_hash(canonical: Mapping[str, Any] | None, case_id: str) -> str:
    """Hash Canonical Analysis when provided, otherwise the case identity key."""
    if canonical is None:
        return stable_hash({"case_id": case_id})
    return stable_hash(dict(canonical))
