"""Parse public JSON into the frozen consultation request. No defaults invented."""

from __future__ import annotations

from typing import Any, Mapping

from consulting.marriage.dto.request import (
    BirthPlaceInput,
    MarriageConsultationOptions,
    MarriageConsultationRequest,
    MarriagePersonInput,
    RequestMeta,
)
from consulting.marriage.exceptions import MarriageValidationError
from consulting.marriage.models.enums import CanonicalGender
from consulting.marriage.models.timing import MarriageLuckWindow

_ALLOWED_GENDERS = {item.value: item for item in CanonicalGender}


def parse_consultation_request(
    payload: Mapping[str, Any],
    *,
    idempotency_key: str | None = None,
) -> MarriageConsultationRequest:
    """Build a request from public JSON. Missing gender is an error, not a default."""
    person_a = payload.get("person_a")
    person_b = payload.get("person_b")
    if not isinstance(person_a, Mapping) or not isinstance(person_b, Mapping):
        raise MarriageValidationError("person_required")
    meta_payload = payload.get("request_meta")
    meta = _parse_meta(meta_payload if isinstance(meta_payload, Mapping) else None, idempotency_key)
    options_payload = payload.get("options")
    return MarriageConsultationRequest(
        person_a=_parse_person(person_a, "person_a"),
        person_b=_parse_person(person_b, "person_b"),
        options=_parse_options(options_payload if isinstance(options_payload, Mapping) else None),
        request_meta=meta,
    )


def request_fingerprint(request: MarriageConsultationRequest) -> str:
    """Stable request identity for idempotency conflict checks. Not an idempotency key."""
    return "|".join(
        [
            _person_fingerprint(request.person_a),
            _person_fingerprint(request.person_b),
            _options_fingerprint(request.options),
        ]
    )


def _parse_person(payload: Mapping[str, Any], label: str) -> MarriagePersonInput:
    """Parse one person. Do not default gender or birth time."""
    raw_gender = payload.get("gender")
    if raw_gender is None or raw_gender == "":
        raise MarriageValidationError(f"{label}_gender_required")
    gender = _ALLOWED_GENDERS.get(str(raw_gender).strip().lower())
    if gender is None:
        raise MarriageValidationError(f"{label}_gender_invalid")
    birth_date = payload.get("birth_date")
    if not birth_date:
        raise MarriageValidationError(f"{label}_birth_date_required")
    birth_time = payload.get("birth_time")
    if birth_time == "":
        birth_time = None
    place_payload = payload.get("birth_place")
    return MarriagePersonInput(
        gender=gender,
        birth_date=str(birth_date),
        full_name=_optional_str(payload.get("full_name")),
        birth_time=_optional_str(birth_time),
        birth_place=_parse_place(place_payload) if isinstance(place_payload, Mapping) else None,
        timezone=_optional_str(payload.get("timezone")),
    )


def _parse_place(payload: Mapping[str, Any]) -> BirthPlaceInput:
    """Parse optional birth place. Do not invent coordinates."""
    return BirthPlaceInput(
        display_name=_optional_str(payload.get("display_name")),
        province=_optional_str(payload.get("province")),
        city=_optional_str(payload.get("city")),
        country=_optional_str(payload.get("country")),
        latitude=_optional_float(payload.get("latitude")),
        longitude=_optional_float(payload.get("longitude")),
    )


def _parse_options(payload: Mapping[str, Any] | None) -> MarriageConsultationOptions | None:
    """Parse approved client options only. No policy overrides."""
    if payload is None:
        return None
    window_payload = payload.get("luck_window")
    window = None
    if isinstance(window_payload, Mapping):
        start = window_payload.get("start_year")
        end = window_payload.get("end_year")
        if start is None or end is None:
            raise MarriageValidationError("luck_window_invalid")
        window = MarriageLuckWindow(start_year=int(start), end_year=int(end))
    return MarriageConsultationOptions(
        include_luck=_optional_bool(payload.get("include_luck")),
        luck_window=window,
        include_shen_sha=_optional_bool(payload.get("include_shen_sha")),
        include_feng_shui_reference=_optional_bool(payload.get("include_feng_shui_reference")),
        narrative_level=_optional_str(payload.get("narrative_level") or payload.get("reading_level")),
        language=_optional_str(payload.get("language")),
        audience=_optional_str(payload.get("audience")),
        reading_level=_optional_str(payload.get("reading_level")),
        expert_mode=_optional_bool(payload.get("expert_mode")),
    )


def _parse_meta(payload: Mapping[str, Any] | None, header_key: str | None) -> RequestMeta | None:
    """Merge header idempotency key over body metadata."""
    body_key = _optional_str(payload.get("idempotency_key") if payload else None)
    key = header_key or body_key
    request_id = _optional_str(payload.get("request_id") if payload else None)
    client = _optional_str(payload.get("client") if payload else None)
    if key is None and request_id is None and client is None:
        return None
    return RequestMeta(request_id=request_id, idempotency_key=key, client=client)


def _person_fingerprint(person: MarriagePersonInput) -> str:
    """Fingerprint person identity fields. Not used as the idempotency key."""
    return ",".join(
        [
            person.gender.value,
            person.birth_date,
            person.birth_time or "",
            person.full_name or "",
            person.timezone or "",
        ]
    )


def _options_fingerprint(options: MarriageConsultationOptions | None) -> str:
    """Fingerprint approved options."""
    if options is None:
        return ""
    window = ""
    if options.luck_window is not None:
        window = f"{options.luck_window.start_year}-{options.luck_window.end_year}"
    return ",".join(
        [
            str(options.language or ""),
            str(options.audience or ""),
            str(options.reading_level or ""),
            str(options.expert_mode),
            window,
        ]
    )


def _optional_str(value: object | None) -> str | None:
    """Return a stripped string or None. Empty string becomes None."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_bool(value: object | None) -> bool | None:
    """Return a bool when provided. Do not default missing flags."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise MarriageValidationError("option_flag_invalid")


def _optional_float(value: object | None) -> float | None:
    """Return a float when provided."""
    if value is None or value == "":
        return None
    return float(str(value))
