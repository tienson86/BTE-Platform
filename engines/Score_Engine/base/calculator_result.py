from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CalculatorResult:
    """
    Kết quả trả về của từng Calculator.

    Ví dụ:
        - WuxingScoreCalculator
        - StrengthScoreCalculator
        - PatternScoreCalculator
    """

    # Tổng điểm của Calculator
    score: float = 0.0

    # Trọng số áp dụng
    weight: float = 1.0

    # Điểm sau khi nhân trọng số
    weighted_score: float = 0.0

    # Tên module
    module: str = ""

    # Danh sách Rule đã áp dụng
    matched_rules: List[Dict[str, Any]] = field(default_factory=list)

    # Chi tiết diễn giải
    details: Dict[str, Any] = field(default_factory=dict)

    # Có lỗi hay không
    success: bool = True

    message: str = ""

    def calculate(self) -> None:
        """
        Tính điểm sau trọng số.
        """
        self.weighted_score = self.score * self.weight

    def add_rule(
        self,
        rule_code: str,
        score: float,
        description: str = ""
    ) -> None:

        self.matched_rules.append({
            "rule_code": rule_code,
            "score": score,
            "description": description,
        })

    def to_dict(self) -> Dict[str, Any]:

        return {
            "module": self.module,
            "score": self.score,
            "weight": self.weight,
            "weighted_score": self.weighted_score,
            "matched_rules": self.matched_rules,
            "details": self.details,
            "success": self.success,
            "message": self.message,
        }
