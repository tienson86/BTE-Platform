"""Canonical Ganzhi source routing for Year / Month / Day / Hour.

Year and Month Can Chi (stem + branch) come from the Tam Nguyên dataset.
Day and Hour Can Chi stay on Hạ Nguyên (JDN / Ngũ Thử Độn).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.cung_phi import cung_for_ganzhi
from engines.calendar_engine.julian.julian import JulianDay
from engines.calendar_engine.tam_nguyen import HA_NGUYEN, calculate_tam_nguyen
from engines.calendar_engine.tam_nguyen_dataset import (
    CALENDAR_RULE_VERSION,
    resolve_month_pillar,
    resolve_year_pillar,
)

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
    """One pillar's actual Can Chi plus the Nguyên that supplied it."""

    pillar: str
    heavenly_stem: str
    earthly_branch: str
    ganzhi: str
    nap_am: str
    source_nguyen: str
    source_nguyen_code: str
    cung_phi: str

    def to_dict(self) -> dict[str, str]:
        """Serialize routing diagnostics for Calendar / tests."""
        return {
            "pillar": self.pillar,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "ganzhi": self.ganzhi,
            "nap_am": self.nap_am,
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


def _route(
    pillar: str,
    ganzhi: str,
    source_nguyen: str,
    reference_year: int,
    *,
    nap_am: str = "",
) -> GanzhiRoute:
    parts = ganzhi.split()
    stem = parts[0] if parts else ""
    branch = parts[1] if len(parts) > 1 else ""
    cung = cung_for_ganzhi(
        ganzhi,
        tam_nguyen=source_nguyen,
        reference_year=reference_year,
        gender="male",
    )
    return GanzhiRoute(
        pillar=pillar,
        heavenly_stem=stem,
        earthly_branch=branch,
        ganzhi=ganzhi,
        nap_am=nap_am,
        source_nguyen=source_nguyen,
        source_nguyen_code=nguyen_code(source_nguyen),
        cung_phi=cung,
    )


def resolve_year_ganzhi(year: int, month: int = 6, day: int = 15) -> GanzhiRoute:
    """Year stem/branch from the Tam Nguyên 60 Hoa Giáp table."""
    resolved = resolve_year_pillar(year, month=month, day=day)
    return _route(
        PILLAR_YEAR,
        resolved.ganzhi,
        resolved.source_nguyen,
        year,
        nap_am=resolved.nap_am,
    )


def resolve_month_ganzhi(year: int, month: int, day: int) -> GanzhiRoute:
    """Month stem/branch from the same Tam Nguyên Year stem (Ngũ Hổ Độn)."""
    resolved = resolve_month_pillar(year, month, day)
    return _route(
        PILLAR_MONTH,
        resolved.ganzhi,
        resolved.source_nguyen,
        year,
        nap_am=resolved.nap_am,
    )


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
    """Canonical four-pillar routing. Year/Month Can Chi come from the dataset."""
    year_route = resolve_year_ganzhi(year)
    month_route = resolve_month_ganzhi(year, month, day)
    if year_ganzhi:
        year_route = _route(
            PILLAR_YEAR,
            year_ganzhi,
            year_route.source_nguyen,
            year,
            nap_am=year_route.nap_am,
        )
    if month_ganzhi:
        month_route = _route(
            PILLAR_MONTH,
            month_ganzhi,
            month_route.source_nguyen,
            year,
            nap_am=month_route.nap_am,
        )
    if day_ganzhi:
        day_label = day_ganzhi
    else:
        day_label = resolve_day_ganzhi(year, month, day).ganzhi
    if hour_ganzhi:
        hour_label = hour_ganzhi
    else:
        hour_label = resolve_hour_ganzhi(year, month, day, hour).ganzhi
    return {
        PILLAR_YEAR: year_route,
        PILLAR_MONTH: month_route,
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
        "calendar_rule_version": CALENDAR_RULE_VERSION,
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
