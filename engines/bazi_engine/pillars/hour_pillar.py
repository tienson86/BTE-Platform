"""
===============================================================================
Bazi Engine - Hour Pillar Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/hour_pillar.py

Description:
    Tính Trụ Giờ (Hour Pillar)

Flow:
        Datetime
            │
            ▼
      Day Heavenly Stem
            │
            ▼
      Hour Branch
            │
            ▼
        Ngũ Thử Độn
            │
            ▼
      Hour Heavenly Stem
            │
            ▼
        Hour Pillar

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict

from bazi_engine.core.base_calculator import BaseCalculator
from bazi_engine.models import Pillar
from database.loader import DatabaseLoader


# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

HEAVENLY_STEMS_COUNT = 10

EARTHLY_BRANCHES_COUNT = 12


# =============================================================================
# EXCEPTIONS
# =============================================================================

class HourPillarError(Exception):
    """Base exception."""


class HourPillarDataError(HourPillarError):
    """Lỗi dữ liệu Hour Pillar."""


class HourPillarCalculationError(HourPillarError):
    """Lỗi tính toán Hour Pillar."""


# =============================================================================
# RESULT
# =============================================================================

@dataclass(slots=True)
class HourPillarResult:
    """
    Kết quả Trụ Giờ.
    """

    hour_index: int

    heavenly_stem_index: int

    earthly_branch_index: int

    heavenly_stem: str

    earthly_branch: str

    pillar: Pillar


# =============================================================================
# CALCULATOR
# =============================================================================

class HourPillarCalculator(BaseCalculator):
    """
    Bộ tính Trụ Giờ.
    """

    def __init__(self):

        super().__init__()

        self._loader = DatabaseLoader()

        self._hour_branch_rules: Dict[int, dict] = {}

        self._hour_stem_rules: Dict[str, dict] = {}

        self._heavenly_stems: Dict[int, dict] = {}

        self._earthly_branches: Dict[int, dict] = {}

        self.reload()

    # -----------------------------------------------------------------

    def reload(self):

        self._load_hour_branch_rules()

        self._load_hour_stem_rules()

        self._load_heavenly_stems()

        self._load_earthly_branches()

        self.mark_loaded()

    # -----------------------------------------------------------------

    def _load_hour_branch_rules(self):

        rows = self._loader.load_csv(
            "02_quy_tac/hour_branch.csv"
        )

        self._hour_branch_rules.clear()

        for row in rows:

            self._hour_branch_rules[
                int(row["branch_index"])
            ] = row

    # -----------------------------------------------------------------

    def _load_hour_stem_rules(self):

        rows = self._loader.load_csv(
            "02_quy_tac/hour_stem_rules.csv"
        )

        self._hour_stem_rules.clear()

        for row in rows:

            self._hour_stem_rules[
                row["day_stem"]
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

        self.ensure_loaded()

        return self._heavenly_stems[index]

    # -----------------------------------------------------------------

    def get_earthly_branch(
        self,
        index: int,
    ) -> dict:

        self.ensure_loaded()

        return self._earthly_branches[index]
          # -----------------------------------------------------------------
    # HOUR BRANCH
    # -----------------------------------------------------------------

    def get_hour_branch_rule(
        self,
        hour: int,
        minute: int,
    ) -> dict:
        """
        Xác định quy tắc Địa Chi giờ.

        Giờ Tý:
            23:00 -> 00:59
        """

        self.ensure_loaded()

        for rule in self._hour_branch_rules.values():

            start_hour = int(rule["start_hour"])
            start_minute = int(rule["start_minute"])

            end_hour = int(rule["end_hour"])
            end_minute = int(rule["end_minute"])

            is_cross_day = int(
                rule.get("is_cross_day", 0)
            )

            # ---------------------------------------------
            # Giờ Tý (qua ngày)
            # ---------------------------------------------

            if is_cross_day:

                if (
                    hour == 23
                    and minute >= start_minute
                ):

                    return rule

                if (
                    hour == 0
                    and minute <= end_minute
                ):

                    return rule

            # ---------------------------------------------
            # Các giờ còn lại
            # ---------------------------------------------

            else:

                if hour < start_hour:

                    continue

                if hour > end_hour:

                    continue

                if (
                    hour == start_hour
                    and minute < start_minute
                ):

                    continue

                if (
                    hour == end_hour
                    and minute > end_minute
                ):

                    continue

                return rule

        raise HourPillarCalculationError(
            "Không xác định được Địa Chi giờ."
        )

    # -----------------------------------------------------------------

    def get_hour_branch(
        self,
        hour: int,
        minute: int,
    ) -> dict:
        """
        Lấy Địa Chi giờ.
        """

        rule = self.get_hour_branch_rule(
            hour,
            minute,
        )

        branch_index = int(
            rule["branch_index"]
        )

        return self.get_earthly_branch(
            branch_index
        )

    # -----------------------------------------------------------------
    # HOUR STEM
    # -----------------------------------------------------------------

    def get_hour_stem_rule(
        self,
        day_stem: str,
    ) -> dict:
        """
        Tra bảng Ngũ Thử Độn.
        """

        self.ensure_loaded()

        if day_stem not in self._hour_stem_rules:

            raise HourPillarCalculationError(
                f"Không có quy tắc cho Can ngày {day_stem}"
            )

        return self._hour_stem_rules[
            day_stem
        ]

    # -----------------------------------------------------------------

    def get_hour_stem(
        self,
        day_stem: str,
        branch_index: int,
    ) -> dict:
        """
        Tính Thiên Can giờ.

        Công thức:

            stem =
            (start_stem + branch_index) % 10
        """

        rule = self.get_hour_stem_rule(
            day_stem
        )

        start_index = int(
            rule["start_hour_stem_index"]
        )

        stem_index = (
            start_index
            + branch_index
        ) % HEAVENLY_STEMS_COUNT

        return self.get_heavenly_stem(
            stem_index
        )

    # -----------------------------------------------------------------
    # PREPARE
    # -----------------------------------------------------------------

    def prepare(
        self,
        target_datetime: datetime,
        day_stem: str,
    ) -> dict:
        """
        Chuẩn bị toàn bộ dữ liệu trước khi
        xây dựng Hour Pillar.
        """

        hour = target_datetime.hour

        minute = target_datetime.minute

        branch = self.get_hour_branch(
            hour,
            minute,
        )

        stem = self.get_hour_stem(
            day_stem,
            int(branch["index"]),
        )

        return {

            "hour": hour,

            "minute": minute,

            "stem": stem,

            "branch": branch,

        }

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate(
        self,
        target_datetime: datetime,
        day_stem: str,
    ) -> None:
        """
        Kiểm tra dữ liệu đầu vào.
        """

        if not isinstance(
            target_datetime,
            datetime,
        ):

            raise HourPillarCalculationError(
                "target_datetime phải là datetime."
            )

        if not isinstance(
            day_stem,
            str,
        ):

            raise HourPillarCalculationError(
                "day_stem phải là chuỗi."
            )

        if day_stem.strip() == "":

            raise HourPillarCalculationError(
                "Thiếu Can ngày."
            )
              # -----------------------------------------------------------------
    # HOUR BRANCH
    # -----------------------------------------------------------------

    def get_hour_branch_rule(
        self,
        hour: int,
        minute: int,
    ) -> dict:
        """
        Xác định quy tắc Địa Chi giờ.

        Giờ Tý:
            23:00 -> 00:59
        """

        self.ensure_loaded()

        for rule in self._hour_branch_rules.values():

            start_hour = int(rule["start_hour"])
            start_minute = int(rule["start_minute"])

            end_hour = int(rule["end_hour"])
            end_minute = int(rule["end_minute"])

            is_cross_day = int(
                rule.get("is_cross_day", 0)
            )

            # ---------------------------------------------
            # Giờ Tý (qua ngày)
            # ---------------------------------------------

            if is_cross_day:

                if (
                    hour == 23
                    and minute >= start_minute
                ):

                    return rule

                if (
                    hour == 0
                    and minute <= end_minute
                ):

                    return rule

            # ---------------------------------------------
            # Các giờ còn lại
            # ---------------------------------------------

            else:

                if hour < start_hour:

                    continue

                if hour > end_hour:

                    continue

                if (
                    hour == start_hour
                    and minute < start_minute
                ):

                    continue

                if (
                    hour == end_hour
                    and minute > end_minute
                ):

                    continue

                return rule

        raise HourPillarCalculationError(
            "Không xác định được Địa Chi giờ."
        )

    # -----------------------------------------------------------------

    def get_hour_branch(
        self,
        hour: int,
        minute: int,
    ) -> dict:
        """
        Lấy Địa Chi giờ.
        """

        rule = self.get_hour_branch_rule(
            hour,
            minute,
        )

        branch_index = int(
            rule["branch_index"]
        )

        return self.get_earthly_branch(
            branch_index
        )

    # -----------------------------------------------------------------
    # HOUR STEM
    # -----------------------------------------------------------------

    def get_hour_stem_rule(
        self,
        day_stem: str,
    ) -> dict:
        """
        Tra bảng Ngũ Thử Độn.
        """

        self.ensure_loaded()

        if day_stem not in self._hour_stem_rules:

            raise HourPillarCalculationError(
                f"Không có quy tắc cho Can ngày {day_stem}"
            )

        return self._hour_stem_rules[
            day_stem
        ]

    # -----------------------------------------------------------------

    def get_hour_stem(
        self,
        day_stem: str,
        branch_index: int,
    ) -> dict:
        """
        Tính Thiên Can giờ.

        Công thức:

            stem =
            (start_stem + branch_index) % 10
        """

        rule = self.get_hour_stem_rule(
            day_stem
        )

        start_index = int(
            rule["start_hour_stem_index"]
        )

        stem_index = (
            start_index
            + branch_index
        ) % HEAVENLY_STEMS_COUNT

        return self.get_heavenly_stem(
            stem_index
        )

    # -----------------------------------------------------------------
    # PREPARE
    # -----------------------------------------------------------------

    def prepare(
        self,
        target_datetime: datetime,
        day_stem: str,
    ) -> dict:
        """
        Chuẩn bị toàn bộ dữ liệu trước khi
        xây dựng Hour Pillar.
        """

        hour = target_datetime.hour

        minute = target_datetime.minute

        branch = self.get_hour_branch(
            hour,
            minute,
        )

        stem = self.get_hour_stem(
            day_stem,
            int(branch["index"]),
        )

        return {

            "hour": hour,

            "minute": minute,

            "stem": stem,

            "branch": branch,

        }

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate(
        self,
        target_datetime: datetime,
        day_stem: str,
    ) -> None:
        """
        Kiểm tra dữ liệu đầu vào.
        """

        if not isinstance(
            target_datetime,
            datetime,
        ):

            raise HourPillarCalculationError(
                "target_datetime phải là datetime."
            )

        if not isinstance(
            day_stem,
            str,
        ):

            raise HourPillarCalculationError(
                "day_stem phải là chuỗi."
            )

        if day_stem.strip() == "":

            raise HourPillarCalculationError(
                "Thiếu Can ngày."
            )
              # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa toàn bộ cache dữ liệu.
        """

        self._hour_branch_rules.clear()

        self._hour_stem_rules.clear()

        self._heavenly_stems.clear()

        self._earthly_branches.clear()

        self.mark_unloaded()

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

            "hour_branch_rules":
                len(self._hour_branch_rules),

            "hour_stem_rules":
                len(self._hour_stem_rules),

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
        Kiểm tra tính toàn vẹn dữ liệu.
        """

        if not self.loaded:

            return False

        if len(self._hour_branch_rules) != 12:

            return False

        # Ngũ Thử Độn có 10 Can ngày
        if len(self._hour_stem_rules) != 10:

            return False

        if len(self._heavenly_stems) != 10:

            return False

        if len(self._earthly_branches) != 12:

            return False

        return True

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Số quy tắc Chi giờ.
        """

        return len(
            self._hour_branch_rules
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<HourPillarCalculator "

            f"loaded={self.loaded} "

            f"hour_rules={len(self._hour_branch_rules)} "

            f"stem_rules={len(self._hour_stem_rules)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

hour_pillar_calculator = HourPillarCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "HourPillarCalculator",

    "HourPillarResult",

    "HourPillarError",

    "HourPillarDataError",

    "HourPillarCalculationError",

    "hour_pillar_calculator",

]
