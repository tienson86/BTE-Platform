"""Cân Xương Đoán Mệnh result model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CAN_XUONG_RULE_VERSION = "G1-11"
CAN_XUONG_SOURCE = "yuan_tian_gang_can_xuong"


@dataclass(slots=True)
class CanXuongResult:
    """Canonical analysis.can_xuong payload. Presentation copies these fields."""

    total_weight: int
    liang: int
    chi: int
    display_weight: str
    classification: str
    rating: str
    summary: str
    interpretation: str
    source: str = CAN_XUONG_SOURCE
    version: str = CAN_XUONG_RULE_VERSION
    year_chi: int = 0
    month_chi: int = 0
    day_chi: int = 0
    hour_chi: int = 0
    year_ganzhi: str = ""
    lunar_month: int = 0
    lunar_day: int = 0
    hour_branch: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API, ResultStore, header, S10, and report."""
        return {
            "total_weight": self.total_weight,
            "liang": self.liang,
            "chi": self.chi,
            "display_weight": self.display_weight,
            "classification": self.classification,
            "rating": self.rating,
            "summary": self.summary,
            "interpretation": self.interpretation,
            "source": self.source,
            "version": self.version,
            "weight": self.display_weight,
            "total": self.display_weight,
            "poem": self.interpretation,
            "year_chi": self.year_chi,
            "month_chi": self.month_chi,
            "day_chi": self.day_chi,
            "hour_chi": self.hour_chi,
            "year_ganzhi": self.year_ganzhi,
            "lunar_month": self.lunar_month,
            "lunar_day": self.lunar_day,
            "hour_branch": self.hour_branch,
        }
