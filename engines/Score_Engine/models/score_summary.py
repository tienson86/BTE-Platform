from dataclasses import dataclass, field
from typing import Dict

from .score_dimension import ScoreDimension


@dataclass
class ScoreSummary:
    """
    Tổng hợp toàn bộ điểm.
    """

    dimensions: Dict[str, ScoreDimension] = field(default_factory=dict)

    total_score: float = 0.0

    confidence: str = ""

    grade: str = ""

    recommendation: str = ""

    def add_dimension(
        self,
        dimension: ScoreDimension
    ):

        self.dimensions[dimension.name] = dimension

    def calculate_total(self):

        self.total_score = sum(
            item.weighted_score
            for item in self.dimensions.values()
        )
