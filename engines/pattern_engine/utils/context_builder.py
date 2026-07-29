"""
PatternContext builder — pre-computes all derived fields for rule matching.

Separates bazi-to-context mapping from PatternContext dataclass.
All field computations are pure functions — no Engine calls, no side effects.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from engines.bazi_engine.ten_god import ten_god_name, STEM_META

from ..context import PatternContext


# ============================================================
# Canonical lookup tables (no hard-coded rule logic)
# ============================================================

# Canonical main stem of each branch (Lệnh Tháng principle — Ziping BaZi)
_BRANCH_MAIN_STEM: dict[str, str] = {
    "Tý": "Quý",  "Sửu": "Kỷ",   "Dần": "Giáp", "Mão": "Ất",
    "Thìn": "Mậu", "Tỵ": "Bính", "Ngọ": "Đinh", "Mùi": "Kỷ",
    "Thân": "Canh", "Dậu": "Tân", "Tuất": "Mậu", "Hợi": "Nhâm",
}

# All hidden stems per branch (including secondary)
_BRANCH_HIDDEN: dict[str, list[str]] = {
    "Tý":   ["Quý"],
    "Sửu":  ["Kỷ", "Quý", "Tân"],
    "Dần":  ["Giáp", "Bính", "Mậu"],
    "Mão":  ["Ất"],
    "Thìn": ["Mậu", "Ất", "Quý"],
    "Tỵ":   ["Bính", "Mậu", "Canh"],
    "Ngọ":  ["Đinh", "Kỷ"],
    "Mùi":  ["Kỷ", "Đinh", "Ất"],
    "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu":  ["Tân"],
    "Tuất": ["Mậu", "Tân", "Đinh"],
    "Hợi":  ["Nhâm", "Giáp"],
}

# Season group per branch
_BRANCH_SEASON: dict[str, str] = {
    "Dần": "spring", "Mão": "spring", "Thìn": "spring",
    "Tỵ": "summer",  "Ngọ": "summer",  "Mùi": "summer",
    "Thân": "autumn", "Dậu": "autumn", "Tuất": "autumn",
    "Hợi": "winter", "Tý": "winter",  "Sửu": "winter",
}

# Season phase (early/mid/late) per branch
_BRANCH_SEASON_PHASE: dict[str, str] = {
    "Dần": "early_spring", "Mão": "mid_spring",  "Thìn": "late_spring",
    "Tỵ":  "early_summer", "Ngọ": "mid_summer",  "Mùi":  "late_summer",
    "Thân": "early_autumn","Dậu": "mid_autumn",  "Tuất": "late_autumn",
    "Hợi": "early_winter", "Tý":  "mid_winter",  "Sửu":  "late_winter",
}

# Temperature tendency per branch
_BRANCH_TEMPERATURE: dict[str, str] = {
    "Dần": "warm", "Mão": "warm",  "Thìn": "warm",
    "Tỵ":  "hot",  "Ngọ": "hot",   "Mùi":  "hot",
    "Thân": "cool","Dậu": "cool",  "Tuất": "cool",
    "Hợi": "cold", "Tý":  "cold",  "Sửu":  "cold",
}

# Ten god family classification
_OFFICER_GODS    = frozenset({"Chính Quan", "Thất Sát"})
_WEALTH_GODS     = frozenset({"Chính Tài", "Thiên Tài"})
_RESOURCE_GODS   = frozenset({"Chính Ấn", "Thiên Ấn"})
_OUTPUT_GODS     = frozenset({"Thực Thần", "Thương Quan"})
_COMPANION_GODS  = frozenset({"Tỷ Kiên", "Kiếp Tài"})


def build_pattern_context(bazi_chart: Any, *, calendar: Any = None) -> PatternContext:
    """
    Build a fully-populated PatternContext from a BaziChart.

    Pre-computes all derived fields so rule conditions can use
    simple equality / contains checks without dotted path traversal.
    """
    day_master: str = str(getattr(bazi_chart, "day_master", "") or "")

    month_pillar  = getattr(bazi_chart, "month_pillar", None)
    year_pillar   = getattr(bazi_chart, "year_pillar", None)
    day_pillar    = getattr(bazi_chart, "day_pillar", None)
    hour_pillar   = getattr(bazi_chart, "hour_pillar", None)

    month_stem:   str = str(getattr(month_pillar,  "stem",   "") or "")
    month_branch: str = str(getattr(month_pillar,  "branch", "") or "")
    year_branch:  str = str(getattr(year_pillar,   "branch", "") or "")
    day_branch:   str = str(getattr(day_pillar,    "branch", "") or "")
    hour_branch:  str = str(getattr(hour_pillar,   "branch", "") or "")

    # ----- Day Master metadata -----
    dm_meta = STEM_META.get(day_master, ("", ""))
    day_master_element: str = dm_meta[0] if dm_meta else ""
    day_master_yin_yang: str = dm_meta[1] if len(dm_meta) > 1 else ""

    # ----- Month branch metadata -----
    mb_meta = STEM_META.get(_BRANCH_MAIN_STEM.get(month_branch, ""), ("", ""))
    month_branch_element: str = mb_meta[0] if mb_meta else ""

    # ----- Ten god of month stem -----
    month_stem_ten_god: str | None = None
    if day_master and month_stem:
        month_stem_ten_god = ten_god_name(day_master, month_stem) or None

    # ----- Ten god of month branch main stem (Lệnh Tháng) -----
    month_branch_ten_god: str | None = None
    if day_master and month_branch:
        main = _BRANCH_MAIN_STEM.get(month_branch)
        if main:
            month_branch_ten_god = ten_god_name(day_master, main) or None

    # ----- Hidden stems per pillar -----
    month_hidden_stems: list[str] = list(_BRANCH_HIDDEN.get(month_branch, []))
    year_hidden_stems:  list[str] = list(_BRANCH_HIDDEN.get(year_branch,  []))
    day_hidden_stems:   list[str] = list(_BRANCH_HIDDEN.get(day_branch,   []))
    hour_hidden_stems:  list[str] = list(_BRANCH_HIDDEN.get(hour_branch,  []))

    # ----- Hidden elements per pillar -----
    month_hidden_elements: list[str] = _stems_to_elements(month_hidden_stems)

    # ----- Flat lists -----
    raw_ten_gods: list[str] = list(bazi_chart.ten_gods or [])
    ten_gods_list: list[str] = [g for g in raw_ten_gods if g and g != "Nhật Chủ"]

    # All hidden stems flat (from bazi or recomputed)
    bazi_hs = getattr(bazi_chart, "hidden_stems", None)
    if isinstance(bazi_hs, list) and bazi_hs:
        hidden_stems_flat: list[str] = list(bazi_hs)
    else:
        hidden_stems_flat = (
            month_hidden_stems + year_hidden_stems +
            day_hidden_stems   + hour_hidden_stems
        )

    # ----- Element distribution -----
    all_stems: list[str] = []
    for pillar in (year_pillar, month_pillar, day_pillar, hour_pillar):
        s = getattr(pillar, "stem", None)
        if s:
            all_stems.append(s)
    all_stems.extend(hidden_stems_flat)

    element_distribution: dict[str, int] = _count_elements(all_stems)

    # ----- Season / temperature -----
    season:        str | None = _BRANCH_SEASON.get(month_branch)
    season_phase:  str | None = _BRANCH_SEASON_PHASE.get(month_branch)
    temperature_type: str | None = _BRANCH_TEMPERATURE.get(month_branch)

    # ----- Ten-god family lists -----
    support_elements:  list[str] = []
    drain_elements:    list[str] = []
    control_elements:  list[str] = []
    resource_elements: list[str] = []
    wealth_elements:   list[str] = []
    officer_elements:  list[str] = []
    output_elements:   list[str] = []
    companion_elements: list[str] = []

    for god in ten_gods_list:
        el = _ten_god_element(god, day_master)
        if god in _OFFICER_GODS:
            officer_elements.append(god)
            control_elements.append(god)
        elif god in _WEALTH_GODS:
            wealth_elements.append(god)
            drain_elements.append(god)
        elif god in _RESOURCE_GODS:
            resource_elements.append(god)
            support_elements.append(god)
        elif god in _OUTPUT_GODS:
            output_elements.append(god)
            drain_elements.append(god)
        elif god in _COMPANION_GODS:
            companion_elements.append(god)
            support_elements.append(god)

    def _pillar_str(p: Any) -> str | None:
        if p is None:
            return None
        s = getattr(p, "stem", "") or ""
        b = getattr(p, "branch", "") or ""
        return f"{s} {b}".strip() or None

    return PatternContext(
        # Basic pillars
        year_pillar=_pillar_str(year_pillar),
        month_pillar=_pillar_str(month_pillar),
        day_pillar=_pillar_str(day_pillar),
        hour_pillar=_pillar_str(hour_pillar),
        # Day master
        day_master=day_master or None,
        day_master_element=day_master_element or None,
        day_master_yin_yang=day_master_yin_yang or None,
        # Month branch metadata
        month_stem=month_stem or None,
        month_branch=month_branch or None,
        month_branch_element=month_branch_element or None,
        month_stem_ten_god=month_stem_ten_god,
        month_branch_ten_god=month_branch_ten_god,
        # Per-pillar hidden stems
        month_hidden_stems=month_hidden_stems,
        year_hidden_stems=year_hidden_stems,
        day_hidden_stems=day_hidden_stems,
        hour_hidden_stems=hour_hidden_stems,
        month_hidden_elements=month_hidden_elements,
        # Flat collections
        ten_gods={"list": raw_ten_gods},
        ten_gods_list=ten_gods_list,
        hidden_stems_flat=hidden_stems_flat,
        # Element distribution
        element_distribution=element_distribution,
        # Season / temperature
        season=season,
        season_phase=season_phase,
        temperature_type=temperature_type,
        # Ten-god family lists
        support_elements=support_elements,
        drain_elements=drain_elements,
        control_elements=control_elements,
        resource_elements=resource_elements,
        wealth_elements=wealth_elements,
        officer_elements=officer_elements,
        output_elements=output_elements,
        companion_elements=companion_elements,
        # Other
        shensha=list(getattr(bazi_chart, "shensha", None) or []),
        calendar=calendar,
        bazi=bazi_chart,
    )


# ============================================================
# Private helpers
# ============================================================

def _stems_to_elements(stems: list[str]) -> list[str]:
    """Convert stem names to their element names."""
    return [STEM_META[s][0] for s in stems if s in STEM_META]


def _count_elements(stems: list[str]) -> dict[str, int]:
    """Count occurrences of each element in a list of stems."""
    counts: dict[str, int] = {}
    for s in stems:
        if s in STEM_META:
            el = STEM_META[s][0]
            counts[el] = counts.get(el, 0) + 1
    return counts


def _ten_god_element(god: str, day_master: str) -> str:
    """Return element of the stem that generates the ten god (approximate)."""
    return ""  # Used for family classification only — element not needed
