"""Read-only upstream Ten God facts. Does not recalculate identity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str
from engines.detailed_interpretation_engine.enums import DayMasterBand, HourCompleteness
from engines.detailed_interpretation_engine.ten_gods.constants import (
    CANONICAL_TEN_GOD_IDS,
    DAY_MASTER_LABELS,
    FORBIDDEN_ALIAS_IDS,
    GOD_ID_TO_LABEL,
    HIDDEN_LAYER_BY_POSITION,
    LABEL_TO_GOD_ID,
    MODERATE_STRENGTH_LEVELS,
    PILLAR_STEM_LAYER,
    STRONG_STRENGTH_LEVELS,
    WEAK_STRENGTH_LEVELS,
)
from engines.detailed_interpretation_engine.ten_gods.models import TenGodOccurrence


@dataclass(frozen=True, slots=True)
class UpstreamTenGodFacts:
    """Canonical identity facts plus consumed structural refs."""

    available: bool = False
    occurrences: dict[str, tuple[TenGodOccurrence, ...]] = field(default_factory=dict)
    elements: dict[str, tuple[str, ...]] = field(default_factory=dict)
    dominant_ids: tuple[str, ...] = ()
    hour_completeness: HourCompleteness = HourCompleteness.UNKNOWN
    day_master_band: DayMasterBand = DayMasterBand.UNRESOLVED
    pattern_text: str = ""
    useful_ten_god_ids: tuple[str, ...] = ()
    favorable_ten_god_ids: tuple[str, ...] = ()
    unfavorable_ten_god_ids: tuple[str, ...] = ()
    useful_elements: tuple[str, ...] = ()
    favorable_elements: tuple[str, ...] = ()
    unfavorable_elements: tuple[str, ...] = ()
    mc01_bound: bool = False
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()
    purity_ref: str = ""


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _normalize_god_id(raw: str, label: str) -> str:
    token = raw.strip().lower().replace("-", "_")
    if token in FORBIDDEN_ALIAS_IDS or token == "qi_sha":
        return "qi_sha"
    if token in CANONICAL_TEN_GOD_IDS:
        return token
    text = label.strip()
    if text in DAY_MASTER_LABELS:
        return ""
    if text in LABEL_TO_GOD_ID:
        return LABEL_TO_GOD_ID[text]
    lowered = text.lower()
    for name, god_id in LABEL_TO_GOD_ID.items():
        if name.lower() == lowered:
            return god_id
    return ""


def _hidden_layer(item: Mapping[str, Any]) -> str:
    name = as_str(item.get("position_name")).strip().lower()
    position = as_str(item.get("hidden_position")).strip()
    return HIDDEN_LAYER_BY_POSITION.get(name) or HIDDEN_LAYER_BY_POSITION.get(position) or "branch_hidden"


def _from_visible(item: Mapping[str, Any], index: int) -> tuple[str, TenGodOccurrence] | None:
    label = as_str(item.get("ten_god"))
    god_id = _normalize_god_id(as_str(item.get("god_id")), label)
    if not god_id:
        return None
    pillar = as_str(item.get("pillar")).strip().lower()
    layer = PILLAR_STEM_LAYER.get(pillar, "year_stem")
    return god_id, TenGodOccurrence(
        pillar=pillar,
        layer=layer,
        stem=as_str(item.get("stem")),
        visible=True,
        evidence_id=as_str(item.get("evidence")) or f"E-DI-TG-{god_id}-vis-{index}",
    )


def _from_hidden(item: Mapping[str, Any], index: int) -> tuple[str, TenGodOccurrence] | None:
    label = as_str(item.get("ten_god"))
    god_id = _normalize_god_id(as_str(item.get("god_id")), label)
    if not god_id:
        return None
    pillar = as_str(item.get("pillar")).strip().lower()
    layer = _hidden_layer(item)
    return god_id, TenGodOccurrence(
        pillar=pillar,
        layer=layer,
        stem=as_str(item.get("hidden_stem") or item.get("stem")),
        branch=as_str(item.get("branch")),
        visible=False,
        evidence_id=as_str(item.get("evidence")) or f"E-DI-TG-{god_id}-hid-{index}",
    )


def _collect_occurrences(
    payload: Mapping[str, Any],
) -> tuple[dict[str, list[TenGodOccurrence]], dict[str, list[str]]]:
    bucket: dict[str, list[TenGodOccurrence]] = {god_id: [] for god_id in CANONICAL_TEN_GOD_IDS}
    elements: dict[str, list[str]] = {god_id: [] for god_id in CANONICAL_TEN_GOD_IDS}
    for index, item in enumerate(payload.get("visible") or ()):
        if not isinstance(item, Mapping):
            continue
        parsed = _from_visible(item, index)
        if parsed is None:
            continue
        god_id, occurrence = parsed
        bucket[god_id].append(occurrence)
        element = as_str(item.get("element")).strip()
        if element:
            elements[god_id].append(element)
    for index, item in enumerate(payload.get("hidden") or ()):
        if not isinstance(item, Mapping):
            continue
        parsed = _from_hidden(item, index)
        if parsed is None:
            continue
        god_id, occurrence = parsed
        bucket[god_id].append(occurrence)
        element = as_str(item.get("element")).strip()
        if element:
            elements[god_id].append(element)
    return bucket, elements


def _day_master_band(raw: str) -> DayMasterBand:
    token = raw.strip().lower()
    if token in WEAK_STRENGTH_LEVELS:
        return DayMasterBand.WEAK
    if token in STRONG_STRENGTH_LEVELS:
        return DayMasterBand.STRONG
    if token in MODERATE_STRENGTH_LEVELS:
        return DayMasterBand.MODERATE
    return DayMasterBand.UNRESOLVED


def _id_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str) and value.strip():
        return (value.strip(),)
    if not isinstance(value, (list, tuple)):
        return ()
    found: list[str] = []
    for item in value:
        if isinstance(item, Mapping):
            token = as_str(item.get("id") or item.get("damage_id") or item.get("rescue_id")).strip()
        else:
            token = as_str(item).strip()
        if token and token not in found:
            found.append(token)
    return tuple(found)


def _ids_from_labels(values: Any) -> tuple[str, ...]:
    found: list[str] = []
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, (list, tuple)):
        return ()
    for item in values:
        text = as_str(item).strip()
        god_id = _normalize_god_id(text, text)
        if god_id and god_id not in found:
            found.append(god_id)
    return tuple(found)


def _elements(values: Any) -> tuple[str, ...]:
    if isinstance(values, str) and values.strip():
        return (values.strip(),)
    if not isinstance(values, (list, tuple)):
        return ()
    return tuple(as_str(item).strip() for item in values if as_str(item).strip())


def has_ten_gods_facts(payload: Mapping[str, Any] | None) -> bool:
    """True when canonical Ten Gods identity payload is present."""
    data = payload or {}
    block = _mapping(data.get("ten_gods")) or _mapping(data.get("ten_gods_result"))
    return bool(block.get("visible") or block.get("hidden") or block.get("source"))


def extract_ten_god_facts(payload: Mapping[str, Any] | None) -> UpstreamTenGodFacts:
    """Copy identity and structural refs. Do not recalculate Ten Gods."""
    data = payload or {}
    block = _mapping(data.get("ten_gods")) or _mapping(data.get("ten_gods_result"))
    if not block:
        return UpstreamTenGodFacts()
    bucket, elements = _collect_occurrences(block)
    dominant_raw = _mapping(block.get("dominant")).get("primary_god_ids")
    identity = _mapping(data.get("identity"))
    four = _mapping(identity.get("four_pillars"))
    hour = _mapping(four.get("hour"))
    hour_state = HourCompleteness.UNKNOWN
    if hour.get("stem") and hour.get("branch"):
        hour_state = HourCompleteness.COMPLETE
    elif four and not hour.get("stem") and not hour.get("branch"):
        hour_state = HourCompleteness.MISSING
    strength = _mapping(data.get("strength"))
    useful = _mapping(data.get("useful_god"))
    pattern = _mapping(data.get("pattern"))
    mc01 = _mapping(data.get("mc01")) or _mapping(data.get("mingju"))
    useful_ids = _ids_from_labels(useful.get("useful_ten_god") or useful.get("useful_god"))
    damage_ids = _id_tuple(mc01.get("damage_ids") or mc01.get("damage") or data.get("damage_ids"))
    rescue_ids = _id_tuple(mc01.get("rescue_ids") or mc01.get("rescue") or data.get("rescue_ids"))
    return UpstreamTenGodFacts(
        available=True,
        occurrences={key: tuple(items) for key, items in bucket.items()},
        elements={key: tuple(dict.fromkeys(items)) for key, items in elements.items()},
        dominant_ids=_ids_from_labels(dominant_raw),
        hour_completeness=hour_state,
        day_master_band=_day_master_band(as_str(strength.get("strength_level"))),
        pattern_text=" ".join(
            part
            for part in (
                as_str(pattern.get("cach_cuc")),
                as_str(pattern.get("pattern")),
                as_str(pattern.get("tong_cach")),
            )
            if part
        ),
        useful_ten_god_ids=useful_ids,
        favorable_ten_god_ids=_ids_from_labels(useful.get("favorable_gods")),
        unfavorable_ten_god_ids=_ids_from_labels(useful.get("unfavorable_gods")),
        useful_elements=_elements(useful.get("useful_element")),
        favorable_elements=_elements(useful.get("favorable_gods"))
        if not _ids_from_labels(useful.get("favorable_gods"))
        else (),
        unfavorable_elements=_elements(useful.get("unfavorable_gods"))
        if not _ids_from_labels(useful.get("unfavorable_gods"))
        else (),
        mc01_bound=bool(as_str(mc01.get("mingju_result_id") or mc01.get("id"))),
        damage_ids=damage_ids,
        rescue_ids=rescue_ids,
        purity_ref=as_str(mc01.get("purity")).strip(),
    )


def pattern_mentions(pattern_text: str, god_id: str) -> bool:
    """True when consumed Pattern label names this Ten God."""
    if not pattern_text:
        return False
    label = GOD_ID_TO_LABEL.get(god_id, "")
    lowered = pattern_text.lower()
    return bool(label and label.lower() in lowered) or god_id in lowered
