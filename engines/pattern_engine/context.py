"""
Pattern Context V2.

Stores all input data and pre-computed derived fields for Pattern Engine rule matching.
All derived fields are computed by context_builder.py — not by PatternEngine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PatternContext:
    # ---- Basic pillars (string "Stem Branch") ----
    year_pillar: Optional[str] = None
    month_pillar: Optional[str] = None
    day_pillar: Optional[str] = None
    hour_pillar: Optional[str] = None

    # ---- Nhật chủ ----
    day_master: Optional[str] = None

    # ---- Day master metadata ----
    day_master_element: Optional[str] = None        # e.g. "Mộc"
    day_master_yin_yang: Optional[str] = None       # "Dương" | "Âm"

    # ---- Month branch metadata ----
    month_stem: Optional[str] = None                # Thiên can tháng
    month_branch: Optional[str] = None              # Địa chi tháng
    month_branch_element: Optional[str] = None      # Ngũ hành địa chi tháng

    # ---- Ten gods of month ----
    month_stem_ten_god: Optional[str] = None        # Thập thần thiên can tháng
    month_branch_ten_god: Optional[str] = None      # Thập thần can chính địa chi tháng (Lệnh Tháng)

    # ---- Per-pillar hidden stems ----
    month_hidden_stems: List[str] = field(default_factory=list)
    year_hidden_stems: List[str] = field(default_factory=list)
    day_hidden_stems: List[str] = field(default_factory=list)
    hour_hidden_stems: List[str] = field(default_factory=list)
    month_hidden_elements: List[str] = field(default_factory=list)

    # ---- Flat collections ----
    ten_gods: Dict[str, Any] = field(default_factory=dict)      # raw {"list": [...]}
    ten_gods_list: List[str] = field(default_factory=list)       # filtered list, no "Nhật Chủ"
    hidden_stems_flat: List[str] = field(default_factory=list)   # all hidden stems

    # ---- Element distribution ----
    # {"Mộc": 3, "Hỏa": 2, ...} — count of stems (incl. hidden) per element
    element_distribution: Dict[str, int] = field(default_factory=dict)

    # ---- Season / climate ----
    season: Optional[str] = None          # "spring" | "summer" | "autumn" | "winter"
    season_phase: Optional[str] = None    # "early_spring" | "mid_spring" | ...
    temperature_type: Optional[str] = None  # "warm" | "hot" | "cool" | "cold"

    # ---- Ten-god family lists (for "contains" conditions) ----
    support_elements: List[str] = field(default_factory=list)    # Tỷ Kiên + Chính Ấn families
    drain_elements: List[str] = field(default_factory=list)      # Thực Thần + Tài families
    control_elements: List[str] = field(default_factory=list)    # Quan/Sát families
    resource_elements: List[str] = field(default_factory=list)   # Ấn families
    wealth_elements: List[str] = field(default_factory=list)     # Tài families
    officer_elements: List[str] = field(default_factory=list)    # Quan/Sát families
    output_elements: List[str] = field(default_factory=list)     # Thực Thần/Thương Quan
    companion_elements: List[str] = field(default_factory=list)  # Tỷ Kiên/Kiếp Tài

    # ---- Strength (populated when Score Engine runs before Pattern) ----
    strength_level: Optional[str] = None    # "strong" | "weak" | "balanced"
    strength_score: float = 0.0

    # ---- Ngũ hành ----
    wuxing_score: Dict[str, float] = field(default_factory=dict)

    # ---- Thần sát ----
    shensha: List[str] = field(default_factory=list)

    # ---- Đại vận ----
    luck_pillar: Optional[str] = None

    # ---- Dụng thần ----
    useful_god: Optional[str] = None

    # ---- Extensible ----
    extra: Dict[str, Any] = field(default_factory=dict)

    # ---- Production pipeline objects ----
    calendar: Any = None
    bazi: Any = None
