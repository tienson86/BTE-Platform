"""
===============================================================================
Calendar Engine - Solar Terms Calculator
-------------------------------------------------------------------------------
Module:
    calendar_engine/solar_terms/calculator.py

Chức năng:
    - Đọc dữ liệu Tiết Khí từ CSV
    - Cache dữ liệu
    - Xác định Tiết Khí hiện tại
    - Xác định Địa Chi tháng
    - Tính Thiên Can tháng theo Ngũ Hổ Độn
    - Trả về SolarTermContext

Phiên bản:
    V1.0 (Data Driven)

Author:
    Phong Thuy AI

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

import csv
from bisect import bisect_right
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from .models import (
    LiChunResult,
    MonthBranchResult,
    SolarTermContext,
    SolarTermResult,
)

# =============================================================================
# PATH
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

DATA_DIR = CURRENT_DIR / "data"

SOLAR_TERMS_FILE = DATA_DIR / "solar_terms.csv"

SOLAR_TERM_DATES_FILE = DATA_DIR / "solar_term_dates.csv"

MONTH_BRANCH_FILE = DATA_DIR / "month_branch.csv"

MONTH_STEM_RULE_FILE = DATA_DIR / "month_stem_rules.csv"

HEAVENLY_STEM_FILE = DATA_DIR / "heavenly_stem_sequence.csv"


# =============================================================================
# EXCEPTION
# =============================================================================


class SolarTermError(Exception):
    """Base exception."""


class SolarTermDataError(SolarTermError):
    """CSV data error."""


class SolarTermNotFoundError(SolarTermError):
    """Solar term not found."""


# =============================================================================
# CALCULATOR
# =============================================================================


class SolarTermCalculator:
    """
    Solar Terms Calculator

    Luồng xử lý:

        Load CSV
            ↓
        Cache dữ liệu
            ↓
        Query Tiết Khí
            ↓
        Query Địa Chi tháng
            ↓
        Query Thiên Can tháng
            ↓
        Build Context
    """

    # -------------------------------------------------------------------------
    # INIT
    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self._solar_terms: List[Dict[str, Any]] = []

        self._term_dates: List[Dict[str, Any]] = []

        self._month_branches: List[Dict[str, Any]] = []

        self._month_stem_rules: List[Dict[str, Any]] = []

        self._heavenly_stems: List[Dict[str, Any]] = []

        self._loaded = False

        self.reload()

    # -------------------------------------------------------------------------
    # PUBLIC
    # -------------------------------------------------------------------------

    @property
    def loaded(self) -> bool:

        return self._loaded

    def reload(self) -> None:

        self._solar_terms = self._load_csv(
            SOLAR_TERMS_FILE
        )

        self._term_dates = self._load_csv(
            SOLAR_TERM_DATES_FILE
        )

        self._month_branches = self._load_csv(
            MONTH_BRANCH_FILE
        )

        self._month_stem_rules = self._load_csv(
            MONTH_STEM_RULE_FILE
        )

        self._heavenly_stems = self._load_csv(
            HEAVENLY_STEM_FILE
        )

        self._prepare_indexes()

        self._loaded = True

    # -------------------------------------------------------------------------
    # CSV LOADER
    # -------------------------------------------------------------------------

    def _load_csv(
        self,
        path: Path,
    ) -> List[Dict[str, Any]]:

        if not path.exists():

            raise SolarTermDataError(
                f"Không tìm thấy dữ liệu: {path}"
            )

        rows: List[Dict[str, Any]] = []

        with open(
            path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                rows.append(dict(row))

        return rows

    # -------------------------------------------------------------------------
    # INDEX
    # -------------------------------------------------------------------------

    def _prepare_indexes(self) -> None:

        self._term_by_code = {
            item["code"]: item
            for item in self._solar_terms
        }

        self._term_by_name = {
            item["name_vi"]: item
            for item in self._solar_terms
        }

        self._month_branch_by_name = {
            item["month_branch"]: item
            for item in self._month_branches
        }

        self._month_rule_by_year_stem = {
            item["year_stem"]: item
            for item in self._month_stem_rules
        }

        self._stem_by_name = {
            item["stem"]: item
            for item in self._heavenly_stems
        }

        self._term_dates_by_year: Dict[
            int,
            List[Dict[str, Any]],
        ] = {}

        for item in self._term_dates:

            year = int(item["year"])

            self._term_dates_by_year.setdefault(
                year,
                []
            ).append(item)

        for year in self._term_dates_by_year:

            self._term_dates_by_year[year].sort(
                key=lambda x: x["datetime"]
            )

    # -------------------------------------------------------------------------
    # CACHE
    # -------------------------------------------------------------------------

    @property
    def solar_terms(self):

        return self._solar_terms

    @property
    def term_dates(self):

        return self._term_dates

    @property
    def month_branches(self):

        return self._month_branches

    @property
    def month_stem_rules(self):

        return self._month_stem_rules

    @property
    def heavenly_stems(self):

        return self._heavenly_stems

    # -------------------------------------------------------------------------
    # VALIDATE
    # -------------------------------------------------------------------------

    def _ensure_loaded(self) -> None:

        if not self._loaded:

            raise SolarTermDataError(
                "SolarTermCalculator chưa load dữ liệu."
            )

    # -------------------------------------------------------------------------
    # PARSE
    # -------------------------------------------------------------------------

    @staticmethod
    def _parse_datetime(
        value: str,
    ) -> datetime:

        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

    @staticmethod
    def _parse_int(
        value: str,
        default: int = 0,
    ) -> int:

        try:

            return int(value)

        except Exception:

            return default

    @staticmethod
    def _parse_float(
        value: str,
        default: float = 0.0,
    ) -> float:

        try:

            return float(value)

        except Exception:

            return default
                # -------------------------------------------------------------------------
    # LOOKUP SOLAR TERM
    # -------------------------------------------------------------------------

    def get_current_term(
        self,
        target_datetime: datetime,
    ) -> Dict[str, Any]:
        """
        Trả về Tiết Khí hiện tại theo thời điểm truyền vào.

        Parameters
        ----------
        target_datetime : datetime

        Returns
        -------
        dict
        """

        self._ensure_loaded()

        year = target_datetime.year

        if year not in self._term_dates_by_year:

            raise SolarTermNotFoundError(
                f"Không có dữ liệu Tiết Khí năm {year}"
            )

        items = self._term_dates_by_year[year]

        current = items[0]

        for item in items:

            dt = self._parse_datetime(
                item["datetime"]
            )

            if target_datetime >= dt:

                current = item

            else:

                break

        return current

    # -------------------------------------------------------------------------

    def get_previous_term(
        self,
        target_datetime: datetime,
    ) -> Optional[Dict[str, Any]]:
        """
        Trả về Tiết Khí trước đó.
        """

        self._ensure_loaded()

        year = target_datetime.year

        if year not in self._term_dates_by_year:

            return None

        items = self._term_dates_by_year[year]

        previous = None

        for item in items:

            dt = self._parse_datetime(
                item["datetime"]
            )

            if dt < target_datetime:

                previous = item

            else:

                break

        return previous

    # -------------------------------------------------------------------------

    def get_next_term(
        self,
        target_datetime: datetime,
    ) -> Optional[Dict[str, Any]]:
        """
        Trả về Tiết Khí kế tiếp.
        """

        self._ensure_loaded()

        year = target_datetime.year

        if year not in self._term_dates_by_year:

            return None

        items = self._term_dates_by_year[year]

        for item in items:

            dt = self._parse_datetime(
                item["datetime"]
            )

            if dt > target_datetime:

                return item

        return None

    # -------------------------------------------------------------------------
    # MONTH BRANCH
    # -------------------------------------------------------------------------

    def get_month_branch(
        self,
        solar_term: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Tra Địa Chi tháng từ Tiết Khí.
        """

        self._ensure_loaded()

        term_name = solar_term["term_name"]

        for item in self._month_branches:

            start_term = item["start_term"]

            end_term = item["end_term"]

            if start_term == term_name:

                return item

        raise SolarTermNotFoundError(
            f"Không xác định được Địa Chi tháng của '{term_name}'"
        )

    # -------------------------------------------------------------------------
    # LICHUN
    # -------------------------------------------------------------------------

    def is_after_lichun(
        self,
        target_datetime: datetime,
    ) -> bool:
        """
        Kiểm tra thời điểm đã qua Lập Xuân hay chưa.
        """

        year = target_datetime.year

        if year not in self._term_dates_by_year:

            return False

        for item in self._term_dates_by_year[year]:

            if item["code"] == "LC":

                lichun = self._parse_datetime(
                    item["datetime"]
                )

                return target_datetime >= lichun

        return False

    # -------------------------------------------------------------------------

    def get_lichun(
        self,
        year: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Trả về dữ liệu Lập Xuân của năm.
        """

        if year not in self._term_dates_by_year:

            return None

        for item in self._term_dates_by_year[year]:

            if item["code"] == "LC":

                return item

        return None

    # -------------------------------------------------------------------------
    # LOOKUP HELPERS
    # -------------------------------------------------------------------------

    def get_term_by_code(
        self,
        code: str,
    ) -> Optional[Dict[str, Any]]:

        return self._term_by_code.get(code)

    # -------------------------------------------------------------------------

    def get_term_by_name(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:

        return self._term_by_name.get(name)

    # -------------------------------------------------------------------------

    def get_month_branch_info(
        self,
        branch: str,
    ) -> Optional[Dict[str, Any]]:

        return self._month_branch_by_name.get(branch)

    # -------------------------------------------------------------------------

    def get_year_stem_rule(
        self,
        year_stem: str,
    ) -> Optional[Dict[str, Any]]:

        return self._month_rule_by_year_stem.get(
            year_stem
        )

    # -------------------------------------------------------------------------

    def get_heavenly_stem(
        self,
        stem: str,
    ) -> Optional[Dict[str, Any]]:

        return self._stem_by_name.get(stem)
            # -------------------------------------------------------------------------
    # HEAVENLY STEM
    # -------------------------------------------------------------------------

    def _get_stem_index(
        self,
        stem: str,
    ) -> int:
        """
        Lấy chỉ số Thiên Can.

        Raises
        ------
        SolarTermNotFoundError
        """

        item = self.get_heavenly_stem(stem)

        if item is None:

            raise SolarTermNotFoundError(
                f"Không tìm thấy Thiên Can '{stem}'"
            )

        return self._parse_int(
            item["stem_index"]
        )

    # -------------------------------------------------------------------------

    def _get_stem_by_index(
        self,
        index: int,
    ) -> Dict[str, Any]:
        """
        Lấy Thiên Can theo chỉ số.
        """

        index = index % 10

        for item in self._heavenly_stems:

            if self._parse_int(
                item["stem_index"]
            ) == index:

                return item

        raise SolarTermNotFoundError(
            f"Không tìm thấy Thiên Can index={index}"
        )

    # -------------------------------------------------------------------------

    def next_stem(
        self,
        stem: str,
        step: int = 1,
    ) -> Dict[str, Any]:
        """
        Lấy Thiên Can kế tiếp.
        """

        stem_index = self._get_stem_index(stem)

        new_index = (stem_index + step) % 10

        return self._get_stem_by_index(
            new_index
        )

    # -------------------------------------------------------------------------
    # MONTH STEM
    # -------------------------------------------------------------------------

    def get_month_stem(
        self,
        year_stem: str,
        month_index: int,
    ) -> Dict[str, Any]:
        """
        Tính Thiên Can tháng theo Ngũ Hổ Độn.

        Parameters
        ----------
        year_stem : str

        month_index : int
            1 -> 12
        """

        rule = self.get_year_stem_rule(
            year_stem
        )

        if rule is None:

            raise SolarTermNotFoundError(
                f"Không có quy tắc Ngũ Hổ Độn cho '{year_stem}'"
            )

        start_stem = rule["start_month_stem"]

        step = month_index - 1

        return self.next_stem(
            start_stem,
            step,
        )

    # -------------------------------------------------------------------------
    # BUILD CONTEXT
    # -------------------------------------------------------------------------

    def build_context(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> SolarTermContext:
        """
        Xây dựng SolarTermContext.
        """

        current_term = self.get_current_term(
            target_datetime
        )

        previous_term = self.get_previous_term(
            target_datetime
        )

        next_term = self.get_next_term(
            target_datetime
        )

        month_branch = self.get_month_branch(
            current_term
        )

        month_index = self._parse_int(
            month_branch["month_index"]
        )

        month_stem = self.get_month_stem(
            year_stem,
            month_index,
        )

        return SolarTermContext(

            current_term=SolarTermResult(

                code=current_term["code"],

                name=current_term["term_name"],

                datetime=self._parse_datetime(
                    current_term["datetime"]
                ),

                longitude=self._parse_float(
                    current_term["solar_longitude"]
                ),

                is_major=bool(
                    self._parse_int(
                        current_term["is_major"]
                    )
                ),
            ),

            previous_term=None
            if previous_term is None
            else SolarTermResult(

                code=previous_term["code"],

                name=previous_term["term_name"],

                datetime=self._parse_datetime(
                    previous_term["datetime"]
                ),

                longitude=self._parse_float(
                    previous_term["solar_longitude"]
                ),

                is_major=bool(
                    self._parse_int(
                        previous_term["is_major"]
                    )
                ),
            ),

            next_term=None
            if next_term is None
            else SolarTermResult(

                code=next_term["code"],

                name=next_term["term_name"],

                datetime=self._parse_datetime(
                    next_term["datetime"]
                ),

                longitude=self._parse_float(
                    next_term["solar_longitude"]
                ),

                is_major=bool(
                    self._parse_int(
                        next_term["is_major"]
                    )
                ),
            ),

            month=MonthBranchResult(

                index=month_index,

                branch=month_branch["month_branch"],

                season=month_branch["season"],
            ),

            month_stem=month_stem["stem"],

            lichun=LiChunResult(

                passed=self.is_after_lichun(
                    target_datetime
                ),

                datetime=self._parse_datetime(
                    self.get_lichun(
                        target_datetime.year
                    )["datetime"]
                )
                if self.get_lichun(
                    target_datetime.year
                )
                else None,
            ),
        )
            # -------------------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------------------

    def calculate(
        self,
        target_datetime: datetime,
        year_stem: str,
    ) -> SolarTermContext:
        """
        API chính của SolarTermCalculator.

        Parameters
        ----------
        target_datetime : datetime
            Thời điểm cần tra cứu.

        year_stem : str
            Thiên Can của năm (Giáp...Quý).

        Returns
        -------
        SolarTermContext
        """

        self._ensure_loaded()

        return self.build_context(
            target_datetime=target_datetime,
            year_stem=year_stem,
        )

    # -------------------------------------------------------------------------

    def calculate_by_date(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 12,
        minute: int = 0,
        second: int = 0,
        year_stem: str = "",
    ) -> SolarTermContext:
        """
        API tiện ích.

        Ví dụ:

            calculate_by_date(
                1987,
                1,
                21,
                4,
                15,
                year_stem="Bính"
            )
        """

        dt = datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
        )

        return self.calculate(
            target_datetime=dt,
            year_stem=year_stem,
        )

    # -------------------------------------------------------------------------
    # CACHE
    # -------------------------------------------------------------------------

    def clear_cache(self) -> None:
        """
        Xóa toàn bộ cache dữ liệu.
        """

        self._solar_terms.clear()

        self._term_dates.clear()

        self._month_branches.clear()

        self._month_stem_rules.clear()

        self._heavenly_stems.clear()

        self._loaded = False

    # -------------------------------------------------------------------------

    def refresh(self) -> None:
        """
        Reload toàn bộ dữ liệu CSV.
        """

        self.clear_cache()

        self.reload()

    # -------------------------------------------------------------------------
    # INFORMATION
    # -------------------------------------------------------------------------

    def statistics(self) -> Dict[str, int]:
        """
        Thống kê dữ liệu đã nạp.
        """

        return {

            "solar_terms":
                len(self._solar_terms),

            "solar_term_dates":
                len(self._term_dates),

            "month_branches":
                len(self._month_branches),

            "month_stem_rules":
                len(self._month_stem_rules),

            "heavenly_stems":
                len(self._heavenly_stems),

        }

    # -------------------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Kiểm tra dữ liệu có đầy đủ hay không.
        """

        if not self.loaded:
            return False

        if len(self._solar_terms) != 24:
            return False

        if len(self._month_branches) != 12:
            return False

        if len(self._month_stem_rules) != 10:
            return False

        if len(self._heavenly_stems) != 10:
            return False

        if len(self._term_dates) == 0:
            return False

        return True

    # -------------------------------------------------------------------------

    def __len__(self) -> int:

        return len(self._term_dates)

    # -------------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"<SolarTermCalculator "
            f"loaded={self.loaded} "
            f"records={len(self._term_dates)}>"
        )


# =============================================================================
# SINGLETON
# =============================================================================

solar_term_calculator = SolarTermCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    "SolarTermCalculator",
    "SolarTermError",
    "SolarTermDataError",
    "SolarTermNotFoundError",
    "solar_term_calculator",
]
