"""
Generated Sentence Model

GeneratedSentence là kết quả trung gian được tạo ra bởi
SentenceGenerator.

Pipeline:

SemanticBlock
    ↓
GeneratedSentence
    ↓
ReportBuilder
    ↓
InterpretationReport

GeneratedSentence biểu diễn một câu luận giải đã hoàn chỉnh,
nhưng vẫn giữ đầy đủ metadata để phục vụ trace, debug,
Golden Dataset và Explainable AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Generated Sentence
# ==========================================================

@dataclass(slots=True)
class GeneratedSentence:
    """
    Một câu luận giải đã được sinh.

    Parameters
    ----------
    topic
        Chủ đề luận giải.

    sentence
        Nội dung câu hoàn chỉnh.

    priority
        Thứ tự sắp xếp.

    confidence
        Độ tin cậy (0.0 -> 1.0).

    source_rules
        Danh sách Rule ID sinh ra câu này.

    metadata
        Dữ liệu mở rộng.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    topic: str

    sentence: str

    # ------------------------------------------------------
    # Ordering
    # ------------------------------------------------------

    priority: int = 100

    # ------------------------------------------------------
    # Quality
    # ------------------------------------------------------

    confidence: float = 1.0

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
    def is_empty(self) -> bool:
        """
        Kiểm tra câu rỗng.
        """
        return not self.sentence.strip()

    @property
    def rule_count(self) -> int:
        """
        Số lượng Rule tạo ra câu.
        """
        return len(self.source_rules)

    # ======================================================
    # Methods
    # ======================================================

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
