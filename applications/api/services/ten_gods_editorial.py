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
    """Use a god once, preferring a visible stem over a hidden occurrence."""
    layers = {str(item.get("pillar") or ""): item for item in four_layer.get("layers", [])
              if isinstance(item, Mapping)}
    choices: list[tuple[str, str, str]] = []
    for visibility in ("visible", "hidden"):
        for pillar in _PILLARS:
            layer = layers.get(pillar, {})
            occurrences = layer.get(visibility, [])
            for occurrence in occurrences if isinstance(occurrences, list) else []:
                if isinstance(occurrence, Mapping):
                    god = str(occurrence.get("ten_god") or "").strip()
                    if god and god != "Nhật Chủ":
                        choices.append((god, pillar, visibility))

    entries = _catalog()
    result: list[str] = []
    seen: set[str] = set()
    for god, pillar, visibility in choices:
        if god in seen:
            continue
        prose = entries.get(god, {}).get("pillar_copy", {}).get(pillar, "")
        if not prose:
            continue
        seen.add(god)
        location = f"trụ {_PILLAR_LABELS[pillar]}"
        mode = "lộ can" if visibility == "visible" else "tàng chi"
        result.append(f"{god} tại {location} ({mode}): {prose}")
    return result
