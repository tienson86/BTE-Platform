"""
===============================================================================
Bazi Engine - Four Pillars Builder
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/pillar_builder.py

Description:
    Builder tạo đối tượng FourPillars từ thời gian sinh.

Flow:

        Datetime
            │
            ▼
      Year Calculator
            │
            ▼
      Month Calculator
            │
            ▼
       Day Calculator
            │
            ▼
      Hour Calculator
            │
            ▼
    Hidden Stem Calculator
            │
            ▼
        FourPillars

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from datetime import datetime
from typing import Dict

from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars
from bazi_engine.models import Pillar

from .year_pillar import year_pillar_calculator
from .month_pillar import month_pillar_calculator
from .day_pillar import day_pillar_calculator
from .hour_pillar import hour_pillar_calculator
from .hidden_stems import hidden_stems_calculator


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PillarBuilderError(Exception):
    """Base Exception."""


class PillarBuilderCalculationError(
    PillarBuilderError,
):
    """Builder Calculation Error."""


# =============================================================================
# BUILDER
# =============================================================================

class PillarBuilder(
    BaseCalculator,
):
    """
    Builder tạo FourPillars.
    """

    def __init__(self):

        super().__init__()

        self.mark_loaded()

    # -----------------------------------------------------------------

    def _attach_hidden_stems(
        self,
        pillar: Pillar,
    ) -> Pillar:
        """
        Gắn Tàng Can vào Pillar.
        """

        result = hidden_stems_calculator.get_hidden_stems(
            pillar.branch
        )

        hidden = tuple(

            stem.stem

            for stem in result.stems

        )

        return replace(

            pillar,

            hidden_stems=hidden,

        )

    # -----------------------------------------------------------------

    def _build_year(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Tạo Trụ Năm.
        """

        pillar = year_pillar_calculator.get_year_pillar(
            target_datetime
        )

        return self._attach_hidden_stems(
            pillar
        )

    # -----------------------------------------------------------------

    def _build_month(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Tạo Trụ Tháng.
        """

        pillar = month_pillar_calculator.get_month_pillar(
            target_datetime
        )

        return self._attach_hidden_stems(
            pillar
        )

    # -----------------------------------------------------------------

    def _build_day(
        self,
        target_datetime: datetime,
    ) -> Pillar:
        """
        Tạo Trụ Ngày.
        """

        pillar = day_pillar_calculator.get_day_pillar(
            target_datetime
        )

        return self._attach_hidden_stems(
            pillar
        )

    # -----------------------------------------------------------------

    def _build_hour(
        self,
        target_datetime: datetime,
        day_stem: str,
    ) -> Pillar:
        """
        Tạo Trụ Giờ.
        """

        pillar = hour_pillar_calculator.get_hour_pillar(

            target_datetime,

            day_stem,

        )

        return self._attach_hidden_stems(
            pillar
        )
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

        self.ensure_loaded()

        year_pillar = self._build_year(
            target_datetime
        )

        month_pillar = self._build_month(
            target_datetime
        )

        day_pillar = self._build_day(
            target_datetime
        )

        hour_pillar = self._build_hour(
            target_datetime,
            day_pillar.stem,
        )

        return FourPillars(

            year=year_pillar,

            month=month_pillar,

            day=day_pillar,

            hour=hour_pillar,

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

    def verify(
        self,
        target_datetime: datetime,
    ) -> bool:
        """
        Kiểm tra có thể tạo Tứ Trụ hay không.
        """

        try:

            self.build(
                target_datetime
            )

            return True

        except Exception:

            return False

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê Builder.
        """

        return {

            "pillar_count": 4,

            "calculator_count": 5,

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái toàn bộ Builder.
        """

        return (

            year_pillar_calculator.health_check()

            and month_pillar_calculator.health_check()

            and day_pillar_calculator.health_check()

            and hour_pillar_calculator.health_check()

            and hidden_stems_calculator.health_check()

        )

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict:
        """
        Thông tin debug.
        """

        return {

            "loaded":
                self.loaded,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<PillarBuilder "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

pillar_builder = PillarBuilder()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "PillarBuilder",

    "PillarBuilderError",

    "PillarBuilderCalculationError",

    "pillar_builder",

]
