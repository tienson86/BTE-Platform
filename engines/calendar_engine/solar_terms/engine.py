"""
===============================================================================
Calendar Engine - Solar Terms Engine
-------------------------------------------------------------------------------
Facade của module Solar Terms.

Các module khác chỉ gọi file này.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from .calculator import SolarTermCalculator
from .models import SolarTermContext


class SolarTermEngine:

    def __init__(self):

        self.calculator = SolarTermCalculator()

    def calculate(
        self,
        birth_datetime: datetime,
    ) -> SolarTermContext:

        return self.calculator.calculate(
            birth_datetime
        )


solar_term_engine = SolarTermEngine()
