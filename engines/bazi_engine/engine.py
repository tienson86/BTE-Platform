"""Public facade for building a Bazi chart from civil datetime.

Pillars follow BTE G1-10B rules:
- Year Can Chi is looked up from the Tam Nguyên 60 Hoa Giáp table of the Gregorian year
- Month Can Chi uses that Year stem (Ngũ Hổ Độn) plus 12-Tiết month branch
- Day uses astronomical Julian Day Number + sexagenary cycle (Hạ Nguyên)
- Hour follows Ngũ Thử Độn from Day Stem (Hạ Nguyên)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.calendar_engine.tam_nguyen_dataset import resolve_month_pillar, resolve_year_pillar

from engines.bazi_engine.ten_god import ten_god_name
from engines.bazi_engine.shensha.models import ShenShaDetectionResult
from engines.bazi_engine.shensha.service import ShenShaService


STEMS = GanzhiAlgorithm.STEM
BRANCHES = GanzhiAlgorithm.BRANCH

# Tàng can phổ thông theo Địa Chi (dùng cho hidden_stems tóm tắt).
HIDDEN: dict[str, list[str]] = {
    "Tý": ["Quý"],
    "Sửu": ["Kỷ", "Quý", "Tân"],
    "Dần": ["Giáp", "Bính", "Mậu"],
    "Mão": ["Ất"],
    "Thìn": ["Mậu", "Ất", "Quý"],
    "Tỵ": ["Bính", "Mậu", "Canh"],
    "Ngọ": ["Đinh", "Kỷ"],
    "Mùi": ["Kỷ", "Đinh", "Ất"],
    "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu": ["Tân"],
    "Tuất": ["Mậu", "Tân", "Đinh"],
    "Hợi": ["Nhâm", "Giáp"],
}

@dataclass(slots=True)
class Pillar:
    """Một trụ Can Chi."""

    stem: str
    branch: str


@dataclass(slots=True)
class BaziChart:
    """Lá số Tứ Trụ rút gọn cho pipeline."""

    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Pillar
    gender: str | None = None
    hidden_stems: list[str] = field(default_factory=list)
    ten_gods: list[str] = field(default_factory=list)
    shensha: list[str] = field(default_factory=list)
    shensha_result: ShenShaDetectionResult | None = None

    @property
    def pillars(self) -> list[Pillar]:
        """Thứ tự Năm → Tháng → Ngày → Giờ."""
        return [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]

    @property
    def day_master(self) -> str:
        """Nhật Chủ (Can ngày)."""
        return self.day_pillar.stem


class BaziEngine:
    """Build a chart from calendar-like input or Gregorian date components."""

    def __init__(self) -> None:
        self._solar_terms = SolarTermEngine()

    def build(
        self,
        year: int | Any,
        month: int | None = None,
        day: int | None = None,
        hour: int = 0,
        minute: int = 0,
        gender: str | None = None,
    ) -> BaziChart:
        """Lập Tứ Trụ từ năm/tháng/ngày/giờ dương lịch (giờ địa phương)."""
        year, month, day, hour, minute = self._normalize_input(
            year, month, day, hour, minute
        )
        datetime(int(year), int(month), int(day), int(hour), int(minute))

        year_resolved = resolve_year_pillar(int(year), month=int(month), day=int(day))
        year_pillar = Pillar(stem=year_resolved.heavenly_stem, branch=year_resolved.earthly_branch)

        month_resolved = resolve_month_pillar(int(year), int(month), int(day))
        month_pillar = Pillar(stem=month_resolved.heavenly_stem, branch=month_resolved.earthly_branch)

        jdn = JulianDay.day_number(year, month, day)
        day_gz = GanzhiAlgorithm.day(jdn)
        day_pillar = Pillar(stem=day_gz["can"], branch=day_gz["chi"])

        hour_pillar = self._hour_pillar(day_pillar.stem, hour)

        pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
        hidden = [stem for pillar in pillars for stem in HIDDEN[pillar.branch]]
        day_master = day_pillar.stem
        ten_gods = [
            "Nhật Chủ" if pillar is day_pillar else ten_god_name(day_master, pillar.stem)
            for pillar in pillars
        ]
        shensha_result = ShenShaService().evaluate(
            day_master=day_master,
            year_branch=year_pillar.branch,
            month_branch=month_pillar.branch,
            day_branch=day_pillar.branch,
            hour_branch=hour_pillar.branch,
            stems=[p.stem for p in pillars],
            branches=[p.branch for p in pillars],
        )
        return BaziChart(
            *pillars,
            gender=gender,
            hidden_stems=hidden,
            ten_gods=ten_gods,
            shensha=shensha_result.canonical_names(),
            shensha_result=shensha_result,
        )

    calculate = build

    def _normalize_input(
        self,
        year: int | Any,
        month: int | None,
        day: int | None,
        hour: int,
        minute: int,
    ) -> tuple[int, int, int, int, int]:
        """Chấp nhận int components hoặc object calendar-like."""
        if not isinstance(year, int):
            source = year
            year = getattr(
                source,
                "solar_year",
                getattr(getattr(source, "solar", None), "year", None),
            )
            month = getattr(
                source,
                "solar_month",
                getattr(getattr(source, "solar", None), "month", None),
            )
            day = getattr(
                source,
                "solar_day",
                getattr(getattr(source, "solar", None), "day", None),
            )
            hour = getattr(source, "solar_hour", hour)
            minute = getattr(source, "solar_minute", minute)
        if month is None or day is None or year is None:
            raise ValueError("year, month and day are required")
        return int(year), int(month), int(day), int(hour), int(minute)

    def _bazi_year(self, year: int, month: int, day: int) -> int:
        """Năm Bát Tự: đổi năm tại Lập Xuân."""
        if self._solar_terms.is_after_li_chun(year, month, day):
            return year
        return year - 1

    def _hour_pillar(self, day_stem: str, hour: int) -> Pillar:
        """Trụ giờ: Địa Chi theo canh giờ, Thiên Can theo Ngũ Thử Độn."""
        if hour >= 23 or hour < 1:
            branch_index = 0
        else:
            branch_index = ((hour + 1) // 2) % 12
        day_stem_index = STEMS.index(day_stem)
        stem_index = (day_stem_index * 2 + branch_index) % 10
        return Pillar(stem=STEMS[stem_index], branch=BRANCHES[branch_index])
