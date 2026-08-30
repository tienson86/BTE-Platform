"""Canonical identity models. Presentation contract only — not an engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PersonIdentity:
    """Request + calendar identity. No engine calculation."""

    full_name: str = ""
    gender: str = ""
    solar_birth: str = ""
    lunar_birth: str = ""
    birth_time: str = ""
    timezone: str = ""
    birth_place: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize person identity."""
        return {
            "full_name": self.full_name,
            "gender": self.gender,
            "solar_birth": self.solar_birth,
            "lunar_birth": self.lunar_birth,
            "birth_time": self.birth_time,
            "timezone": self.timezone,
            "birth_place": self.birth_place,
        }


@dataclass(slots=True)
class CalendarIdentity:
    """Calendar identity copied from CalendarResult. No new fields computed."""

    solar_date: str = ""
    lunar_date: str = ""
    weekday: str = ""
    solar_term: str = ""
    season: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize calendar identity."""
        return {
            "solar_date": self.solar_date,
            "lunar_date": self.lunar_date,
            "weekday": self.weekday,
            "solar_term": self.solar_term,
            "season": self.season,
        }


@dataclass(slots=True)
class PillarIdentity:
    """One Four Pillars cell. Year/Month Cung follow Calendar Tam Nguyên when published."""

    stem: str
    branch: str
    can_chi: str
    nayin_element: str
    cung_phi: str
    pillar_type: str

    def to_dict(self) -> dict[str, str]:
        """Serialize one pillar identity cell."""
        return {
            "stem": self.stem,
            "branch": self.branch,
            "can_chi": self.can_chi,
            "nayin_element": self.nayin_element,
            "cung_phi": self.cung_phi,
            "pillar_type": self.pillar_type,
        }


@dataclass(slots=True)
class FourPillarIdentity:
    """Year / Month / Day / Hour identity."""

    year: PillarIdentity
    month: PillarIdentity
    day: PillarIdentity
    hour: PillarIdentity

    def to_dict(self) -> dict[str, dict[str, str]]:
        """Serialize ``year`` / ``month`` / ``day`` / ``hour`` cells."""
        return {
            "year": self.year.to_dict(),
            "month": self.month.to_dict(),
            "day": self.day.to_dict(),
            "hour": self.hour.to_dict(),
        }


@dataclass(slots=True)
class BoneWeightIdentity:
    """Existing Cân Xương output, or empty when the pipeline has none."""

    weight: str = ""
    classification: str = ""
    rating: str = ""
    summary: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize bone-weight identity. Empty strings when unavailable."""
        return {
            "weight": self.weight,
            "classification": self.classification,
            "rating": self.rating,
            "summary": self.summary,
        }


@dataclass(slots=True)
class LuckIdentity:
    """Luck identity copied from LuckEngine output. No derived values."""

    current_cycle: str = ""
    current_cycle_age: str = ""
    current_cycle_ganzhi: str = ""
    cycle_index: str = ""
    reference_year: str = ""
    current_year: str = ""
    current_liunian_ganzhi: str = ""
    current_liunian_year: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize luck identity. Empty strings when unavailable."""
        return {
            "current_cycle": self.current_cycle,
            "current_cycle_age": self.current_cycle_age,
            "current_cycle_ganzhi": self.current_cycle_ganzhi,
            "cycle_index": self.cycle_index,
            "reference_year": self.reference_year,
            "current_year": self.current_year,
            "current_liunian_ganzhi": self.current_liunian_ganzhi,
            "current_liunian_year": self.current_liunian_year,
        }


@dataclass(slots=True)
class InterpretationIdentity:
    """Section identifiers and already-published conclusion/action copies."""

    observation_id: str = "sec-observation"
    reasoning_id: str = "sec-reasoning"
    recommendation_id: str = "sec-recommendation"
    conclusion_id: str = "sec-conclusion"
    conclusion: str = ""
    action: dict[str, Any] = field(default_factory=dict)
    section_keys: list[str] = field(
        default_factory=lambda: [
            "sec-observation",
            "sec-reasoning",
            "sec-recommendation",
            "sec-conclusion",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation identity keys and copied payloads."""
        return {
            "observation_id": self.observation_id,
            "reasoning_id": self.reasoning_id,
            "recommendation_id": self.recommendation_id,
            "conclusion_id": self.conclusion_id,
            "conclusion": self.conclusion,
            "action": dict(self.action),
            "section_keys": list(self.section_keys),
        }


@dataclass(slots=True)
class CanonicalIdentity:
    """Analysis Result identity slice (BZ-ID-02)."""

    person: PersonIdentity = field(default_factory=PersonIdentity)
    calendar: CalendarIdentity = field(default_factory=CalendarIdentity)
    four_pillars: FourPillarIdentity | None = None
    bone_weight: BoneWeightIdentity = field(default_factory=BoneWeightIdentity)
    luck: LuckIdentity = field(default_factory=LuckIdentity)
    interpretation: InterpretationIdentity = field(default_factory=InterpretationIdentity)

    def to_dict(self) -> dict[str, Any]:
        """Serialize ``identity`` for Analysis Result."""
        return {
            "person": self.person.to_dict(),
            "calendar": self.calendar.to_dict(),
            "four_pillars": self.four_pillars.to_dict() if self.four_pillars else {},
            "bone_weight": self.bone_weight.to_dict(),
            "luck": self.luck.to_dict(),
            "interpretation": self.interpretation.to_dict(),
        }
