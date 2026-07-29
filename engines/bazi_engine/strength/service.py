"""
===============================================================================
Bazi Engine - Strength Service
-------------------------------------------------------------------------------
File:
    bazi_engine/strength/service.py

Description:
    Facade Service cho Strength Engine.

Version:
    1.1.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict

from bazi_engine.models import FourPillars

from .strength import (
    StrengthLevel,
    StrengthResult,
)

from .calculator import (
    strength_calculator,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class StrengthServiceError(
    Exception,
):
    """
    Base Exception.
    """


class StrengthServiceCalculationError(
    StrengthServiceError,
):
    """
    Calculation Error.
    """


# =============================================================================
# SERVICE
# =============================================================================

class StrengthService:
    """
    Facade của Strength Engine.
    """

    def __init__(
        self,
    ):

        self._calculator = (
            strength_calculator
        )

    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        Tính Thân Vượng Nhược.
        """

        return self._calculator.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_result(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        Alias của calculate().
        """

        return self.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Lấy điểm Thân.
        """

        return self._calculator.calculate_score(
            pillars
        )

    # -----------------------------------------------------------------

    def get_level(
        self,
        pillars: FourPillars,
    ) -> StrengthLevel:
        """
        Lấy cấp độ Thân.
        """

        return self._calculator.calculate_level(
            pillars
        )

    # -----------------------------------------------------------------

    def is_strong(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra Thân Vượng.
        """

        return self._calculator.is_strong(
            pillars
        )

    # -----------------------------------------------------------------

    def is_weak(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra Thân Nhược.
        """

        return self._calculator.is_weak(
            pillars
        )

    # -----------------------------------------------------------------

    def summary(
        self,
        pillars: FourPillars,
    ) -> Dict[str, object]:
        """
        Tổng hợp kết quả.
        """

        return self._calculator.summary(
            pillars
        )

    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra dữ liệu.
        """

        return self._calculator.verify(
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
        Truy cập StrengthCalculator.
        """

        return self._calculator


    # -----------------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Phiên bản Service.
        """

        return "1.1.0"


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái của Strength Engine.
        """

        return self._calculator.health_check()


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

            "version":
                self.version,

            "calculator":
                self._calculator.__class__.__name__,

            "calculator_statistics":
                self._calculator.statistics(),

        }


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }


    # -----------------------------------------------------------------
    # RELOAD
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload toàn bộ Strength Engine.
        """

        self._calculator.refresh()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache.
        """

        self._calculator.clear_cache()


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<StrengthService "

            f"version={self.version} "

            f"health={self.health_check()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

strength_service = StrengthService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "StrengthService",

    "StrengthServiceError",

    "StrengthServiceCalculationError",

    "strength_service",

]
