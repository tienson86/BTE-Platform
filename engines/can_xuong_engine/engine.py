"""Cân Xương Đoán Mệnh engine — lookup only, no BaZi recalculation."""

from __future__ import annotations

from typing import Any

from engines.can_xuong_engine.calculator import CanXuongCalculator
from engines.can_xuong_engine.exceptions import CanXuongEngineError
from engines.can_xuong_engine.loader import CanXuongLoader
from engines.can_xuong_engine.models import CanXuongResult


class CanXuongEngine:
    """Public API: resolve Cân Xương from published Calendar / BaZi inputs."""

    def __init__(
        self,
        loader: CanXuongLoader | None = None,
        calculator: CanXuongCalculator | None = None,
    ) -> None:
        self.loader = loader or CanXuongLoader()
        self.calculator = calculator or CanXuongCalculator(self.loader)

    def calculate(
        self,
        *,
        year_ganzhi: str,
        lunar_month: int,
        lunar_day: int,
        hour_branch: str,
    ) -> CanXuongResult:
        """Return canonical can_xuong from year Hoa Giáp and lunar date/hour branch."""
        try:
            return self.calculator.calculate(
                year_ganzhi=year_ganzhi,
                lunar_month=lunar_month,
                lunar_day=lunar_day,
                hour_branch=hour_branch,
            )
        except CanXuongEngineError:
            raise
        except Exception as exc:
            raise CanXuongEngineError(f"Cân Xương calculation failed: {exc}") from exc

    def calculate_from_calendar_bazi(self, calendar: Any, bazi: Any) -> CanXuongResult:
        """Extract inputs from CalendarResult + BaziChart. Does not recompute pillars."""
        year_ganzhi = str(getattr(calendar, "year_can_chi", "") or "").strip()
        lunar_month = int(getattr(calendar, "lunar_month", 0) or 0)
        lunar_day = int(getattr(calendar, "lunar_day", 0) or 0)
        hour_pillar = getattr(bazi, "hour_pillar", None)
        hour_branch = str(getattr(hour_pillar, "branch", "") or "").strip()
        if not year_ganzhi or not hour_branch or lunar_month < 1 or lunar_day < 1:
            raise CanXuongEngineError(
                "Cân Xương requires year_can_chi, lunar month/day, and hour branch."
            )
        return self.calculate(
            year_ganzhi=year_ganzhi,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            hour_branch=hour_branch,
        )


class CanXuongService:
    """Service wrapper matching other engines' public surface."""

    def __init__(self, engine: CanXuongEngine | None = None) -> None:
        self.engine = engine or CanXuongEngine()

    def calculate(
        self,
        *,
        year_ganzhi: str,
        lunar_month: int,
        lunar_day: int,
        hour_branch: str,
    ) -> CanXuongResult:
        """Delegate to CanXuongEngine.calculate."""
        return self.engine.calculate(
            year_ganzhi=year_ganzhi,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            hour_branch=hour_branch,
        )
