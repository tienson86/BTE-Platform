"""Person and canonical version reference models."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import CanonicalGender


@dataclass(slots=True)
class CanonicalVersionReference:
    """Versions of Canonical engines used for a person analysis."""

    calendar_version: str | None = None
    bazi_version: str | None = None
    strength_version: str | None = None
    pattern_version: str | None = None
    useful_god_version: str | None = None
    ten_gods_version: str | None = None
    luck_version: str | None = None
    shen_sha_version: str | None = None


@dataclass(slots=True)
class BirthDataQuality:
    """Input data quality. Not a compatibility score."""

    birth_date_known: bool
    birth_time_known: bool
    birth_place_known: bool
    timezone_resolved: bool
    completeness_score: float
    limitations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriagePersonReference:
    """Reference to a person after Canonical analysis."""

    analysis_id: str
    gender: CanonicalGender
    birth_data_quality: BirthDataQuality
    canonical_version: CanonicalVersionReference
    person_id: str | None = None
    display_name: str | None = None
