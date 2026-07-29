"""
BTE Platform
Bazi Engine Models

Part 1
Core Models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Heavenly Stem
# ==========================================================

@dataclass(slots=True)
class HeavenlyStem:
    """
    Thiên Can.
    """

    index: int

    name: str

    yin_yang: str

    element: str

    pinyin: str = ""

    chinese: str = ""

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Earthly Branch
# ==========================================================

@dataclass(slots=True)
class EarthlyBranch:
    """
    Địa Chi.
    """

    index: int

    name: str

    animal: str

    yin_yang: str

    element: str

    season: str

    month: int

    hour_start: int

    hour_end: int

    pinyin: str = ""

    chinese: str = ""

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Pillar
# ==========================================================

@dataclass(slots=True)
class Pillar:
    """
    Một trụ Can Chi.
    """

    stem: HeavenlyStem

    branch: EarthlyBranch

    hidden_stems: list[Any] = field(default_factory=list)

    ten_gods: list[Any] = field(default_factory=list)

    shensha: list[Any] = field(default_factory=list)

    nayin: str = ""

    xunkong: str = ""

    twelve_stage: str = ""

    score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        """
        Ví dụ: Giáp Tý.
        """
        return f"{self.stem.name} {self.branch.name}"


# ==========================================================
# Four Pillars
# ==========================================================

@dataclass(slots=True)
class FourPillars:
    """
    Tứ Trụ Bát Tự.
    """

    year: Pillar

    month: Pillar

    day: Pillar

    hour: Pillar

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def pillars(self) -> list[Pillar]:
        """
        Trả về danh sách 4 trụ.
        """
        return [
            self.year,
            self.month,
            self.day,
            self.hour,
        ]

    @property
    def day_master(self) -> HeavenlyStem:
        """
        Nhật Chủ.
        """
        return self.day.stem

    @property
    def day_branch(self) -> EarthlyBranch:
        """
        Nhật Chi.
        """
        return self.day.branch
      # ==========================================================
# Hidden Stem
# ==========================================================

@dataclass(slots=True)
class HiddenStem:
    """
    Một Tàng Can trong Địa Chi.
    """

    stem: HeavenlyStem

    weight: float

    is_main: bool = False

    position: int = 1

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Hidden Stem Result
# ==========================================================

@dataclass(slots=True)
class HiddenStemResult:
    """
    Kết quả phân tích Tàng Can của toàn bộ Tứ Trụ.
    """

    year: list[HiddenStem] = field(default_factory=list)

    month: list[HiddenStem] = field(default_factory=list)

    day: list[HiddenStem] = field(default_factory=list)

    hour: list[HiddenStem] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all(self) -> list[HiddenStem]:

        return (
            self.year
            + self.month
            + self.day
            + self.hour
        )


# ==========================================================
# Ten God
# ==========================================================

@dataclass(slots=True)
class TenGod:
    """
    Một Thập Thần.
    """

    name: str

    short_name: str

    element: str

    yin_yang: str

    relation: str

    score: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Ten God Result
# ==========================================================

@dataclass(slots=True)
class TenGodResult:
    """
    Kết quả phân tích Thập Thần.
    """

    year: list[TenGod] = field(default_factory=list)

    month: list[TenGod] = field(default_factory=list)

    day: list[TenGod] = field(default_factory=list)

    hour: list[TenGod] = field(default_factory=list)

    statistics: dict[str, int] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all(self) -> list[TenGod]:

        return (
            self.year
            + self.month
            + self.day
            + self.hour
        )


# ==========================================================
# Strength Result
# ==========================================================

@dataclass(slots=True)
class StrengthResult:
    """
    Kết quả đánh giá Thân vượng - nhược.
    """

    score: float = 0.0

    level: str = ""

    category: str = ""

    season_support: float = 0.0

    root_support: float = 0.0

    combination_support: float = 0.0

    hidden_stem_support: float = 0.0

    final_score: float = 0.0

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Useful God Result
# ==========================================================

@dataclass(slots=True)
class UsefulGodResult:
    """
    Kết quả xác định Dụng thần.
    """

    useful_god: str = ""

    favorable_gods: list[str] = field(default_factory=list)

    unfavorable_gods: list[str] = field(default_factory=list)

    avoid_gods: list[str] = field(default_factory=list)

    method: str = ""

    confidence: float = 0.0

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)
# ==========================================================
# Pattern Result
# ==========================================================

@dataclass(slots=True)
class PatternResult:
    """
    Kết quả xác định Cách Cục.
    """

    name: str = ""

    category: str = ""

    subtype: str = ""

    score: float = 0.0

    confidence: float = 0.0

    description: str = ""

    matched_rules: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Shen Sha
# ==========================================================

@dataclass(slots=True)
class ShenSha:
    """
    Một Thần Sát.
    """

    code: str

    name: str

    category: str

    pillar: str

    description: str = ""

    level: str = ""

    positive: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Shen Sha Result
# ==========================================================

@dataclass(slots=True)
class ShenShaResult:
    """
    Kết quả phân tích Thần Sát.
    """

    year: list[ShenSha] = field(default_factory=list)

    month: list[ShenSha] = field(default_factory=list)

    day: list[ShenSha] = field(default_factory=list)

    hour: list[ShenSha] = field(default_factory=list)

    statistics: dict[str, int] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all(self) -> list[ShenSha]:

        return (
            self.year
            + self.month
            + self.day
            + self.hour
        )


# ==========================================================
# Luck Pillar
# ==========================================================

@dataclass(slots=True)
class LuckPillar:
    """
    Một Đại Vận.
    """

    index: int

    start_age: int

    end_age: int

    start_year: int

    end_year: int

    pillar: Pillar

    heavenly_stem: HeavenlyStem

    earthly_branch: EarthlyBranch

    score: float = 0.0

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Annual Luck
# ==========================================================

@dataclass(slots=True)
class AnnualLuck:
    """
    Một Lưu Niên.
    """

    year: int

    pillar: Pillar

    heavenly_stem: HeavenlyStem

    earthly_branch: EarthlyBranch

    age: int

    score: float = 0.0

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Fortune Result
# ==========================================================

@dataclass(slots=True)
class FortuneResult:
    """
    Kết quả tổng hợp vận trình.
    """

    luck_pillars: list[LuckPillar] = field(default_factory=list)

    annual_luck: list[AnnualLuck] = field(default_factory=list)

    current_luck: LuckPillar | None = None

    current_year: AnnualLuck | None = None

    overall_score: float = 0.0

    trend: str = ""

    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)
  # ==========================================================
# Bazi Context
# ==========================================================

@dataclass(slots=True)
class BaziContext:
    """
    Đầu vào của Bazi Engine.
    """

    # Calendar Engine Result
    calendar_result: Any | None = None

    # Four Pillars
    four_pillars: FourPillars | None = None

    # Operation
    operation: str = "full_analysis"

    # User Options
    options: dict[str, Any] = field(default_factory=dict)

    # Runtime Metadata
    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Bazi Result
# ==========================================================

@dataclass(slots=True)
class BaziResult:
    """
    Kết quả đầu ra của Bazi Engine.
    """

    success: bool = True

    message: str = ""

    # Core
    four_pillars: FourPillars | None = None

    hidden_stems: HiddenStemResult | None = None

    ten_gods: TenGodResult | None = None

    # Analysis
    strength: StrengthResult | None = None

    useful_god: UsefulGodResult | None = None

    pattern: PatternResult | None = None

    shensha: ShenShaResult | None = None

    # Fortune
    fortune: FortuneResult | None = None

    # Score
    score: float = 0.0

    confidence: float = 0.0

    # Extension
    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Engine Options
# ==========================================================

@dataclass(slots=True)
class BaziOptions:
    """
    Tùy chọn khi thực hiện phân tích.
    """

    calculate_hidden_stems: bool = True

    calculate_ten_gods: bool = True

    calculate_strength: bool = True

    calculate_useful_god: bool = True

    calculate_pattern: bool = True

    calculate_shensha: bool = True

    calculate_fortune: bool = True

    calculate_luck_pillars: bool = True

    calculate_annual_luck: bool = True

    use_cache: bool = True

    high_precision: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Engine State
# ==========================================================

@dataclass(slots=True)
class BaziState:
    """
    Trạng thái của Bazi Engine.
    """

    initialized: bool = False

    data_loaded: bool = False

    validated: bool = False

    calculated: bool = False

    completed: bool = False

    elapsed_time: float = 0.0

    current_step: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)
