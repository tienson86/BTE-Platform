"""
===============================================================================
Bazi Engine - Useful God Service
-------------------------------------------------------------------------------
File:
    bazi_engine/useful_god/service.py

Description:
    Facade Service cho Useful God Engine.

Version:
    1.1.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict

from bazi_engine.models import FourPillars

from .useful_god import (
    UsefulGodResult,
)

from .calculator import (
    useful_god_calculator,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class UsefulGodServiceError(
    Exception,
):
    """
    Base Exception.
    """


class UsefulGodServiceCalculationError(
    UsefulGodServiceError,
):
    """
    Calculation Error.
    """


# =============================================================================
# SERVICE
# =============================================================================

class UsefulGodService:
    """
    Facade Service của Useful God Engine.
    """

    def __init__(
        self,
    ):

        self._calculator = (
            useful_god_calculator
        )


    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> UsefulGodResult:
        """
        Tính Dụng Thần.
        """

        return self._calculator.calculate(
            pillars
        )


    # -----------------------------------------------------------------

    def get_result(
        self,
        pillars: FourPillars,
    ) -> UsefulGodResult:
        """
        Alias của calculate().
        """

        return self.calculate(
            pillars
        )


    # -----------------------------------------------------------------

    def get_useful_god(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy Dụng Thần.
        """

        return (

            self.calculate(
                pillars
            ).useful_god

        )


    # -----------------------------------------------------------------

    def get_favorable_gods(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy Hỷ Thần.
        """

        return (

            self.calculate(
                pillars
            ).favorable_gods

        )


    # -----------------------------------------------------------------

    def get_unfavorable_gods(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy Kỵ Thần.
        """

        return (

            self.calculate(
                pillars
            ).unfavorable_gods

        )


    # -----------------------------------------------------------------

    def get_neutral_gods(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy Nhàn Thần.
        """

        return (

            self.calculate(
                pillars
            ).neutral_gods

        )


    # -----------------------------------------------------------------

    def summary(
        self,
        pillars: FourPillars,
    ) -> Dict[str, object]:
        """
        Tóm tắt kết quả.
        """

        return (

            self.calculate(
                pillars
            ).summary()

        )


    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra khả năng tính toán.
        """

        try:

            result = self.calculate(
                pillars
            )

            return result.has_useful_god()

        except Exception:

            return False
              # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    @property
    def calculator(
        self,
    ):
        """
        Truy cập UsefulGodCalculator.
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
        Kiểm tra trạng thái Engine.
        """

        return self._calculator.health_check()


    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Useful God Engine.
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

            "calculator":
                repr(
                    self._calculator
                ),

        }


    # -----------------------------------------------------------------
    # RELOAD
    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
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

            "<UsefulGodService "

            f"version={self.version} "

            f"health={self.health_check()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

useful_god_service = UsefulGodService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "UsefulGodService",

    "UsefulGodServiceError",

    "UsefulGodServiceCalculationError",

    "useful_god_service",

]
