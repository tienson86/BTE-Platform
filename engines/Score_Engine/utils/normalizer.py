"""
Score Normalizer

Chuẩn hóa điểm của từng Dimension.
"""


class ScoreNormalizer:

    @staticmethod
    def clamp(
        score: float,
        minimum: float = 0,
        maximum: float = 100
    ) -> float:

        return max(
            minimum,
            min(maximum, score)
        )

    @staticmethod
    def percentage(
        value: float,
        total: float
    ) -> float:

        if total == 0:
            return 0.0

        return round(
            value / total * 100,
            2
        )

    @staticmethod
    def weighted(
        score: float,
        weight: float
    ) -> float:

        return round(
            score * weight,
            2
        )

    @staticmethod
    def normalize_range(
        score: float,
        source_min: float,
        source_max: float,
        target_min: float = 0,
        target_max: float = 100
    ) -> float:

        if source_max == source_min:
            return target_min

        value = (
            (score - source_min)
            / (source_max - source_min)
        )

        result = target_min + (
            value * (target_max - target_min)
        )

        return round(result, 2)
