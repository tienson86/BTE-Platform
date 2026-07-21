"""
Semantic Block Model

SemanticBlock là đơn vị tri thức trung gian giữa
InterpretationBuilder và SentenceGenerator.

Pipeline:

MatchedRule
    ↓
SemanticBlock
    ↓
GeneratedSentence
    ↓
InterpretationReport

SemanticBlock KHÔNG chứa câu văn hoàn chỉnh.

Nó chỉ biểu diễn ý nghĩa luận giải (semantic meaning),
giúp SentenceGenerator có thể sinh nhiều phong cách diễn đạt
khác nhau mà không làm thay đổi logic luận giải.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Semantic Block
# ==========================================================

@dataclass(slots=True)
class SemanticBlock:
    """
    Đơn vị tri thức trung gian của Interpretation Engine.

    Parameters
    ----------
    topic
        Chủ đề luận giải.

    title
        Tiêu đề hiển thị.

    priority
        Mức ưu tiên khi sinh báo cáo.

    severity
        Mức đánh giá.

    facts
        Danh sách các facts đã được Builder tổng hợp.

    source_rules
        Danh sách Rule ID tạo ra block này.

    metadata
        Dữ liệu mở rộng.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    topic: str

    title: str

    # ------------------------------------------------------
    # Ordering
    # ------------------------------------------------------

    priority: int = 100

    # ------------------------------------------------------
    # Severity
    # ------------------------------------------------------

    severity: str = "info"
    # info
    # good
    # warning
    # bad
    # critical

    # ------------------------------------------------------
    # Semantic Facts
    # ------------------------------------------------------

    facts: list[str] = field(default_factory=list)

    # ------------------------------------------------------
    # Traceability
    # ------------------------------------------------------

    source_rules: list[str] = field(default_factory=list)

    # ------------------------------------------------------
    # Extension Data
    # ------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Helper
    # ======================================================

    @property
    def fact_count(self) -> int:
        """Số lượng semantic facts."""
        return len(self.facts)

    @property
    def rule_count(self) -> int:
        """Số lượng rule đã kích hoạt."""
        return len(self.source_rules)

    @property
    def is_empty(self) -> bool:
        """Không có semantic facts."""
        return self.fact_count == 0

    # ======================================================
    # Methods
    # ======================================================

    def add_fact(self, fact: str) -> None:
        """
        Thêm một semantic fact.
        """

        if fact not in self.facts:
            self.facts.append(fact)

    def add_rule(self, rule_id: str) -> None:
        """
        Thêm Rule ID.
        """

        if rule_id not in self.source_rules:
            self.source_rules.append(rule_id)

    def update_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Cập nhật metadata.
        """

        self.metadata[key] = value
