"""Copy published Pattern (and optional Temperature) fields. No scoring."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.pattern.constants import EVIDENCE_FIELDS, SOURCE_PATH
from engines.narrative_framework.pattern.models import PatternEvidence

_OBJECT_EXTRA: tuple[str, ...] = (
    "matched_rules",
    "reason",
    "description",
    "confidence",
    "recommendations",
    "success_reason",
    "failure_reason",
    "detected_special_pattern",
    "follow_type",
    "pattern_quality",
    "combination_status",
    "clash_status",
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
            if value not in (None, "", (), []):
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


def bind_pattern_evidence(pattern: Any, temperature: Any = None) -> PatternEvidence:
    """Populate PatternEvidence from a published Pattern payload."""
    data = _payload(pattern)
    temp = _payload(temperature)
    values: dict[str, Any] = {
        "pattern_name": _optional_text(data, "cach_cuc", "pattern_name", "pattern"),
        "pattern_type": _optional_text(data, "follow_type", "pattern_type", "tong_cach"),
        "pattern_class": _optional_text(data, "pattern_class", "pattern_quality", "pattern"),
        "temperature_state": _optional_text(
            temp,
            "climate_state_label",
            "climate_state",
            "temperature_level",
            "temperature_state",
        ),
        "dieu_hau": _optional_text(data, "dieu_hau"),
        "special_pattern": _optional_text(
            data,
            "detected_special_pattern",
            "special_pattern",
        ),
        "winning_rule": _optional_text(data, "winning_rule_id", "winning_rule"),
        "matched_rules": _text_tuple(data, "matched_rules"),
        "reasoning": _optional_text(data, "reason", "success_reason", "reasoning", "description"),
        "confidence": _optional_float(data, "confidence"),
        "evidence_compact": _optional_text(data, "evidence_compact"),
        "success_reason": _optional_text(data, "success_reason"),
        "failure_reason": _optional_text(data, "failure_reason"),
        "clash_status": _optional_text(data, "clash_status"),
        "combination_status": _optional_text(data, "combination_status"),
        "dung_than": _optional_text(data, "dung_than"),
        "hy_than": _optional_text(data, "hy_than"),
        "ky_than": _optional_text(data, "ky_than"),
        "recommendations": _text_tuple(data, "recommendations"),
        "metadata": {
            key: data[key]
            for key in (
                "pattern_rank",
                "fallback_used",
                "ug_override_eligible",
                "qualification_level",
                "month_branch",
                "month_main_qi",
            )
            if key in data and data[key] not in (None, "")
        },
    }
    missing = tuple(name for name in EVIDENCE_FIELDS if values[name] in (None, "", ()))
    return PatternEvidence(
        missing=missing,
        source_path=SOURCE_PATH,
        **values,
    )
