"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : phase.py
Module      : calendar_engine.moon
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Moon Phase Engine

Tính:

    • Moon Age
    • Phase Angle
    • Illumination
    • Waxing / Waning
    • Phase Name

Dựa trên:

    Jean Meeus
    Astronomical Algorithms

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos

from .constants import (
    RAD,
    MEAN_SYNODIC_MONTH,
)

from .arguments import (
    MoonArgumentsEngine,
)

from ..core.solar import SolarEngine


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass(slots=True)
class MoonPhase:

    age: float

    angle: float

    illumination: float

    waxing: bool

    phase_name: str


# ==========================================================
# ENGINE
# ==========================================================

class MoonPhaseEngine:

    """
    Moon Phase Engine
    """

    # ------------------------------------------------------

    @staticmethod
    def phase_angle(jdn: float) -> float:
        """
        Góc pha Mặt Trăng.
        """

        solar = SolarEngine.solar_longitude(jdn)

        moon = MoonArgumentsEngine.calculate(jdn)

        angle = moon.L_prime - solar

        angle %= 360.0

        return angle

    # ------------------------------------------------------

    @classmethod
    def moon_age(cls, jdn: float) -> float:
        """
        Tuổi Mặt Trăng.
        """

        angle = cls.phase_angle(jdn)

        return (
            angle / 360.0
        ) * MEAN_SYNODIC_MONTH

    # ------------------------------------------------------

    @classmethod
    def illumination(cls, jdn: float) -> float:
        """
        Độ sáng (%)
        """

        angle = cls.phase_angle(jdn)

        k = (1 - cos(angle * RAD)) / 2

        return k * 100.0

    # ------------------------------------------------------

    @classmethod
    def is_waxing(cls, jdn: float) -> bool:
        """
        True nếu đang trăng lên.
        """

        angle = cls.phase_angle(jdn)

        return angle < 180.0

    # ------------------------------------------------------

    @classmethod
    def phase_name(cls, jdn: float) -> str:

        age = cls.moon_age(jdn)

        if age < 1.0:
            return "New Moon"

        if age < 6.4:
            return "Waxing Crescent"

        if age < 8.4:
            return "First Quarter"

        if age < 13.8:
            return "Waxing Gibbous"

        if age < 15.8:
            return "Full Moon"

        if age < 21.1:
            return "Waning Gibbous"

        if age < 23.1:
            return "Last Quarter"

        if age < 28.5:
            return "Waning Crescent"

        return "New Moon"

    # ------------------------------------------------------

    @classmethod
    def calculate(cls, jdn: float) -> MoonPhase:

        return MoonPhase(

            age=cls.moon_age(jdn),

            angle=cls.phase_angle(jdn),

            illumination=cls.illumination(jdn),

            waxing=cls.is_waxing(jdn),

            phase_name=cls.phase_name(jdn),

        )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    from ..core.julian import JulianEngine

    jdn = JulianEngine.solar_to_jdn(
        2026,
        7,
        11,
    )

    phase = MoonPhaseEngine.calculate(jdn)

    print("=" * 60)

    print("Moon Phase")

    print("=" * 60)

    print("Age          :", phase.age)

    print("Angle        :", phase.angle)

    print("Light (%)    :", phase.illumination)

    print("Waxing       :", phase.waxing)

    print("Phase        :", phase.phase_name)
