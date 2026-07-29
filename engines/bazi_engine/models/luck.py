"""
===============================================================================
Bazi Engine - Luck Models
-------------------------------------------------------------------------------
File:
    bazi_engine/models/luck.py

Description:
    Domain Models cho Đại Vận, Tiểu Vận, Lưu Niên và Lưu Nguyệt.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


# =============================================================================
# BASE LUCK
# =============================================================================

@dataclass(slots=True)
class BaseLuck:
    """
    Mô hình cơ sở cho các loại vận.
    """

    name: str = ""

    start_year: int = 0

    end_year: int = 0

    age_start: int = 0

    age_end: int = 0

    stem: str = ""

    branch: str = ""

    stem_index: int = 0

    branch_index: int = 0

    stem_element: str = ""

    branch_element: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ganzhi(self) -> str:
        return f"{self.stem}{self.branch}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)


# =============================================================================
# MAJOR LUCK (ĐẠI VẬN)
# =============================================================================

@dataclass(slots=True)
class LuckPillar(BaseLuck):
    """
    Một Đại Vận 10 năm.
    """

    order: int = 0

    direction: str = ""

    years: List[int] = field(default_factory=list)


# =============================================================================
# ANNUAL LUCK (LƯU NIÊN)
# =============================================================================

@dataclass(slots=True)
class AnnualLuck(BaseLuck):
    """
    Một năm vận.
    """

    year: int = 0


# =============================================================================
# MONTHLY LUCK (LƯU NGUYỆT)
# =============================================================================

@dataclass(slots=True)
class MonthlyLuck(BaseLuck):
    """
    Một tháng vận.
    """

    year: int = 0

    month: int = 0


# =============================================================================
# MINOR LUCK (TIỂU VẬN)
# =============================================================================

@dataclass(slots=True)
class MinorLuck(BaseLuck):
    """
    Một Tiểu Vận.
    """

    year: int = 0

    age: int = 0


# =============================================================================
# LUCK COLLECTION
# =============================================================================

@dataclass(slots=True)
class LuckCycle:
    """
    Tập hợp toàn bộ các vận của lá số.
    """

    major_luck: List[LuckPillar] = field(default_factory=list)

    minor_luck: List[MinorLuck] = field(default_factory=list)

    annual_luck: List[AnnualLuck] = field(default_factory=list)

    monthly_luck: List[MonthlyLuck] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def has_major_luck(self) -> bool:
        return len(self.major_luck) > 0

    @property
    def has_minor_luck(self) -> bool:
        return len(self.minor_luck) > 0

    @property
    def has_annual_luck(self) -> bool:
        return len(self.annual_luck) > 0

    @property
    def has_monthly_luck(self) -> bool:
        return len(self.monthly_luck) > 0

    def clear(self):

        self.major_luck.clear()

        self.minor_luck.clear()

        self.annual_luck.clear()

        self.monthly_luck.clear()

        self.metadata.clear()

    def __len__(self):

        return (
            len(self.major_luck)
            + len(self.minor_luck)
            + len(self.annual_luck)
            + len(self.monthly_luck)
        )

    def __repr__(self):

        return (
            "<LuckCycle "
            f"major={len(self.major_luck)} "
            f"minor={len(self.minor_luck)} "
            f"annual={len(self.annual_luck)} "
            f"monthly={len(self.monthly_luck)}>"
        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "BaseLuck",

    "LuckPillar",

    "MinorLuck",

    "AnnualLuck",

    "MonthlyLuck",

    "LuckCycle",

]
