"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : arguments.py
Module      : calendar_engine.moon
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Moon Fundamental Arguments

Các tham số cơ bản của Mặt Trăng theo
Jean Meeus - Astronomical Algorithms (2nd Edition)

Các tham số được sử dụng bởi:

    phase.py
    newmoon.py
    engine.py

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import (
    J2000,
    DAYS_PER_CENTURY,
    RAD,
)

from ..core.base import normalize_degree


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass(slots=True)
class MoonArguments:
    """
    Fundamental Lunar Arguments
    """

    T: float

    L_prime: float

    D: float

    M: float

    M_prime: float

    F: float

    Omega: float


# ==========================================================
# ENGINE
# ==========================================================

class MoonArgumentsEngine:

    """
    Tính các tham số cơ bản của Mặt Trăng.
    """

    # ------------------------------------------------------

    @staticmethod
    def julian_century(jdn: float) -> float:
        """
        Julian Century kể từ J2000.
        """

        return (jdn - J2000) / DAYS_PER_CENTURY

    # ------------------------------------------------------

    @staticmethod
    def mean_longitude(T: float) -> float:
        """
        Mean Longitude of the Moon (L')
        """

        value = (
            218.3164477
            + 481267.88123421 * T
            - 0.0015786 * T * T
            + T * T * T / 538841.0
            - T * T * T * T / 65194000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def mean_elongation(T: float) -> float:
        """
        Mean Elongation (D)
        """

        value = (
            297.8501921
            + 445267.1114034 * T
            - 0.0018819 * T * T
            + T * T * T / 545868.0
            - T * T * T * T / 113065000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def sun_mean_anomaly(T: float) -> float:
        """
        Mean Anomaly of the Sun (M)
        """

        value = (
            357.5291092
            + 35999.0502909 * T
            - 0.0001536 * T * T
            + T * T * T / 24490000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def moon_mean_anomaly(T: float) -> float:
        """
        Mean Anomaly of the Moon (M')
        """

        value = (
            134.9633964
            + 477198.8675055 * T
            + 0.0087414 * T * T
            + T * T * T / 69699.0
            - T * T * T * T / 14712000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def moon_argument_latitude(T: float) -> float:
        """
        Argument of Latitude (F)
        """

        value = (
            93.2720950
            + 483202.0175233 * T
            - 0.0036539 * T * T
            - T * T * T / 3526000.0
            + T * T * T * T / 863310000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def ascending_node(T: float) -> float:
        """
        Longitude of Ascending Node (Ω)
        """

        value = (
            125.0445479
            - 1934.1362891 * T
            + 0.0020754 * T * T
            + T * T * T / 467441.0
            - T * T * T * T / 60616000.0
        )

        return normalize_degree(value)

    # ------------------------------------------------------

    @staticmethod
    def eccentricity(T: float) -> float:
        """
        Độ lệch tâm quỹ đạo Trái Đất.
        """

        return (
            1
            - 0.002516 * T
            - 0.0000074 * T * T
        )

    # ------------------------------------------------------

    @classmethod
    def calculate(cls, jdn: float) -> MoonArguments:
        """
        Tính toàn bộ tham số cơ bản.
        """

        T = cls.julian_century(jdn)

        return MoonArguments(
            T=T,
            L_prime=cls.mean_longitude(T),
            D=cls.mean_elongation(T),
            M=cls.sun_mean_anomaly(T),
            M_prime=cls.moon_mean_anomaly(T),
            F=cls.moon_argument_latitude(T),
            Omega=cls.ascending_node(T),
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

    args = MoonArgumentsEngine.calculate(jdn)

    print("=" * 60)

    print("Moon Fundamental Arguments")

    print("=" * 60)

    print(args)
