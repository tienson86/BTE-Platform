"""Birth-input normalization. Format only. No BaZi calculation."""

from __future__ import annotations

from consulting.marriage.dto.request import (
    BirthPlaceInput,
    CanonicalBirthInput,
    MarriageConsultationOptions,
    MarriageConsultationRequest,
    MarriagePersonInput,
    NormalizedMarriageRequest,
)
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.models.timing import MarriageLuckWindow


def normalize_marriage_request(
    request: MarriageConsultationRequest,
) -> NormalizedMarriageRequest:
    """Normalize person and option formats. Does not infer gender or birth time."""
    return NormalizedMarriageRequest(
        person_a=_normalize_person(request.person_a),
        person_b=_normalize_person(request.person_b),
        options=_normalize_options(request.options),
    )


def _normalize_person(person: MarriagePersonInput) -> CanonicalBirthInput:
    """Trim display text and keep canonical date/time strings."""
    place = person.birth_place
    normalized_place = None
    if place is not None:
        normalized_place = BirthPlaceInput(
            display_name=_trim(place.display_name),
            province=_trim(place.province),
            city=_trim(place.city),
            country=_trim(place.country),
            latitude=place.latitude,
            longitude=place.longitude,
        )
    return CanonicalBirthInput(
        gender=person.gender,
        birth_date=person.birth_date.strip(),
        full_name=_trim(person.full_name),
        birth_time=_trim(person.birth_time),
        birth_place=normalized_place,
        timezone=_trim(person.timezone),
    )


def _normalize_options(
    options: MarriageConsultationOptions | None,
) -> ResolvedMarriageOptions:
    """Copy option flags without applying policy defaults."""
    if options is None:
        return ResolvedMarriageOptions()
    window = options.luck_window
    resolved_window = None
    if window is not None:
        resolved_window = MarriageLuckWindow(
            start_year=window.start_year,
            end_year=window.end_year,
        )
    return ResolvedMarriageOptions(
        include_luck=options.include_luck,
        luck_window=resolved_window,
        include_shen_sha=options.include_shen_sha,
        include_feng_shui_reference=options.include_feng_shui_reference,
        narrative_level=_trim(options.narrative_level),
        language=_trim(options.language),
        audience=_trim(options.audience),
        reading_level=_trim(options.reading_level),
        expert_mode=options.expert_mode,
    )


def _trim(value: str | None) -> str | None:
    """Trim whitespace. Empty strings become None."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
