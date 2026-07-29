"""Temperature context builder from BaziChart."""

from __future__ import annotations

from collections import Counter
from typing import Any

from engines.bazi_engine.ten_god import STEM_META, ten_god_name

from engines.temperature_engine.context import TemperatureContext


_BRANCH_MAIN_STEM: dict[str, str] = {
    "Tý": "Quý", "Sửu": "Kỷ", "Dần": "Giáp", "Mão": "Ất",
    "Thìn": "Mậu", "Tỵ": "Bính", "Ngọ": "Đinh", "Mùi": "Kỷ",
    "Thân": "Canh", "Dậu": "Tân", "Tuất": "Mậu", "Hợi": "Nhâm",
}

_BRANCH_HIDDEN: dict[str, list[str]] = {
    "Tý": ["Quý"], "Sửu": ["Kỷ", "Quý", "Tân"], "Dần": ["Giáp", "Bính", "Mậu"],
    "Mão": ["Ất"], "Thìn": ["Mậu", "Ất", "Quý"], "Tỵ": ["Bính", "Mậu", "Canh"],
    "Ngọ": ["Đinh", "Kỷ"], "Mùi": ["Kỷ", "Đinh", "Ất"], "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu": ["Tân"], "Tuất": ["Mậu", "Tân", "Đinh"], "Hợi": ["Nhâm", "Giáp"],
}

_BRANCH_SEASON: dict[str, str] = {
    "Dần": "spring", "Mão": "spring", "Thìn": "spring",
    "Tỵ": "summer", "Ngọ": "summer", "Mùi": "summer",
    "Thân": "autumn", "Dậu": "autumn", "Tuất": "autumn",
    "Hợi": "winter", "Tý": "winter", "Sửu": "winter",
}

_BRANCH_SEASON_PHASE: dict[str, str] = {
    "Dần": "early_spring", "Mão": "mid_spring", "Thìn": "late_spring",
    "Tỵ": "early_summer", "Ngọ": "mid_summer", "Mùi": "late_summer",
    "Thân": "early_autumn", "Dậu": "mid_autumn", "Tuất": "late_autumn",
    "Hợi": "early_winter", "Tý": "mid_winter", "Sửu": "late_winter",
}

_BRANCH_CLIMATE: dict[str, str] = {
    "Dần": "warm", "Mão": "warm", "Thìn": "warm",
    "Tỵ": "hot", "Ngọ": "hot", "Mùi": "hot",
    "Thân": "cool", "Dậu": "cool", "Tuất": "cool",
    "Hợi": "cold", "Tý": "cold", "Sửu": "cold",
}


def build_temperature_context(
    bazi_chart: Any,
    *,
    calendar: Any = None,
    strength_level: str | None = None,
    strength_score: float = 0.0,
) -> TemperatureContext:
    """Build TemperatureContext from BaziChart."""
    day_master = str(getattr(bazi_chart, "day_master", "") or "")

    month_pillar = getattr(bazi_chart, "month_pillar", None)
    year_pillar = getattr(bazi_chart, "year_pillar", None)
    day_pillar = getattr(bazi_chart, "day_pillar", None)
    hour_pillar = getattr(bazi_chart, "hour_pillar", None)

    month_stem = str(getattr(month_pillar, "stem", "") or "")
    month_branch = str(getattr(month_pillar, "branch", "") or "")

    dm_meta = STEM_META.get(day_master, ("", ""))
    day_master_element = dm_meta[0] if dm_meta else ""
    day_master_yin_yang = dm_meta[1] if len(dm_meta) > 1 else ""

    mb_main = _BRANCH_MAIN_STEM.get(month_branch, "")
    mb_meta = STEM_META.get(mb_main, ("", ""))
    month_branch_element = mb_meta[0] if mb_meta else ""

    month_branch_ten_god: str | None = None
    if day_master and month_branch:
        main = _BRANCH_MAIN_STEM.get(month_branch)
        if main:
            month_branch_ten_god = ten_god_name(day_master, main) or None

    all_stems: list[str] = []
    for pillar in (year_pillar, month_pillar, day_pillar, hour_pillar):
        stem = getattr(pillar, "stem", None)
        if stem:
            all_stems.append(str(stem))
    for branch in (
        getattr(month_pillar, "branch", ""),
        getattr(year_pillar, "branch", ""),
        getattr(day_pillar, "branch", ""),
        getattr(hour_pillar, "branch", ""),
    ):
        all_stems.extend(_BRANCH_HIDDEN.get(str(branch), []))

    element_distribution = dict(Counter(_stem_to_element(s) for s in all_stems if _stem_to_element(s)))
    fire_count = int(element_distribution.get("Hỏa", 0))
    water_count = int(element_distribution.get("Thủy", 0))
    earth_count = int(element_distribution.get("Thổ", 0))
    wood_count = int(element_distribution.get("Mộc", 0))
    metal_count = int(element_distribution.get("Kim", 0))

    dryness_level = _compute_dryness(fire_count, earth_count, water_count)
    humidity_level = _compute_humidity(water_count, earth_count, fire_count)

    raw_ten_gods = list(getattr(bazi_chart, "ten_gods", []) or [])
    ten_gods_list = [g for g in raw_ten_gods if g and g != "Nhật Chủ"]

    return TemperatureContext(
        day_master=day_master or None,
        day_master_element=day_master_element or None,
        day_master_yin_yang=day_master_yin_yang or None,
        month_stem=month_stem or None,
        month_branch=month_branch or None,
        month_branch_element=month_branch_element or None,
        month_branch_ten_god=month_branch_ten_god,
        season=_BRANCH_SEASON.get(month_branch),
        season_phase=_BRANCH_SEASON_PHASE.get(month_branch),
        climate_type=_BRANCH_CLIMATE.get(month_branch),
        dryness_level=dryness_level,
        humidity_level=humidity_level,
        fire_count=fire_count,
        water_count=water_count,
        earth_count=earth_count,
        wood_count=wood_count,
        metal_count=metal_count,
        element_distribution=element_distribution,
        ten_gods_list=ten_gods_list,
        strength_level=strength_level,
        strength_score=float(strength_score or 0.0),
        metadata={"builder": "temperature_context_builder_v2"},
        source_bazi=bazi_chart,
    )


def _stem_to_element(stem: str) -> str | None:
    meta = STEM_META.get(stem)
    return meta[0] if meta else None


def _compute_dryness(fire: int, earth: int, water: int) -> str:
    dry_index = fire + earth - water
    if dry_index >= 4:
        return "dry"
    if dry_index >= 2:
        return "slightly_dry"
    return "normal"


def _compute_humidity(water: int, earth: int, fire: int) -> str:
    humid_index = water + earth - fire
    if humid_index >= 4:
        return "humid"
    if humid_index >= 2:
        return "slightly_humid"
    return "normal"
