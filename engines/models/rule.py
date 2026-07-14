"""
rule.py
========

Định nghĩa Rule Model.

Mọi Rule trong Rule Database sau khi đọc từ CSV
đều được chuyển thành Rule object.

Interpretation Engine chỉ làm việc với Rule,
không làm việc trực tiếp với dict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(slots=True)
class Rule:

    # -----------------------------
    # Định danh
    # -----------------------------
    rule_id: str

    module: str

    category: str

    sub_category: str = ""

    # -----------------------------
    # Điều kiện
    # -----------------------------
    condition: str = ""

    # -----------------------------
    # Nội dung
    # -----------------------------
    result: str = ""

    template_id: str = ""

    # -----------------------------
    # Đánh giá
    # -----------------------------
    priority: int = 0

    weight: float = 0.0

    score: float = 0.0

    # -----------------------------
    # Metadata
    # -----------------------------
    version: str = "1.0"

    enabled: bool = True

    tags: List[str] = field(default_factory=list)

    author: str = ""

    note: str = ""

    # -----------------------------
    # Runtime
    # -----------------------------
    matched: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ======================================

    def mark_matched(self):
        self.matched = True

    def mark_unmatched(self):
        self.matched = False

    def add_score(self, value: float):
        self.score += value

    def reset_score(self):
        self.score = 0.0

    @property
    def is_enabled(self):
        return self.enabled

    @property
    def is_matched(self):
        return self.matched
