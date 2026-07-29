"""
===============================================================================
Bazi Engine - Useful God Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/useful_god/calculator.py

Description:
    Engine xác định Dụng Thần - Hỷ Thần - Kỵ Thần.

Version:
    1.1.0
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from bazi_engine.core.base_calculator import BaseCalculator

from bazi_engine.models import FourPillars

from bazi_engine.strength.service import (
    strength_service,
)

from bazi_engine.five_elements.service import (
    five_element_service,
)

from .useful_god import (
    GodElement,
    UsefulGodResult,
)

from .rule_loader import (
    useful_god_rule_loader,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class UsefulGodCalculatorError(
    Exception,
):
    """
    Base Exception.
    """


class UsefulGodCalculationError(
    UsefulGodCalculatorError,
):
    """
    Calculation Error.
    """


# =============================================================================
# CALCULATOR
# =============================================================================

class UsefulGodCalculator(
    BaseCalculator,
):
    """
    Engine xác định Dụng Thần.
    """


    def __init__(
        self,
    ):

        super().__init__()

        self._strength_service = (
            strength_service
        )

        self._element_service = (
            five_element_service
        )

        self._loader = (
            useful_god_rule_loader
        )

        self.mark_loaded()


    # -----------------------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------------------

    def get_strength(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy kết quả Thân Vượng.
        """

        return self._strength_service.calculate(
            pillars
        )


    # -----------------------------------------------------------------

    def get_element_balance(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy cân bằng Ngũ Hành.
        """

        return self._element_service.calculate(
            pillars
        )


    # -----------------------------------------------------------------

    def get_day_master(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Nhật Chủ.
        """

        return pillars.day.stem


    # -----------------------------------------------------------------

    def get_day_master_element(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Ngũ Hành Nhật Chủ.
        """

        strength = self.get_strength(
            pillars
        )

        return strength.element


    # -----------------------------------------------------------------
    # RULE ANALYSIS
    # -----------------------------------------------------------------

    def analyze_strength(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích theo Thân Vượng/Nhược.
        """

        strength = self.get_strength(
            pillars
        )

        rules = (
            self._loader
            .get_strength_rules()
        )

        return {

            "strength":

                strength,

            "rules":

                rules,

        }


    # -----------------------------------------------------------------

    def analyze_season(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Điều Hậu theo mùa.
        """

        return {

            "month":

                pillars.month.branch,

            "rules":

                self._loader
                .get_season_rules(),

        }


    # -----------------------------------------------------------------

    def analyze_temperature(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Hàn - Nhiệt - Táo - Thấp.
        """

        return {

            "rules":

                self._loader
                .get_temperature_rules(),

        }
          # -----------------------------------------------------------------
    # PATTERN
    # -----------------------------------------------------------------

    def analyze_pattern(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Cách Cục.
        """

        return {

            "rules":

                self._loader.get_pattern_rules(),

            "matched":

                [],

        }


    # -----------------------------------------------------------------
    # SPECIAL CASE
    # -----------------------------------------------------------------

    def analyze_special_case(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Ngoại Lệ.
        """

        return {

            "rules":

                self._loader.get_special_rules(),

            "matched":

                [],

        }


    # -----------------------------------------------------------------
    # FOLLOW PATTERN
    # -----------------------------------------------------------------

    def analyze_follow_pattern(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Tòng Cách.
        """

        return {

            "rules":

                self._loader
                .get_follow_pattern_rules(),

            "matched":

                [],

        }


    # -----------------------------------------------------------------
    # COMBINATION
    # -----------------------------------------------------------------

    def analyze_combination(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Hợp Hóa.
        """

        return {

            "rules":

                self._loader
                .get_combination_rules(),

            "matched":

                [],

        }


    # -----------------------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------------------

    def resolve_priority(
        self,
        context: Dict,
    ) -> Dict:
        """
        Áp dụng Rule ưu tiên.

        V1.1:
            Trả về Context.

        V2:
            Rule Engine sẽ xử lý.
        """

        context["priority_rules"] = (

            self._loader
            .get_priority_rules()

        )

        return context


    # -----------------------------------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------------------------------

    def build_context(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Xây dựng Context tổng hợp.
        """

        context = {

            "strength":

                self.analyze_strength(
                    pillars
                ),

            "season":

                self.analyze_season(
                    pillars
                ),

            "temperature":

                self.analyze_temperature(
                    pillars
                ),

            "pattern":

                self.analyze_pattern(
                    pillars
                ),

            "special":

                self.analyze_special_case(
                    pillars
                ),

            "follow":

                self.analyze_follow_pattern(
                    pillars
                ),

            "combination":

                self.analyze_combination(
                    pillars
                ),

        }

        return self.resolve_priority(
            context
        )
          # -----------------------------------------------------------------
    # RULE MATCHER
    # -----------------------------------------------------------------

    def match_strength_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule theo Thân Vượng / Thân Nhược.
        """

        strength = context["strength"]["strength"]

        level = strength.level.code

        for rule in context["strength"]["rules"]:

            if rule.get("strength") == level:

                return rule

        return None


    # -----------------------------------------------------------------

    def match_season_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule theo Tháng Lệnh.
        """

        branch = context["season"]["month"]

        for rule in context["season"]["rules"]:

            if rule.get("month_branch") == branch:

                return rule

        return None


    # -----------------------------------------------------------------

    def match_pattern_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule Cách Cục.

        V1.1:
            Chưa triển khai Pattern Engine.
        """

        return None


    # -----------------------------------------------------------------

    def match_special_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule Ngoại Lệ.
        """

        return None


    # -----------------------------------------------------------------

    def match_follow_pattern_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule Tòng Cách.
        """

        return None


    # -----------------------------------------------------------------

    def match_combination_rule(
        self,
        context: Dict,
    ) -> Optional[dict]:
        """
        Ghép Rule Hợp Hóa.
        """

        return None


    # -----------------------------------------------------------------
    # BUILD MATCHES
    # -----------------------------------------------------------------

    def build_matches(
        self,
        context: Dict,
    ) -> Dict:
        """
        Thu thập toàn bộ Rule phù hợp.
        """

        return {

            "strength":

                self.match_strength_rule(
                    context
                ),

            "season":

                self.match_season_rule(
                    context
                ),

            "pattern":

                self.match_pattern_rule(
                    context
                ),

            "special":

                self.match_special_rule(
                    context
                ),

            "follow":

                self.match_follow_pattern_rule(
                    context
                ),

            "combination":

                self.match_combination_rule(
                    context
                ),

        }


    # -----------------------------------------------------------------
    # BUILD RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        pillars: FourPillars,
    ) -> UsefulGodResult:
        """
        Xây dựng UsefulGodResult.

        V1.1:
            Chỉ sinh khung dữ liệu.

        Rule Resolver sẽ mở rộng ở V2.
        """

        context = self.build_context(
            pillars
        )

        matches = self.build_matches(
            context
        )

        result = UsefulGodResult()

        strength = context["strength"]["strength"]

        result.strength = strength.level.name

        result.metadata = {

            "context":

                context,

            "matches":

                matches,

            "version":

                "1.1",

        }

        return result
          # -----------------------------------------------------------------
    # PRIORITY RESOLVER
    # -----------------------------------------------------------------

    def resolve_useful_god(
        self,
        context: Dict,
        matches: Dict,
    ) -> Optional[dict]:
        """
        Chọn Rule cuối cùng theo thứ tự ưu tiên.

        Thứ tự ưu tiên được định nghĩa trong:
            08_priority_rules.csv
        """

        priorities = context.get(
            "priority_rules",
            [],
        )

        for priority in priorities:

            source = priority.get("source")

            if not source:

                continue

            rule = matches.get(source)

            if rule:

                return rule

        return None


    # -----------------------------------------------------------------

    def build_god_element(
        self,
        rule: Optional[dict],
        role: str,
    ) -> GodElement:
        """
        Chuyển Rule -> GodElement.
        """

        if rule is None:

            return GodElement()

        return GodElement(

            code=rule.get(
                "code",
                "",
            ),

            name=rule.get(
                "element",
                "",
            ),

            role=role,

            score=float(
                rule.get(
                    "score",
                    0.0,
                )
            ),

            description=rule.get(
                "description",
                "",
            ),

            metadata=rule,

        )


    # -----------------------------------------------------------------
    # MAIN RESULT
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> UsefulGodResult:
        """
        API chính của Useful God Engine.
        """

        self.ensure_loaded()

        context = self.build_context(
            pillars
        )

        matches = self.build_matches(
            context
        )

        selected_rule = self.resolve_useful_god(
            context,
            matches,
        )

        result = self.build_result(
            pillars
        )

        result.useful_god = self.build_god_element(
            selected_rule,
            role="Dụng Thần",
        )

        #
        # V1.1:
        # Hỷ Thần / Kỵ Thần / Nhàn Thần
        # sẽ được sinh từ Rule Database
        # ở phiên bản tiếp theo.
        #

        result.metadata.update({

            "selected_rule":

                selected_rule,

            "resolver":

                "PriorityResolver",

            "engine_version":

                self.version,

        })

        return result


    # -----------------------------------------------------------------
    # INFORMATION
    # -----------------------------------------------------------------

    @property
    def version(
        self,
    ) -> str:
        """
        Phiên bản Calculator.
        """

        return "1.1.0"


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        return self.loaded and self._loader.health_check()


    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Engine.
        """

        return {

            "calculator":

                self.__class__.__name__,

            "version":

                self.version,

            "rule_loader":

                self._loader.statistics(),

        }


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

    def clear_cache(
        self,
    ) -> None:
        """
        Xóa cache Rule.
        """

        self._loader.clear_cache()


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<UsefulGodCalculator "

            f"version={self.version} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

useful_god_calculator = UsefulGodCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "UsefulGodCalculator",

    "UsefulGodCalculatorError",

    "UsefulGodCalculationError",

    "useful_god_calculator",

]
