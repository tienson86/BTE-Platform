"""
Tổng hợp kết quả Pattern.
"""

from ..models.pattern_result import PatternResultModel


class CombinationCalculator:

    def combine(

        self,

        structure,

        follow,

        special

    ) -> PatternResultModel:

        result = PatternResultModel()

        if structure:

            result.pattern = structure.pattern

            result.score = structure.score

            result.priority = structure.priority

        result.follow_pattern = follow

        result.special_pattern = special

        return result
