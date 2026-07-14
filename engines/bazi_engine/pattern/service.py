"""
===============================================================================
Bazi Engine - Pattern Service
-------------------------------------------------------------------------------
File:
    bazi_engine/pattern/service.py

Description:
    Facade Service cho Pattern Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict

from bazi_engine.models import FourPillars

from .pattern import Pattern
from .pattern import PatternResult

from .calculator import (
    pattern_calculator,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PatternServiceError(Exception):
    """
    Base Exception.
    """


class PatternServiceCalculationError(
    PatternServiceError,
):
    """
    Calculation Error.
    """


# =============================================================================
# SERVICE
# =============================================================================

class PatternService:
    """
    Facade Service của Pattern Engine.
    """

    def __init__(
        self,
    ):

        self._calculator = (
            pattern_calculator
        )

    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> PatternResult:
        """
        Xác định Cách Cục.
        """

        return self._calculator.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_result(
        self,
        pillars: FourPillars,
    ) -> PatternResult:
        """
        Alias của calculate().
        """

        return self.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_pattern(
        self,
        pillars: FourPillars,
    ) -> Pattern:
        """
        Lấy Chính Cách.
        """

        return (

            self.calculate(
                pillars
            ).main_pattern

        )

    # -----------------------------------------------------------------

    def get_patterns(
        self,
        pillars: FourPillars,
    ):
        """
        Danh sách các Cách Cục phù hợp.
        """

        return (

            self.calculate(
                pillars
            ).matched_patterns

        )

    # -----------------------------------------------------------------

    def is_follow_pattern(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Có phải Tòng Cách.
        """

        return (

            self.calculate(
                pillars
            ).follow_pattern

        )

    # -----------------------------------------------------------------

    def is_transformation_pattern(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Có phải Hóa Khí Cách.
        """

        return (

            self.calculate(
                pillars
            ).transformation_pattern

        )

    # -----------------------------------------------------------------

    def is_special_pattern(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Có phải Ngoại Cách.
        """

        return (

            self.calculate(
                pillars
            ).special_pattern

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
        Kiểm tra khả năng xác định Cách Cục.
        """

        try:

            result = self.calculate(
                pillars
            )

            return result.has_pattern()

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
        Truy cập PatternCalculator.
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

        return "1.0.0"


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
        Thống kê Pattern Engine.
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
                repr(self._calculator),

        }


    # -----------------------------------------------------------------
    # CACHE
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
    # MAGIC METHODS
    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<PatternService "

            f"version={self.version} "

            f"health={self.health_check()}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

pattern_service = PatternService()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "PatternService",

    "PatternServiceError",

    "PatternServiceCalculationError",

    "pattern_service",

]
