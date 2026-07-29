"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : newmoon.py
Module      : calendar_engine.moon
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Moon Phase & New Moon Engine

Theo:

Jean Meeus
Astronomical Algorithms
Chapter 49

Chức năng

    • Mean New Moon
    • True New Moon
    • Full Moon
    • First Quarter
    • Last Quarter

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sin

from .constants import (
    RAD,
    J2000,
    MEAN_SYNODIC_MONTH,
)

from .arguments import MoonArgumentsEngine


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass(slots=True)
class MoonEvent:

    """
    Kết quả tính một pha trăng.
    """

    lunation: float

    jde: float

    phase: str


# ==========================================================
# ENGINE
# ==========================================================

class NewMoonEngine:

    """
    Engine tính các pha Mặt Trăng.
    """

    # ------------------------------------------------------

    @staticmethod
    def julian_century(jde: float) -> float:
        """
        Julian Century từ J2000.
        """

        return (jde - J2000) / 36525.0

    # ------------------------------------------------------

    @staticmethod
    def lunation_number(jdn: float) -> float:
        """
        Tính số chu kỳ giao hội (lunation).

        K = số chu kỳ kể từ mốc chuẩn
        2000-01-06 18:14 UTC.
        """

        return (jdn - 2451550.09765) / MEAN_SYNODIC_MONTH

    # ------------------------------------------------------

    @staticmethod
    def mean_new_moon(k: float) -> float:
        """
        Mean New Moon.

        Đây là nghiệm gần đúng trước khi
        áp dụng các hiệu chỉnh thiên văn.
        """

        T = k / 1236.85

        T2 = T * T
        T3 = T2 * T
        T4 = T3 * T

        jde = (
            2451550.09765
            + 29.530588853 * k
            + 0.0001337 * T2
            - 0.000000150 * T3
            + 0.00000000073 * T4
        )

        return jde

    # ------------------------------------------------------

    @staticmethod
    def eccentricity(T: float) -> float:
        """
        Độ lệch tâm quỹ đạo Trái Đất.
        """

        return (
            1.0
            - 0.002516 * T
            - 0.0000074 * T * T
        )

    # ------------------------------------------------------

    @staticmethod
    def fundamental_arguments(T: float):

        """
        Các tham số cơ bản dùng cho
        hiệu chỉnh New Moon.
        """

        M = (
            2.5534
            + 29.10535670 * 1236.85 * T
            - 0.0000014 * T * T
            - 0.00000011 * T * T * T
        )

        Mprime = (
            201.5643
            + 385.81693528 * 1236.85 * T
            + 0.0107582 * T * T
            + 0.00001238 * T * T * T
            - 0.000000058 * T * T * T * T
        )

        F = (
            160.7108
            + 390.67050284 * 1236.85 * T
            - 0.0016118 * T * T
            - 0.00000227 * T * T * T
            + 0.000000011 * T * T * T * T
        )

        Omega = (
            124.7746
            - 1.56375588 * 1236.85 * T
            + 0.0020672 * T * T
            + 0.00000215 * T * T * T
        )

        return (
            M,
            Mprime,
            F,
            Omega,
        )

    # ------------------------------------------------------

    @staticmethod
    def normalize(value: float) -> float:

        return value % 360.0
