"""
Integration Context.

Lưu toàn bộ dữ liệu xuyên suốt Pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class IntegrationContext:

    # ===============================
    # Input
    # ===============================

    birth_info: Optional[Any] = None

    # ===============================
    # Context truyền cho từng Engine
    # ===============================

    calendar: Optional[Any] = None

    bazi: Optional[Any] = None

    score: Optional[Any] = None

    pattern: Optional[Any] = None

    interpretation: Optional[Any] = None

    report: Optional[Any] = None

    # ===============================
    # Kết quả từng bước
    # ===============================

    calendar_result: Optional[Any] = None

    bazi_result: Optional[Any] = None

    score_result: Optional[Any] = None

    pattern_result: Optional[Any] = None

    interpretation_result: Optional[Any] = None

    report_result: Optional[Any] = None

    # ===============================

    metadata: dict = field(default_factory=dict)

    extra: dict = field(default_factory=dict)

    def set(self, key: str, value: Any):

        self.extra[key] = value

    def get(self, key: str, default=None):

        return self.extra.get(key, default)
