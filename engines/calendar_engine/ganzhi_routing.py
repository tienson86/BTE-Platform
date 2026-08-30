"""Canonical Ganzhi source routing for Year / Month / Day / Hour.

Year and Month identity rows use the Tam Nguyên of the Gregorian year.
Day and Hour identity rows stay on Hạ Nguyên.

Can Chi stems/branches are still computed by Calendar algorithms
(solar-term month, JDN day, Ngũ Thử Độn hour). Nguyên routing selects
which 60 Hoa Giáp Cung dataset those labels resolve against.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.cung_phi import cung_for_ganzhi, ganzhi_label_for_year
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.month_ganzhi import month_pillar
from engines.calendar_engine.tam_nguyen import HA_NGUYEN, calculate_tam_nguyen, tam_nguyen_for_year

PILLAR_YEAR = "year"
PILLAR_MONTH = "month"
PILLAR_DAY = "day"
PILLAR_HOUR = "hour"

NGUYEN_CODE = {
    "Thượng Nguyên": "THUONG_NGUYEN",
    "Trung Nguyên": "TRUNG_NGUYEN",
    "Hạ Nguyên": "HA_NGUYEN",
}


@dataclass(slots=True)
class GanzhiRoute:
    """One pillar's Can Chi plus the Nguyên dataset used for its Cung row."""

    pillar: str
    ganzhi: str
    source_nguyen: str
    source_nguyen_code: str
    cung_phi: str

    def to_dict(self) -> dict[str, str]:
        """Serialize routing diagnostics for Calendar / tests."""
        return {
            "pillar": self.pillar,
            "ganzhi": self.ganzhi,
            "source_nguyen": self.source_nguyen,
            "source_nguyen_code": self.source_nguyen_code,
            "cung_phi": self.cung_phi,
        }


def nguyen_code(tam_nguyen: str) -> str:
    """Stable machine code for a Tam Nguyên label."""
    return NGUYEN_CODE.get(tam_nguyen, tam_nguyen)


def source_nguyen_for_pillar(pillar: str, tam_nguyen: str) -> str:
    """Year/Month follow the birth/selected year; Day/Hour stay Hạ Nguyên."""
    if pillar in {PILLAR_YEAR, PILLAR_MONTH}:
        return tam_nguyen
    return HA_NGUYEN


def _route(pillar: str, ganzhi: str, source_nguyen: str, reference_year: int) -> GanzhiRoute:
    cung = cung_for_ganzhi(
        ganzhi,
        tam_nguyen=source_nguyen,
        reference_year=reference_year,
        gender="male",
    )
    return GanzhiRoute(
        pillar=pillar,
        ganzhi=ganzhi,
        source_nguyen=source_nguyen,
        source_nguyen_code=nguyen_code(source_nguyen),
        cung_phi=cung,
    )


def resolve_year_ganzhi(year: int) -> GanzhiRoute:
    """Look up Year Can Chi in the Tam Nguyên 60 Hoa Giáp block containing ``year``."""
    yuan = tam_nguyen_for_year(year)
    label = ganzhi_label_for_year(year)
    return _route(PILLAR_YEAR, label, yuan, year)


def resolve_month_ganzhi(year: int, month: int, day: int) -> GanzhiRoute:
    """Month Can Chi from solar-term Ngũ Hổ Độn; Cung from the year's Tam Nguyên."""
    yuan = tam_nguyen_for_year(year)
    stem, branch = month_pillar(year, month, day)
    return _route(PILLAR_MONTH, f"{stem} {branch}", yuan, year)


def resolve_day_ganzhi(year: int, month: int, day: int) -> GanzhiRoute:
    """Day Can Chi from noon JDN; Cung from Hạ Nguyên."""
    jdn = JulianDay.day_number(year, month, day)
    gz = GanzhiAlgorithm.day(jdn)
    return _route(PILLAR_DAY, f"{gz['can']} {gz['chi']}", HA_NGUYEN, year)


