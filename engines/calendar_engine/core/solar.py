"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : solar.py
Module      : calendar_engine.core
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

MÔ TẢ

Tính toán vị trí biểu kiến của Mặt Trời theo thời gian.

Input:
    Julian Day Number (JDN)

Output:
    - Solar Longitude (λ)
    - Mean Longitude
    - Mean Anomaly
    - Apparent Longitude
    - Julian Century

Module này là nền tảng để:

    - jieqi.py
    - converter.py
    - lunar calendar
    - bazi engine

Thuật toán:

Jean Meeus
Astronomical Algorithms

============================================================
"""

from __future__ import annotations

from math import sin

from .base import (
    DEG,
    RAD,
    J2000,
    normalize_degree,
)

# ==========================================================
# SOLAR ENGINE
# ==========================================================


class SolarEngine:
    """
    Tính toán vị trí Mặt Trời.
    """

    # ------------------------------------------------------

    @staticmethod
    def julian_century(jdn: float) -> float:
        """
        Julian Century từ J2000.
        """

        return (jdn - J2000) / 36525.0

    # ------------------------------------------------------

    @staticmethod
    def mean_longitude(jdn: float) -> float:
        """
        Mean Solar Longitude.
        """

        T = SolarEngine.julian_century(jdn)

        L0 = (
            280.46646
            + 36000.76983 * T
            + 0.0003032 * T * T
        )

        return normalize_degree(L0)

    # ------------------------------------------------------

    @staticmethod
    def mean_anomaly(jdn: float) -> float:
        """
        Mean Anomaly.
        """

        T = SolarEngine.julian_century(jdn)

        M = (
            357.52911
            + 35999.05029 * T
            - 0.0001537 * T * T
        )

        return normalize_degree(M)

    # ------------------------------------------------------

    @staticmethod
    def equation_of_center(jdn: float) -> float:
        """
        Equation of Center.
        """

        T = SolarEngine.julian_century(jdn)

        M = SolarEngine.mean_anomaly(jdn)

        Mrad = M * RAD

        C = (
            (1.914602 - 0.004817 * T - 0.000014 * T * T)
            * sin(Mrad)
            + (0.019993 - 0.000101 * T)
            * sin(2 * Mrad)
            + 0.000289
            * sin(3 * Mrad)
        )

        return C

    # ------------------------------------------------------

    @staticmethod
    def true_longitude(jdn: float) -> float:
        """
        True Longitude.
        """

        return normalize_degree(
            SolarEngine.mean_longitude(jdn)
            + SolarEngine.equation_of_center(jdn)
        )

    # ------------------------------------------------------

    @staticmethod
    def apparent_longitude(jdn: float) -> float:
        """
        Apparent Longitude.
        """

        T = SolarEngine.julian_century(jdn)

        omega = 125.04 - 1934.136 * T

        lam = (
            SolarEngine.true_longitude(jdn)
            - 0.00569
            - 0.00478 * sin(omega * RAD)
        )

        return normalize_degree(lam)

    # ------------------------------------------------------

    @staticmethod
    def solar_longitude(jdn: float) -> float:
        """
        API chính.

        Trả về Solar Longitude.
        """

        return SolarEngine.apparent_longitude(jdn)


# ==========================================================
# UNIT TEST
# ==========================================================

if __name__ == "__main__":

    from .julian import JulianEngine

    print("=" * 60)
    print("BTE SOLAR ENGINE")
    print("=" * 60)

    jdn = JulianEngine.solar_to_jdn(
        2026,
        7,
        11,
    )

    print("JDN :", jdn)

    print()

    print(
        "Julian Century :",
        SolarEngine.julian_century(jdn),
    )

    print(
        "Mean Longitude :",
        SolarEngine.mean_longitude(jdn),
    )

    print(
        "Mean Anomaly :",
        SolarEngine.mean_anomaly(jdn),
    )

    print(
        "Equation Of Center :",
        SolarEngine.equation_of_center(jdn),
    )

    print(
        "True Longitude :",
        SolarEngine.true_longitude(jdn),
    )

    print(
        "Apparent Longitude :",
        SolarEngine.apparent_longitude(jdn),
    )

    print(
        "Solar Longitude :",
        SolarEngine.solar_longitude(jdn),
    )
