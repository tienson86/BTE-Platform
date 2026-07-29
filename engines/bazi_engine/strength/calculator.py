"""
===============================================================================
Bazi Engine - Strength Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/strength/calculator.py

Description:
    Engine tính Thân Vượng - Thân Nhược.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations


from typing import Dict


from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars


from bazi_engine.five_elements.service import (
    five_element_service,
)


from bazi_engine.ten_gods.service import (
    ten_god_service,
)


from .strength import (
    StrengthResult,
    StrengthScore,
    StrengthLevel,
)


from .rule_loader import (
    strength_rule_loader,
)



# =============================================================================
# EXCEPTIONS
# =============================================================================

class StrengthCalculatorError(
    Exception,
):
    """
    Base Exception.
    """



class StrengthCalculationError(
    StrengthCalculatorError,
):
    """
    Calculation Error.
    """



# =============================================================================
# CALCULATOR
# =============================================================================

class StrengthCalculator(
    BaseCalculator,
):
    """
    Bộ tính Thân Vượng Nhược.
    """



    def __init__(
        self,
    ):

        super().__init__()


        self._element_service = (
            five_element_service
        )


        self._ten_god_service = (
            ten_god_service
        )


        self._loader = (
            strength_rule_loader
        )


        self.mark_loaded()



    # -----------------------------------------------------------------
    # DAY MASTER
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

    def get_day_master_element(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Lấy Ngũ Hành Nhật Chủ.
        """

        element = (

            self._element_service
            .calculator
            .get_stem_element(

                pillars.day.stem

            )

        )


        return element.name
          # -----------------------------------------------------------------
    # SEASON
    # -----------------------------------------------------------------

    def calculate_season_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Tính điểm Tháng Lệnh (Đắc Lệnh).

        Đây là yếu tố quan trọng nhất
        trong đánh giá Thân Vượng.
        """

        month_branch = pillars.month.branch

        rule = self._loader.get_season_rule(
            month_branch
        )

        if not rule:

            return 0.0

        return float(
            rule.get(
                "weight",
                0.0,
            )
        )


    # -----------------------------------------------------------------
    # ROOT
    # -----------------------------------------------------------------

    def calculate_root_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Tính điểm Thông Căn.

        V1.1:
        Tạm thời sử dụng số lượng
        Tàng Can đồng hành với Nhật Chủ.
        """

        day_element = self.get_day_master_element(
            pillars
        )

        score = 0.0

        for pillar in (

            pillars.year,
            pillars.month,
            pillars.day,
            pillars.hour,

        ):

            hidden = (
                self._element_service
                .calculator
                .get_hidden_stem_elements(
                    pillar.branch
                )
            )

            for item in hidden:

                if item.name == day_element:

                    score += 1.0

        return score


    # -----------------------------------------------------------------
    # SUPPORT
    # -----------------------------------------------------------------

    def calculate_support_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Điểm đồng hành (Tỷ Kiếp).

        V1.1:
        Mỗi Can đồng hành = 1 điểm.
        """

        day_element = self.get_day_master_element(
            pillars
        )

        score = 0.0

        stems = (

            pillars.year.stem,
            pillars.month.stem,
            pillars.day.stem,
            pillars.hour.stem,

        )

        for stem in stems:

            element = (
                self._element_service
                .calculator
                .get_stem_element(
                    stem
                )
            )

            if element.name == day_element:

                score += 1.0

        return score


    # -----------------------------------------------------------------
    # RESOURCE
    # -----------------------------------------------------------------

    def calculate_resource_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Điểm Ấn (Hành sinh Nhật Chủ).

        V1.1:
        Sử dụng Rule Database.
        """

        day_element = self.get_day_master_element(
            pillars
        )

        score = 0.0

        rules = self._loader.get_support_rules()

        for rule in rules:

            if rule.get("target") != day_element:

                continue

            support_element = rule.get("element")

            balance = self._element_service.calculate(
                pillars
            )

            score += balance.get_value(
                support_element
            )

        return score


    # -----------------------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------------------

    def calculate_output_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Điểm Thực Thương.

        V1.1:
        Placeholder.

        Sẽ thay bằng Ten God Engine V2.
        """

        return 0.0


    # -----------------------------------------------------------------
    # WEALTH
    # -----------------------------------------------------------------

    def calculate_wealth_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Điểm Tài.

        V1.1 Placeholder.
        """

        return 0.0


    # -----------------------------------------------------------------
    # OFFICER
    # -----------------------------------------------------------------

    def calculate_officer_score(
        self,
        pillars: FourPillars,
    ) -> float:
        """
        Điểm Quan Sát.

        V1.1 Placeholder.
        """

        return 0.0


    # -----------------------------------------------------------------
    # BUILD SCORE
    # -----------------------------------------------------------------

    def build_strength_score(
        self,
        pillars: FourPillars,
    ) -> StrengthScore:
        """
        Xây dựng bảng điểm Thân Vượng.
        """

        score = StrengthScore()

        score.season = self.calculate_season_score(
            pillars
        )

        score.root = self.calculate_root_score(
            pillars
        )

        score.support = self.calculate_support_score(
            pillars
        )

        score.resource = self.calculate_resource_score(
            pillars
        )

        score.output = self.calculate_output_score(
            pillars
        )

        score.wealth = self.calculate_wealth_score(
            pillars
        )

        score.officer = self.calculate_officer_score(
            pillars
        )

        score.hidden_support = 0.0

        score.hidden_drain = 0.0

        return score
          # -----------------------------------------------------------------
    # SCORE
    # -----------------------------------------------------------------

    def calculate_final_score(
        self,
        score: StrengthScore,
    ) -> float:
        """
        Tính điểm cuối cùng.

        Công thức:

            Positive × Weight
            -
            Negative × Weight
        """

        positive = (

            score.season
            * self._loader.get_weight("season")

            +

            score.root
            * self._loader.get_weight("root")

            +

            score.support
            * self._loader.get_weight("support")

            +

            score.resource
            * self._loader.get_weight("resource")

            +

            score.hidden_support
            * self._loader.get_weight(
                "hidden_support"
            )

        )


        negative = (

            score.output
            * self._loader.get_weight("output")

            +

            score.wealth
            * self._loader.get_weight("wealth")

            +

            score.officer
            * self._loader.get_weight("officer")

            +

            score.hidden_drain
            * self._loader.get_weight(
                "hidden_drain"
            )

        )


        total = positive - negative


        #
        # Chuẩn hóa về thang điểm 0 - 100
        #

        total = 50.0 + total


        if total < 0:

            total = 0.0


        elif total > 100:

            total = 100.0


        return round(
            total,
            2,
        )


    # -----------------------------------------------------------------
    # LEVEL
    # -----------------------------------------------------------------

    def build_level(
        self,
        score: float,
    ) -> StrengthLevel:
        """
        Xây dựng StrengthLevel.
        """

        data = self._loader.get_level(
            score
        )


        if data is None:

            return StrengthLevel(

                code="UNKNOWN",

                name="Không xác định",

                score_min=0,

                score_max=100,

                description="",

            )


        return StrengthLevel(

            code=data.get(
                "code",
                "",
            ),

            name=data.get(
                "name",
                "",
            ),

            score_min=float(
                data.get(
                    "min_score",
                    0,
                )
            ),

            score_max=float(
                data.get(
                    "max_score",
                    100,
                )
            ),

            description=data.get(
                "description",
                "",
            ),

            metadata=data,

        )


    # -----------------------------------------------------------------
    # RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        Xây dựng kết quả Thân Vượng.
        """

        score_detail = self.build_strength_score(
            pillars
        )


        final_score = self.calculate_final_score(
            score_detail
        )


        level = self.build_level(
            final_score
        )


        result = StrengthResult(

            day_master=self.get_day_master(
                pillars
            ),

            element=self.get_day_master_element(
                pillars
            ),

            score=final_score,

            level=level,

            strength_score=score_detail,

            month_branch=(
                pillars.month.branch
            ),

        )


        result.description = (
            level.description
        )


        result.metadata = {

            "version": "1.1",

            "engine": "StrengthCalculator",

            "algorithm":
                "weighted_score",

        }


        return result


    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        API chính của Strength Engine.
        """

        self.ensure_loaded()

        return self.build_result(
            pillars
        )
          # -----------------------------------------------------------------
    # SCORE
    # -----------------------------------------------------------------

    def calculate_final_score(
        self,
        score: StrengthScore,
    ) -> float:
        """
        Tính điểm cuối cùng.

        Công thức:

            Positive × Weight
            -
            Negative × Weight
        """

        positive = (

            score.season
            * self._loader.get_weight("season")

            +

            score.root
            * self._loader.get_weight("root")

            +

            score.support
            * self._loader.get_weight("support")

            +

            score.resource
            * self._loader.get_weight("resource")

            +

            score.hidden_support
            * self._loader.get_weight(
                "hidden_support"
            )

        )


        negative = (

            score.output
            * self._loader.get_weight("output")

            +

            score.wealth
            * self._loader.get_weight("wealth")

            +

            score.officer
            * self._loader.get_weight("officer")

            +

            score.hidden_drain
            * self._loader.get_weight(
                "hidden_drain"
            )

        )


        total = positive - negative


        #
        # Chuẩn hóa về thang điểm 0 - 100
        #

        total = 50.0 + total


        if total < 0:

            total = 0.0


        elif total > 100:

            total = 100.0


        return round(
            total,
            2,
        )


    # -----------------------------------------------------------------
    # LEVEL
    # -----------------------------------------------------------------

    def build_level(
        self,
        score: float,
    ) -> StrengthLevel:
        """
        Xây dựng StrengthLevel.
        """

        data = self._loader.get_level(
            score
        )


        if data is None:

            return StrengthLevel(

                code="UNKNOWN",

                name="Không xác định",

                score_min=0,

                score_max=100,

                description="",

            )


        return StrengthLevel(

            code=data.get(
                "code",
                "",
            ),

            name=data.get(
                "name",
                "",
            ),

            score_min=float(
                data.get(
                    "min_score",
                    0,
                )
            ),

            score_max=float(
                data.get(
                    "max_score",
                    100,
                )
            ),

            description=data.get(
                "description",
                "",
            ),

            metadata=data,

        )


    # -----------------------------------------------------------------
    # RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        Xây dựng kết quả Thân Vượng.
        """

        score_detail = self.build_strength_score(
            pillars
        )


        final_score = self.calculate_final_score(
            score_detail
        )


        level = self.build_level(
            final_score
        )


        result = StrengthResult(

            day_master=self.get_day_master(
                pillars
            ),

            element=self.get_day_master_element(
                pillars
            ),

            score=final_score,

            level=level,

            strength_score=score_detail,

            month_branch=(
                pillars.month.branch
            ),

        )


        result.description = (
            level.description
        )


        result.metadata = {

            "version": "1.1",

            "engine": "StrengthCalculator",

            "algorithm":
                "weighted_score",

        }


        return result


    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> StrengthResult:
        """
        API chính của Strength Engine.
        """

        self.ensure_loaded()

        return self.build_result(
            pillars
        )
