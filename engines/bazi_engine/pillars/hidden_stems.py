"""
===============================================================================
Bazi Engine - Hidden Stems Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/pillars/hidden_stems.py

Description:
    Tính Tàng Can (Hidden Heavenly Stems) của Địa Chi.

Flow:

        Earthly Branch
              │
              ▼
      hidden_stems.csv
              │
              ▼
     Primary / Secondary / Tertiary
              │
              ▼
        Hidden Stem Objects

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import List

from bazi_engine.core.base_calculator import BaseCalculator

from database.loader import DatabaseLoader


# =============================================================================
# CONSTANTS
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

HIDDEN_STEMS_DATABASE = (
    "09_hidden_stems/hidden_stems.csv"
)

HEAVENLY_STEMS_DATABASE = (
    "01_can_chi/heavenly_stems.csv"
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class HiddenStemsError(Exception):
    """Base Exception."""


class HiddenStemDataError(
    HiddenStemsError,
):
    """Lỗi dữ liệu."""


class HiddenStemCalculationError(
    HiddenStemsError,
):
    """Lỗi tính toán."""


# =============================================================================
# RESULT
# =============================================================================

@dataclass(slots=True)
class HiddenStem:

    stem: str

    index: int

    element: str

    yin_yang: str

    weight: float = 1.0


@dataclass(slots=True)
class HiddenStemResult:

    branch: str

    branch_index: int

    stems: List[HiddenStem]


# =============================================================================
# CALCULATOR
# =============================================================================

class HiddenStemCalculator(
    BaseCalculator,
):

    """
    Bộ tính Tàng Can.
    """

    # -----------------------------------------------------------------

    def __init__(self):

        super().__init__()

        self._loader = DatabaseLoader()

        self._hidden_rules: Dict[
            str,
            dict,
        ] = {}

        self._heavenly_stems: Dict[
            int,
            dict,
        ] = {}

        self.reload()

    # -----------------------------------------------------------------

    def reload(self):

        self._load_hidden_rules()

        self._load_heavenly_stems()

        self.mark_loaded()

    # -----------------------------------------------------------------

    def _load_hidden_rules(self):

        rows = self._loader.load_csv(
            HIDDEN_STEMS_DATABASE
        )

        self._hidden_rules.clear()

        for row in rows:

            self._hidden_rules[
                row["branch"]
            ] = row

    # -----------------------------------------------------------------

    def _load_heavenly_stems(self):

        rows = self._loader.load_csv(
            HEAVENLY_STEMS_DATABASE
        )

        self._heavenly_stems.clear()

        for row in rows:

            self._heavenly_stems[
                int(row["index"])
            ] = row
              # -----------------------------------------------------------------
    # LOOKUP
    # -----------------------------------------------------------------

    def get_rule(
        self,
        branch: str,
    ) -> dict:
        """
        Lấy quy tắc Tàng Can của một Địa Chi.
        """

        self.ensure_loaded()

        if branch not in self._hidden_rules:

            raise HiddenStemCalculationError(
                f"Không tìm thấy dữ liệu Tàng Can của '{branch}'."
            )

        return self._hidden_rules[branch]

    # -----------------------------------------------------------------

    def get_heavenly_stem_by_name(
        self,
        stem_name: str,
    ) -> dict:
        """
        Tra Thiên Can theo tên.
        """

        self.ensure_loaded()

        for stem in self._heavenly_stems.values():

            if stem["name"] == stem_name:

                return stem

        raise HiddenStemCalculationError(
            f"Không tìm thấy Thiên Can '{stem_name}'."
        )

    # -----------------------------------------------------------------

    def create_hidden_stem(
        self,
        stem_name: str,
        weight: float,
    ) -> HiddenStem:
        """
        Tạo đối tượng HiddenStem.
        """

        stem = self.get_heavenly_stem_by_name(
            stem_name
        )

        return HiddenStem(

            stem=stem["name"],

            index=int(
                stem["index"]
            ),

            element=stem["element"],

            yin_yang=stem["yin_yang"],

            weight=float(weight),

        )

    # -----------------------------------------------------------------
    # PARSER
    # -----------------------------------------------------------------

    def parse_rule(
        self,
        rule: dict,
    ) -> List[HiddenStem]:
        """
        Chuyển một dòng CSV thành danh sách HiddenStem.
        """

        result: List[HiddenStem] = []

        mapping = [

            (
                "primary",
                "primary_weight",
            ),

            (
                "secondary",
                "secondary_weight",
            ),

            (
                "tertiary",
                "tertiary_weight",
            ),

        ]

        for stem_key, weight_key in mapping:

            stem_name = rule.get(
                stem_key,
                "",
            ).strip()

            if stem_name == "":

                continue

            weight = float(

                rule.get(
                    weight_key,
                    1.0,
                )

            )

            result.append(

                self.create_hidden_stem(

                    stem_name,

                    weight,

                )

            )

        return result

    # -----------------------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------------------

    def get_hidden_stems(
        self,
        branch: str,
    ) -> HiddenStemResult:
        """
        Lấy toàn bộ Tàng Can của một Địa Chi.
        """

        rule = self.get_rule(
            branch
        )

        stems = self.parse_rule(
            rule
        )

        return HiddenStemResult(

            branch=branch,

            branch_index=int(
                rule["branch_index"]
            ),

            stems=stems,

        )

    # -----------------------------------------------------------------

    def get_hidden_stem_names(
        self,
        branch: str,
    ) -> List[str]:
        """
        Danh sách tên các Tàng Can.
        """

        result = self.get_hidden_stems(
            branch
        )

        return [

            stem.stem

            for stem in result.stems

        ]

    # -----------------------------------------------------------------

    def get_primary_hidden_stem(
        self,
        branch: str,
    ) -> HiddenStem:
        """
        Tàng Can chính.
        """

        result = self.get_hidden_stems(
            branch
        )

        return result.stems[0]
    # -----------------------------------------------------------------
    # VERIFY
    # -----------------------------------------------------------------

    def verify(
        self,
        branch: str,
    ) -> bool:
        """
        Kiểm tra dữ liệu của một Địa Chi.
        """

        try:

            result = self.get_hidden_stems(
                branch
            )

            return len(
                result.stems
            ) > 0

        except Exception:

            return False

    # -----------------------------------------------------------------

    def verify_all(
        self,
    ) -> Dict[str, bool]:
        """
        Kiểm tra toàn bộ 12 Địa Chi.
        """

        result = {}

        for branch in self._hidden_rules:

            result[branch] = self.verify(
                branch
            )

        return result

    # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def has_hidden_stems(
        self,
        branch: str,
    ) -> bool:
        """
        Kiểm tra Chi có Tàng Can hay không.
        """

        return self.verify(
            branch
        )

    # -----------------------------------------------------------------

    def count_hidden_stems(
        self,
        branch: str,
    ) -> int:
        """
        Đếm số lượng Tàng Can.
        """

        result = self.get_hidden_stems(
            branch
        )

        return len(
            result.stems
        )

    # -----------------------------------------------------------------

    def get_hidden_stem_elements(
        self,
        branch: str,
    ) -> List[str]:
        """
        Danh sách Ngũ Hành của Tàng Can.
        """

        result = self.get_hidden_stems(
            branch
        )

        return [

            stem.element

            for stem in result.stems

        ]

    # -----------------------------------------------------------------

    def get_hidden_stem_weights(
        self,
        branch: str,
    ) -> List[float]:
        """
        Danh sách trọng số.
        """

        result = self.get_hidden_stems(
            branch
        )

        return [

            stem.weight

            for stem in result.stems

        ]

    # -----------------------------------------------------------------

    def get_hidden_stem_dict(
        self,
        branch: str,
    ) -> Dict[str, float]:
        """
        Dict:

            Can -> Trọng số
        """

        result = self.get_hidden_stems(
            branch
        )

        return {

            stem.stem: stem.weight

            for stem in result.stems

        }

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict:
        """
        Thông tin Debug.
        """

        return {

            "loaded":
                self.loaded,

            "hidden_rules":
                len(
                    self._hidden_rules
                ),

            "heavenly_stems":
                len(
                    self._heavenly_stems
                ),

            "verify":
                self.verify_all(),

        }

    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, int]:
        """
        Thống kê dữ liệu.
        """

        total_hidden = 0

        for branch in self._hidden_rules:

            total_hidden += self.count_hidden_stems(
                branch
            )

        return {

            "branches":
                len(
                    self._hidden_rules
                ),

            "hidden_stems":
                total_hidden,

            "heavenly_stems":
                len(
                    self._heavenly_stems
                ),

        }
          # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa toàn bộ dữ liệu cache.
        """

        self._hidden_rules.clear()

        self._heavenly_stems.clear()

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
    # HEALTH CHECK
    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra tính toàn vẹn dữ liệu.
        """

        if not self.loaded:

            return False

        # 12 Địa Chi

        if len(self._hidden_rules) != 12:

            return False

        # 10 Thiên Can

        if len(self._heavenly_stems) != 10:

            return False

        # Kiểm tra từng Chi đều có ít nhất 1 Tàng Can

        for branch in self._hidden_rules:

            if not self.verify(branch):

                return False

        return True

    # -----------------------------------------------------------------
    # QUERY
    # -----------------------------------------------------------------

    def get_all_branches(
        self,
    ) -> List[str]:
        """
        Danh sách toàn bộ Địa Chi.
        """

        return list(
            self._hidden_rules.keys()
        )

    # -----------------------------------------------------------------

    def get_all_hidden_stems(
        self,
    ) -> Dict[str, HiddenStemResult]:
        """
        Lấy toàn bộ dữ liệu Tàng Can.
        """

        result = {}

        for branch in self.get_all_branches():

            result[branch] = self.get_hidden_stems(
                branch
            )

        return result

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Số lượng quy tắc Tàng Can.
        """

        return len(
            self._hidden_rules
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            f"<HiddenStemCalculator "

            f"loaded={self.loaded} "

            f"branches={len(self._hidden_rules)} "

            f"stems={len(self._heavenly_stems)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

hidden_stem_calculator = HiddenStemCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "HiddenStem",

    "HiddenStemResult",

    "HiddenStemCalculator",

    "HiddenStemsError",

    "HiddenStemDataError",

    "HiddenStemCalculationError",

    "hidden_stem_calculator",

]
