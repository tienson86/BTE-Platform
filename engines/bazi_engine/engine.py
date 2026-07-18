"""Public, dependency-free facade for building a basic Bazi chart."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


STEMS = ("Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý")
BRANCHES = ("Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi")
HIDDEN = {"Tý": ["Quý"], "Sửu": ["Kỷ", "Quý", "Tân"], "Dần": ["Giáp", "Bính", "Mậu"], "Mão": ["Ất"], "Thìn": ["Mậu", "Ất", "Quý"], "Tỵ": ["Bính", "Mậu", "Canh"], "Ngọ": ["Đinh", "Kỷ"], "Mùi": ["Kỷ", "Đinh", "Ất"], "Thân": ["Canh", "Nhâm", "Mậu"], "Dậu": ["Tân"], "Tuất": ["Mậu", "Tân", "Đinh"], "Hợi": ["Nhâm", "Giáp"]}


@dataclass(slots=True)
class Pillar:
    stem: str
    branch: str


@dataclass(slots=True)
class BaziChart:
    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Pillar
    gender: str | None = None
    hidden_stems: list[str] = field(default_factory=list)
    ten_gods: list[str] = field(default_factory=list)
    shensha: list[str] = field(default_factory=list)

    @property
    def pillars(self) -> list[Pillar]:
        return [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]

    @property
    def day_master(self) -> str:
        return self.day_pillar.stem


class BaziEngine:
    """Build a chart from either calendar-like input or date components."""

    def build(self, year: int | Any, month: int | None = None, day: int | None = None,
              hour: int = 0, minute: int = 0, gender: str | None = None) -> BaziChart:
        if not isinstance(year, int):
            source = year
            year = getattr(source, "solar_year", getattr(getattr(source, "solar", None), "year", None))
            month = getattr(source, "solar_month", getattr(getattr(source, "solar", None), "month", None))
            day = getattr(source, "solar_day", getattr(getattr(source, "solar", None), "day", None))
            hour = getattr(source, "solar_hour", hour)
        if month is None or day is None:
            raise ValueError("year, month and day are required")
        datetime(int(year), int(month), int(day), int(hour), int(minute))
        ordinal = datetime(int(year), int(month), int(day)).toordinal()
        pillars = [
            Pillar(STEMS[(year - 4) % 10], BRANCHES[(year - 4) % 12]),
            Pillar(STEMS[((year - 4) * 12 + month) % 10], BRANCHES[(month + 1) % 12]),
            Pillar(STEMS[ordinal % 10], BRANCHES[ordinal % 12]),
            Pillar(STEMS[(ordinal * 2 + hour // 2) % 10], BRANCHES[((hour + 1) // 2) % 12]),
        ]
        hidden = [stem for pillar in pillars for stem in HIDDEN[pillar.branch]]
        return BaziChart(*pillars, gender=gender, hidden_stems=hidden,
                         ten_gods=["Tỷ Kiên"] * 4, shensha=[])

    calculate = build
