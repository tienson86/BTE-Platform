"""
===============================================================================
Bazi Engine - Four Pillars Model
-------------------------------------------------------------------------------
File:
    bazi_engine/models/four_pillars.py

Description:
    Domain Model của Tứ Trụ Bát Tự.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from .pillar import Pillar


# =============================================================================
# MODEL
# =============================================================================

@dataclass(slots=True)
class FourPillars:
    """
    Mô hình Tứ Trụ Bát Tự.
    """

    # -----------------------------------------------------------------
    # Bốn trụ
    # -----------------------------------------------------------------

    year: Pillar

    month: Pillar

    day: Pillar

    hour: Optional[Pillar] = None

    # -----------------------------------------------------------------
    # Thông tin ngày giờ sinh
    # -----------------------------------------------------------------

    birth_datetime: Optional[datetime] = None

    gender: str = ""

    timezone: str = "Asia/Ho_Chi_Minh"

    longitude: float = 0.0

    latitude: float = 0.0

    # -----------------------------------------------------------------
    # Dữ liệu mở rộng
    # -----------------------------------------------------------------

    metadata: Dict = field(default_factory=dict)

    tags: List[str] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------

    @property
    def year_ganzhi(self) -> str:
        return self.year.ganzhi

    @property
    def month_ganzhi(self) -> str:
        return self.month.ganzhi

    @property
    def day_ganzhi(self) -> str:
        return self.day.ganzhi

    @property
    def hour_ganzhi(self) -> str:
        if self.hour is None:
            return ""
        return self.hour.ganzhi

    @property
    def pillars(self) -> List[Pillar]:
        """
        Danh sách các trụ theo thứ tự.
        """

        result = [
            self.year,
            self.month,
            self.day,
        ]

        if self.hour is not None:
            result.append(self.hour)

        return result

    @property
    def stem_sequence(self) -> List[str]:
        return [pillar.stem for pillar in self.pillars]

    @property
    def branch_sequence(self) -> List[str]:
        return [pillar.branch for pillar in self.pillars]

    @property
    def ganzhi_sequence(self) -> List[str]:
        return [pillar.ganzhi for pillar in self.pillars]

    # -----------------------------------------------------------------
    # Methods
    # -----------------------------------------------------------------

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):

        return cls(

            year=Pillar.from_dict(
                data["year"]
            ),

            month=Pillar.from_dict(
                data["month"]
            ),

            day=Pillar.from_dict(
                data["day"]
            ),

            hour=(
                Pillar.from_dict(
                    data["hour"]
                )
                if data.get("hour")
                else None
            ),

            birth_datetime=data.get(
                "birth_datetime"
            ),

            gender=data.get(
                "gender",
                ""
            ),

            timezone=data.get(
                "timezone",
                "Asia/Ho_Chi_Minh"
            ),

            longitude=float(
                data.get(
                    "longitude",
                    0.0
                )
            ),

            latitude=float(
                data.get(
                    "latitude",
                    0.0
                )
            ),

            metadata=data.get(
                "metadata",
                {}
            ),

            tags=list(
                data.get(
                    "tags",
                    []
                )
            ),
        )

    def copy(self):

        return FourPillars(

            year=self.year.copy(),

            month=self.month.copy(),

            day=self.day.copy(),

            hour=(
                self.hour.copy()
                if self.hour
                else None
            ),

            birth_datetime=self.birth_datetime,

            gender=self.gender,

            timezone=self.timezone,

            longitude=self.longitude,

            latitude=self.latitude,

            metadata=self.metadata.copy(),

            tags=self.tags.copy(),
        )

    # -----------------------------------------------------------------

    def __len__(self):

        return len(
            self.pillars
        )

    # -----------------------------------------------------------------

    def __iter__(self):

        return iter(
            self.pillars
        )

    # -----------------------------------------------------------------

    def __getitem__(self, index):

        return self.pillars[index]

    # -----------------------------------------------------------------

    def __repr__(self):

        hour = (
            self.hour.ganzhi
            if self.hour
            else "--"
        )

        return (

            f"<FourPillars "

            f"{self.year.ganzhi} "

            f"{self.month.ganzhi} "

            f"{self.day.ganzhi} "

            f"{hour}>"

        )


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "FourPillars",

]
