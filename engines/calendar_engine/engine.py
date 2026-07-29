from dataclasses import dataclass
from datetime import datetime

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
        lunar_date = f"{parts.day:02d}/{parts.month:02d}/{year_can_chi}"
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
        )

    def calculate(self, birth_datetime: datetime, timezone: str = "Asia/Ho_Chi_Minh") -> CalendarResult:
        """Wrapper: build from a datetime (timezone label reserved for future use)."""
        del timezone  # reserved — conversion currently uses UTC+7 civil date
        return self.build(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            birth_datetime.hour,
            birth_datetime.minute,
        )
