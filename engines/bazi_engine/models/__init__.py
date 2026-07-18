"""
===============================================================================
Bazi Engine - Models
-------------------------------------------------------------------------------
Description:
    Các Domain Model dùng chung cho toàn bộ Bazi Engine.

Version:
    1.0.0
===============================================================================
"""

from .pillar import Pillar
from .four_pillars import FourPillars
from .bazi_chart import BaziChart
from .luck import (
    LuckPillar,
    AnnualLuck,
    MonthlyLuck,
)
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BaziResult:
    """Compatibility result model used by the interpretation layer."""
    success: bool = True
    chart: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

__all__ = [

    "Pillar",

    "FourPillars",

    "BaziChart",

    "LuckPillar",

    "AnnualLuck",

    "MonthlyLuck",
    "BaziResult",

]
