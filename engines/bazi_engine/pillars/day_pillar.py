"""
===============================================================================
Bazi Engine - Day Pillar Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/day_pillar.py

Description:
    Tính Trụ Ngày (Day Pillar) theo phương pháp:

        Datetime
            │
            ▼
        Julian Day Number (JDN)
            │
            ▼
        GanZhi Index (0-59)
            │
            ▼
        Heavenly Stem
            │
            ▼
        Earthly Branch
            │
            ▼
        Day Pillar

Version:
    1.0.0

Architecture:
    Data Driven
    Stateless
    Cache Friendly

Author:
    PhongThuy AI Project
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import Optional

from calendar_engine.julian.engine import JulianEngine

from database.loader import DatabaseLoader

from database.cache import DatabaseCache

from bazi_engine.models import Pillar

# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------
# Epoch dùng để tính Can Chi ngày
#
# Công thức:
#
# ganzhi_index = (JDN + DAY_GANZHI_OFFSET) % 60
#
# Offset sẽ được kiểm chứng trong quá trình test với các lá số chuẩn.
# ---------------------------------------------------------------------

DAY_GANZHI_OFFSET = 49

STEM_COUNT = 10

BRANCH_COUNT = 12

JIAZI_COUNT = 60


# =============================================================================
# EXCEPTIONS
# =============================================================================


class DayPillarError(Exception):
    """Base exception."""


class DayPillarDataError(DayPillarError):
    """Database error."""


class DayPillarCalculationError(DayPillarError):
    """Calculation error."""


# =============================================================================
# RESULT
# =============================================================================


@dataclass(slots=True)
class DayPillarResult:
    """
    Kết quả tính Trụ Ngày.
    """

    julian_day: int

    ganzhi_index: int

    heavenly_stem_index: int

    earthly_branch_index: int

    heavenly_stem: str

    earthly_branch: str

    pillar: Pillar


# =============================================================================
# CALCULATOR
# =============================================================================


class DayPillarCalculator:
    """
    Day Pillar Calculator

    Flow

        Datetime
            │
            ▼
        Julian Engine
            │
            ▼
        JDN
            │
            ▼
        Can Chi Index
            │
            ▼
        Stem
            │
            ▼
        Branch
            │
            ▼
        Pillar
    """

    # -----------------------------------------------------------------
    # INIT
    # -----------------------------------------------------------------

    def __init__(self):

        self._julian = JulianEngine()

        self._loader = DatabaseLoader()

        self._cache = DatabaseCache()

        self._loaded = False

        self._heavenly_stems: Dict[int, dict] = {}

        self._earthly_branches: Dict[int, dict] = {}

        self._jiazi: Dict[int, dict] = {}

        self.reload()

    # -----------------------------------------------------------------
    # PROPERTIES
    # -----------------------------------------------------------------

    @property
    def loaded(self) -> bool:

        return self._loaded

    # -----------------------------------------------------------------
    # LOAD
    # -----------------------------------------------------------------

    def reload(self):

        self._load_heavenly_stems()

        self._load_earthly_branches()

        self._load_sixty_jiazi()

        self._loaded = True

    # -----------------------------------------------------------------

    def _load_heavenly_stems(self):

        rows = self._loader.load_csv(
            "01_can_chi/heavenly_stems.csv"
        )

        self._heavenly_stems.clear()

        for row in rows:

            index = int(row["index"])

            self._heavenly_stems[index] = row

    # -----------------------------------------------------------------

    def _load_earthly_branches(self):

        rows = self._loader.load_csv(
            "01_can_chi/earthly_branches.csv"
        )

        self._earthly_branches.clear()

        for row in rows:

            index = int(row["index"])

            self._earthly_branches[index] = row

    # -----------------------------------------------------------------

    def _load_sixty_jiazi(self):

        rows = self._loader.load_csv(
            "01_can_chi/sixty_jiazi.csv"
        )

        self._jiazi.clear()

        for row in rows:

            index = int(row["index"])

            self._jiazi[index] = row

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def _ensure_loaded(self):

        if not self._loaded:

            raise DayPillarDataError(
                "DayPillarCalculator chưa được khởi tạo."
            )

    # -----------------------------------------------------------------
    # LOOKUP
    # -----------------------------------------------------------------

    def get_heavenly_stem(
        self,
        index: int,
    ) -> dict:

        self._ensure_loaded()

        return self._heavenly_stems[index % STEM_COUNT]

    # -----------------------------------------------------------------

    def get_earthly_branch(
        self,
        index: int,
    ) -> dict:

        self._ensure_loaded()

        return self._earthly_branches[index % BRANCH_COUNT]

    # -----------------------------------------------------------------

    def get_jiazi(
        self,
        index: int,
    ) -> dict:

        self._ensure_loaded()

        return self._jiazi[index % JIAZI_COUNT]
    # -----------------------------------------------------------------
    # JULIAN DAY
    # -----------------------------------------------------------------

    def get_julian_day(
        self,
        target_datetime: datetime,
    ) -> int:
        """
        Chuyển datetime thành Julian Day Number (JDN).

        Returns
        -------
        int
            Julian Day Number
        """

        self._ensure_loaded()

        try:

            jdn = self._julian.to_julian_day(target_datetime)

        except Exception as ex:

            raise DayPillarCalculationError(
                f"Không thể tính Julian Day: {ex}"
            ) from ex

        return int(jdn)

    # -----------------------------------------------------------------
    # GANZHI INDEX
    # -----------------------------------------------------------------

    def get_ganzhi_index(
        self,
        julian_day: int,
    ) -> int:
        """
        Tính chỉ số Can Chi ngày.

        Formula
        -------
            (JDN + OFFSET) % 60
        """

        return (
            julian_day + DAY_GANZHI_OFFSET
        ) % JIAZI_COUNT

    # -----------------------------------------------------------------

    def get_stem_index(
        self,
        ganzhi_index: int,
    ) -> int:
        """
        Chỉ số Thiên Can.

        Range
        -----
        0 ~ 9
        """

        return ganzhi_index % STEM_COUNT

    # -----------------------------------------------------------------

    def get_branch_index(
        self,
        ganzhi_index: int,
    ) -> int:
        """
        Chỉ số Địa Chi.

        Range
        -----
        0 ~ 11
        """

        return ganzhi_index % BRANCH_COUNT

    # -----------------------------------------------------------------
    # CORE CALCULATION
    # -----------------------------------------------------------------

    def calculate_indices(
        self,
        target_datetime: datetime,
    ) -> dict:
        """
        Tính toàn bộ index cần thiết.
        """

        julian_day = self.get_julian_day(
            target_datetime
        )

        ganzhi_index = self.get_ganzhi_index(
            julian_day
        )

        stem_index = self.get_stem_index(
            ganzhi_index
        )

        branch_index = self.get_branch_index(
            ganzhi_index
        )

        return {

            "julian_day": julian_day,

            "ganzhi_index": ganzhi_index,

            "stem_index": stem_index,

            "branch_index": branch_index,

        }

    # -----------------------------------------------------------------
    # LOOKUP OBJECTS
    # -----------------------------------------------------------------

    def get_day_stem(
        self,
        stem_index: int,
    ) -> dict:
        """
        Tra Thiên Can ngày.
        """

        stem = self.get_heavenly_stem(
            stem_index
        )

        if stem is None:

            raise DayPillarCalculationError(
                "Không tìm thấy Thiên Can."
            )

        return stem

    # -----------------------------------------------------------------

    def get_day_branch(
        self,
        branch_index: int,
    ) -> dict:
        """
        Tra Địa Chi ngày.
        """

        branch = self.get_earthly_branch(
            branch_index
        )

        if branch is None:

            raise DayPillarCalculationError(
                "Không tìm thấy Địa Chi."
            )

        return branch

    # -----------------------------------------------------------------

    def get_day_jiazi(
        self,
        ganzhi_index: int,
    ) -> dict:
        """
        Tra bảng Lục Thập Hoa Giáp.
        """

        jiazi = self.get_jiazi(
            ganzhi_index
        )

        if jiazi is None:

            raise DayPillarCalculationError(
                "Không tìm thấy Hoa Giáp."
            )

        return jiazi

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate_datetime(
        self,
        target_datetime: datetime,
    ) -> None:
        """
        Kiểm tra dữ liệu đầu vào.
        """

        if not isinstance(
            target_datetime,
            datetime,
        ):

            raise DayPillarCalculationError(
                "target_datetime phải là datetime."
            )

    # -----------------------------------------------------------------

    def prepare(
        self,
        target_datetime: datetime,
    ) -> dict:
        """
        Chuẩn bị toàn bộ dữ liệu tính toán.
        """

        self.validate_datetime(
            target_datetime
        )

        indices = self.calculate_indices(
            target_datetime
        )

        indices["stem"] = self.get_day_stem(
            indices["stem_index"]
        )

        indices["branch"] = self.get_day_branch(
            indices["branch_index"]
        )

        indices["jiazi"] = self.get_day_jiazi(
            indices["ganzhi_index"]
        )

        return indices
          # -----------------------------------------------------------------
    # BUILD PILLAR
    # -----------------------------------------------------------------

    def build_pillar(
        self,
        target_datetime: datetime,
    ) -> DayPillarResult:
        """
        Xây dựng Day Pillar hoàn chỉnh.

        Parameters
        ----------
        target_datetime : datetime

        Returns
        -------
        DayPillarResult
        """

        self._ensure_loaded()

        data = self.prepare(
            target_datetime
        )

        stem = data["stem"]

        branch = data["branch"]

        pillar = Pillar(

            stem=stem["stem"],

            stem_index=int(stem["index"]),

            stem_yinyang=stem["yin_yang"],

            stem_element=stem["element"],

            branch=branch["branch"],

            branch_index=int(branch["index"]),

            branch_yinyang=branch["yin_yang"],

            branch_element=branch["element"],
        )

        return DayPillarResult(

            julian_day=data["julian_day"],

            ganzhi_index=data["ganzhi_index"],

            heavenly_stem_index=data["stem_index"],

            earthly_branch_index=data["branch_index"],

            heavenly_stem=stem["stem"],

            earthly_branch=branch["branch"],

            pillar=pillar,
        )

    # -----------------------------------------------------------------
    # SHORTCUT
    # -----------------------------------------------------------------

    def get_day_stem_name(
        self,
        target_datetime: datetime,
    ) -> str:

        return self.build_pillar(
            target_datetime
        ).heavenly_stem

    # -----------------------------------------------------------------

    def get_day_branch_name(
        self,
        target_datetime: datetime,
    ) -> str:

        return self.build_pillar(
            target_datetime
        ).earthly_branch

    # -----------------------------------------------------------------

    def get_day_ganzhi(
        self,
        target_datetime: datetime,
    ) -> str:

        pillar = self.build_pillar(
            target_datetime
        )

        return (
            pillar.heavenly_stem
            + pillar.earthly_branch
        )

    # -----------------------------------------------------------------

    def get_day_pillar(
        self,
        target_datetime: datetime,
    ) -> Pillar:

        return self.build_pillar(
            target_datetime
        ).pillar

    # -----------------------------------------------------------------
    # DEBUG
    # -----------------------------------------------------------------

    def debug(
        self,
        target_datetime: datetime,
    ) -> dict:

        result = self.build_pillar(
            target_datetime
        )

        return {

            "julian_day":
                result.julian_day,

            "ganzhi_index":
                result.ganzhi_index,

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
        expected: str,
    ) -> bool:

        return (
            self.get_day_ganzhi(
                target_datetime
            )
            == expected
        )
          # -----------------------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------------------

    def calculate(
        self,
        target_datetime: datetime,
    ) -> DayPillarResult:
        """
        API chính.

        Parameters
        ----------
        target_datetime : datetime

        Returns
        -------
        DayPillarResult
        """

        return self.build_pillar(
            target_datetime
        )

    # -----------------------------------------------------------------

    def calculate_from_datetime(
        self,
        target_datetime: datetime,
    ) -> DayPillarResult:
        """
        Alias của calculate().
        """

        return self.calculate(
            target_datetime
        )

    # -----------------------------------------------------------------

    def calculate_from_jdn(
        self,
        julian_day: int,
    ) -> DayPillarResult:
        """
        Tính trực tiếp từ Julian Day Number.

        Parameters
        ----------
        julian_day : int

        Returns
        -------
        DayPillarResult
        """

        ganzhi_index = self.get_ganzhi_index(
            julian_day
        )

        jiazi = self.get_day_jiazi(
            ganzhi_index
        )

        stem_index = int(
            jiazi["stem_index"]
        )

        branch_index = int(
            jiazi["branch_index"]
        )

        stem = self.get_day_stem(
            stem_index
        )

        branch = self.get_day_branch(
            branch_index
        )

        pillar = Pillar(

            stem=stem["stem"],

            stem_index=stem_index,

            stem_yinyang=stem["yin_yang"],

            stem_element=stem["element"],

            branch=branch["branch"],

            branch_index=branch_index,

            branch_yinyang=branch["yin_yang"],

            branch_element=branch["element"],
        )

        return DayPillarResult(

            julian_day=julian_day,

            ganzhi_index=ganzhi_index,

            heavenly_stem_index=stem_index,

            earthly_branch_index=branch_index,

            heavenly_stem=stem["stem"],

            earthly_branch=branch["branch"],

            pillar=pillar,
        )

    # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache.
        """

        self._heavenly_stems.clear()

        self._earthly_branches.clear()

        self._jiazi.clear()

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
        Thống kê dữ liệu.
        """

        return {

            "heavenly_stems":
                len(self._heavenly_stems),

            "earthly_branches":
                len(self._earthly_branches),

            "sixty_jiazi":
                len(self._jiazi),

        }

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra dữ liệu đã nạp.
        """

        if not self.loaded:

            return False

        if len(self._heavenly_stems) != 10:

            return False

        if len(self._earthly_branches) != 12:

            return False

        if len(self._jiazi) != 60:

            return False

        return True

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._jiazi
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<DayPillarCalculator "

            f"loaded={self.loaded} "

            f"jiazi={len(self._jiazi)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

day_pillar_calculator = DayPillarCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "DayPillarCalculator",

    "DayPillarResult",

    "DayPillarError",

    "DayPillarDataError",

    "DayPillarCalculationError",

    "day_pillar_calculator",

]
