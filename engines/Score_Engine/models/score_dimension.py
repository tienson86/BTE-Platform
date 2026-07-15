from dataclasses import dataclass, field
from typing import List

from .score_rule import ScoreRule


@dataclass
class ScoreDimension:
    """
    Điểm của một Dimension.

    Ví dụ:

    Ngũ hành

    Thập thần

    Dụng thần
    """

    name: str

    score: float = 0.0

    weight: float = 1.0

    weighted_score: float = 0.0

    rules: List[ScoreRule] = field(default_factory=list)

    def calculate(self):

        self.weighted_score = self.score * self.weight
