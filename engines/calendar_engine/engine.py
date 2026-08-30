from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .algorithms.ganzhi import GanzhiAlgorithm
from .cung_phi import CungPhiResult, calculate_cung_phi
from .exceptions import CalendarValidationError
from .ganzhi_routing import hour_ganzhi_from_day_stem, routing_payload
from .julian.julian import JulianDay
from .lunar.converter import solar_to_lunar
from .lunar.lunar import LunarDate
from .solar.solar import SolarDate
from .solar_terms.engine import SolarTerm, SolarTermEngine
from .tam_nguyen import calculate_tam_nguyen
from .tam_nguyen_dataset import (
    CALENDAR_RULE_VERSION,
    resolve_month_pillar,
    resolve_year_pillar,
)


@dataclass(slots=True)
class CalendarResult:
    """Canonical calendar output, including Tam Nguyên and personal Cung Phi."""
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
    year_stem: str | None = None
    year_branch: str | None = None
    year_can_chi: str | None = None
    month_stem: str | None = None
    month_branch: str | None = None
    month_can_chi: str | None = None
    calendar_rule_version: str = CALENDAR_RULE_VERSION
    tam_nguyen: str | None = None
    cuu_van: int | None = None
    cung_phi: str | None = None
    menh_quai: str | None = None
    house_group: str | None = None
    nhom_trach: str | None = None
    gua_number: int | None = None
    cung_phi_remainder: int | None = None
    ganzhi_routing: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize canonical calendar truth for API / Portal / PDF / Cân Xương.

        Day Ganzhi uses integer noon JDN (``JulianDay.day_number``), matching Bazi.
        """
        leap = bool(self.leap_month)
        lunar_year_can_chi = self.lunar.year_can_chi if self.lunar else None
        jdn = JulianDay.day_number(self.solar_year, self.solar_month, self.solar_day)
        day_ganzhi = GanzhiAlgorithm.day(jdn)
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
            "year_can_chi": self.year_can_chi,
            "year_stem": self.year_stem,
            "year_branch": self.year_branch,
            "month_stem": self.month_stem,
            "month_branch": self.month_branch,
            "month_can_chi": self.month_can_chi,
            "calendar_rule_version": self.calendar_rule_version,
            "tam_nguyen": self.tam_nguyen,
            "cuu_van": self.cuu_van,
            "cung_phi": self.cung_phi,
            "menh_quai": self.menh_quai,
            "house_group": self.house_group,
            "nhom_trach": self.nhom_trach or self.house_group,
            "gua_number": self.gua_number,
            "cung_phi_remainder": self.cung_phi_remainder,
            "ganzhi_routing": self.ganzhi_routing or {},
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
        gender: str | None = None,
    ) -> CalendarResult:
        """Build calendar result from Gregorian civil date/time (Vietnam UTC+7 by default)."""
        datetime(year, month, day, hour, minute)
        solar = SolarDate(year, month, day)
        # Must convert via lunar algorithm — never copy solar Y/M/D into lunar.
        parts = solar_to_lunar(day, month, year, time_zone=time_zone)
        lunar_ganzhi = GanzhiAlgorithm.year(parts.year)
        lunar_year_can_chi = f"{lunar_ganzhi['can']} {lunar_ganzhi['chi']}"
        lunar = LunarDate(
            year=parts.year,
            month=parts.month,
            day=parts.day,
            leap=parts.leap,
            year_can_chi=lunar_year_can_chi,
        )
        solar_date = f"{day:02d}/{month:02d}/{year:04d}"
        lunar_date = _format_lunar_date(parts.day, parts.month, parts.year, parts.leap)
        year_resolved = resolve_year_pillar(year, month=month, day=day)
        month_resolved = resolve_month_pillar(year, month, day)
        cycle = calculate_tam_nguyen(year)
        cung = _cung_phi_for_gender(year, gender)
        jdn = JulianDay.day_number(year, month, day)
        day_gz = GanzhiAlgorithm.day(jdn)
        day_can_chi = f"{day_gz['can']} {day_gz['chi']}"
        hour_can_chi = hour_ganzhi_from_day_stem(day_gz["can"], hour)
        routing = routing_payload(
            year,
            month,
            day,
            hour,
            year_ganzhi=year_resolved.ganzhi,
            month_ganzhi=month_resolved.ganzhi,
            day_ganzhi=day_can_chi,
            hour_ganzhi=hour_can_chi,
        )
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
            year_stem=year_resolved.heavenly_stem,
            year_branch=year_resolved.earthly_branch,
            year_can_chi=year_resolved.ganzhi,
            month_stem=month_resolved.heavenly_stem,
            month_branch=month_resolved.earthly_branch,
            month_can_chi=month_resolved.ganzhi,
            calendar_rule_version=CALENDAR_RULE_VERSION,
            tam_nguyen=cycle.tam_nguyen,
            cuu_van=cycle.cuu_van,
            cung_phi=None if cung is None else cung.cung_phi,
            menh_quai=None if cung is None else cung.menh_quai,
            house_group=None if cung is None else cung.house_group,
            nhom_trach=None if cung is None else cung.house_group,
            gua_number=None if cung is None else cung.gua_number,
            cung_phi_remainder=None if cung is None else cung.remainder,
            ganzhi_routing=routing,
        )

    def calculate(
        self,
        birth_datetime: datetime,
        timezone: str = "Asia/Ho_Chi_Minh",
        gender: str | None = None,
    ) -> CalendarResult:
        """Wrapper: build from a datetime (timezone label stored, conversion stays UTC+7)."""
        return self.build(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            birth_datetime.hour,
            birth_datetime.minute,
            timezone_name=timezone,
            gender=gender,
        )


def _cung_phi_for_gender(year: int, gender: str | None) -> CungPhiResult | None:
    """Cung Phi when gender is present and valid. Leave empty otherwise."""
    if gender is None or str(gender).strip() == "":
        return None
    try:
        return calculate_cung_phi(year=year, gender=gender)
    except CalendarValidationError:
        return None
