from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ScoreReport:
    """
    Báo cáo đầu ra của Score Engine.
    """

    total_score: float

    grade: str

    confidence: str

    recommendation: str

    dimensions: Dict = field(default_factory=dict)

    matched_rules: List = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    notes: List[str] = field(default_factory=list)
