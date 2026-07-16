from dataclasses import dataclass


@dataclass
class ScoreGrade:
    """
    Xếp hạng cuối.
    """

    grade: str

    min_score: float

    max_score: float

    level: str

    description: str = ""

    def contains(
        self,
        score: float
    ) -> bool:

        return self.min_score <= score <= self.max_score
