"""Date Selection result models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from engines.date_selection.exceptions import DateSelectionError


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
    month_ganzhi: str
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
        from engines.date_selection.identity import hoa_giap_view

        view = hoa_giap_view(self.ganzhi, self.trach)
        payload = {
            "window": self.window.to_dict(),
            "ganzhi": self.ganzhi,
            "hour_value": self.hour_value,
            "six_state": self.six_state.to_dict(),
            "trach": self.trach.to_dict() if self.trach else None,
            "ke_slots": [slot.to_dict() for slot in self.ke_slots],
        }
        payload.update(view)
        payload["can_chi"] = view["ganzhi"]
        payload["cung_phi"] = view["cung"]
        return payload


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
        from engines.date_selection.identity import hoa_giap_view, pillar_contract

        payload = {
            "calendar": self.calendar.to_dict(),
            "day_value": self.day_value,
            "six_state": self.six_state.to_dict(),
            "trach": self.trach.to_dict() if self.trach else None,
            "hours": [hour.to_dict() for hour in self.hours],
            "month_ganzhi": self.calendar.month_ganzhi,
        }
        payload.update(hoa_giap_view(self.calendar.day_ganzhi, self.trach))
        payload["year"] = pillar_contract(self.calendar.year_ganzhi)
        payload["month"] = pillar_contract(self.calendar.month_ganzhi)
        payload["day"] = pillar_contract(self.calendar.day_ganzhi)
        return payload


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
        from engines.date_selection.identity import hoa_giap_view

        view = hoa_giap_view(self.ganzhi, self.trach)
        payload = {
            "full_name": self.full_name,
            "gender": self.gender,
            "gender_label": self.gender_label,
            "solar_label": self.solar_label,
            "lunar_label": self.lunar_label,
            "ganzhi": self.ganzhi,
            "year_ganzhi": self.ganzhi,
            "trach": self.trach.to_dict(),
        }
        payload.update(view)
        payload["cung_phi"] = view["cung"]
        return payload


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
        from engines.date_selection.identity import hoa_giap_view, pillar_contract

        day_payload = {
            "calendar": self.day.calendar.to_dict(),
            "six_state": self.day.six_state.to_dict(),
            "trach": self.day.trach.to_dict() if self.day.trach else None,
            "month_ganzhi": self.day.calendar.month_ganzhi,
        }
        day_payload.update(hoa_giap_view(self.day.calendar.day_ganzhi, self.day.trach))
        day_payload["year"] = pillar_contract(self.day.calendar.year_ganzhi)
        day_payload["month"] = pillar_contract(self.day.calendar.month_ganzhi)
        day_payload["day"] = pillar_contract(self.day.calendar.day_ganzhi)
        return {
            "day": day_payload,
            "compatible_hours": _compatible_hours_view(self.day),
            "recommendations": [
                _recommendation_view(item, self.day) for item in self.recommendations
            ],
        }


def _compatible_hours_view(day: DaySelection) -> list[dict[str, Any]]:
    """All same-Trạch hours with their positive khắc. No single-hour winner."""
    from engines.date_selection.constants import POSITIVE_KE_CODES
    from engines.date_selection.identity import hoa_giap_view

    group = day.trach.trach_group_code if day.trach else None
    rows: list[dict[str, Any]] = []
    for hour in day.hours:
        if hour.trach is None or hour.trach.trach_group_code != group:
            continue
        view = hoa_giap_view(hour.ganzhi, hour.trach)
        rows.append(
            {
                "branch": hour.window.branch,
                "full_time_range": hour.window.time_range,
                "ganzhi": hour.ganzhi,
                "can_chi": view["ganzhi"],
                "nayin": view["nayin"],
                "nayin_element": view["nayin_element"],
                "cung": view["cung"],
                "cung_phi": view["cung"],
                "cung_element": view["cung_element"],
                "trach_group": view["trach_group"],
                "trach_group_label": view["trach_group_label"],
                "positive_ke": [
                    {
                        "index": slot.ke_index,
                        "time_range": slot.time_range,
                        "result": slot.six_state.label,
                    }
                    for slot in hour.ke_slots
                    if slot.six_state.code in POSITIVE_KE_CODES
                ],
            }
        )
    return rows


def _recommendation_view(item: HourRecommendation, day: DaySelection) -> dict[str, Any]:
    """Attach canonical hour identity without changing ranking selection."""
    from engines.date_selection.identity import hoa_giap_view

    payload = item.to_dict()
    hour = next((row for row in day.hours if row.window.branch == item.branch), None)
    if hour is None:
        return payload
    view = hoa_giap_view(hour.ganzhi, hour.trach)
    payload.update(
        {
            "full_time_range": hour.window.time_range,
            "ganzhi": hour.ganzhi,
            "can_chi": view["ganzhi"],
            "nayin": view["nayin"],
            "nayin_element": view["nayin_element"],
            "cung": view["cung"],
            "cung_phi": view["cung"],
            "cung_element": view["cung_element"],
            "trach_group": view["trach_group"],
            "trach_group_label": view["trach_group_label"],
            "ke_result": item.classification,
            "ke_time_range": item.time_range,
            "recommended_ke": {
                "index": item.ke_index,
                "time_range": item.time_range,
                "result": item.classification,
            },
        }
    )
    return payload


def _assert_same_trach(person_group: str, ranked: RankedDate) -> None:
    """Fail loudly if a recommended day/hour contradicts the person's Trạch."""
    day_group = ranked.day.trach.trach_group_code if ranked.day.trach else None
    if day_group != person_group:
        raise DateSelectionError(
            f"recommended day trach {day_group!r} != person {person_group!r}"
        )
    for rec in ranked.recommendations:
        hour = next((row for row in ranked.day.hours if row.window.branch == rec.branch), None)
        hour_group = hour.trach.trach_group_code if hour is not None and hour.trach else None
        if hour_group != person_group:
            raise DateSelectionError(
                f"recommended hour {rec.branch!r} trach {hour_group!r} != person {person_group!r}"
            )


@dataclass(slots=True)
class SearchResult:
    """Personalized Top-N date search."""

    person: PersonProfile
    target_year: int
    target_month: int
    dates: list[RankedDate]

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation."""
        person_group = self.person.trach.trach_group_code
        dates: list[dict[str, Any]] = []
        for item in self.dates:
            _assert_same_trach(person_group, item)
            payload = item.to_dict()
            for hour in payload["compatible_hours"]:
                if hour.get("trach_group") != person_group:
                    raise DateSelectionError(
                        f"compatible hour {hour.get('branch')!r} trach "
                        f"{hour.get('trach_group')!r} != person {person_group!r}"
                    )
            dates.append(payload)
        return {
            "person": self.person.to_dict(),
            "target_year": self.target_year,
            "target_month": self.target_month,
            "dates": dates,
        }
