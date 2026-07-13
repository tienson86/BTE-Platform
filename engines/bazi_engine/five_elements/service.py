"""
===============================================================================
Bazi Engine - Five Elements Service
-------------------------------------------------------------------------------
File:
    bazi_engine/five_elements/service.py

Description:
    Facade Service cho Ngũ Hành Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations


from typing import Dict


from bazi_engine.models import FourPillars


from .element import (
    ElementBalance,
)


from .calculator import (
    five_element_calculator,
)



# =============================================================================
# EXCEPTIONS
# =============================================================================

class FiveElementServiceError(
    Exception,
):
    """
    Base Exception.
    """



class FiveElementServiceCalculationError(
    FiveElementServiceError,
):
    """
    Calculation Error.
    """



# =============================================================================
# SERVICE
# =============================================================================

class FiveElementService:
    """
    Facade của Five Elements Engine.
    """


    def __init__(
        self,
    ):

        self._calculator = (
            five_element_calculator
        )



    # -----------------------------------------------------------------
    # CALCULATE
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> ElementBalance:
        """
        Tính toàn bộ Ngũ Hành.
        """

        return self._calculator.calculate(
            pillars
        )



    # -----------------------------------------------------------------

    def get_balance(
        self,
        pillars: FourPillars,
    ) -> ElementBalance:
        """
        Lấy bảng cân bằng Ngũ Hành.
        """

        return self.calculate(
            pillars
        )



    # -----------------------------------------------------------------

    def get_percentage(
        self,
        pillars: FourPillars,
    ) -> Dict[str, float]:
        """
        Lấy tỷ lệ phần trăm Ngũ Hành.
        """

        return self._calculator.calculate_percentage(
            pillars
        )



    # -----------------------------------------------------------------

    def get_dominant(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy hành mạnh nhất.
        """

        return self._calculator.dominant_element(
            pillars
        )



    # -----------------------------------------------------------------

    def get_weakest(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy hành yếu nhất.
        """

        return self._calculator.weakest_element(
            pillars
        )



    # -----------------------------------------------------------------

    def summary(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Tổng hợp nhanh Ngũ Hành.
        """

        balance = self.calculate(
            pillars
        )


        return balance.summary()



    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra tính hợp lệ.
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
        Truy cập FiveElementCalculator.
        """

        return self._calculator



    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái toàn bộ Module.
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
        Reload toàn bộ dữ liệu Ngũ Hành.
        """

        self._calculator.refresh()



    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache dữ liệu.
        """

        self._calculator.clear_cache()



    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<FiveElementService "

            f"health={self.health_check()}>"

        )



# =============================================================================
# SINGLETON
# =============================================================================

five_element_service = FiveElementService()



# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "FiveElementService",

    "FiveElementServiceError",

    "FiveElementServiceCalculationError",

    "five_element_service",

]
