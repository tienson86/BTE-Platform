"""
===============================================================================
Bazi Engine - Base Result
-------------------------------------------------------------------------------
File:
    bazi_engine/core/base_result.py

Description:
    Các Dataclass nền tảng dùng chung cho Bazi Engine.

Version:
    1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any, Dict, Optional


# =============================================================================
# BASE RESULT
# =============================================================================

@dataclass(slots=True)
class BaseResult:
    """
    Kết quả cơ sở.
    """

    success: bool = True

    message: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)

    # ------------------------------------------------------------------

    def is_success(self) -> bool:

        return self.success


# =============================================================================
# CALCULATION RESULT
# =============================================================================

@dataclass(slots=True)
class CalculationResult(BaseResult):
    """
    Kết quả tính toán.
    """

    calculator: str = ""

    execution_time_ms: float = 0.0


# =============================================================================
# PILLAR RESULT
# =============================================================================

@dataclass(slots=True)
class PillarResult(BaseResult):
    """
    Kết quả chung của các Trụ.
    """

    pillar_name: str = ""

    stem: str = ""

    branch: str = ""

    stem_index: int = 0

    branch_index: int = 0

    ganzhi: str = ""

    element: str = ""

    yin_yang: str = ""


# =============================================================================
# ENGINE RESULT
# =============================================================================

@dataclass(slots=True)
class EngineResult(BaseResult):
    """
    Kết quả tổng hợp của Engine.
    """

    created_at: datetime = field(default_factory=datetime.now)

    version: str = "1.0.0"


__all__ = [

    "BaseResult",

    "CalculationResult",

    "PillarResult",

    "EngineResult",

]
