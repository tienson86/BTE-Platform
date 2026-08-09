"""Deterministic LuckTimeline serialization. No calculations."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.luck_engine.contracts.luck_contracts import LuckTimeline
from engines.luck_engine.timeline.builder import construct_timeline


def timeline_to_dict(timeline: LuckTimeline) -> dict[str, Any]:
    """Return the published timeline mapping."""
    return timeline.to_dict()


def timeline_to_json(timeline: LuckTimeline) -> str:
    """Return canonical JSON (sorted keys, UTF-8, trailing newline omitted)."""
    return json.dumps(
        timeline.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def timeline_from_dict(payload: Mapping[str, Any]) -> LuckTimeline:
    """Rehydrate a timeline from a published mapping."""
    metadata = dict(payload.get("timeline_metadata") or {})
    timeline_id = str(metadata.get("timeline_id") or payload.get("timeline_id") or "timeline")
    return construct_timeline(
        timeline_id=timeline_id,
        natal_chart=payload["natal_chart"],
        major_cycles=payload.get("major_cycles") or (),
        annual_cycles=payload.get("annual_cycles") or (),
        monthly_cycles=payload.get("monthly_cycles") or (),
        daily_cycles=metadata.get("daily_cycles") or payload.get("daily_cycles") or (),
        hourly_cycles=metadata.get("hourly_cycles") or payload.get("hourly_cycles") or (),
        events=metadata.get("events") or payload.get("events") or (),
        timeline_metadata={
            key: value
            for key, value in metadata.items()
            if key not in {"timeline_id", "daily_cycles", "hourly_cycles", "events"}
        },
        timeline_version=str(payload.get("timeline_version") or ""),
    )
