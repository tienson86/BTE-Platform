"""Copy published Useful God fields. No scoring."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.useful_god.constants import EVIDENCE_FIELDS, SOURCE_PATH
from engines.narrative_framework.useful_god.models import UsefulGodEvidence

_OBJECT_EXTRA: tuple[str, ...] = (
    "recommendations",
    "season_reason",
    "strength_reason",
    "temperature_reason",
    "balance_reason",
)


def _payload(raw: Any) -> dict[str, Any]:
    if raw is None:
        return {}
    if hasattr(raw, "to_portal_dict"):
        data = dict(raw.to_portal_dict())
        for key in _OBJECT_EXTRA:
            if data.get(key):
                continue
            value = getattr(raw, key, None)
            if value:
                data[key] = value
        return data
    if hasattr(raw, "to_dict"):
        return dict(raw.to_dict())
    if isinstance(raw, Mapping):
        return dict(raw)
    return {}


def _optional_float(data: Mapping[str, Any], *keys: str) -> float | None:
    for key in keys:
        if key not in data or data[key] is None or data[key] == "":
            continue
        try:
            return float(data[key])
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


def _optional_bool(data: Mapping[str, Any], *keys: str) -> bool:
    for key in keys:
        if key not in data or data[key] in (None, ""):
            continue
        return bool(data[key])
    return False


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


def bind_useful_god_evidence(useful_god: Any) -> UsefulGodEvidence:
    """Populate UsefulGodEvidence from a published Useful God payload."""
    data = _payload(useful_god)
    values: dict[str, Any] = {
        "useful_god": _optional_text(data, "useful_god", "overall_useful_god"),
        "useful_display": _optional_text(data, "useful_display"),
        "useful_ten_god": _optional_text(data, "useful_ten_god"),
        "useful_stem": _optional_text(data, "useful_stem"),
        "useful_element": _optional_text(data, "useful_element"),
        "favorable_gods": _text_tuple(data, "favorable_gods"),
        "unfavorable_gods": _text_tuple(data, "unfavorable_gods"),
        "favorable_display": _optional_text(data, "favorable_display"),
        "unfavorable_display": _optional_text(data, "unfavorable_display"),
        "winning_rule_id": _optional_text(data, "winning_rule_id"),
        "winning_rule_group": _optional_text(data, "winning_rule_group"),
        "reasoning": _optional_text(data, "reasoning"),
        "confidence": _optional_float(data, "confidence"),
        "matched_rules": _text_tuple(data, "matched_rules"),
        "recommendations": _text_tuple(data, "recommendations"),
        "climate_display": _optional_text(data, "climate_display", "climate_candidate"),
        "climate_reason": _optional_text(data, "climate_reason"),
        "climate_preference_label": _optional_text(data, "climate_preference_label"),
        "strength_reason": _optional_text(data, "strength_reason"),
        "season_reason": _optional_text(data, "season_reason"),
        "temperature_reason": _optional_text(data, "temperature_reason"),
        "balance_reason": _optional_text(data, "balance_reason"),
        "overall_incomplete": _optional_bool(data, "overall_incomplete"),
    }
    missing = tuple(
        name
        for name in EVIDENCE_FIELDS
        if values[name] in (None, "", ())
    )
    return UsefulGodEvidence(
        missing=missing,
        source_path=SOURCE_PATH,
        **values,
    )
