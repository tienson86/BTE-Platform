"""Expert-B packet blinding validator (research workflow only)."""

from __future__ import annotations

import json
from typing import Any

FORBIDDEN_KEYS = frozenset(
    {
        "expert_a",
        "expert_a_label",
        "expert_a_rationale",
        "expert_a_evidence",
        "adjudication",
        "runtime_score",
        "runtime_band",
        "future_taxonomy",
        "t1",
        "t2",
        "t3",
        "t4",
        "t5",
        "t6",
    }
)


def _walk_keys(obj: Any, found: set[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.add(str(key).lower())
            _walk_keys(value, found)
    elif isinstance(obj, list):
        for item in obj:
            _walk_keys(item, found)


def validate_expert_b_packet(packet: dict[str, Any]) -> list[str]:
    """Return list of forbidden keys present in packet (empty = pass)."""
    found: set[str] = set()
    _walk_keys(packet, found)
    return sorted(FORBIDDEN_KEYS.intersection(found))


def validate_expert_b_packet_json(text: str) -> list[str]:
    """Validate a JSON string Expert-B packet for blinding leaks."""
    return validate_expert_b_packet(json.loads(text))
