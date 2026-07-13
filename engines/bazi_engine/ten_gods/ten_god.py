"""
===============================================================================
Bazi Engine - Ten Gods Models
-------------------------------------------------------------------------------
File:
    bazi_engine/ten_gods/ten_god.py

Description:
    Domain Models cho Thập Thần (Ten Gods).

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# =============================================================================
# TEN GOD
# =============================================================================

@dataclass(slots=True)
class TenGod:
    """
    Mô hình một Thập Thần.
    """

    code: str = ""

    name: str = ""

    chinese: str = ""

    short_name: str = ""

    category: str = ""

    polarity: str = ""

    element_relation: str = ""

    description: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "TenGod":

        return cls(**data)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:

        return (
            f"<TenGod "
            f"{self.code}:{self.name}>"
        )


# =============================================================================
# TEN GOD RESULT
# =============================================================================

@dataclass(slots=True)
class TenGodResult:
    """
    Kết quả tính một Thập Thần.
    """

    day_master: str

    target_stem: str

    ten_god: TenGod

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:

        return self.ten_god.name

    @property
    def code(self) -> str:

        return self.ten_god.code

    def to_dict(self):

        return {

            "day_master": self.day_master,

            "target_stem": self.target_stem,

            "ten_god": self.ten_god.to_dict(),

            "metadata": self.metadata,

        }


# =============================================================================
# TEN GOD CHART
# =============================================================================

@dataclass(slots=True)
class TenGodChart:
    """
    Toàn bộ Thập Thần của một lá số.
    """

    year_stem: Optional[TenGodResult] = None

    month_stem: Optional[TenGodResult] = None

    day_stem: Optional[TenGodResult] = None

    hour_stem: Optional[TenGodResult] = None

    hidden_stems: Dict[str, List[TenGodResult]] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
  # =============================================================================
# HELPERS
# =============================================================================

    @property
    def heavenly_stems(self) -> List[TenGodResult]:
        """
        Danh sách Thập Thần của 4 Thiên Can.
        """

        result = []

        if self.year_stem:

            result.append(self.year_stem)

        if self.month_stem:

            result.append(self.month_stem)

        if self.day_stem:

            result.append(self.day_stem)

        if self.hour_stem:

            result.append(self.hour_stem)

        return result

    @property
    def hidden_count(self) -> int:
        """
        Tổng số Thập Thần của Tàng Can.
        """

        total = 0

        for values in self.hidden_stems.values():

            total += len(values)

        return total

    @property
    def total_count(self) -> int:
        """
        Tổng số Thập Thần.
        """

        return len(self.heavenly_stems) + self.hidden_count

    def to_dict(self):

        return {

            "year_stem":
                self.year_stem.to_dict()
                if self.year_stem
                else None,

            "month_stem":
                self.month_stem.to_dict()
                if self.month_stem
                else None,

            "day_stem":
                self.day_stem.to_dict()
                if self.day_stem
                else None,

            "hour_stem":
                self.hour_stem.to_dict()
                if self.hour_stem
                else None,

            "hidden_stems": {

                key: [

                    item.to_dict()

                    for item in value

                ]

                for key, value

                in self.hidden_stems.items()

            },

            "metadata": self.metadata,

        }

    def __len__(self):

        return self.total_count

    def __repr__(self):

        return (

            "<TenGodChart "

            f"stems={len(self.heavenly_stems)} "

            f"hidden={self.hidden_count}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "TenGod",

    "TenGodResult",

    "TenGodChart",

]
