"""Strength context builder from BaziChart.

Visible heavenly stems drive support/control presence lists.
Drain also reads earthly-branch bản khí so output (tiết) cannot vanish
when it sits only in địa chi / tàng can chính khí (e.g. Tỵ/Hỏa for Ất Mộc).
Repeated branches are counted per pillar, not collapsed by branch name.
Residual (non-main) hidden stems are not copied into drain lists.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from engines.bazi_engine.ten_god import STEM_META, ten_god_name

from engines.strength_engine.context import StrengthContext


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

_BRANCH_TEMPERATURE: dict[str, str] = {
    "Dần": "warm", "Mão": "warm", "Thìn": "warm",
    "Tỵ": "hot", "Ngọ": "hot", "Mùi": "hot",
    "Thân": "cool", "Dậu": "cool", "Tuất": "cool",
    "Hợi": "cold", "Tý": "cold", "Sửu": "cold",
}

_ELEMENT_PRODUCES: dict[str, str] = {
    "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc",
}

_ELEMENT_CONTROLS: dict[str, str] = {
    "Mộc": "Thổ", "Hỏa": "Kim", "Thổ": "Thủy", "Kim": "Mộc", "Thủy": "Hỏa",
}

_OFFICER_GODS = frozenset({"Chính Quan", "Thất Sát"})
_WEALTH_GODS = frozenset({"Chính Tài", "Thiên Tài"})
_RESOURCE_GODS = frozenset({"Chính Ấn", "Thiên Ấn"})
_OUTPUT_GODS = frozenset({"Thực Thần", "Thương Quan"})
_COMPANION_GODS = frozenset({"Tỷ Kiên", "Kiếp Tài"})

_ROOT_LEVEL_LABELS: tuple[tuple[int, str], ...] = (
    (3, "Thông căn 3 chi trở lên"),
    (2, "Thông căn 2 chi"),
    (1, "Thông căn 1 chi"),
)

_SUPPORT_LABELS = {
    "same": "Đồng hành trợ thân",
    "resource": "Ấn tinh sinh thân",
    "stem": "Thiên Can trợ lực",
    "branch": "Địa Chi trợ lực",
    "combination": "Hợp hóa sinh thân",
}

_CONTROL_LABELS = {
    "officer": "Bị Quan Sát khắc",
    "output": "Bị Thực Thương tiết",
    "wealth": "Bị Tài tinh hao",
    "root_destroyed": "Căn khí bị xung",
    "combination_lost": "Hợp hóa mất gốc",
}

_DRAIN_LABELS = {
    "output": "Thực Thương tiết khí",
    "wealth": "Tài tinh hao thân",
}


def build_strength_context(bazi_chart: Any, *, calendar: Any = None) -> StrengthContext:
    """Build StrengthContext from BaziChart without Pattern Engine dependency."""
    day_master = str(getattr(bazi_chart, "day_master", "") or "")

    month_pillar = getattr(bazi_chart, "month_pillar", None)
    year_pillar = getattr(bazi_chart, "year_pillar", None)
    day_pillar = getattr(bazi_chart, "day_pillar", None)
    hour_pillar = getattr(bazi_chart, "hour_pillar", None)

    month_stem = str(getattr(month_pillar, "stem", "") or "")
    month_branch = str(getattr(month_pillar, "branch", "") or "")
    year_branch = str(getattr(year_pillar, "branch", "") or "")
    day_branch = str(getattr(day_pillar, "branch", "") or "")
    hour_branch = str(getattr(hour_pillar, "branch", "") or "")

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

    month_status = _compute_month_status(day_master_element, month_branch_element)

    # One entry per pillar so repeated branches (e.g. three Tỵ) are not collapsed.
    pillar_hidden: list[tuple[str, list[str]]] = [
        (year_branch, list(_BRANCH_HIDDEN.get(year_branch, []))),
        (month_branch, list(_BRANCH_HIDDEN.get(month_branch, []))),
        (day_branch, list(_BRANCH_HIDDEN.get(day_branch, []))),
        (hour_branch, list(_BRANCH_HIDDEN.get(hour_branch, []))),
    ]
    root_count, root_level = _compute_root(day_master_element, pillar_hidden, bazi_chart)

    raw_ten_gods = list(getattr(bazi_chart, "ten_gods", []) or [])
    ten_gods_list = [g for g in raw_ten_gods if g and g != "Nhật Chủ"]

    resource_elements: list[str] = []
    companion_elements: list[str] = []
    wealth_elements: list[str] = []
    officer_elements: list[str] = []
    output_elements: list[str] = []

    for god in ten_gods_list:
        if god in _OFFICER_GODS:
            officer_elements.append(god)
        elif god in _WEALTH_GODS:
            wealth_elements.append(god)
        elif god in _RESOURCE_GODS:
            resource_elements.append(god)
        elif god in _OUTPUT_GODS:
            output_elements.append(god)
        elif god in _COMPANION_GODS:
            companion_elements.append(god)

    support_type = _detect_support_type(day_master, year_pillar, month_pillar, hour_pillar)
    control_type = _detect_control_type(day_master, year_pillar, month_pillar, hour_pillar)
    output_branch_count = _count_output_branches(
        day_master_element,
        (year_branch, month_branch, day_branch, hour_branch),
    )
    drain_type = _detect_drain_type(output_elements, wealth_elements, output_branch_count)

    all_stems: list[str] = []
    for pillar in (year_pillar, month_pillar, day_pillar, hour_pillar):
        stem = getattr(pillar, "stem", None)
        if stem:
            all_stems.append(str(stem))
    for _branch, stems in pillar_hidden:
        all_stems.extend(stems)
    element_distribution = dict(Counter(_stem_to_element(s) for s in all_stems if _stem_to_element(s)))

    drain_count = len(output_elements) + len(wealth_elements) + output_branch_count

    return StrengthContext(
        day_master=day_master or None,
        day_master_element=day_master_element or None,
        day_master_yin_yang=day_master_yin_yang or None,
        month_stem=month_stem or None,
        month_branch=month_branch or None,
        month_branch_element=month_branch_element or None,
        month_branch_ten_god=month_branch_ten_god,
        month_status=month_status,
        root_level=root_level,
        root_count=root_count,
        support_type=support_type,
        control_type=control_type,
        drain_type=drain_type,
        season=_BRANCH_SEASON.get(month_branch),
        season_phase=_BRANCH_SEASON_PHASE.get(month_branch),
        temperature_type=_BRANCH_TEMPERATURE.get(month_branch),
        element_distribution=element_distribution,
        ten_gods_list=ten_gods_list,
        resource_elements=resource_elements,
        companion_elements=companion_elements,
        wealth_elements=wealth_elements,
        officer_elements=officer_elements,
        output_elements=output_elements,
        resource_count=len(resource_elements),
        companion_count=len(companion_elements),
        wealth_count=len(wealth_elements),
        officer_count=len(officer_elements),
        output_count=len(output_elements),
        drain_count=drain_count,
        output_branch_count=output_branch_count,
        metadata={"builder": "strength_context_builder_v2"},
        source_bazi=bazi_chart,
    )


def _stem_to_element(stem: str) -> str | None:
    meta = STEM_META.get(stem)
    return meta[0] if meta else None


def _compute_month_status(day_el: str, month_el: str) -> str | None:
    if not day_el or not month_el:
        return None
    if day_el == month_el:
        return "Đắc lệnh"
    if _ELEMENT_PRODUCES.get(month_el) == day_el:
        return "Tướng"
    if _ELEMENT_PRODUCES.get(day_el) == month_el:
        return "Hưu"
    if _ELEMENT_CONTROLS.get(day_el) == month_el:
        return "Tù"
    if _ELEMENT_CONTROLS.get(month_el) == day_el:
        return "Tử"
    return "Hưu"


def _compute_root(
    day_el: str,
    pillar_hidden: list[tuple[str, list[str]]],
    bazi_chart: Any,
) -> tuple[int, str]:
    if not day_el:
        return 0, "Vô căn"

    root_pillars = 0
    for branch, hidden in pillar_hidden:
        if not branch:
            continue
        if any(STEM_META.get(stem, (None,))[0] == day_el for stem in hidden):
            root_pillars += 1

    if root_pillars == 0:
        flat = list(getattr(bazi_chart, "hidden_stems", []) or [])
        if any(STEM_META.get(stem, (None,))[0] == day_el for stem in flat):
            return 0, "Thông căn tàng can"
        return 0, "Vô căn"

    for threshold, label in _ROOT_LEVEL_LABELS:
        if root_pillars >= threshold:
            return root_pillars, label
    return root_pillars, "Vô căn"


def _ten_god_between(day_master: str, stem: str) -> str | None:
    if not day_master or not stem:
        return None
    return ten_god_name(day_master, stem) or None


def _detect_support_type(day_master: str, *pillars: Any) -> str | None:
    for pillar in pillars:
        stem = getattr(pillar, "stem", None)
        if not stem or stem not in STEM_META:
            continue
        god = _ten_god_between(day_master, str(stem))
        if god in _COMPANION_GODS:
            return _SUPPORT_LABELS["same"]
        if god in _RESOURCE_GODS:
            return _SUPPORT_LABELS["resource"]
    dm_el = STEM_META.get(day_master, (None,))[0]
    for pillar in pillars:
        stem = getattr(pillar, "stem", None)
        if stem and STEM_META.get(str(stem), (None,))[0] == dm_el:
            return _SUPPORT_LABELS["stem"]
    return None


def _detect_control_type(day_master: str, *pillars: Any) -> str | None:
    for pillar in pillars:
        stem = getattr(pillar, "stem", None)
        if not stem:
            continue
        god = _ten_god_between(day_master, str(stem))
        if god in _OFFICER_GODS:
            return _CONTROL_LABELS["officer"]
        if god in _OUTPUT_GODS:
            return _CONTROL_LABELS["output"]
        if god in _WEALTH_GODS:
            return _CONTROL_LABELS["wealth"]
    return None


def _branch_element(branch: str) -> str:
    """Bản khí of an earthly branch via its main hidden stem."""
    main = _BRANCH_MAIN_STEM.get(branch, "")
    meta = STEM_META.get(main, ("", ""))
    return meta[0] if meta else ""


def _count_output_branches(day_el: str, branches: tuple[str, ...]) -> int:
    """Count pillars whose branch bản khí is produced by the Day Master."""
    produced = _ELEMENT_PRODUCES.get(day_el)
    if not day_el or not produced:
        return 0
    return sum(1 for branch in branches if branch and _branch_element(branch) == produced)


def _detect_drain_type(
    output_elements: list[str],
    wealth_elements: list[str],
    output_branch_count: int = 0,
) -> str | None:
    if output_elements:
        return _DRAIN_LABELS["output"]
    if output_branch_count > 0:
        return _DRAIN_LABELS["output"]
    if wealth_elements:
        return _DRAIN_LABELS["wealth"]
    return None
