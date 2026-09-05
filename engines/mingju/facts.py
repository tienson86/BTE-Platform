"""Ten God activation facts consumed from canonical upstream payload."""

from __future__ import annotations

from typing import Any, Mapping

from engines.mingju.constants import (
    GOD_FAMILY,
    LAYER_WEIGHT,
    PILLAR_EXPOSURE_WEIGHT,
)
from engines.mingju.models import GodActivation
from engines.ten_gods_engine.constants import GOD_ID_TO_LABEL, LABEL_TO_GOD_ID, TEN_GOD_IDS

_FORBIDDEN = frozenset({"thien_quan", "thienquan", "day_master"})


def _as_str(value: Any) -> str:
    return str(value or "").strip()


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def normalize_god_id(raw: str, label: str = "") -> str:
    """Map engine codes and Vietnamese labels onto canonical Ten God IDs."""
    token = raw.strip().lower().replace("-", "_").replace(" ", "_")
    if token in _FORBIDDEN:
        return ""
    if token in TEN_GOD_IDS:
        return token
    text = label.strip() or raw.strip()
    if text in LABEL_TO_GOD_ID:
        return LABEL_TO_GOD_ID[text]
    lowered = text.lower()
    for name, god_id in LABEL_TO_GOD_ID.items():
        if name.lower() == lowered:
            return god_id
    return ""


def _hidden_layer(item: Mapping[str, Any]) -> str:
    name = _as_str(item.get("position_name")).lower()
    position = _as_str(item.get("hidden_position") or item.get("position"))
    mapping = {
        "primary": "main_qi",
        "1": "main_qi",
        "main_qi": "main_qi",
        "secondary": "middle_qi",
        "2": "middle_qi",
        "middle_qi": "middle_qi",
        "tertiary": "residual_qi",
        "3": "residual_qi",
        "residual_qi": "residual_qi",
    }
    return mapping.get(name) or mapping.get(position) or "branch_hidden"


def _activation(pillar: str, layer: str) -> float:
    pillar_weight = PILLAR_EXPOSURE_WEIGHT.get(pillar, 1.5)
    layer_weight = LAYER_WEIGHT.get(layer, 0.5)
    return round(pillar_weight * layer_weight / 4.0, 4)


def _fact(
    god_id: str,
    pillar: str,
    layer: str,
    stem: str = "",
    element: str = "",
    label: str = "",
) -> GodActivation:
    score = _activation(pillar, layer)
    material = layer == "visible" or (layer == "main_qi" and pillar == "month") or score >= 2.0
    return GodActivation(
        god_id=god_id,
        label=label or GOD_ID_TO_LABEL.get(god_id, god_id),
        family=GOD_FAMILY.get(god_id, ""),
        pillar=pillar,
        layer=layer,
        stem=stem,
        element=element,
        activation=score,
        material=material,
    )


def extract_activations(ten_gods: Mapping[str, Any] | None) -> tuple[GodActivation, ...]:
    """Copy visible/hidden Ten God facts. Does not recalculate identity."""
    data = ten_gods or {}
    found: list[GodActivation] = []
    for item in data.get("visible") or []:
        row = _mapping(item)
        label = _as_str(row.get("ten_god"))
        god_id = normalize_god_id(_as_str(row.get("god_id")), label)
        if not god_id:
            continue
        pillar = _as_str(row.get("pillar")).lower() or "unknown"
        found.append(
            _fact(
                god_id,
                pillar,
                "visible",
                stem=_as_str(row.get("stem")),
                element=_as_str(row.get("element")),
                label=label,
            )
        )
    for item in data.get("hidden") or []:
        row = _mapping(item)
        label = _as_str(row.get("ten_god"))
        god_id = normalize_god_id(_as_str(row.get("god_id")), label)
        if not god_id:
            continue
        pillar = _as_str(row.get("pillar")).lower() or "unknown"
        found.append(
            _fact(
                god_id,
                pillar,
                _hidden_layer(row),
                stem=_as_str(row.get("hidden_stem") or row.get("stem")),
                element=_as_str(row.get("element")),
                label=label,
            )
        )
    found.sort(key=lambda item: (item.god_id, item.pillar, item.layer, item.stem))
    return tuple(found)


def god_power(activations: tuple[GodActivation, ...], god_id: str) -> float:
    """Sum activation for one Ten God."""
    return round(sum(item.activation for item in activations if item.god_id == god_id), 4)


def family_power(activations: tuple[GodActivation, ...], family: str) -> float:
    """Sum activation for a Ten God family."""
    return round(sum(item.activation for item in activations if item.family == family), 4)


def is_material(activations: tuple[GodActivation, ...], god_id: str) -> bool:
    """True when the deity is structurally active, not merely co-present."""
    return any(item.god_id == god_id and item.material for item in activations)


def present_ids(activations: tuple[GodActivation, ...]) -> frozenset[str]:
    """All observed Ten God IDs, including weak hidden presence."""
    return frozenset(item.god_id for item in activations)
