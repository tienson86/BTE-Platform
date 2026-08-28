"""Copy identity fields from existing engine / request payloads.

Does not calculate Ganzhi, Hạ Nguyên, luck, bone weight, or narrative.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.identity.four_pillars import four_pillar_identity_from_bazi
from engines.identity.models import (
    BoneWeightIdentity,
    CalendarIdentity,
    CanonicalIdentity,
    InterpretationIdentity,
    LuckIdentity,
    PersonIdentity,
)

_STABLE_OBSERVATION = "sec-observation"
_STABLE_REASONING = "sec-reasoning"
_STABLE_RECOMMENDATION = "sec-recommendation"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _calendar_mapping(calendar: Any) -> Mapping[str, Any]:
    if calendar is None:
        return {}
    if isinstance(calendar, Mapping):
        return calendar
    if hasattr(calendar, "to_dict"):
        data = calendar.to_dict()
        return data if isinstance(data, Mapping) else {}
    return {}


def person_identity_from_sources(
    *,
    person: Mapping[str, Any] | None = None,
    calendar: Any | None = None,
    input_fields: Mapping[str, Any] | None = None,
) -> PersonIdentity:
    """Copy person identity from request metadata and Calendar labels."""
    hints = _mapping(person)
    incoming = _mapping(input_fields)
    cal = _calendar_mapping(calendar)
    solar = cal.get("solar") if isinstance(cal.get("solar"), Mapping) else {}
    hour = solar.get("hour", cal.get("solar_hour"))
    minute = solar.get("minute", cal.get("solar_minute"))
    birth_time = _text(hints.get("birth_time"))
    if not birth_time and hour is not None and minute is not None:
        birth_time = f"{int(hour):02d}:{int(minute):02d}"
    return PersonIdentity(
        full_name=_text(hints.get("full_name") or incoming.get("full_name")),
        gender=_text(hints.get("gender") or incoming.get("gender") or cal.get("gender")),
        solar_birth=_text(hints.get("solar_birth") or cal.get("solar_date")),
        lunar_birth=_text(hints.get("lunar_birth") or cal.get("lunar_date")),
        birth_time=birth_time,
        timezone=_text(
            hints.get("timezone")
            or incoming.get("timezone")
            or cal.get("timezone_name")
            or (_mapping(cal.get("timezone")).get("name"))
        ),
        birth_place=_text(hints.get("birth_place") or incoming.get("birth_place")),
    )


def calendar_identity_from_calendar(calendar: Any | None) -> CalendarIdentity:
    """Copy solar/lunar/term labels already on CalendarResult. No weekday math."""
    cal = _calendar_mapping(calendar)
    term = cal.get("solar_term")
    if isinstance(term, Mapping):
        solar_term = _text(term.get("name"))
        season = _text(term.get("season") or cal.get("season"))
    else:
        solar_term = _text(term or getattr(getattr(calendar, "solar_term", None), "name", ""))
        season = _text(cal.get("season"))
    weekday = cal.get("weekday")
    if weekday is None:
        weekday = getattr(calendar, "weekday", "")
    return CalendarIdentity(
        solar_date=_text(cal.get("solar_date")),
        lunar_date=_text(cal.get("lunar_date")),
        weekday=_text(weekday),
        solar_term=solar_term,
        season=season,
    )


def bone_weight_identity_from_payload(payload: Any | None) -> BoneWeightIdentity:
    """Copy published bone-weight fields. Empty object when the pipeline has none."""
    raw = _mapping(payload)
    if not raw:
        return BoneWeightIdentity()
    return BoneWeightIdentity(
        weight=_text(raw.get("weight") or raw.get("amount") or raw.get("total")),
        classification=_text(raw.get("classification")),
        rating=_text(raw.get("rating") or raw.get("grade")),
    )


def luck_identity_from_payload(payload: Any | None) -> LuckIdentity:
    """Copy current-cycle identity from the already-shaped Luck payload."""
    raw = _mapping(payload)
    if not raw:
        return LuckIdentity()
    cycle = _mapping(raw.get("current_cycle"))
    dayun = _mapping(raw.get("current_dayun"))
    metadata = _mapping(dayun.get("metadata") or raw.get("metadata"))
    ganzhi = _text(cycle.get("gan_zhi") or cycle.get("ganzhi"))
    age = raw.get("current_age_for_luck")
    if age is None:
        age = cycle.get("age_start")
    index = cycle.get("index")
    if index is None:
        index = dayun.get("index")
    year = metadata.get("reference_year") or raw.get("current_year")
    return LuckIdentity(
        current_cycle=ganzhi,
        current_cycle_age=_text(age),
        current_cycle_ganzhi=ganzhi,
        cycle_index=_text(index),
        current_year=_text(year),
    )


def interpretation_identity_from_payload(
    interpretation: Any | None = None,
    narrative: Any | None = None,
) -> InterpretationIdentity:
    """Publish observation/reasoning/recommendation ids. No narrative text."""
    narrative_map = _mapping(narrative)
    interpretation_map = _mapping(interpretation)
    sections = list(narrative_map.get("sections") or interpretation_map.get("sections") or [])
    found: dict[str, str] = {}
    keys: list[str] = []
    for item in sections:
        row = _mapping(item)
        section_id = _text(row.get("id") or row.get("section_id"))
        if not section_id:
            continue
        keys.append(section_id)
        lowered = section_id.casefold()
        if "observation" in lowered and "observation" not in found:
            found["observation"] = section_id
        elif "reasoning" in lowered and "reasoning" not in found:
            found["reasoning"] = section_id
        elif "recommendation" in lowered and "recommendation" not in found:
            found["recommendation"] = section_id
    return InterpretationIdentity(
        observation_id=found.get("observation", _STABLE_OBSERVATION),
        reasoning_id=found.get("reasoning", _STABLE_REASONING),
        recommendation_id=found.get("recommendation", _STABLE_RECOMMENDATION),
        section_keys=keys
        or [_STABLE_OBSERVATION, _STABLE_REASONING, _STABLE_RECOMMENDATION],
    )


def build_canonical_identity(
    *,
    bazi: Any | None = None,
    calendar: Any | None = None,
    person: Mapping[str, Any] | None = None,
    input_fields: Mapping[str, Any] | None = None,
    bone_weight: Any | None = None,
    luck: Any | None = None,
    interpretation: Any | None = None,
    narrative: Any | None = None,
) -> CanonicalIdentity:
    """Assemble identity from existing outputs. Four pillars require Bazi Can Chi."""
    four = four_pillar_identity_from_bazi(bazi) if bazi is not None else None
    return CanonicalIdentity(
        person=person_identity_from_sources(
            person=person,
            calendar=calendar,
            input_fields=input_fields,
        ),
        calendar=calendar_identity_from_calendar(calendar),
        four_pillars=four,
        bone_weight=bone_weight_identity_from_payload(bone_weight),
        luck=luck_identity_from_payload(luck),
        interpretation=interpretation_identity_from_payload(interpretation, narrative),
    )


def canonical_identity_from_bazi(bazi: Any) -> CanonicalIdentity:
    """Analysis Result ``identity`` slice from authoritative Bazi pillars."""
    return build_canonical_identity(bazi=bazi)


def merge_person_into_identity_payload(
    payload: dict[str, Any],
    person: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Copy request person fields onto ``identity.person`` without changing engines."""
    identity = dict(payload.get("identity") or {})
    current = dict(identity.get("person") or {})
    hints = _mapping(person)
    for key in ("full_name", "gender", "birth_place", "timezone"):
        value = _text(hints.get(key))
        if value:
            current[key] = value
    identity["person"] = current
    payload["identity"] = identity
    return payload
