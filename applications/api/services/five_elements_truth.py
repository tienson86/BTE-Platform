"""Five Elements analytical fact mapping — not score components."""

from __future__ import annotations

from typing import Any, Mapping

ELEMENT_KEYS: tuple[str, ...] = ("wood", "fire", "earth", "metal", "water")
ELEMENT_LABELS: dict[str, str] = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}
_LABEL_TO_ELEMENT: dict[str, str] = {
    "wood": "wood",
    "fire": "fire",
    "earth": "earth",
    "metal": "metal",
    "water": "water",
    "mộc": "wood",
    "hỏa": "fire",
    "thổ": "earth",
    "kim": "metal",
    "thủy": "water",
    "moc": "wood",
    "hoa": "fire",
    "tho": "earth",
    "thuy": "water",
}


def normalize_element_key(token: str | None) -> str | None:
    """Map a label/name/element token onto wood/fire/earth/metal/water."""
    raw = str(token or "").strip().lower()
    if not raw:
        return None
    return _LABEL_TO_ELEMENT.get(raw)


def build_five_elements_payload(wuxing: Mapping[str, Any] | None) -> dict[str, Any]:
    """Publish RuleContext wuxing counts as the customer Five Elements fact."""
    section = dict(wuxing or {})
    counts = dict(section.get("counts") or {})
    payload: dict[str, Any] = {}
    raw_counts: dict[str, float | int | None] = {}
    missing: list[str] = []
    for key in ELEMENT_KEYS:
        entry = dict(section.get(key) or {})
        count = counts.get(key)
        if count is None:
            count = entry.get("count")
        raw_counts[key] = count
        payload[key] = {
            "count": count,
            "status": entry.get("status"),
            "label": ELEMENT_LABELS[key],
        }
        if count in (None, 0, 0.0):
            missing.append(key)
    numeric = [
        (key, float(value))
        for key, value in raw_counts.items()
        if isinstance(value, (int, float))
    ]
    dominant = max(numeric, key=lambda item: item[1])[0] if numeric else None
    payload["counts"] = raw_counts
    payload["status"] = section.get("status")
    payload["dominant"] = dominant
    payload["missing"] = missing
    return payload
