"""Copy published Luck fields. No scoring."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.luck.constants import EVIDENCE_FIELDS, SOURCE_PATH
from engines.narrative_framework.luck.models import LuckEvidence

_SKIP_REASONS: frozenset[str] = frozenset(
    {
        "luck_engine_foundation_no_calculation",
        "luck_providers_unavailable",
        "no_business_rule_defined",
    }
)


def _payload(raw: Any) -> dict[str, Any]:
    if raw is None:
        return {}
    if hasattr(raw, "to_portal_dict"):
        data = dict(raw.to_portal_dict())
    elif hasattr(raw, "to_dict"):
        data = dict(raw.to_dict())
    elif isinstance(raw, Mapping):
        data = dict(raw)
    else:
        return {}
    return _flatten(data)


def _flatten(data: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(data)
    for nested_key in ("timeline_result", "analysis_result", "metadata"):
        nested = data.get(nested_key)
        if not isinstance(nested, Mapping):
            continue
        for key, value in nested.items():
            if key not in merged or merged[key] in (None, "", (), []):
                merged[key] = value
    return merged


def _optional_float(data: Mapping[str, Any], *keys: str) -> float | None:
    for key in keys:
        if key not in data or data[key] is None or data[key] == "":
            continue
        try:
            return float(data[key])
        except (TypeError, ValueError):
            continue
    return None


def _optional_int(data: Mapping[str, Any], *keys: str) -> int | None:
    for key in keys:
        if key not in data or data[key] is None or data[key] == "":
            continue
        try:
            return int(data[key])
        except (TypeError, ValueError):
            continue
    return None


def _optional_text(data: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        if key not in data or data[key] is None:
            continue
        text = str(data[key]).strip()
        if text:
            return text
    return ""


def _text_tuple(data: Mapping[str, Any], *keys: str) -> tuple[str, ...]:
    for key in keys:
        value = data.get(key)
        if value is None or value == "":
            continue
        if isinstance(value, (list, tuple)):
            return tuple(str(item).strip() for item in value if str(item).strip())
        text = str(value).strip()
        if text:
            return (text,)
    return ()


def _period_text(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value.strip()
    if hasattr(value, "ganzhi") and getattr(value, "ganzhi"):
        return str(value.ganzhi).strip()
    if isinstance(value, Mapping):
        return _optional_text(value, "ganzhi", "label", "display", "current_cycle")
    return str(value).strip()


def _period_int(value: Any, *keys: str) -> int | None:
    if isinstance(value, Mapping):
        return _optional_int(value, *keys)
    for key in keys:
        raw = getattr(value, key, None) if value is not None else None
        if raw in (None, ""):
            continue
        try:
            return int(raw)
        except (TypeError, ValueError):
            continue
    return None


def _timeline_text(data: Mapping[str, Any]) -> str:
    value = data.get("timeline")
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (list, tuple)):
        parts = [str(item).strip() for item in value if str(item).strip()]
        return " · ".join(parts)
    if isinstance(value, Mapping):
        return _optional_text(value, "display", "label", "timeline_id")
    return _optional_text(data, "timeline_display", "timeline_label")


def bind_luck_evidence(luck: Any) -> LuckEvidence:
    """Populate LuckEvidence from a published Luck payload."""
    data = _payload(luck)
    dayun = data.get("current_dayun", data.get("current_cycle"))
    liunian = data.get("current_liunian")
    index = _optional_int(data, "cycle_index")
    if index is None:
        index = _period_int(dayun, "index", "cycle_index")
    age = _optional_int(data, "age")
    if age is None:
        age = _period_int(dayun, "start_age", "age")
    year = _optional_int(data, "reference_year")
    if year is None:
        year = _period_int(liunian, "year")
    if year is None:
        year = _period_int(dayun, "start_year")
    reasoning = _optional_text(data, "luck_summary", "reasoning", "reason")
    if reasoning in _SKIP_REASONS:
        reasoning = ""
    cycle_raw = data.get("current_cycle")
    cycle = cycle_raw.strip() if isinstance(cycle_raw, str) else ""
    values: dict[str, Any] = {
        "current_cycle": cycle or _period_text(data.get("current_dayun") or cycle_raw),
        "current_liunian": _optional_text(data, "current_liunian_display")
        or _period_text(liunian),
        "cycle_index": index,
        "age": age,
        "reference_year": year,
        "timeline": _timeline_text(data),
        "reasoning": reasoning,
        "confidence": _optional_float(data, "confidence"),
        "recommendations": _text_tuple(data, "recommendations", "luck_recommendations"),
        "luck_stage": _optional_text(data, "luck_stage", "stage"),
        "support_elements": _text_tuple(data, "support_elements"),
        "attack_elements": _text_tuple(data, "attack_elements"),
        "support_level": _optional_text(data, "support_level"),
        "attack_level": _optional_text(data, "attack_level"),
    }
    missing = tuple(name for name in EVIDENCE_FIELDS if values[name] in (None, "", ()))
    return LuckEvidence(
        missing=missing,
        source_path=SOURCE_PATH,
        **values,
    )
