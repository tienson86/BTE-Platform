from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ScoreResult:
    """
    Kết quả cuối cùng của Score Engine.
    """

    wuxing_score: float = 0.0
    strength_score: float = 0.0
    ten_god_score: float = 0.0
    pattern_score: float = 0.0
    useful_god_score: float = 0.0
    shensha_score: float = 0.0
    luck_score: float = 0.0

    total_score: float = 0.0

    grade: str = ""
    confidence: str = ""

    recommendation: str = ""

    details: Dict[str, Any] = field(default_factory=dict)

    success: bool = True

    @property
    def modules(self):

        return list(self.details.keys())

    def to_dict(self):

        return {
            "success": self.success,
            "wuxing_score": self.wuxing_score,
            "strength_score": self.strength_score,
            "ten_god_score": self.ten_god_score,
            "pattern_score": self.pattern_score,
            "useful_god_score": self.useful_god_score,
            "shensha_score": self.shensha_score,
            "luck_score": self.luck_score,
            "total_score": self.total_score,
            "grade": self.grade,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "modules": self.modules,
            "details": self.details
        }
