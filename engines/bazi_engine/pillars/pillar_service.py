"""
===============================================================================
Bazi Engine - Pillar Service
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/pillar_service.py

Description:
    Facade Service cho toàn bộ tầng Pillars.

Flow:

        Datetime
            │
            ▼
      PillarBuilder
            │
            ▼
      FourPillars
            │
            ▼
      Service API

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict
from typing import Optional

from bazi_engine.models import FourPillars
from bazi_engine.models import Pillar

from .pillar_builder import pillar_builder


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PillarServiceError(Exception):
    """Base Exception."""


class PillarServiceCalculationError(
    PillarServiceError,
):
    """Calculation Error."""


# =============================================================================
# SERVICE
# =============================================================================

class PillarService:
    """
    Facade của toàn bộ tầng Pillars.
    """

    def __init__(self):

        self._builder = pillar_builder

    # -----------------------------------------------------------------
    # BUILD
    # -----------------------------------------------------------------

    def build(
        self,
        target_datetime: datetime,
    ) -> FourPillars:
        """
        Xây dựng đầy đủ Tứ Trụ.
        """

        return self._builder.build(
            target_datetime
        )

    # -----------------------------------------------------------------

    def build_from_datetime(
        self,
        target_datetime: datetime,
    ) -> FourPillars:
        """
        Alias của build().
        """

        return self.build(
            target_datetime
        )

    # -----------------------------------------------------------------
    # GETTERS
    # -----------------------------------------------------------------

    def get_four_pillars(
        self,
        target_datetime: datetime,
    ) -> FourPillars:
        """
        Lấy đối tượng FourPillars.
        """

        return self.build(
            target_datetime
        )

    # -----------------------------------------------------------------

    def get_year_pillar(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Lấy Trụ Năm.
        """

        return self.build(
            target_datetime
        ).year

    # -----------------------------------------------------------------

    def get_month_pillar(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Lấy Trụ Tháng.
        """

        return self.build(
            target_datetime
        ).month

    # -----------------------------------------------------------------

    def get_day_pillar(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Lấy Trụ Ngày.
        """

        return self.build(
            target_datetime
        ).day

    # -----------------------------------------------------------------

    def get_hour_pillar(
        self,
        target_datetime: datetime,
    ) -> Optional[Pillar]:
        """
        Lấy Trụ Giờ.
        """

        return self.build(
            target_datetime
        ).hour

    # -----------------------------------------------------------------

    def get_pillars_dict(
        self,
        target_datetime: datetime,
    ) -> Dict[str, Pillar]:
        """
        Trả về dict gồm bốn trụ.
        """

        pillars = self.build(
            target_datetime
        )

        return {

            "year": pillars.year,

            "month": pillars.month,

            "day": pillars.day,

            "hour": pillars.hour,

        }

    # -----------------------------------------------------------------

    def get_ganzhi(
        self,
        target_datetime: datetime,
    ) -> Dict[str, str]:
        """
        Trả về Can Chi của bốn trụ.
        """

        pillars = self.build(
            target_datetime
        )

        return {

            "year": pillars.year.ganzhi,

            "month": pillars.month.ganzhi,

            "day": pillars.day.ganzhi,

            "hour": pillars.hour.ganzhi
            if pillars.hour
            else "",

        }
          # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def verify(
        self,
        target_datetime: datetime,
    ) -> bool:
        """
        Kiểm tra có thể lập Tứ Trụ hay không.
        """

        try:

            self.build(
                target_datetime
            )

            return True

        except Exception:

            return False

    # -----------------------------------------------------------------

    def is_valid(
        self,
        target_datetime: datetime,
    ) -> bool:
        """
        Alias của verify().
        """

        return self.verify(
            target_datetime
        )

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    @property
    def builder(self):
        """
        Trả về PillarBuilder.
        """

        return self._builder

    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Service.
        """

        return {

            "service": self.__class__.__name__,

            "builder": self._builder.__class__.__name__,

            "builder_statistics":
                self._builder.statistics(),

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra toàn bộ tầng Pillars.
        """

        return self._builder.health_check()

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin debug.
        """

        return {

            "service":
                self.__class__.__name__,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }

    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Builder.

        Builder sẽ tự reload các Calculator bên dưới nếu cần.
        """

        if hasattr(self._builder, "refresh"):

            self._builder.refresh()

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<PillarService "

            f"health={self.health_check()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

pillar_service = PillarService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "PillarService",

    "PillarServiceError",

    "PillarServiceCalculationError",

    "pillar_service",

]
