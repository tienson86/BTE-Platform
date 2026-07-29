"""
===============================================================================
Bazi Engine - Common Types
-------------------------------------------------------------------------------
Định nghĩa các kiểu dữ liệu dùng chung cho toàn bộ Bazi Engine.

Nguyên tắc:
- Không chứa logic.
- Chỉ khai báo TypeAlias, TypedDict, Enum...
- Giúp toàn bộ Engine thống nhất kiểu dữ liệu.
===============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, TypeAlias, TypedDict

# =============================================================================
# BASIC TYPE ALIAS
# =============================================================================

Stem: TypeAlias = str
Branch: TypeAlias = str
Element: TypeAlias = str
TenGod: TypeAlias = str
Direction: TypeAlias = str
Gender: TypeAlias = str
Season: TypeAlias = str
SolarTerm: TypeAlias = str

Year: TypeAlias = int
Month: TypeAlias = int
Day: TypeAlias = int
Hour: TypeAlias = int
Minute: TypeAlias = int

FilePath: TypeAlias = str | Path

# =============================================================================
# FOUR PILLAR
# =============================================================================


class PillarDict(TypedDict):
    stem: Stem
    branch: Branch


class FourPillarsDict(TypedDict):
    year: PillarDict
    month: PillarDict
    day: PillarDict
    hour: PillarDict


# =============================================================================
# INPUT
# =============================================================================


class BirthInput(TypedDict):
    year: Year
    month: Month
    day: Day
    hour: Hour
    minute: Minute
    gender: Gender
    timezone: str


# =============================================================================
# FIVE ELEMENT
# =============================================================================


class FiveElementStat(TypedDict):
    wood: float
    fire: float
    earth: float
    metal: float
    water: float


# =============================================================================
# TEN GOD
# =============================================================================


class TenGodResult(TypedDict):
    year: TenGod
    month: TenGod
    day: TenGod
    hour: TenGod


# =============================================================================
# LUCK
# =============================================================================


class LuckCycle(TypedDict):
    start_age: int
    stem: Stem
    branch: Branch
    direction: Direction


# =============================================================================
# CHART
# =============================================================================


class BaziChart(TypedDict, total=False):

    input: BirthInput

    pillars: FourPillarsDict

    hidden_stems: dict[str, Any]

    ten_gods: TenGodResult

    five_elements: FiveElementStat

    strength: dict[str, Any]

    useful_god: dict[str, Any]

    shen_sha: dict[str, Any]

    luck: list[LuckCycle]

    metadata: dict[str, Any]
