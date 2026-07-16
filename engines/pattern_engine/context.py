"""
Pattern Context.

Lưu toàn bộ dữ liệu đầu vào phục vụ Pattern Engine.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PatternContext:
    # Bát tự
    year_pillar: Optional[str] = None
    month_pillar: Optional[str] = None
    day_pillar: Optional[str] = None
    hour_pillar: Optional[str] = None

    # Nhật chủ
    day_master: Optional[str] = None

    # Thân vượng nhược
    strength_level: Optional[str] = None
    strength_score: float = 0.0

    # Ngũ hành
    wuxing_score: Dict[str, float] = field(default_factory=dict)

    # Thập thần
    ten_gods: Dict[str, Any] = field(default_factory=dict)

    # Thần sát
    shensha: List[str] = field(default_factory=list)

    # Đại vận
    luck_pillar: Optional[str] = None

    # Dụng thần
    useful_god: Optional[str] = None

    # Dữ liệu mở rộng
    extra: Dict[str, Any] = field(default_factory=dict)
