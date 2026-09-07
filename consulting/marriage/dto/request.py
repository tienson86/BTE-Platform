"""Request DTOs for TV-01 Marriage Consulting."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import CanonicalGender
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.models.timing import MarriageLuckWindow


@dataclass(slots=True)
class BirthPlaceInput:
    """Optional birth-place payload. Geocoding is not owned by TV-01."""

    display_name: str | None = None
    province: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None


@dataclass(slots=True)
class MarriagePersonInput:
    """Person input. birth_time remains None when unknown."""

    gender: CanonicalGender
    birth_date: str
    full_name: str | None = None
    birth_time: str | None = None
    birth_place: BirthPlaceInput | None = None
    timezone: str | None = None


@dataclass(slots=True)
class MarriageConsultationOptions:
    """Consultation options. Flags only. No policy override."""

    include_luck: bool | None = None
    luck_window: MarriageLuckWindow | None = None
    include_shen_sha: bool | None = None
    include_feng_shui_reference: bool | None = None
    narrative_level: str | None = None
    language: str | None = None
    audience: str | None = None
    reading_level: str | None = None
    expert_mode: bool | None = None


@dataclass(slots=True)
class RequestMeta:
    """Optional request metadata. Not a decision input."""

    request_id: str | None = None
    idempotency_key: str | None = None
    client: str | None = None


@dataclass(slots=True)
class MarriageConsultationRequest:
    """L0 consultation request."""

    person_a: MarriagePersonInput
    person_b: MarriagePersonInput
    options: MarriageConsultationOptions | None = None
    request_meta: RequestMeta | None = None


@dataclass(slots=True)
class CanonicalBirthInput:
    """Normalized birth input after format mapping. No BaZi calculation."""

    gender: CanonicalGender
    birth_date: str
    full_name: str | None = None
    birth_time: str | None = None
    birth_place: BirthPlaceInput | None = None
    timezone: str | None = None


@dataclass(slots=True)
class NormalizedMarriageRequest:
    """Output of birth-input normalization. No Canonical calculation."""

    person_a: CanonicalBirthInput
    person_b: CanonicalBirthInput
    options: ResolvedMarriageOptions
