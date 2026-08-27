"""Date Selection result models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SixStateResult:
    """One of the six public day/hour/khắc classifications."""

    remainder: int
    code: str
    label: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return asdict(self)


@dataclass(slots=True)
class TrachInfo:
    """Cung Phi, ngũ hành, and Đông/Tây Tứ Trạch."""

    cung: str
    element_code: str
    element_label: str
    trach_group_code: str
    trach_group_label: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return asdict(self)


@dataclass(slots=True)
class CalendarSnapshot:
    """Canonical calendar fields reused from Calendar Engine."""

    solar_year: int
    solar_month: int
    solar_day: int
    solar_label: str
    lunar_year: int
    lunar_month: int
    lunar_day: int
    lunar_leap: bool
    lunar_label: str
    year_ganzhi: str
    day_ganzhi: str
    year_branch: str
    weekday: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return asdict(self)


@dataclass(slots=True)
class KeSlot:
    """One 20-minute khắc inside a traditional hour."""

    ke_index: int
    time_range: str
    start_minute_of_day: int
    six_state: SixStateResult

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "ke_index": self.ke_index,
            "time_range": self.time_range,
            "start_minute_of_day": self.start_minute_of_day,
            "six_state": self.six_state.to_dict(),
        }


@dataclass(slots=True)
class HourWindow:
    """Canonical two-hour traditional branch window."""

    branch: str
    branch_index: int
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    time_range: str
    is_cross_day: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return asdict(self)


@dataclass(slots=True)
class HourSelection:
    """Hour-level Date Selection result."""

    window: HourWindow
    ganzhi: str
    hour_value: int
    six_state: SixStateResult
    trach: TrachInfo | None
    ke_slots: list[KeSlot] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "window": self.window.to_dict(),
            "ganzhi": self.ganzhi,
            "hour_value": self.hour_value,
            "six_state": self.six_state.to_dict(),
            "trach": self.trach.to_dict() if self.trach else None,
            "ke_slots": [slot.to_dict() for slot in self.ke_slots],
        }


@dataclass(slots=True)
class DaySelection:
    """Day-level Date Selection result."""

    calendar: CalendarSnapshot
    day_value: int
    six_state: SixStateResult
    trach: TrachInfo | None
    hours: list[HourSelection] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "calendar": self.calendar.to_dict(),
            "day_value": self.day_value,
            "six_state": self.six_state.to_dict(),
            "trach": self.trach.to_dict() if self.trach else None,
            "hours": [hour.to_dict() for hour in self.hours],
        }


@dataclass(slots=True)
class CalendarCell:
    """Compact monthly calendar cell."""

    solar_year: int
    solar_month: int
    solar_day: int
    lunar_day: int
    lunar_month: int
    lunar_leap: bool
    weekday: int
    six_state: SixStateResult
    in_month: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "solar_year": self.solar_year,
            "solar_month": self.solar_month,
            "solar_day": self.solar_day,
            "lunar_day": self.lunar_day,
            "lunar_month": self.lunar_month,
            "lunar_leap": self.lunar_leap,
            "weekday": self.weekday,
            "six_state": self.six_state.to_dict(),
            "in_month": self.in_month,
        }


@dataclass(slots=True)
class MonthCalendar:
    """Gregorian month grid with six-state labels."""

    year: int
    month: int
    cells: list[CalendarCell]

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "year": self.year,
            "month": self.month,
            "cells": [cell.to_dict() for cell in self.cells],
        }


@dataclass(slots=True)
class PersonProfile:
    """Derived personal Date Selection identity."""

    full_name: str
    gender: str
    gender_label: str
    solar_label: str
    lunar_label: str
    ganzhi: str
    trach: TrachInfo

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "full_name": self.full_name,
            "gender": self.gender,
            "gender_label": self.gender_label,
            "solar_label": self.solar_label,
            "lunar_label": self.lunar_label,
            "ganzhi": self.ganzhi,
            "trach": self.trach.to_dict(),
        }


@dataclass(slots=True)
class HourRecommendation:
    """Public recommended hour / khắc range for a candidate day."""

    branch: str
    time_range: str
    ke_index: int
    classification: str
    primary: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return asdict(self)


@dataclass(slots=True)
class RankedDate:
    """One recommended date card."""

    day: DaySelection
    recommendations: list[HourRecommendation]

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "day": {
                "calendar": self.day.calendar.to_dict(),
                "six_state": self.day.six_state.to_dict(),
                "trach": self.day.trach.to_dict() if self.day.trach else None,
            },
            "recommendations": [item.to_dict() for item in self.recommendations],
        }


@dataclass(slots=True)
class SearchResult:
    """Personalized Top-N date search."""

    person: PersonProfile
    target_year: int
    target_month: int
    dates: list[RankedDate]

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        return {
            "person": self.person.to_dict(),
            "target_year": self.target_year,
            "target_month": self.target_month,
            "dates": [item.to_dict() for item in self.dates],
        }
