"""
===============================================================================
Bazi Engine - Shen Sha Service
-------------------------------------------------------------------------------
File:
    bazi_engine/shensha/service.py

Description:
    Service Layer cho Shen Sha Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from bazi_engine.core.base_service import BaseService

from bazi_engine.models import FourPillars

from .calculator import (
    ShenShaCalculator,
    shensha_calculator,
)

from .shensha import (
    ShenShaResult,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ShenShaServiceError(Exception):
    """
    Base Exception.
    """


class ShenShaServiceCalculationError(
    ShenShaServiceError,
):
    """
    Calculation Error.
    """


# =============================================================================
# SERVICE
# =============================================================================

class ShenShaService(BaseService):
    """
    Service của Shen Sha Engine.
    """

    def __init__(
        self,
    ):

        super().__init__(

            shensha_calculator

        )

    # -----------------------------------------------------------------
    # MAIN API
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> ShenShaResult:
        """
        Lập toàn bộ Thần Sát.
        """

        try:

            return self.calculator.calculate(
                pillars
            )

        except Exception as ex:

            raise ShenShaServiceCalculationError(
                str(ex)
            ) from ex


    # -----------------------------------------------------------------

    def get_shensha(
        self,
        pillars: FourPillars,
    ) -> ShenShaResult:
        """
        Alias của calculate().
        """

        return self.calculate(
            pillars
        )


    # -----------------------------------------------------------------

    def has_shensha(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Lá số có Thần Sát hay không.
        """

        result = self.calculate(
            pillars
        )

        return result.has_shensha()


    # -----------------------------------------------------------------

    def count(
        self,
        pillars: FourPillars,
    ) -> int:
        """
        Tổng số Thần Sát.
        """

        result = self.calculate(
            pillars
        )

        return result.count()
          # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def find(
        self,
        pillars: FourPillars,
        code: str,
    ):
        """
        Tìm Thần Sát theo mã.
        """

        result = self.calculate(
            pillars
        )

        return result.find(
            code
        )


    # -----------------------------------------------------------------

    def summary(
        self,
        pillars: FourPillars,
    ) -> dict:
        """
        Tóm tắt kết quả Thần Sát.
        """

        result = self.calculate(
            pillars
        )

        return result.summary()


    # -----------------------------------------------------------------

    def to_dict(
        self,
        pillars: FourPillars,
    ) -> dict:
        """
        Chuyển kết quả sang Dictionary.
        """

        result = self.calculate(
            pillars
        )

        return result.to_dict()


    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> dict:
        """
        Thống kê Service.
        """

        return {

            "service":
                self.service_name,

            "calculator":
                self.calculator_name,

            "version":
                self.version,

            "available":
                self.available(),

            "calculator_statistics":
                self.calculator.statistics(),

        }


    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload dữ liệu.
        """

        self.calculator.refresh()


    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa Cache.
        """

        self.calculator.clear_cache()


    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> dict:
        """
        Thông tin Debug.
        """

        return {

            "service":
                self.service_name,

            "version":
                self.version,

            "available":
                self.available(),

            "calculator":
                repr(
                    self.calculator
                ),

            "statistics":
                self.statistics(),

        }


    # -----------------------------------------------------------------
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<ShenShaService "

            f"version={self.version} "

            f"available={self.available()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

shensha_service = ShenShaService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "ShenShaService",

    "ShenShaServiceError",

    "ShenShaServiceCalculationError",

    "shensha_service",

]
