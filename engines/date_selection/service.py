"""Date Selection public service."""

from __future__ import annotations

import calendar as gregorian
from datetime import date

from engines.calendar_engine.engine import CalendarEngine
from engines.date_selection.calendar_adapter import snapshot_for_solar
from engines.date_selection.constants import BRANCH_INDEX, MAX_RANKED_DATES
from engines.date_selection.cung_phi import (
    gender_label,
    normalize_gender,
    trach_for_date_ganzhi,
    trach_for_person,
)
from engines.date_selection.exceptions import DateSelectionMappingError, DateSelectionValidationError
from engines.date_selection.hour import all_hour_windows, hour_ganzhi, window_for_branch
from engines.date_selection.ke import current_ke_index, ke_slots_for_hour
from engines.date_selection.liu_ren import day_value, hour_value, six_state_from_value
from engines.date_selection.models import (
    CalendarCell,
    DaySelection,
    HourSelection,
    MonthCalendar,
    PersonProfile,
    SearchResult,
)
from engines.date_selection.ranking import rank_dates


class DateSelectionService:
    """
    Public Date Selection API.

    Calendar truth comes from CalendarEngine. This service only classifies
    dates, hours, and khắc, and ranks personalized candidates.
    """

    def __init__(self, calendar_engine: CalendarEngine | None = None) -> None:
        self._calendar = calendar_engine or CalendarEngine()

    def month_calendar(self, year: int, month: int) -> MonthCalendar:
        """Build a real Gregorian month grid with six-state labels."""
        self._validate_year_month(year, month)
        last_day = gregorian.monthrange(year, month)[1]
        cells: list[CalendarCell] = []
        for day in range(1, last_day + 1):
            snapshot = snapshot_for_solar(year, month, day, engine=self._calendar)
            total = day_value(
                BRANCH_INDEX[snapshot.year_branch],
                snapshot.lunar_month,
                snapshot.lunar_day,
            )
            cells.append(
                CalendarCell(
                    solar_year=year,
                    solar_month=month,
                    solar_day=day,
                    lunar_day=snapshot.lunar_day,
                    lunar_month=snapshot.lunar_month,
                    lunar_leap=snapshot.lunar_leap,
                    weekday=snapshot.weekday,
                    six_state=six_state_from_value(total),
                )
            )
        return MonthCalendar(year=year, month=month, cells=cells)

    def inspect_day(
        self,
        year: int,
        month: int,
        day: int,
        *,
        hour_branch: str | None = None,
        gender: str | None = None,
    ) -> DaySelection:
        """Full day + 12-hour + six-khắc inspection."""
        del gender  # Viewer gender must not select date/hour Cung.
        day_result = self._build_day(year, month, day)
        if hour_branch:
            window_for_branch(hour_branch)
        return day_result

    def current_hour_branch(self, hour: int, minute: int) -> str:
        """Traditional hour branch for a civil clock time."""
        from engines.date_selection.hour import window_for_clock

        return window_for_clock(hour, minute).branch

    def current_ke(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        *,
        gender: str | None = None,
    ) -> dict[str, object]:
        """Resolve the live traditional hour and khắc for a civil timestamp."""
        del gender
        inspected = self.inspect_day(year, month, day)
        window = None
        for item in inspected.hours:
            if item.window.branch == self.current_hour_branch(hour, minute):
                window = item
                break
        if window is None:
            raise DateSelectionValidationError("traditional hour not found")
        ke_index = current_ke_index(window.window, hour, minute)
        slot = next(item for item in window.ke_slots if item.ke_index == ke_index)
        return {
            "hour": window.to_dict(),
            "ke": slot.to_dict(),
        }

    def person_profile(
        self,
        *,
        full_name: str,
        gender: str,
        birth_year: int,
        birth_month: int,
        birth_day: int,
    ) -> PersonProfile:
        """Derive lunar birth data and personal Cung Phi from solar birth date."""
        name = (full_name or "").strip()
        if not name:
            raise DateSelectionValidationError("full_name is required")
        sex = normalize_gender(gender)
        snapshot = snapshot_for_solar(
            birth_year,
            birth_month,
            birth_day,
            engine=self._calendar,
        )
        trach = trach_for_person(lunar_year=snapshot.lunar_year, gender=sex)
        return PersonProfile(
            full_name=name,
            gender=sex,
            gender_label=gender_label(sex),
            solar_label=snapshot.solar_label,
            lunar_label=snapshot.lunar_label,
            ganzhi=snapshot.year_ganzhi,
            trach=trach,
        )

    def search(
        self,
        *,
        full_name: str,
        gender: str,
        birth_year: int,
        birth_month: int,
        birth_day: int,
        target_year: int,
        target_month: int,
    ) -> SearchResult:
        """Return up to five personalized candidate dates for a target month."""
        person = self.person_profile(
            full_name=full_name,
            gender=gender,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
        )
        self._validate_year_month(target_year, target_month)
        last_day = gregorian.monthrange(target_year, target_month)[1]
        days = [
            self._build_day(target_year, target_month, day)
            for day in range(1, last_day + 1)
        ]
        ranked = rank_dates(days, person.trach.trach_group_code)[:MAX_RANKED_DATES]
        return SearchResult(
            person=person,
            target_year=target_year,
            target_month=target_month,
            dates=ranked,
        )

    def _build_day(
        self,
        year: int,
        month: int,
        day: int,
    ) -> DaySelection:
        snapshot = snapshot_for_solar(year, month, day, engine=self._calendar)
        total = day_value(
            BRANCH_INDEX[snapshot.year_branch],
            snapshot.lunar_month,
            snapshot.lunar_day,
        )
        day_stem = snapshot.day_ganzhi.split(" ", 1)[0]
        try:
            trach = trach_for_date_ganzhi(snapshot.day_ganzhi)
        except DateSelectionMappingError:
            trach = None
        hours = [
            self._build_hour(day_stem, window, total)
            for window in all_hour_windows()
        ]
        return DaySelection(
            calendar=snapshot,
            day_value=total,
            six_state=six_state_from_value(total),
            trach=trach,
            hours=hours,
        )

    def _build_hour(
        self,
        day_stem: str,
        window,
        day_total: int,
    ) -> HourSelection:
        hour_total = hour_value(day_total, window.branch_index)
        ganzhi = hour_ganzhi(day_stem, window.branch)
        try:
            trach = trach_for_date_ganzhi(ganzhi)
        except DateSelectionMappingError:
            trach = None
        return HourSelection(
            window=window,
            ganzhi=ganzhi,
            hour_value=hour_total,
            six_state=six_state_from_value(hour_total),
            trach=trach,
            ke_slots=ke_slots_for_hour(window, hour_total),
        )

    @staticmethod
    def _validate_year_month(year: int, month: int) -> None:
        if year < 1 or month < 1 or month > 12:
            raise DateSelectionValidationError(f"invalid year/month: {year}-{month}")
        date(year, month, 1)


class DateSelectionEngine:
    """Thin engine facade (orchestrator-friendly Public API)."""

    def __init__(self, service: DateSelectionService | None = None) -> None:
        self._service = service or DateSelectionService()

    def month_calendar(self, year: int, month: int) -> MonthCalendar:
        """Delegate to DateSelectionService.month_calendar."""
        return self._service.month_calendar(year, month)

    def inspect_day(self, year: int, month: int, day: int, **kwargs) -> DaySelection:
        """Delegate to DateSelectionService.inspect_day."""
        return self._service.inspect_day(year, month, day, **kwargs)

    def search(self, **kwargs) -> SearchResult:
        """Delegate to DateSelectionService.search."""
        return self._service.search(**kwargs)
