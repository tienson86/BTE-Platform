"""Copy published Strength (and optional Temperature) fields. No scoring."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.strength.constants import EVIDENCE_FIELDS, SOURCE_PATH
from engines.narrative_framework.strength.models import StrengthEvidence


def _payload(raw: Any) -> dict[str, Any]:
    if raw is None:
        return {}
    if hasattr(raw, "to_portal_dict"):
        return dict(raw.to_portal_dict())
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


def _special_entries(
    data: Mapping[str, Any],
) -> tuple[tuple[str, ...], tuple[dict[str, Any], ...]]:
    metadata = data.get("metadata")
    if not isinstance(metadata, Mapping):
        return (), ()
    trace = metadata.get("trace") if isinstance(metadata.get("trace"), Mapping) else metadata
    analysis = trace.get("analysis") if isinstance(trace, Mapping) else None
    if not isinstance(analysis, Mapping):
        return (), ()
    ids: list[str] = []
    details: list[dict[str, Any]] = []
    for item in analysis.get("special_matches") or []:
        if isinstance(item, Mapping):
            details.append(dict(item))
            rule_id = str(item.get("rule_id") or item.get("id") or "").strip()
            if rule_id:
                ids.append(rule_id)
            continue
        text = str(item).strip()
        if text:
            ids.append(text)
    return tuple(ids), tuple(details)


def bind_strength_evidence(
    strength: Any,
    temperature: Any = None,
) -> StrengthEvidence:
    """Populate StrengthEvidence from published Strength / Temperature payloads."""
    data = _payload(strength)
    temp = _payload(temperature)
    special_ids, special_details = _special_entries(data)
    values: dict[str, Any] = {
        "season_strength": _optional_float(data, "season_score", "season_strength"),
        "root_strength": _optional_float(data, "root_score", "root_strength"),
        "support_strength": _optional_float(data, "support_score", "support_strength"),
        "control_strength": _optional_float(data, "control_score", "control_strength"),
        "drain_strength": _optional_float(data, "drain_score", "drain_strength"),
        "temperature_state": _optional_text(
            temp,
            "climate_state_label",
            "climate_state",
            "temperature_level",
            "temperature_state",
        ),
        "special_rules": special_ids,
        "special_rule_details": special_details,
        "confidence": _optional_float(data, "confidence"),
        "strength_level": _optional_text(data, "strength_level").lower(),
        "score": _optional_float(data, "strength_score", "score"),
        "reasoning": _optional_text(data, "reasoning"),
        "evidence_compact": _optional_text(data, "evidence_compact"),
    }
    missing = tuple(
        name
        for name in EVIDENCE_FIELDS
        if (name == "special_rules" and not values["special_rules"])
        or (name != "special_rules" and values[name] in (None, "", ()))
    )
    return StrengthEvidence(
        missing=missing,
        source_path=SOURCE_PATH,
        **values,
    )
