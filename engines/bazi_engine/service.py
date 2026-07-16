"""
BTE Platform
Bazi Engine Service

API công khai của Bazi Engine.
"""

from __future__ import annotations

from typing import Optional

from .engine import BaziEngine
from .config import BaziConfig
from .models import (
    BaziContext,
    BaziResult,
)


class BaziService:
    """
    Public Service của Bazi Engine.
    """

    def __init__(
        self,
        config: Optional[BaziConfig] = None,
    ) -> None:

        self.engine = BaziEngine(config=config)

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        context: BaziContext,
    ) -> BaziResult:
        """
        Thực thi toàn bộ Bazi Engine.
        """

        return self.engine.execute(context)

    # =====================================================
    # Build Chart
    # =====================================================

    def build_chart(
        self,
        context: BaziContext,
    ) -> BaziResult:
        """
        Lập đầy đủ lá số Bát Tự.
        """

        context.operation = "build_chart"

        return self.execute(context)

    # =====================================================
    # Four Pillars
    # =====================================================

    def build_four_pillars(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "four_pillars"

        return self.execute(context)

    # =====================================================
    # Ten Gods
    # =====================================================

    def calculate_ten_gods(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "ten_gods"

        return self.execute(context)

    # =====================================================
    # Strength
    # =====================================================

    def calculate_strength(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "strength"

        return self.execute(context)

    # =====================================================
    # Useful God
    # =====================================================

    def calculate_useful_god(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "useful_god"

        return self.execute(context)

    # =====================================================
    # Shen Sha
    # =====================================================

    def calculate_shensha(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "shensha"

        return self.execute(context)

    # =====================================================
    # Luck Pillars
    # =====================================================

    def calculate_luck_pillars(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "luck_pillars"

        return self.execute(context)

    # =====================================================
    # Annual Luck
    # =====================================================

    def calculate_annual_luck(
        self,
        context: BaziContext,
    ) -> BaziResult:

        context.operation = "annual_luck"

        return self.execute(context)
