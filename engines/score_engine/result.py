"""ScoreResult — authoritative Score Engine output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoreResult:
    """
    Kết quả cuối cùng của Score Engine.

    Production serialization uses ``to_portal_dict()`` (excludes internals).
    """

    wuxing_score: float = 0.0
    strength_score: float = 0.0
    ten_god_score: float = 0.0
    pattern_score: float = 0.0
    useful_god_score: float = 0.0
    shensha_score: float = 0.0
    luck_score: float = 0.0

    total_score: float = 0.0

    grade: str = ""
    confidence: str = ""

    recommendation: str = ""

    details: dict[str, Any] = field(default_factory=dict)

    success: bool = True

    wuxing_series: list[dict[str, Any]] = field(default_factory=list)
    ten_god_series: list[dict[str, Any]] = field(default_factory=list)
    interpretation_score: float | None = None

    @property
    def modules(self) -> list[str]:
        """Module names from calculator details (internal)."""
        return list(self.details.keys())

    def to_dict(self) -> dict[str, Any]:
        """Full internal dict (includes details/modules — not for Portal)."""
        return {
            "success": self.success,
            "wuxing_score": self.wuxing_score,
            "strength_score": self.strength_score,
            "ten_god_score": self.ten_god_score,
            "pattern_score": self.pattern_score,
            "useful_god_score": self.useful_god_score,
            "shensha_score": self.shensha_score,
            "luck_score": self.luck_score,
            "total_score": self.total_score,
            "grade": self.grade,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "modules": self.modules,
            "details": self.details,
        }

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize ScoreView fields for API / Portal (no internal fields)."""
        payload: dict[str, Any] = {
            "success": self.success,
            "total_score": float(self.total_score or 0.0),
            "strength_score": float(self.strength_score or 0.0),
            "pattern_score": float(self.pattern_score or 0.0),
            "ten_god_score": float(self.ten_god_score or 0.0),
            "wuxing_score": float(self.wuxing_score or 0.0),
            "useful_god_score": float(self.useful_god_score or 0.0),
            "shensha_score": float(self.shensha_score or 0.0),
            "luck_score": float(self.luck_score or 0.0),
            "grade": self.grade or "",
            "confidence": self.confidence or "",
            "recommendation": self.recommendation or "",
        }
        if self.interpretation_score is not None:
            payload["interpretation_score"] = float(self.interpretation_score)
        if self.wuxing_series:
            payload["wuxing_series"] = list(self.wuxing_series)
        if self.ten_god_series:
            payload["ten_god_series"] = list(self.ten_god_series)
        return payload
