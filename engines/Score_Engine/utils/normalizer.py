"""
Normalize Score
"""


class ScoreNormalizer:

    @staticmethod
    def clamp(
        score: float,
        minimum: float = 0,
        maximum: float = 100
    ):

        if score < minimum:
            return minimum

        if score > maximum:
            return maximum

        return score

    @staticmethod
    def percentage(
        value,
        total
    ):

        if total == 0:
            return 0

        return value / total * 100

    @staticmethod
    def weighted(
        score,
        weight
    ):

        return score * weight
