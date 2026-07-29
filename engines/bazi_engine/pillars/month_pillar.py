"""
===============================================================================
Bazi Engine - Month Pillar Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/month_pillar.py

Description:
    Tính Trụ Tháng (Month Pillar)

Flow:
        Datetime
            │
            ▼
      Solar Term Engine
            │
            ▼
     Current Solar Term
            │
            ▼
      Month Branch
            │
            ▼
      Year Heavenly Stem
            │
            ▼
        Ngũ Hổ Độn
            │
            ▼
      Month Heavenly Stem
            │
            ▼
        Month Pillar

Version:
    1.0.0

Architecture:
    Data Driven
    Cache Friendly
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict

from calendar_engine.solar_terms.calculator import (
    SolarTermCalculator,
)

from bazi_engine.models import Pillar

from database.loader import DatabaseLoader
from database.cache import DatabaseCache

# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

MONTH_COUNT = 12

STEM_COUNT = 10

BRANCH_COUNT = 12


# =============================================================================
# EXCEPTIONS
# =============================================================================

class MonthPillarError(Exception):
    """Base exception."""


class MonthPillarDataError(MonthPillarError):
    """Lỗi dữ liệu."""


class MonthPillarCalculationError(MonthPillarError):
    """Lỗi tính toán."""


# =============================================================================
# RESULT
# =============================================================================

@dataclass(slots=True)
class MonthPillarResult:
    """
    Kết quả Trụ Tháng.
    """

    solar_term: str

    month_index: int

    heavenly_stem_index: int

    earthly_branch_index: int

    heavenly_stem: str

    earthly_branch: str

    pillar: Pillar


# =============================================================================
# CALCULATOR
# =============================================================================

class MonthPillarCalculator:

    """
    Month Pillar Calculator

    Flow

        Datetime
            │
            ▼
      Solar Term
            │
            ▼
      Month Branch
            │
            ▼
      Year Stem
            │
            ▼
      Ngũ Hổ Độn
            │
            ▼
      Month Stem
            │
            ▼
      Month Pillar
    """

    # -----------------------------------------------------------------

    def __init__(self):

        self._solar_term = SolarTermCalculator()

        self._loader = DatabaseLoader()

        self._cache = DatabaseCache()

        self._loaded = False

        self._month_branch_rules: Dict[int, dict] = {}

        self._month_stem_rules: Dict[int, dict] = {}

        self._heavenly_stems: Dict[int, dict] = {}

        self._earthly_branches: Dict[int, dict] = {}

        self.reload()

    # -----------------------------------------------------------------

    @property
    def loaded(self) -> bool:

        return self._loaded

    # -----------------------------------------------------------------

    def reload(self):

        self._load_month_branch_rules()

        self._load_month_stem_rules()

        self._load_heavenly_stems()

        self._load_earthly_branches()

        self._loaded = True

    # -----------------------------------------------------------------

    def _ensure_loaded(self):

        if not self._loaded:

            raise MonthPillarDataError(
                "MonthPillarCalculator chưa được khởi tạo."
            )

    # -----------------------------------------------------------------

    def _load_month_branch_rules(self):

        rows = self._loader.load_csv(
            "02_quy_tac/month_branch.csv"
        )

        self._month_branch_rules.clear()

        for row in rows:

            self._month_branch_rules[
                int(row["month_index"])
            ] = row

    # -----------------------------------------------------------------

    def _load_month_stem_rules(self):

        rows = self._loader.load_csv(
            "02_quy_tac/month_stem_rules.csv"
        )

        self._month_stem_rules.clear()

        for row in rows:

            self._month_stem_rules[
                row["year_stem"]
            ] = row

    # -----------------------------------------------------------------

    def _load_heavenly_stems(self):

        rows = self._loader.load_csv(
            "01_can_chi/heavenly_stems.csv"
        )

        self._heavenly_stems.clear()

        for row in rows:

            self._heavenly_stems[
                int(row["index"])
            ] = row

    # -----------------------------------------------------------------

    def _load_earthly_branches(self):

        rows = self._loader.load_csv(
            "01_can_chi/earthly_branches.csv"
        )

        self._earthly_branches.clear()

        for row in rows:

            self._earthly_branches[
                int(row["index"])
            ] = row

    # -----------------------------------------------------------------

    def get_heavenly_stem(
        self,
        index: int,
    ) -> dict:

        self._ensure_loaded()

        return self._heavenly_stems[index]

    # -----------------------------------------------------------------

    def get_earthly_branch(
        self,
        index: int,
    ) -> dict:

        self._ensure_loaded()

        return self._earthly_branches[index]
          # -----------------------------------------------------------------
    # SOLAR TERM
    # -----------------------------------------------------------------

    def get_solar_term(
        self,
        target_datetime: datetime,
    ):
        """
        Lấy Tiết Khí hiện tại.

        Returns
        -------
        SolarTermResult
        """

        self._ensure_loaded()

        return self._solar_term.calculate(
            target_datetime=target_datetime,
            year_stem=""
        )

    # -----------------------------------------------------------------
    # MONTH BRANCH
    # -----------------------------------------------------------------

    def get_month_branch_rule(
        self,
        month_index: int,
    ) -> dict:
        """
        Tra quy tắc Địa Chi tháng.
        """

        self._ensure_loaded()

        if month_index not in self._month_branch_rules:

            raise MonthPillarCalculationError(
                f"Không tồn tại month_index={month_index}"
            )

        return self._month_branch_rules[
            month_index
        ]

    # -----------------------------------------------------------------

    def get_month_branch(
        self,
        month_index: int,
    ) -> dict:
        """
        Lấy Địa Chi tháng.
        """

        rule = self.get_month_branch_rule(
            month_index
        )

        branch_index = int(
            rule["branch_index"]
        )

        return self.get_earthly_branch(
            branch_index
        )

    # -----------------------------------------------------------------
    # MONTH STEM
    # -----------------------------------------------------------------

    def get_month_stem_rule(
        self,
        year_stem: str,
    ) -> dict:
        """
        Tra bảng Ngũ Hổ Độn.
        """

        self._ensure_loaded()

        if year_stem not in self._month_stem_rules:

            raise MonthPillarCalculationError(
                f"Không có quy tắc cho Can năm {year_stem}"
            )

        return self._month_stem_rules[
            year_stem
        ]

    # -----------------------------------------------------------------

    def get_month_stem(
        self,
        year_stem: str,
        month_index: int,
    ) -> dict:
        """
        Tính Thiên Can tháng.

        Formula

            stem =
            (start_stem + month_index - 1) % 10
        """

        rule = self.get_month_stem_rule(
            year_stem
        )

        start_index = int(
            rule["start_stem_index"]
        )

        stem_index = (
            start_index
            + month_index
            - 1
        ) % STEM_COUNT

        return self.get_heavenly_stem(
            stem_index
        )

    # -----------------------------------------------------------------
    # PREPARE
    # -----------------------------------------------------------------

    def prepare(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> dict:
        """
        Chuẩn bị toàn bộ dữ liệu.
        """

        solar_term = self.get_solar_term(
            target_datetime
        )

        month_index = int(
            solar_term.month_index
        )

        branch = self.get_month_branch(
            month_index
        )

        stem = self.get_month_stem(
            year_stem,
            month_index,
        )

        return {

            "solar_term":
                solar_term,

            "month_index":
                month_index,

            "stem":
                stem,

            "branch":
                branch,

        }

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> None:
        """
        Kiểm tra dữ liệu đầu vào.
        """

        if not isinstance(
            target_datetime,
            datetime,
        ):

            raise MonthPillarCalculationError(
                "target_datetime phải là datetime."
            )

        if not year_stem:

            raise MonthPillarCalculationError(
                "Thiếu Thiên Can năm."
            )
              # -----------------------------------------------------------------
    # BUILD PILLAR
    # -----------------------------------------------------------------

    def build_pillar(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> MonthPillarResult:
        """
        Xây dựng Trụ Tháng hoàn chỉnh.

        Parameters
        ----------
        target_datetime : datetime

        year_stem : str

        Returns
        -------
        MonthPillarResult
        """

        self._ensure_loaded()

        self.validate(
            target_datetime,
            year_stem,
        )

        data = self.prepare(
            target_datetime,
            year_stem,
        )

        stem = data["stem"]

        branch = data["branch"]

        pillar = Pillar(

            stem=stem["stem"],

            stem_index=int(
                stem["index"]
            ),

            stem_element=stem["element"],

            stem_yinyang=stem["yin_yang"],

            branch=branch["branch"],

            branch_index=int(
                branch["index"]
            ),

            branch_element=branch["element"],

            branch_yinyang=branch["yin_yang"],
        )

        return MonthPillarResult(

            solar_term=data[
                "solar_term"
            ].current_term,

            month_index=data[
                "month_index"
            ],

            heavenly_stem_index=int(
                stem["index"]
            ),

            earthly_branch_index=int(
                branch["index"]
            ),

            heavenly_stem=stem[
                "stem"
            ],

            earthly_branch=branch[
                "branch"
            ],

            pillar=pillar,
        )

    # -----------------------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------------------

    def calculate(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> MonthPillarResult:
        """
        API chính.
        """

        return self.build_pillar(
            target_datetime,
            year_stem,
        )

    # -----------------------------------------------------------------

    def calculate_from_datetime(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> MonthPillarResult:
        """
        Alias.
        """

        return self.calculate(
            target_datetime,
            year_stem,
        )

    # -----------------------------------------------------------------

    def get_month_pillar(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> Pillar:
        """
        Chỉ lấy đối tượng Pillar.
        """

        return self.calculate(
            target_datetime,
            year_stem,
        ).pillar

    # -----------------------------------------------------------------

    def get_month_ganzhi(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> str:
        """
        Trả về Can Chi tháng.
        """

        result = self.calculate(
            target_datetime,
            year_stem,
        )

        return (
            result.heavenly_stem
            + result.earthly_branch
        )

    # -----------------------------------------------------------------

    def get_month_stem_name(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> str:

        return self.calculate(
            target_datetime,
            year_stem,
        ).heavenly_stem

    # -----------------------------------------------------------------

    def get_month_branch_name(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> str:

        return self.calculate(
            target_datetime,
            year_stem,
        ).earthly_branch

    # -----------------------------------------------------------------
    # DEBUG
    # -----------------------------------------------------------------

    def debug(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> dict:
        """
        Trả về dữ liệu debug.
        """

        result = self.calculate(
            target_datetime,
            year_stem,
        )

        return {

            "solar_term":
                result.solar_term,

            "month_index":
                result.month_index,

            "stem_index":
                result.heavenly_stem_index,

            "branch_index":
                result.earthly_branch_index,

            "stem":
                result.heavenly_stem,

            "branch":
                result.earthly_branch,

            "pillar":
                result.heavenly_stem
                + result.earthly_branch,

        }

    # -----------------------------------------------------------------
    # VERIFY
    # -----------------------------------------------------------------

    def verify(
        self,
        target_datetime: datetime,
        year_stem: str,
        expected: str,
    ) -> bool:
        """
        Kiểm tra kết quả.
        """

        return (
            self.get_month_ganzhi(
                target_datetime,
                year_stem,
            )
            == expected
        )
          # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa toàn bộ cache.
        """

        self._month_branch_rules.clear()

        self._month_stem_rules.clear()

        self._heavenly_stems.clear()

        self._earthly_branches.clear()

        self._loaded = False

    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload toàn bộ dữ liệu.
        """

        self.clear_cache()

        self.reload()

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê dữ liệu đã nạp.
        """

        return {

            "month_branch_rules":
                len(self._month_branch_rules),

            "month_stem_rules":
                len(self._month_stem_rules),

            "heavenly_stems":
                len(self._heavenly_stems),

            "earthly_branches":
                len(self._earthly_branches),

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái dữ liệu.
        """

        if not self.loaded:

            return False

        if len(
            self._month_branch_rules
        ) != 12:

            return False

        if len(
            self._month_stem_rules
        ) != 10:

            return False

        if len(
            self._heavenly_stems
        ) != 10:

            return False

        if len(
            self._earthly_branches
        ) != 12:

            return False

        return True

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._month_branch_rules
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<MonthPillarCalculator "

            f"loaded={self.loaded} "

            f"month_rules={len(self._month_branch_rules)} "

            f"stem_rules={len(self._month_stem_rules)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

month_pillar_calculator = MonthPillarCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "MonthPillarCalculator",

    "MonthPillarResult",

    "MonthPillarError",

    "MonthPillarDataError",

    "MonthPillarCalculationError",

    "month_pillar_calculator",

]
