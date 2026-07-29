"""
===============================================================================
Bazi Engine - Pattern Calculator
-------------------------------------------------------------------------------
File:
    bazi_engine/pattern/calculator.py

Description:
    Engine xác định Cách Cục (格局).

Version:
    1.0.0
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

from bazi_engine.ten_gods.service import (
    ten_god_service,
)

from .pattern import (
    Pattern,
    PatternResult,
)

from .rule_loader import (
    pattern_rule_loader,
)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PatternCalculatorError(Exception):
    """
    Base Exception.
    """


class PatternCalculationError(
    PatternCalculatorError,
):
    """
    Calculation Error.
    """


# =============================================================================
# CALCULATOR
# =============================================================================

class PatternCalculator(BaseCalculator):
    """
    Engine xác định Cách Cục.
    """

    def __init__(self):

        super().__init__()

        self._loader = pattern_rule_loader

        self._strength_service = strength_service

        self._ten_god_service = ten_god_service

        self.mark_loaded()

    # -----------------------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------------------

    def get_strength(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy kết quả Thân Vượng/Nhược.
        """

        return self._strength_service.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_ten_gods(
        self,
        pillars: FourPillars,
    ):
        """
        Lấy kết quả Thập Thần.
        """

        return self._ten_god_service.calculate(
            pillars
        )

    # -----------------------------------------------------------------

    def get_month_branch(
        self,
        pillars: FourPillars,
    ) -> str:
        """
        Địa Chi Tháng.
        """

        return pillars.month.branch

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
    # ANALYSIS
    # -----------------------------------------------------------------

    def analyze_main_patterns(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Chính Cách.
        """

        return {

            "rules":

                self._loader.get_main_patterns(),

            "matched":

                [],

        }

    # -----------------------------------------------------------------

    def analyze_follow_patterns(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Tòng Cách.
        """

        return {

            "rules":

                self._loader.get_follow_patterns(),

            "matched":

                [],

        }

    # -----------------------------------------------------------------

    def analyze_transformation(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Hóa Khí Cách.
        """

        return {

            "rules":

                self._loader.get_transformations(),

            "matched":

                [],

        }

    # -----------------------------------------------------------------

    def analyze_special_patterns(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Phân tích Ngoại Cách.
        """

        return {

            "rules":

                self._loader.get_special_patterns(),

            "matched":

                [],

        }
          # -----------------------------------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------------------------------

    def build_context(
        self,
        pillars: FourPillars,
    ) -> Dict:
        """
        Xây dựng Context phục vụ Pattern Engine.
        """

        strength = self.get_strength(
            pillars
        )

        ten_gods = self.get_ten_gods(
            pillars
        )

        return {

            "pillars":

                pillars,

            "day_master":

                self.get_day_master(
                    pillars
                ),

            "month_branch":

                self.get_month_branch(
                    pillars
                ),

            "strength":

                strength,

            "ten_gods":

                ten_gods,

            "main":

                self.analyze_main_patterns(
                    pillars
                ),

            "follow":

                self.analyze_follow_patterns(
                    pillars
                ),

            "transformation":

                self.analyze_transformation(
                    pillars
                ),

            "special":

                self.analyze_special_patterns(
                    pillars
                ),

        }


    # -----------------------------------------------------------------
    # MATCH MAIN PATTERN
    # -----------------------------------------------------------------

    def match_main_patterns(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Chính Cách.

        V1:
            Trả về danh sách Rule phù hợp.
        """

        matched = []

        month_branch = context["month_branch"]

        for rule in context["main"]["rules"]:

            if rule.get("month_branch") == month_branch:

                matched.append(rule)

        return matched


    # -----------------------------------------------------------------
    # MATCH FOLLOW PATTERN
    # -----------------------------------------------------------------

    def match_follow_patterns(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Tòng Cách.

        V1:
            Placeholder.
        """

        return []


    # -----------------------------------------------------------------
    # MATCH TRANSFORMATION
    # -----------------------------------------------------------------

    def match_transformation_patterns(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Hóa Khí Cách.

        V1:
            Placeholder.
        """

        return []


    # -----------------------------------------------------------------
    # MATCH SPECIAL
    # -----------------------------------------------------------------

    def match_special_patterns(
        self,
        context: Dict,
    ) -> List[dict]:
        """
        Ghép Ngoại Cách.

        V1:
            Placeholder.
        """

        return []


    # -----------------------------------------------------------------
    # BUILD CANDIDATES
    # -----------------------------------------------------------------

    def build_candidates(
        self,
        context: Dict,
    ) -> Dict[str, List[dict]]:
        """
        Xây dựng danh sách ứng viên Cách Cục.
        """

        return {

            "main":

                self.match_main_patterns(
                    context
                ),

            "follow":

                self.match_follow_patterns(
                    context
                ),

            "transformation":

                self.match_transformation_patterns(
                    context
                ),

            "special":

                self.match_special_patterns(
                    context
                ),

        }
          # -----------------------------------------------------------------
    # CONDITION CHECKER
    # -----------------------------------------------------------------

    def check_conditions(
        self,
        candidate: dict,
        context: Dict,
    ) -> bool:
        """
        Kiểm tra điều kiện thành/phá Cách.

        V1:
            Chỉ kiểm tra các điều kiện cơ bản.

        V2:
            Rule Engine sẽ đánh giá toàn bộ điều kiện.
        """

        conditions = self._loader.get_condition_rules()

        code = candidate.get("code")

        for condition in conditions:

            if condition.get("pattern_code") != code:

                continue

            #
            # Placeholder:
            # Điều kiện sẽ được Rule Engine xử lý.
            #

            return True

        return True


    # -----------------------------------------------------------------
    # SCORE
    # -----------------------------------------------------------------

    def calculate_pattern_score(
        self,
        candidate: dict,
        context: Dict,
    ) -> float:
        """
        Tính điểm Cách Cục.

        Điểm được lấy từ
        07_pattern_scoring.csv
        """

        scoring_rules = (
            self._loader
            .get_scoring_rules()
        )

        code = candidate.get("code")

        for score_rule in scoring_rules:

            if score_rule.get("pattern_code") == code:

                try:

                    return float(
                        score_rule.get(
                            "score",
                            0,
                        )
                    )

                except Exception:

                    return 0.0

        return 0.0


    # -----------------------------------------------------------------
    # BUILD PATTERN
    # -----------------------------------------------------------------

    def build_pattern(
        self,
        candidate: dict,
        score: float,
    ) -> Pattern:
        """
        Chuyển Rule -> Pattern Model.
        """

        return Pattern(

            code=candidate.get(
                "code",
                "",
            ),

            name=candidate.get(
                "name",
                "",
            ),

            category=candidate.get(
                "category",
                "",
            ),

            priority=int(
                candidate.get(
                    "priority",
                    0,
                )
            ),

            score=score,

            description=candidate.get(
                "description",
                "",
            ),

            metadata=candidate,

        )


    # -----------------------------------------------------------------
    # RANK
    # -----------------------------------------------------------------

    def rank_candidates(
        self,
        candidates: Dict[str, List[dict]],
        context: Dict,
    ) -> List[Pattern]:
        """
        Chấm điểm toàn bộ ứng viên.
        """

        ranked: List[Pattern] = []

        for group in candidates.values():

            for candidate in group:

                if not self.check_conditions(
                    candidate,
                    context,
                ):

                    continue

                score = self.calculate_pattern_score(
                    candidate,
                    context,
                )

                ranked.append(

                    self.build_pattern(
                        candidate,
                        score,
                    )

                )

        ranked.sort(

            key=lambda x: (

                x.priority,

                -x.score,

            )

        )

        return ranked


    # -----------------------------------------------------------------
    # SELECT
    # -----------------------------------------------------------------

    def select_best_pattern(
        self,
        ranked: List[Pattern],
    ) -> Optional[Pattern]:
        """
        Chọn Cách Cục tốt nhất.
        """

        if not ranked:

            return None

        return ranked[0]
          # -----------------------------------------------------------------
    # RESULT
    # -----------------------------------------------------------------

    def build_result(
        self,
        ranked: List[Pattern],
        context: Dict,
    ) -> PatternResult:
        """
        Xây dựng PatternResult.
        """

        result = PatternResult()

        if ranked:

            result.main_pattern = ranked[0]

            result.matched_patterns = ranked

            #
            # Confidence
            #

            result.confidence = min(

                ranked[0].score / 100.0,

                1.0,

            )

            category = (
                ranked[0]
                .category
                .lower()
            )

            result.follow_pattern = (
                category == "follow"
            )

            result.transformation_pattern = (
                category == "transformation"
            )

            result.special_pattern = (
                category == "special"
            )

            result.description = (
                ranked[0]
                .description
            )

        result.metadata = {

            "context":

                context,

            "candidate_count":

                len(ranked),

            "engine":

                self.__class__.__name__,

        }

        return result


    # -----------------------------------------------------------------
    # MAIN
    # -----------------------------------------------------------------

    def calculate(
        self,
        pillars: FourPillars,
    ) -> PatternResult:
        """
        API chính của Pattern Engine.
        """

        self.ensure_loaded()

        context = self.build_context(
            pillars
        )

        candidates = self.build_candidates(
            context
        )

        ranked = self.rank_candidates(
            candidates,
            context,
        )

        return self.build_result(
            ranked,
            context,
        )


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

        return "1.0.0"


    # -----------------------------------------------------------------

    def health_check(
        self,
    ) -> bool:
        """
        Kiểm tra trạng thái Calculator.
        """

        return (

            self.loaded

            and

            self._loader.health_check()

        )


    # -----------------------------------------------------------------

    def statistics(
        self,
    ) -> Dict[str, object]:
        """
        Thống kê Pattern Engine.
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
        Xóa cache.
        """

        self._loader.clear_cache()


    # -----------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (

            "<PatternCalculator "

            f"version={self.version} "

            f"loaded={self.loaded}>"

        )


# =============================================================================
# SINGLETON
# =============================================================================

pattern_calculator = PatternCalculator()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [

    "PatternCalculator",

    "PatternCalculatorError",

    "PatternCalculationError",

    "pattern_calculator",

]
