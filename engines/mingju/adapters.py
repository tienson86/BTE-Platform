"""Normalize upstream engine payloads into MingJuContext. No MC-01 logic."""

from __future__ import annotations

from typing import Any, Mapping

from engines.mingju.facts import extract_activations
from engines.mingju.models import MingJuContext
from engines.mingju.versions import PATTERN_SOURCE, SCHEMA_CONTEXT


def _as_str(value: Any) -> str:
    return str(value or "").strip()


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _first(mapping: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        text = _as_str(mapping.get(key))
        if text:
            return text
    return ""


def _hour_present(payload: Mapping[str, Any]) -> bool:
    identity = _mapping(payload.get("identity"))
    pillars = _mapping(identity.get("four_pillars"))
    hour = _mapping(pillars.get("hour"))
    if _first(hour, "stem", "branch"):
        return True
    bazi = _mapping(payload.get("bazi"))
    hour_pillar = _mapping(bazi.get("hour_pillar") or bazi.get("hour"))
    return bool(_first(hour_pillar, "stem", "branch"))


def _chart_id(payload: Mapping[str, Any]) -> str:
    identity = _mapping(payload.get("identity"))
    person = _mapping(identity.get("person"))
    calendar = _mapping(identity.get("calendar")) or _mapping(payload.get("calendar"))
    return (
        _first(payload, "chart_id")
        or _first(calendar, "solar_date")
        or _first(person, "solar_birth")
    )


def build_mingju_context(
    *,
    chart: object | None = None,
    five_elements: object | None = None,
    ten_gods: object | None = None,
    strength: object | None = None,
    temperature: object | None = None,
    pattern: object | None = None,
    useful_god: object | None = None,
    relations: object | None = None,
    metadata: object | None = None,
    payload: Mapping[str, Any] | None = None,
) -> MingJuContext:
    """Normalize canonical upstream contracts. Does not decide Mệnh Cục."""
    data = dict(payload or {})
    if chart is not None and "bazi" not in data:
        data["bazi"] = chart
    if five_elements is not None:
        data["five_elements"] = five_elements
    if ten_gods is not None:
        data["ten_gods"] = ten_gods
    if strength is not None:
        data["strength"] = strength
    if temperature is not None:
        data["temperature"] = temperature
    if pattern is not None:
        data["pattern"] = pattern
    if useful_god is not None:
        data["useful_god"] = useful_god
    _ = relations
    meta = _mapping(metadata)
    pattern_row = _mapping(data.get("pattern"))
    strength_row = _mapping(data.get("strength"))
    useful_row = _mapping(data.get("useful_god"))
    temperature_row = _mapping(data.get("temperature"))
    analysis_id = _first(data, "analysis_id", "request_id") or _first(meta, "analysis_id")
    strength_score = strength_row.get("strength_score")
    numeric_strength = float(strength_score) if isinstance(strength_score, (int, float)) else None
    return MingJuContext(
        schema_version=SCHEMA_CONTEXT,
        analysis_id=analysis_id,
        chart_id=_chart_id(data),
        pattern_code=_first(pattern_row, "pattern", "winning_rule_id"),
        pattern_label=_first(pattern_row, "cach_cuc", "pattern", "tong_cach"),
        pattern_success=bool(pattern_row.get("success", True)) and bool(
            _first(pattern_row, "cach_cuc", "pattern")
        ),
        secondary_labels=tuple(
            str(item) for item in (pattern_row.get("candidate_patterns") or []) if str(item).strip()
        ),
        month_branch=_first(pattern_row, "month_branch"),
        month_main_qi=_first(pattern_row, "month_main_qi"),
        month_main_qi_ten_god=_first(pattern_row, "month_main_qi_ten_god"),
        day_master=_first(pattern_row, "day_master") or _first(_mapping(data.get("bazi")), "day_master"),
        day_master_strength_level=_first(strength_row, "strength_level", "than_vuong_nhuoc"),
        day_master_strength_score=numeric_strength,
        useful_god=_first(
            useful_row, "useful_display", "useful_god", "dung_than", "overall_useful_god"
        ),
        useful_ten_god=_first(useful_row, "useful_ten_god"),
        useful_element=_first(useful_row, "useful_element"),
        climate_state=_first(temperature_row, "climate_state", "temperature_level", "temperature_type"),
        five_elements=_mapping(data.get("five_elements")),
        activations=extract_activations(_mapping(data.get("ten_gods"))),
        hour_present=_hour_present(data),
        source_versions={
            "pattern": PATTERN_SOURCE,
            "strength": "canonical_strength_engine",
            "useful_god": "canonical_useful_god_engine",
            "temperature": "canonical_temperature_engine",
            "ten_gods": "canonical_ten_gods_engine",
        },
    )
