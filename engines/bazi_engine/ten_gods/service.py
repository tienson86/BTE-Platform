"""
===============================================================================
Bazi Engine - Ten Gods Service
-------------------------------------------------------------------------------
File:
    bazi_engine/ten_gods/service.py

Description:
    Facade Service cho module Thập Thần.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List

from bazi_engine.models import FourPillars

from .ten_god import (
    TenGodChart,
    TenGodResult,
)

from .calculator import (
    ten_god_calculator,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class TenGodServiceError(Exception):
    """
    Base Exception.
    """


class TenGodServiceCalculationError(
    TenGodServiceError,
):
    """
    Calculation Error.
    """


# =============================================================================
# SERVICE
# =============================================================================

class TenGodService:
    """
    Facade của toàn bộ Ten Gods Engine.
    """

    def __init__(self):

        self._calculator = ten_god_calculator

    # -----------------------------------------------------------------
    # BUILD CHART
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> TenGodChart:
        """
        Tính toàn bộ Thập Thần.
        """

        return self._calculator.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_chart(
        self,
        pillars: FourPillars,
    ) -> TenGodChart:
        """
        Lấy TenGodChart.
        """

        return self.calculate(
            pillars
        )

    # -----------------------------------------------------------------
    # SINGLE STEM
    # -----------------------------------------------------------------

    def get_stem_ten_god(
        self,
        day_master: str,
        target_stem: str,
    ) -> TenGodResult:
        """
        Tính Thập Thần của một Thiên Can.
        """

        return self._calculator.calculate_stem(

            day_master,

            target_stem,

        )

    # -----------------------------------------------------------------

    def get_hidden_ten_gods(
        self,
        day_master: str,
        hidden_stems: List[str],
    ) -> List[TenGodResult]:
        """
        Tính Thập Thần của danh sách Tàng Can.
        """

        return self._calculator.calculate_hidden_stems(

            day_master,

            hidden_stems,

        )

    # -----------------------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------------------

    def get_summary(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Tổng hợp nhanh Thập Thần.
        """

        chart = self.calculate(
            pillars
        )

        return chart.summary()

    # -----------------------------------------------------------------

    def get_frequency(
        self,
        pillars: FourPillars,
    ) -> Dict[str, int]:
        """
        Thống kê tần suất Thập Thần.
        """

        chart = self.calculate(
            pillars
        )

        return chart.frequency()

    # -----------------------------------------------------------------

    def count(
        self,
        pillars: FourPillars,
        ten_god_name: str,
    ) -> int:
        """
        Đếm số lượng một Thập Thần.
        """

        chart = self.calculate(
            pillars
        )

        return chart.count_by_name(
            ten_god_name
        )
    # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def get_all(
        self,
        pillars: FourPillars,
    ) -> List[TenGodResult]:
        """
        Lấy toàn bộ Thập Thần trong lá số.
        """

        chart = self.calculate(
            pillars
        )

        return chart.get_all()

    # -----------------------------------------------------------------

    def contains(
        self,
        pillars: FourPillars,
        ten_god_name: str,
    ) -> bool:
        """
        Kiểm tra lá số có Thập Thần này không.
        """

        chart = self.calculate(
            pillars
        )

        return chart.contains(
            ten_god_name
        )

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra có thể tính Thập Thần.
        """

        try:

            chart = self.calculate(
                pillars
            )

            return not chart.is_empty

        except Exception:

            return False

    # -----------------------------------------------------------------

    def is_valid(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Alias verify().
        """

        return self.verify(
            pillars
        )

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    @property
    def calculator(
        self,
    ):
        """
        Truy cập TenGodCalculator.
        """

        return self._calculator

    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Service.
        """

        return {

            "service":
                self.__class__.__name__,

            "calculator":
                self._calculator.__class__.__name__,

            "calculator_statistics":
                self._calculator.statistics(),

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra toàn bộ module.
        """

        return self._calculator.health_check()

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin debug.
        """

        return {

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }

    # -----------------------------------------------------------------
    # CACHE / RELOAD
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload toàn bộ Rule Database.
        """

        self._calculator.refresh()

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<TenGodService "

            f"health={self.health_check()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

ten_god_service = TenGodService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "TenGodService",

    "TenGodServiceError",

    "TenGodServiceCalculationError",

    "ten_god_service",

]
