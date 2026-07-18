"""
Score Engine

Điều phối toàn bộ quá trình chấm điểm lá số.

Pipeline:

Context
    ↓
Wuxing Calculator
    ↓
Strength Calculator
    ↓
Ten God Calculator
    ↓
Pattern Calculator
    ↓
Useful God Calculator
    ↓
ShenSha Calculator
    ↓
Luck Calculator
    ↓
Final Score Calculator
    ↓
ScoreResult
"""

from .result import ScoreResult
from .loader import ScoreLoader

from .calculators import (
    WuxingScoreCalculator,
    StrengthScoreCalculator,
    TenGodScoreCalculator,
    PatternScoreCalculator,
    UsefulGodScoreCalculator,
    ShenshaScoreCalculator,
    LuckScoreCalculator,
    FinalScoreCalculator,
)


class ScoreEngine:
    """
    Engine chính của Score Engine.
    """

    def __init__(self, loader=None):

        self.loader = loader or ScoreLoader(
            "database/15_score_engine"
        )

        self.calculators = self._build_pipeline()

    def _build_pipeline(self):
        """
        Khởi tạo Pipeline.

        Thứ tự rất quan trọng.
        """

        return [

            WuxingScoreCalculator(self.loader),

            StrengthScoreCalculator(self.loader),

            TenGodScoreCalculator(self.loader),

            PatternScoreCalculator(self.loader),

            UsefulGodScoreCalculator(self.loader),

            ShenshaScoreCalculator(self.loader),

            LuckScoreCalculator(self.loader),

            FinalScoreCalculator(self.loader),

        ]

    def calculate(self, context):

        if hasattr(context, "validate"):
            context.validate()

        result = ScoreResult()

        calculator_results = {}

        for calculator in self.calculators:

            calc_result = calculator.safe_execute(context)

            calculator_results[
                calculator.module_name
            ] = calc_result

        #
        # Đưa dữ liệu từng module vào ScoreResult
        #

        if "wuxing" in calculator_results:
            result.wuxing_score = calculator_results[
                "wuxing"
            ].weighted_score

        if "strength" in calculator_results:
            result.strength_score = calculator_results[
                "strength"
            ].weighted_score

        if "ten_gods" in calculator_results:
            result.ten_god_score = calculator_results[
                "ten_gods"
            ].weighted_score

        if "pattern" in calculator_results:
            result.pattern_score = calculator_results[
                "pattern"
            ].weighted_score

        if "useful_god" in calculator_results:
            result.useful_god_score = calculator_results[
                "useful_god"
            ].weighted_score

        if "shensha" in calculator_results:
            result.shensha_score = calculator_results[
                "shensha"
            ].weighted_score

        if "luck" in calculator_results:
            result.luck_score = calculator_results[
                "luck"
            ].weighted_score

        #
        # Final Calculator
        #

        if "final_score" in calculator_results:

            final = calculator_results["final_score"]

            result.total_score = final.score

            result.grade = final.details.get(
                "grade",
                ""
            )

            result.confidence = final.details.get(
                "confidence",
                ""
            )

            result.recommendation = final.details.get(
                "recommendation",
                ""
            )

        #
        # Lưu toàn bộ kết quả
        #

        result.details = calculator_results

        return result