def hour_ganzhi_from_day_stem(day_stem: str, hour: int) -> str:
    """Ngũ Thử Độn hour Can Chi (same rule as BaziEngine hour pillar)."""
    stems = GanzhiAlgorithm.STEM
    branches = GanzhiAlgorithm.BRANCH
    if hour >= 23 or hour < 1:
        branch_index = 0
    else:
        branch_index = ((hour + 1) // 2) % 12
    stem_index = (stems.index(day_stem) * 2 + branch_index) % 10
    return f"{stems[stem_index]} {branches[branch_index]}"


def resolve_hour_ganzhi(year: int, month: int, day: int, hour: int = 0) -> GanzhiRoute:
    """Hour Can Chi from day stem + clock hour; Cung from Hạ Nguyên."""
    day_route = resolve_day_ganzhi(year, month, day)
    day_stem = day_route.ganzhi.split()[0]
    label = hour_ganzhi_from_day_stem(day_stem, hour)
    return _route(PILLAR_HOUR, label, HA_NGUYEN, year)


def routing_table(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    *,
    year_ganzhi: str | None = None,
    month_ganzhi: str | None = None,
    day_ganzhi: str | None = None,
    hour_ganzhi: str | None = None,
) -> dict[str, GanzhiRoute]:
    """Canonical four-pillar Nguyên routing for one civil datetime.

    Can Chi labels may be supplied from Calendar / BaZi. Nguyên source is
    always Year/Month = Tam Nguyên of ``year``, Day/Hour = Hạ Nguyên.
    """
    yuan = tam_nguyen_for_year(year)
    year_label = year_ganzhi or ganzhi_label_for_year(year)
    if month_ganzhi:
        month_label = month_ganzhi
    else:
        stem, branch = month_pillar(year, month, day)
        month_label = f"{stem} {branch}"
    if day_ganzhi:
        day_label = day_ganzhi
    else:
        day_label = resolve_day_ganzhi(year, month, day).ganzhi
    if hour_ganzhi:
        hour_label = hour_ganzhi
    else:
        hour_label = resolve_hour_ganzhi(year, month, day, hour).ganzhi
    return {
        PILLAR_YEAR: _route(PILLAR_YEAR, year_label, yuan, year),
        PILLAR_MONTH: _route(PILLAR_MONTH, month_label, yuan, year),
        PILLAR_DAY: _route(PILLAR_DAY, day_label, HA_NGUYEN, year),
        PILLAR_HOUR: _route(PILLAR_HOUR, hour_label, HA_NGUYEN, year),
    }


def routing_payload(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    *,
    year_ganzhi: str | None = None,
    month_ganzhi: str | None = None,
    day_ganzhi: str | None = None,
    hour_ganzhi: str | None = None,
) -> dict[str, Any]:
    """Serialize routing plus the Tam Nguyên of the civil year."""
    cycle = calculate_tam_nguyen(year)
    routes = routing_table(
        year,
        month,
        day,
        hour,
        year_ganzhi=year_ganzhi,
        month_ganzhi=month_ganzhi,
        day_ganzhi=day_ganzhi,
        hour_ganzhi=hour_ganzhi,
    )
    return {
        "tam_nguyen": cycle.tam_nguyen,
        "tam_nguyen_code": nguyen_code(cycle.tam_nguyen),
        "cuu_van": cycle.cuu_van,
        "year": routes[PILLAR_YEAR].to_dict(),
        "month": routes[PILLAR_MONTH].to_dict(),
        "day": routes[PILLAR_DAY].to_dict(),
        "hour": routes[PILLAR_HOUR].to_dict(),
    }


def stamp_bazi_source_nguyen(
    bazi: dict[str, Any] | None,
    routing: dict[str, Any] | None,
) -> dict[str, Any]:
    """Copy Nguyên diagnostics onto serialized BaZi pillars. Does not change stems."""
    payload = bazi if isinstance(bazi, dict) else {}
    routes = routing if isinstance(routing, dict) else {}
    for pillar in (PILLAR_YEAR, PILLAR_MONTH, PILLAR_DAY, PILLAR_HOUR):
        cell = payload.get(f"{pillar}_pillar")
        route = routes.get(pillar)
        if not isinstance(cell, dict) or not isinstance(route, dict):
            continue
        cell["source_nguyen"] = route.get("source_nguyen")
        cell["source_nguyen_code"] = route.get("source_nguyen_code")
    return payload
