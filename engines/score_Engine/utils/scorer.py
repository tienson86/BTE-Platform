"""
Rule Scorer

Chức năng
---------
- Cộng/trừ điểm theo Rule.
- Áp dụng trọng số.
- Giới hạn điểm.
- Lưu lịch sử tính điểm.
"""

from typing import List, Dict


class RuleScorer:

    def __init__(self):

        self.reset()

    def reset(self):

        self._score = 0.0
        self._history: List[Dict] = []

    def add(
        self,
        score: float,
        rule_code: str = "",
        description: str = ""
    ):

        self._score += score

        self._history.append({
            "rule_code": rule_code,
            "action": "add",
            "score": score,
            "description": description,
        })

    def subtract(
        self,
        score: float,
        rule_code: str = "",
        description: str = ""
    ):

        score = abs(score)

        self._score -= score

        self._history.append({
            "rule_code": rule_code,
            "action": "subtract",
            "score": score,
            "description": description,
        })

    def apply_weight(self, weight: float):

        self._score *= weight

    def clamp(
        self,
        minimum: float = 0,
        maximum: float = 100
    ):

        self._score = max(
            minimum,
            min(maximum, self._score)
        )

    @property
    def score(self):

        return self._score

    @property
    def history(self):

        return self._history.copy()

    def summary(self):

        return {
            "score": self._score,
            "rule_count": len(self._history),
            "history": self._history,
        }
