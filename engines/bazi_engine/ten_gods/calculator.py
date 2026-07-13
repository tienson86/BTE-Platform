"""
===============================================================================
Bazi Engine - Ten Gods Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/ten_gods/calculator.py

Description:
    Bộ tính Thập Thần (Ten Gods Calculator).

Flow:

        FourPillars
             │
             ▼
      Day Master (Nhật Chủ)
             │
             ▼
      Rule Loader (CSV)
             │
             ▼
        TenGodResult
             │
             ▼
        TenGodChart

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List

from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars
from bazi_engine.models import Pillar

from .rule_loader import ten_god_rule_loader
from .ten_god import (
    TenGod,
    TenGodChart,
    TenGodResult,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class TenGodCalculatorError(Exception):
    """Base Exception."""


class TenGodCalculationError(
    TenGodCalculatorError,
):
    """Calculation Error."""


# =============================================================================
# CALCULATOR
# =============================================================================

class TenGodCalculator(
    BaseCalculator,
):
    """
    Bộ tính Thập Thần.
    """

    def __init__(self):

        super().__init__()

        self._loader = ten_god_rule_loader

        self.mark_loaded()

    # -----------------------------------------------------------------
    # INTERNAL
    # -----------------------------------------------------------------

    def _build_ten_god(
        self,
        day_master: str,
        target_stem: str,
    ) -> TenGod:
        """
        Tạo đối tượng TenGod từ Rule Database.
        """

        rule = self._loader.get_rule(
            day_master,
            target_stem,
        )

        description = self._loader.get_description(
            rule["code"]
        )

        if description is None:

            description = {}

        return TenGod(

            code=rule["code"],

            name=rule["name"],

            chinese=description.get(
                "chinese",
                "",
            ),

            short_name=description.get(
                "short_name",
                "",
            ),

            category=description.get(
                "category",
                "",
            ),

            polarity=description.get(
                "polarity",
                "",
            ),

            element_relation=description.get(
                "element_relation",
                "",
            ),

            description=description.get(
                "description",
                "",
            ),

            metadata=description,

        )

    # -----------------------------------------------------------------

    def _calculate_stem(
        self,
        day_master: str,
        target_stem: str,
    ) -> TenGodResult:
        """
        Tính Thập Thần của một Thiên Can.
        """

        ten_god = self._build_ten_god(

            day_master,

            target_stem,

        )

        return TenGodResult(

            day_master=day_master,

            target_stem=target_stem,

            ten_god=ten_god,

        )
    # -----------------------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------------------

    def calculate_stem(
        self,
        day_master: str,
        target_stem: str,
    ) -> TenGodResult:
        """
        Tính Thập Thần của một Thiên Can.
        """

        self.ensure_loaded()

        return self._calculate_stem(

            day_master,

            target_stem,

        )

    # -----------------------------------------------------------------

    def calculate_hidden_stems(
        self,
        day_master: str,
        hidden_stems: List[str],
    ) -> List[TenGodResult]:
        """
        Tính Thập Thần của toàn bộ Tàng Can.
        """

        result: List[TenGodResult] = []

        for stem in hidden_stems:

            result.append(

                self.calculate_stem(

                    day_master,

                    stem,

                )

            )

        return result

    # -----------------------------------------------------------------

    def calculate_pillar(
        self,
        day_master: str,
        pillar: Pillar,
    ) -> Dict[str, object]:
        """
        Tính Thập Thần của một Trụ.
        """

        stem = self.calculate_stem(

            day_master,

            pillar.stem,

        )

        hidden = self.calculate_hidden_stems(

            day_master,

            list(pillar.hidden_stems),

        )

        return {

            "stem": stem,

            "hidden_stems": hidden,

        }

    # -----------------------------------------------------------------

    def calculate_all_heavenly_stems(
        self,
        pillars: FourPillars,
    ) -> Dict[str, TenGodResult]:
        """
        Tính Thập Thần của bốn Thiên Can.
        """

        day_master = pillars.day.stem

        return {

            "year":

                self.calculate_stem(

                    day_master,

                    pillars.year.stem,

                ),

            "month":

                self.calculate_stem(

                    day_master,

                    pillars.month.stem,

                ),

            "day":

                self.calculate_stem(

                    day_master,

                    pillars.day.stem,

                ),

            "hour":

                self.calculate_stem(

                    day_master,

                    pillars.hour.stem,

                ),

        }

    # -----------------------------------------------------------------

    def calculate_all_hidden_stems(
        self,
        pillars: FourPillars,
    ) -> Dict[str, List[TenGodResult]]:
        """
        Tính Thập Thần của toàn bộ Tàng Can.
        """

        day_master = pillars.day.stem

        return {

            "year":

                self.calculate_hidden_stems(

                    day_master,

                    list(

                        pillars.year.hidden_stems

                    ),

                ),

            "month":

                self.calculate_hidden_stems(

                    day_master,

                    list(

                        pillars.month.hidden_stems

                    ),

                ),

            "day":

                self.calculate_hidden_stems(

                    day_master,

                    list(

                        pillars.day.hidden_stems

                    ),

                ),

            "hour":

                self.calculate_hidden_stems(

                    day_master,

                    list(

                        pillars.hour.hidden_stems

                    ),

                ),

        }
          # -----------------------------------------------------------------
    # CHART
    # -----------------------------------------------------------------

    def calculate_chart(
        self,
        pillars: FourPillars,
    ) -> TenGodChart:
        """
        Tính toàn bộ Thập Thần của lá số.
        """

        self.ensure_loaded()

        heavenly = self.calculate_all_heavenly_stems(
            pillars
        )

        hidden = self.calculate_all_hidden_stems(
            pillars
        )

        chart = TenGodChart(

            year_stem=heavenly["year"],

            month_stem=heavenly["month"],

            day_stem=heavenly["day"],

            hour_stem=heavenly["hour"],

            hidden_stems=hidden,

        )

        chart.metadata = {

            "day_master":
                pillars.day.stem,

            "day_master_branch":
                pillars.day.branch,

            "pillar_count":
                4,

            "hidden_stem_count":
                sum(

                    len(value)

                    for value

                    in hidden.values()

                ),

        }

        return chart

    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> TenGodChart:
        """
        Alias của calculate_chart().
        """

        return self.calculate_chart(
            pillars
        )

    # -----------------------------------------------------------------

    def calculate_from_day_master(
        self,
        day_master: str,
        stems: List[str],
    ) -> List[TenGodResult]:
        """
        Tính Thập Thần từ Nhật Chủ và danh sách Thiên Can.
        """

        result: List[TenGodResult] = []

        for stem in stems:

            result.append(

                self.calculate_stem(

                    day_master,

                    stem,

                )

            )

        return result

    # -----------------------------------------------------------------

    def get_day_master(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy Nhật Chủ.
        """

        return pillars.day.stem

    # -----------------------------------------------------------------

    def get_statistics(
        self,
        chart: TenGodChart,
    ) -> Dict[str, int]:
        """
        Thống kê Thập Thần của lá số.
        """

        return {

            "heavenly_stems":
                len(chart.heavenly_stems),

            "hidden_stems":
                chart.hidden_count,

            "total":
                chart.total_count,

            "unique":
                len(chart.unique_names()),

        }
          # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def verify(
        self,
        pillars: FourPillars,
    ) -> bool:
        """
        Kiểm tra có thể tính Thập Thần hay không.
        """

        try:

            chart = self.calculate(
                pillars
            )

            return chart.total_count > 0

        except Exception:

            return False

    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        if not self.loaded:

            return False

        return self._loader.health_check()

    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Calculator.
        """

        return {

            "calculator":
                self.__class__.__name__,

            "rule_loader":
                self._loader.statistics(),

        }

    # -----------------------------------------------------------------

    def debug(
        self,
    ) -> Dict[str, object]:
        """
        Thông tin Debug.
        """

        return {

            "loaded":
                self.loaded,

            "health":
                self.health_check(),

            "statistics":
                self.statistics(),

        }

    # -----------------------------------------------------------------
    # CACHE
    # -----------------------------------------------------------------

    def clear_cache(
        self,
    ) -> None:
        """
        Calculator không cache dữ liệu.

        Hàm này được giữ lại để thống nhất giao diện
        với các Calculator khác.
        """

        return None

    # -----------------------------------------------------------------

    def refresh(
        self,
    ) -> None:
        """
        Reload Rule Database.
        """

        self._loader.refresh()

        self.mark_loaded()

    # -----------------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Số lượng Rule.
        """

        return len(
            self._loader
        )

    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<TenGodCalculator "

            f"loaded={self.loaded} "

            f"rules={len(self)}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

ten_god_calculator = TenGodCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "TenGodCalculator",

    "TenGodCalculatorError",

    "TenGodCalculationError",

    "ten_god_calculator",

]
