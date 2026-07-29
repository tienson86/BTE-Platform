"""
===============================================================================
Bazi Engine - Year Pillar Calculator
-------------------------------------------------------------------------------
Tính Can Chi Năm (Niên Trụ)

Quy tắc:

1. Sử dụng mốc Lập Xuân để đổi năm.
2. Nếu sinh trước Lập Xuân:
       dùng năm trước.
3. Nếu sinh từ Lập Xuân trở đi:
       dùng năm hiện tại.
4. Sau khi xác định năm Bát Tự mới tính Thiên Can và Địa Chi.

Không tự tính Lập Xuân trong module này.
Module chỉ nhận dữ liệu từ Calendar Engine.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..core.constants import HEAVENLY_STEMS
from ..core.constants import EARTHLY_BRANCHES

from ..core.exceptions import PillarCalculationError

# =============================================================================
# REFERENCE YEAR
# =============================================================================
#
# 1984 = Giáp Tý
#
# Đây là mốc chuẩn thường dùng trong các thư viện Bát Tự.
#
# =============================================================================

REFERENCE_YEAR = 1984

REFERENCE_STEM_INDEX = 0
REFERENCE_BRANCH_INDEX = 0


# =============================================================================
# DATA MODEL
# =============================================================================

@dataclass(slots=True)
class YearPillar:

    year: int

    stem: str

    branch: str

    adjusted_year: int

    after_li_chun: bool


# =============================================================================
# CALCULATOR
# =============================================================================

class YearPillarCalculator:

    """
    Calculator tính Niên Trụ.
    """

    def __init__(self):

        pass

    # -------------------------------------------------------------------------
    # DETERMINE BAZI YEAR
    # -------------------------------------------------------------------------

    def determine_year(
        self,
        birth_datetime: datetime,
        li_chun_datetime: datetime,
    ) -> tuple[int, bool]:

        """
        Xác định năm Bát Tự.

        Returns
        -------
        adjusted_year
        after_li_chun
        """

        if birth_datetime >= li_chun_datetime:

            return birth_datetime.year, True

        return birth_datetime.year - 1, False

    # -------------------------------------------------------------------------
    # STEM
    # -------------------------------------------------------------------------

    def calculate_stem(
        self,
        adjusted_year: int,
    ) -> str:

        index = (
            adjusted_year
            - REFERENCE_YEAR
            + REFERENCE_STEM_INDEX
        ) % 10

        return HEAVENLY_STEMS[index]

    # -------------------------------------------------------------------------
    # BRANCH
    # -------------------------------------------------------------------------

    def calculate_branch(
        self,
        adjusted_year: int,
    ) -> str:

        index = (
            adjusted_year
            - REFERENCE_YEAR
            + REFERENCE_BRANCH_INDEX
        ) % 12

        return EARTHLY_BRANCHES[index]

    # -------------------------------------------------------------------------
    # MAIN
    # -------------------------------------------------------------------------

    def calculate(
        self,
        birth_datetime: datetime,
        li_chun_datetime: datetime,
    ) -> YearPillar:

        """
        Tính Niên Trụ.
        """

        try:

            adjusted_year, after_li_chun = self.determine_year(
                birth_datetime,
                li_chun_datetime,
            )

            stem = self.calculate_stem(adjusted_year)

            branch = self.calculate_branch(adjusted_year)

            return YearPillar(
                year=birth_datetime.year,
                stem=stem,
                branch=branch,
                adjusted_year=adjusted_year,
                after_li_chun=after_li_chun,
            )

        except Exception as exc:

            raise PillarCalculationError(
                f"Không thể tính Niên Trụ: {exc}"
            ) from exc


# =============================================================================
# SINGLETON
# =============================================================================

year_pillar_calculator = YearPillarCalculator()
