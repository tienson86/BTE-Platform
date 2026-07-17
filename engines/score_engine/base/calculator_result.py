"""
Calculator Result

Đối tượng chuẩn lưu kết quả của một Calculator.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class CalculatorResult:

    # =========================
    # Metadata
    # =========================

    module: str = ""

    dimension: str = ""

    success: bool = True

    message: str = ""

    # =========================
    # Score
    # =========================

    score: float = 0.0

    weighted_score: float = 0.0

    weight: float = 1.0

    # =========================
    # Rule
    # =========================

    matched_rules: list = field(default_factory=list)

    history: list = field(default_factory=list)

    # =========================
    # Extra
    # =========================

    warnings: list = field(default_factory=list)

    errors: list = field(default_factory=list)

    details: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

    execution_time: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =========================

    @property
    def rule_count(self):

        return len(self.matched_rules)

    def add_warning(self, text):

        self.warnings.append(text)

    def add_error(self, text):

        self.errors.append(text)

        self.success = False

    def set_detail(self, key, value):

        self.details[key] = value

    def get_detail(self, key, default=None):

        return self.details.get(key, default)

    def to_dict(self):

        return {

            "module": self.module,

            "dimension": self.dimension,

            "success": self.success,

            "score": self.score,

            "weighted_score": self.weighted_score,

            "weight": self.weight,

            "matched_rules": self.matched_rules,

            "history": self.history,

            "warnings": self.warnings,

            "errors": self.errors,

            "details": self.details,

            "metadata": self.metadata,

            "execution_time": self.execution_time,

            "created_at": self.created_at.isoformat(),

        }

    def __repr__(self):

        return (

            f"<CalculatorResult "

            f"{self.module} "

            f"score={self.score}>"

        )
