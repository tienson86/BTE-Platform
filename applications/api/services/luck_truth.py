"""Public Luck / Đại Vận contract from LuckEngine output."""

from __future__ import annotations

from typing import Any, Mapping


def shape_luck_payload(luck: Any) -> dict[str, Any]:
    """
    Publish structured Luck data without recalculating Da Yun.

    Reads the existing engine sequence from ``current_dayun.metadata.sequence``.
    """
    raw = luck.to_dict() if hasattr(luck, "to_dict") else dict(luck or {})
    current = raw.get("current_dayun") or {}
    if not isinstance(current, Mapping):
        current = {}
    metadata = dict(current.get("metadata") or {})
    sequence = metadata.get("sequence") or []
    if not isinstance(sequence, list):
        sequence = []
    cycles = [_cycle_from_item(item, index) for index, item in enumerate(sequence)]
    direction = str(metadata.get("direction") or "")
    if not direction and sequence and isinstance(sequence[0], Mapping):
        direction = str((sequence[0].get("metadata") or {}).get("direction") or "")
    start_age = None
    if cycles:
        start_age = cycles[0].get("age_start")
    calc = metadata.get("start_age_calc") or {}
    if start_age is None and isinstance(calc, Mapping):
        start_age = calc.get("start_age") or calc.get("age")
    current_cycle = None
    if isinstance(current, Mapping) and current:
        current_cycle = _cycle_from_item(current, int(current.get("index") or 0))
    elif cycles:
        current_cycle = cycles[0]
    return {
        "available": bool(raw.get("available")),
        "reason": raw.get("reason"),
        "direction": direction,
        "start_age": start_age,
        "current_cycle": current_cycle,
        "cycles": cycles,
        "current_dayun": dict(current),
        "metadata": dict(raw.get("metadata") or {}),
    }


def _cycle_from_item(item: Any, fallback_index: int) -> dict[str, Any]:
    data = item if isinstance(item, Mapping) else {}
    stem = str(data.get("heavenly_stem") or data.get("stem") or "")
    branch = str(data.get("earthly_branch") or data.get("branch") or "")
    gan_zhi = str(data.get("ganzhi") or data.get("gan_zhi") or "").strip()
    if not gan_zhi:
        gan_zhi = f"{stem} {branch}".strip()
    return {
        "index": int(data.get("index") if data.get("index") is not None else fallback_index),
        "age_start": data.get("start_age", data.get("age_start")),
        "age_end": data.get("end_age", data.get("age_end")),
        "year_start": data.get("start_year", data.get("year_start")),
        "year_end": data.get("end_year", data.get("year_end")),
        "gan_zhi": gan_zhi,
        "stem": stem,
        "branch": branch,
    }
