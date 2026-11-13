"""Published Ten Gods facts to approved customer prose; no chart recalculation."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_CATALOG = Path(__file__).resolve().parents[3] / "knowledge" / "editorial" / "ten_gods_v1.json"
_PILLARS = ("year", "month", "day", "hour")
_PILLAR_LABELS = {"year": "năm", "month": "tháng", "day": "ngày", "hour": "giờ"}


@lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    with _CATALOG.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if data.get("version") != "editorial.ten_gods.v1":
        raise ValueError("Unknown Ten Gods editorial catalog version")
    return dict(data["entries"])


def ten_gods_editorial_paragraphs(four_layer: Mapping[str, Any]) -> list[str]:
    """Keep every published god/pillar occurrence without repeating a pillar's prose."""
    raw_layers = four_layer.get("layers", [])
    if not isinstance(raw_layers, list):
        return []
    layers = {str(item.get("pillar") or ""): item for item in raw_layers
              if isinstance(item, Mapping)}
    # Insertion order preserves visible-first ordering, while modes are merged per position.
    choices: dict[tuple[str, str], set[str]] = {}
    for visibility in ("visible", "hidden"):
        for pillar in _PILLARS:
            occurrences = layers.get(pillar, {}).get(visibility, [])
            for occurrence in occurrences if isinstance(occurrences, list) else []:
                if not isinstance(occurrence, Mapping):
                    continue
                god = str(occurrence.get("ten_god") or "").strip()
                if god and god.lower() != "nhật chủ":
                    choices.setdefault((god, pillar), set()).add(visibility)

    entries = _catalog()
    result: list[str] = []
    # Group identical copy for the same god if a future catalog shares it between pillars.
    grouped: dict[tuple[str, str], list[str]] = {}
    for (god, pillar), modes in choices.items():
        prose = entries.get(god, {}).get("pillar_copy", {}).get(pillar, "")
        if not prose:
            continue
        prose = prose.replace("Người này", "Bạn").replace("người này", "bạn")
        mode = "lộ can và tàng chi" if modes == {"visible", "hidden"} else (
            "lộ can" if "visible" in modes else "tàng chi")
        location = f"trụ {_PILLAR_LABELS[pillar]} ({mode})"
        grouped.setdefault((god, prose), []).append(location)
    for (god, prose), locations in grouped.items():
        result.append(f"{god} tại {'; '.join(locations)}: {prose}")
    return result
