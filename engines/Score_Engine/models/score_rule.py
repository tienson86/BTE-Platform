from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoreRule:
    """
    Một Rule được đọc từ CSV.
    """

    id: str

    rule_code: str

    score: float

    priority: int = 0

    weight: float = 1.0

    description: str = ""

    source_file: Optional[str] = None

    matched: bool = False
