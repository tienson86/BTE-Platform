"""
context.py
==========

Định nghĩa InterpretationContext.

Đây là đối tượng trung tâm của Interpretation Engine.

Toàn bộ dữ liệu từ Bazi Engine sẽ được chuẩn hóa thành
InterpretationContext trước khi đưa vào Rule Engine.

Luồng xử lý:

Bazi Engine
      │
      ▼
InterpretationContext
      │
      ├── Rule Loader
      ├── Rule Matcher
      ├── Conflict Resolver
      ├── Rule Scoring
      ├── Interpretation Builder
      └── Formatter
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==========================================================
# Tứ Trụ
# ==========================================================

@dataclass(slots=True)
class Pillar:

    heavenly_stem: str
    earthly_branch: str

    hidden_stems: List[str] = field(default_factory=list)

    ten_gods: List[str] = field(default_factory=list)

    na_yin: Optional[str] = None

    stage_of_life: Optional[str] = None


# ==========================================================
# Đại Vận
# ==========================================================

@dataclass(slots=True)
class LuckPillar:

    stem: str

    branch: str

    start_age: int

    end_age: int

    start_year: int

    end_year: int


# ==========================================================
# Lưu Niên
# ==========================================================

@dataclass(slots=True)
class AnnualLuck:

    year: int

    stem: str

    branch: str


# ==========================================================
# Metadata
# ==========================================================

@dataclass(slots=True)
class Metadata:

    version: str = "1.0"

    school: str = "Tu Binh"

    language: str = "vi"

    created_at: Optional[str] = None


# ==========================================================
# Interpretation Context
# ==========================================================

@dataclass(slots=True)
class InterpretationContext:
    """
    Đối tượng chuẩn truyền giữa các module.

    Đây là model duy nhất mà Interpretation Engine làm việc.
    """

    # --------------------------------------------------
    # Thông tin cơ bản
    # --------------------------------------------------

    gender: str

    solar_datetime: str

    lunar_datetime: str

    timezone: str = "Asia/Ho_Chi_Minh"

    location: Optional[str] = None

    # --------------------------------------------------
    # Tứ Trụ
    # --------------------------------------------------

    year: Optional[Pillar] = None

    month: Optional[Pillar] = None

    day: Optional[Pillar] = None

    hour: Optional[Pillar] = None

    # --------------------------------------------------
    # Nhật Chủ
    # --------------------------------------------------

    day_master: Optional[str] = None

    # --------------------------------------------------
    # Phân tích mệnh
    # --------------------------------------------------

    strength: Optional[str] = None

    pattern: Optional[str] = None

    useful_god: Optional[str] = None

    favorable_gods: List[str] = field(default_factory=list)

    unfavorable_gods: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # Quan hệ
    # --------------------------------------------------

    combinations: List[str] = field(default_factory=list)

    clashes: List[str] = field(default_factory=list)

    harms: List[str] = field(default_factory=list)

    punishments: List[str] = field(default_factory=list)

    destructions: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # Thần sát
    # --------------------------------------------------

    shensha: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # Đại vận
    # --------------------------------------------------

    current_luck: Optional[LuckPillar] = None

    luck_cycles: List[LuckPillar] = field(default_factory=list)

    # --------------------------------------------------
    # Lưu niên
    # --------------------------------------------------

    current_annual: Optional[AnnualLuck] = None

    # --------------------------------------------------
    # Điểm số
    # --------------------------------------------------

    scores: Dict[str, float] = field(default_factory=dict)

    # --------------------------------------------------
    # Dữ liệu mở rộng
    # --------------------------------------------------

    metadata: Metadata = field(default_factory=Metadata)

    extra: Dict[str, Any] = field(default_factory=dict)

    # ==================================================
    # Helper Methods
    # ==================================================

    def has_useful_god(self) -> bool:
        return bool(self.useful_god)

    def has_pattern(self) -> bool:
        return bool(self.pattern)

    def has_shensha(self, name: str) -> bool:
        return name in self.shensha

    def get_score(self, key: str, default: float = 0.0) -> float:
        return self.scores.get(key, default)

    def set_score(self, key: str, value: float) -> None:
        self.scores[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển Context thành dict.
        Hữu ích khi export JSON hoặc ghi log.
        """
        from dataclasses import asdict
        return asdict(self)
