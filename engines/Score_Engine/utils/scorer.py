"""
Rule Scorer

Cộng điểm theo Rule.
"""


class RuleScorer:

    def __init__(self):

        self.total = 0.0

    def add(
        self,
        score: float
    ):

        self.total += score

    def subtract(
        self,
        score: float
    ):

        self.total -= abs(score)

    def apply_weight(
        self,
        weight: float
    ):

        self.total *= weight

    def reset(self):

        self.total = 0.0

    def value(self):

        return self.total
