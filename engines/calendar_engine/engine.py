from dataclasses import dataclass
from datetime import datetime

from .julian.julian import JulianDay
from .lunar.lunar import LunarDate
from .solar.solar import SolarDate
from .solar_terms.engine import SolarTermEngine, SolarTerm


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


class CalendarEngine:
    def build(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0) -> CalendarResult:
        datetime(year, month, day, hour, minute)
        solar = SolarDate(year, month, day)
        return CalendarResult(solar, LunarDate(year, month, day), JulianDay.from_gregorian(year, month, day),
                              SolarTermEngine().get_current_term(year, month, day), year, month, day, hour, minute)

    def calculate(self, birth_datetime: datetime, timezone: str = "Asia/Ho_Chi_Minh") -> CalendarResult:
        return self.build(birth_datetime.year, birth_datetime.month, birth_datetime.day,
                          birth_datetime.hour, birth_datetime.minute)
