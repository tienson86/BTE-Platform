from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .algorithms.ganzhi import GanzhiAlgorithm
from .julian.julian import JulianDay
from .lunar.converter import solar_to_lunar
from .lunar.lunar import LunarDate
from .solar.solar import SolarDate
from .solar_terms.engine import SolarTerm, SolarTermEngine


@dataclass(slots=True)
class CalendarResult:
    solar: SolarDate
    lunar: LunarDate
    julian_day: float
    solar_term: SolarTerm
    solar_year: int
    solar_month: int
    solar_day: int
    solar_hour: int = 0
    solar_minute: int = 0
    lunar_year: int | None = None
    lunar_month: int | None = None
    lunar_day: int | None = None
    leap_month: bool | None = None
    solar_date: str | None = None
    lunar_date: str | None = None
    timezone_offset: float = 7.0
    timezone_name: str = "UTC+7"

    def to_dict(self) -> dict[str, Any]:
        """Serialize canonical calendar truth for API / Portal / PDF / Cân Xương."""
        leap = bool(self.leap_month)
        lunar_year_can_chi = self.lunar.year_can_chi if self.lunar else None
        day_ganzhi = GanzhiAlgorithm.day(self.julian_day)
        lunar_can_chi: dict[str, str] = {}
        if lunar_year_can_chi:
            lunar_can_chi["year"] = lunar_year_can_chi
        lunar_can_chi["day"] = f"{day_ganzhi['can']} {day_ganzhi['chi']}"
        solar_term = {
            "name": getattr(self.solar_term, "name", None),
            "index": getattr(self.solar_term, "index", None),
        }
        return {
            "solar": {
                "year": self.solar_year,
                "month": self.solar_month,
                "day": self.solar_day,
                "hour": self.solar_hour,
                "minute": self.solar_minute,
            },
            "lunar": {
                "year": self.lunar_year,
                "month": self.lunar_month,
                "day": self.lunar_day,
                "is_leap_month": leap,
                "leap": leap,
                "year_can_chi": lunar_year_can_chi,
            },
            "lunar_can_chi": lunar_can_chi,
            "solar_term": solar_term,
            "timezone": {
                "offset_hours": self.timezone_offset,
                "name": self.timezone_name,
            },
            "julian_day": self.julian_day,
            "solar_year": self.solar_year,
            "solar_month": self.solar_month,
            "solar_day": self.solar_day,
            "solar_hour": self.solar_hour,
            "solar_minute": self.solar_minute,
            "lunar_year": self.lunar_year,
            "lunar_month": self.lunar_month,
            "lunar_day": self.lunar_day,
            "leap_month": leap,
            "is_leap_month": leap,
            "solar_date": self.solar_date,
            "lunar_date": self.lunar_date,
            "timezone_offset": self.timezone_offset,
            "timezone_name": self.timezone_name,
        }


def _format_lunar_date(day: int, month: int, year: int, leap: bool) -> str:
    """Customer lunar date: dd/mm/yyyy with leap marker."""
    text = f"{day:02d}/{month:02d}/{year:04d}"
    if leap:
        return f"{text} nhuận"
    return text


class CalendarEngine:
    """Calendar Engine public API — solar/lunar/JD/solar-term for a birth moment."""

    def build(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        time_zone: float = 7.0,
        timezone_name: str | None = None,
    ) -> CalendarResult:
        """Build calendar result from Gregorian civil date/time (Vietnam UTC+7 by default)."""
        datetime(year, month, day, hour, minute)
        solar = SolarDate(year, month, day)
        # Must convert via lunar algorithm — never copy solar Y/M/D into lunar.
        parts = solar_to_lunar(day, month, year, time_zone=time_zone)
        ganzhi = GanzhiAlgorithm.year(parts.year)
        year_can_chi = f"{ganzhi['can']} {ganzhi['chi']}"
        lunar = LunarDate(
            year=parts.year,
            month=parts.month,
            day=parts.day,
            leap=parts.leap,
            year_can_chi=year_can_chi,
        )
        solar_date = f"{day:02d}/{month:02d}/{year:04d}"
        lunar_date = _format_lunar_date(parts.day, parts.month, parts.year, parts.leap)
        return CalendarResult(
            solar=solar,
            lunar=lunar,
            julian_day=JulianDay.from_gregorian(year, month, day),
            solar_term=SolarTermEngine().get_current_term(year, month, day),
            solar_year=year,
            solar_month=month,
            solar_day=day,
            solar_hour=hour,
            solar_minute=minute,
            lunar_year=parts.year,
            lunar_month=parts.month,
            lunar_day=parts.day,
            leap_month=parts.leap,
            solar_date=solar_date,
            lunar_date=lunar_date,
            timezone_offset=time_zone,
            timezone_name=timezone_name or "UTC+7",
        )

    def calculate(self, birth_datetime: datetime, timezone: str = "Asia/Ho_Chi_Minh") -> CalendarResult:
        """Wrapper: build from a datetime (timezone label stored, conversion stays UTC+7)."""
        return self.build(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            birth_datetime.hour,
            birth_datetime.minute,
            timezone_name=timezone,
        )
