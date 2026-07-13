"""
===============================================================================
Bazi Engine - Bazi Chart Model
-------------------------------------------------------------------------------
File:
    bazi_engine/models/bazi_chart.py

Description:
    Domain Model của toàn bộ lá số Bát Tự.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .four_pillars import FourPillars


# =============================================================================
# MODEL
# =============================================================================

@dataclass(slots=True)
class BaziChart:
    """
    Mô hình đầy đủ của một lá số Bát Tự.

    Đây là đối tượng trung tâm của toàn bộ Bazi Engine.
    """

    # -----------------------------------------------------------------
    # THÔNG TIN CƠ BẢN
    # -----------------------------------------------------------------

    chart_id: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    version: str = "1.0.0"

    # -----------------------------------------------------------------
    # THÔNG TIN NGƯỜI ĐƯỢC LẬP LÁ SỐ
    # -----------------------------------------------------------------

    full_name: str = ""

    gender: str = ""

    birth_datetime: Optional[datetime] = None

    timezone: str = "Asia/Ho_Chi_Minh"

    longitude: float = 0.0

    latitude: float = 0.0

    place_of_birth: str = ""

    # -----------------------------------------------------------------
    # TỨ TRỤ
    # -----------------------------------------------------------------

    four_pillars: Optional[FourPillars] = None

    # -----------------------------------------------------------------
    # TÀNG CAN
    # -----------------------------------------------------------------

    hidden_stems: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # THẬP THẦN
    # -----------------------------------------------------------------

    ten_gods: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # THẬP NHỊ TRƯỜNG SINH
    # -----------------------------------------------------------------

    twelve_stages: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # VƯỢNG SUY
    # -----------------------------------------------------------------

    strength: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # DỤNG THẦN
    # -----------------------------------------------------------------

    useful_god: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # THẦN SÁT
    # -----------------------------------------------------------------

    shensha: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # NẠP ÂM
    # -----------------------------------------------------------------

    nayin: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # KHÔNG VONG
    # -----------------------------------------------------------------

    xunkong: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # ĐẠI VẬN
    # -----------------------------------------------------------------

    major_luck: List[Any] = field(default_factory=list)

    # -----------------------------------------------------------------
    # TIỂU VẬN
    # -----------------------------------------------------------------

    minor_luck: List[Any] = field(default_factory=list)

    # -----------------------------------------------------------------
    # LƯU NIÊN
    # -----------------------------------------------------------------

    annual_luck: List[Any] = field(default_factory=list)

    # -----------------------------------------------------------------
    # LƯU NGUYỆT
    # -----------------------------------------------------------------

    monthly_luck: List[Any] = field(default_factory=list)

    # -----------------------------------------------------------------
    # PHÂN TÍCH
    # -----------------------------------------------------------------

    analysis: Dict[str, Any] = field(default_factory=dict)

    interpretation: Dict[str, Any] = field(default_factory=dict)

    recommendations: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # MỞ RỘNG
    # -----------------------------------------------------------------

    metadata: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------
    # PROPERTY
    # -----------------------------------------------------------------

    @property
    def has_hour_pillar(self) -> bool:

        if self.four_pillars is None:

            return False

        return self.four_pillars.hour is not None

    @property
    def day_master(self):

        if self.four_pillars is None:

            return None

        return self.four_pillars.day

    @property
    def day_master_stem(self):

        if self.day_master is None:

            return ""

        return self.day_master.stem

    @property
    def day_master_element(self):

        if self.day_master is None:

            return ""

        return self.day_master.stem_element

    @property
    def pillars(self):

        if self.four_pillars is None:

            return []

        return self.four_pillars.pillars

    # -----------------------------------------------------------------
    # METHODS
    # -----------------------------------------------------------------

    def to_dict(self):

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: Dict,
    ):

        chart = cls()

        chart.chart_id = data.get("chart_id", "")

        chart.created_at = data.get(
            "created_at",
            datetime.now(),
        )

        chart.version = data.get(
            "version",
            "1.0.0",
        )

        chart.full_name = data.get(
            "full_name",
            "",
        )

        chart.gender = data.get(
            "gender",
            "",
        )

        chart.birth_datetime = data.get(
            "birth_datetime",
        )

        chart.timezone = data.get(
            "timezone",
            "Asia/Ho_Chi_Minh",
        )

        chart.longitude = float(
            data.get(
                "longitude",
                0.0,
            )
        )

        chart.latitude = float(
            data.get(
                "latitude",
                0.0,
            )
        )

        chart.place_of_birth = data.get(
            "place_of_birth",
            "",
        )

        if data.get("four_pillars"):

            chart.four_pillars = FourPillars.from_dict(
                data["four_pillars"]
            )

        chart.hidden_stems = data.get(
            "hidden_stems",
            {},
        )

        chart.ten_gods = data.get(
            "ten_gods",
            {},
        )

        chart.twelve_stages = data.get(
            "twelve_stages",
            {},
        )

        chart.strength = data.get(
            "strength",
            {},
        )

        chart.useful_god = data.get(
            "useful_god",
            {},
        )

        chart.shensha = data.get(
            "shensha",
            {},
        )

        chart.nayin = data.get(
            "nayin",
            {},
        )

        chart.xunkong = data.get(
            "xunkong",
            {},
        )

        chart.major_luck = list(
            data.get(
                "major_luck",
                [],
            )
        )

        chart.minor_luck = list(
            data.get(
                "minor_luck",
                [],
            )
        )

        chart.annual_luck = list(
            data.get(
                "annual_luck",
                [],
            )
        )

        chart.monthly_luck = list(
            data.get(
                "monthly_luck",
                [],
            )
        )

        chart.analysis = data.get(
            "analysis",
            {},
        )

        chart.interpretation = data.get(
            "interpretation",
            {},
        )

        chart.recommendations = data.get(
            "recommendations",
            {},
        )

        chart.metadata = data.get(
            "metadata",
            {},
        )

        return chart

    def __repr__(self):

        if self.four_pillars:

            return (
                f"<BaziChart "
                f"{self.four_pillars.year.ganzhi} "
                f"{self.four_pillars.month.ganzhi} "
                f"{self.four_pillars.day.ganzhi}>"
            )

        return "<BaziChart Empty>"


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "BaziChart",

]
