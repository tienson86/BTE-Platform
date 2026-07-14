"""
rule.py
=======

Định nghĩa Rule của Interpretation Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Rule:
    """
    Rule diễn giải.

    Một Rule đại diện cho một quy tắc trong Rule Database.
    """

    # =====================================================
    # Định danh
    # =====================================================

    id: str

    name: str

    description: str = ""

    # =====================================================
    # Phân loại
    # =====================================================

    module: str = ""
    # Ví dụ:
    # useful_god
    # ten_gods
    # shensha
    # marriage

    category: str = ""
    # Ví dụ:
    # Mệnh cục
    # Thần sát
    # Hôn nhân
    # Tài vận

    topic: str = ""
    # Ví dụ:
    # Dụng thần
    # Thiên Ất
    # Phối ngẫu

    section: str = ""
    # Tiêu đề hiển thị trong báo cáo

    tags: list[str] = field(default_factory=list)

    # =====================================================
    # Điều kiện
    # =====================================================

    condition: str = ""

    priority: int = 100

    weight: float = 1.0

    enabled: bool = True

    # =====================================================
    # Kết quả
    # =====================================================

    result: str = ""

    recommendation: str = ""

    note: str = ""

    # =====================================================
    # Metadata
    # =====================================================

    source: str = ""

    school: str = ""
    # Tử Bình
    # Manh Phái
    # Tân Phái
    # ...

    version: str = "1.0"

    metadata: dict[str, Any] = field(default_factory=dict)
