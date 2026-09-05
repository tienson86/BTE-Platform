"""Read-only upstream structural references for Pack 07 context.

This adapter copies identifiers from existing payload keys.
It does not recalculate Pattern, Grade, Strength, or MC-01.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str
from engines.detailed_interpretation_engine.constants import DEFAULT_LOCALE
from engines.detailed_interpretation_engine.enums import EvaluationStatus, HourCompleteness
from engines.detailed_interpretation_engine.value_objects import ChartIdentity, Mc01Reference


@dataclass(frozen=True, slots=True)
class UpstreamStructuralRefs:
    """Immutable upstream IDs collected for InterpretationContext."""

    analysis_id: str = ""
    chart_id: str = ""
    locale: str = DEFAULT_LOCALE
    mingju_result_id: str = ""
    mingju_content_hash: str = ""
    mc01: Mc01Reference = field(default_factory=Mc01Reference)
    pattern_ref: str = ""
    grade_ref: str = ""
    integrity_ref: str = ""
    strength_ref: str = ""
    useful_god_ref: str = ""
    temperature_ref: str = ""
    five_elements_ref: str = ""
    chart_identity: ChartIdentity = field(default_factory=ChartIdentity)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _first_text(mapping: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        text = as_str(mapping.get(key)).strip()
        if text:
            return text
    return ""


def _hour_completeness(four_pillars: Mapping[str, Any]) -> HourCompleteness:
    hour = _mapping(four_pillars.get("hour"))
    stem = as_str(hour.get("stem")).strip()
    branch = as_str(hour.get("branch")).strip()
    if not four_pillars:
        return HourCompleteness.UNKNOWN
    if stem and branch:
        return HourCompleteness.COMPLETE
    if not stem and not branch:
        return HourCompleteness.MISSING
    return HourCompleteness.UNKNOWN


def _mc01_reference(payload: Mapping[str, Any]) -> Mc01Reference:
    # MC-01 exists upstream but is not yet bound into Pack 07 context.
    raw = _mapping(payload.get("mc01")) or _mapping(payload.get("mingju"))
    mingju_result_id = _first_text(raw, "mingju_result_id", "id")
    content_hash = _first_text(raw, "content_hash")
    return Mc01Reference(
        mingju_result_id=mingju_result_id,
        content_hash=content_hash,
        status=EvaluationStatus.NOT_EVALUATED,
    )


def _chart_identity(
    payload: Mapping[str, Any],
    *,
    analysis_id: str,
    chart_id: str,
) -> ChartIdentity:
    identity = _mapping(payload.get("identity"))
    person = _mapping(identity.get("person"))
    calendar = _mapping(identity.get("calendar")) or _mapping(payload.get("calendar"))
    four = _mapping(identity.get("four_pillars"))
    birth_civil = _first_text(person, "solar_birth") or _first_text(calendar, "solar_date")
    timezone_ref = _first_text(person, "timezone") or _first_text(
        _mapping(payload.get("input")), "timezone"
    )
    return ChartIdentity(
        analysis_id=analysis_id,
        chart_id=chart_id,
        person_label_ref=_first_text(person, "full_name"),
        birth_civil=birth_civil,
        calendar_system_ref=_first_text(calendar, "solar_date", "lunar_date"),
        gender_or_party_ref=_first_text(person, "gender")
        or _first_text(_mapping(payload.get("input")), "gender"),
        hour_completeness=_hour_completeness(four),
        timezone_ref=timezone_ref,
    )


def extract_upstream_refs(payload: Mapping[str, Any] | None) -> UpstreamStructuralRefs:
    """Collect immutable upstream references. No interpretation."""
    data = payload or {}
    identity = _mapping(data.get("identity"))
    person = _mapping(identity.get("person"))
    calendar = _mapping(identity.get("calendar")) or _mapping(data.get("calendar"))
    pattern = _mapping(data.get("pattern"))
    score = _mapping(data.get("score"))
    strength = _mapping(data.get("strength"))
    useful_god = _mapping(data.get("useful_god"))
    temperature = _mapping(data.get("temperature"))
    five_elements = _mapping(data.get("five_elements"))
    integrity = _mapping(data.get("integrity"))
    mc01 = _mc01_reference(data)
    analysis_id = _first_text(data, "analysis_id", "request_id")
    chart_id = _first_text(data, "chart_id") or _first_text(calendar, "solar_date") or _first_text(
        person, "solar_birth"
    )
    five_elements_ref = "five_elements" if five_elements else ""
    return UpstreamStructuralRefs(
        analysis_id=analysis_id,
        chart_id=chart_id,
        locale=_first_text(data, "locale") or DEFAULT_LOCALE,
        mingju_result_id=mc01.mingju_result_id,
        mingju_content_hash=mc01.content_hash,
        mc01=mc01,
        pattern_ref=_first_text(pattern, "cach_cuc", "pattern", "tong_cach"),
        grade_ref=_first_text(score, "grade"),
        integrity_ref=_first_text(integrity, "id", "state", "integrity_ref"),
        strength_ref=_first_text(strength, "strength_level", "than_vuong_nhuoc"),
        useful_god_ref=_first_text(
            useful_god, "useful_display", "useful_god", "dung_than", "overall_useful_god"
        ),
        temperature_ref=_first_text(
            temperature, "climate_state", "temperature_level", "temperature_type"
        ),
        five_elements_ref=five_elements_ref,
        chart_identity=_chart_identity(data, analysis_id=analysis_id, chart_id=chart_id),
    )
