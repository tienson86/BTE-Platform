"""
newmoon.py
==============================

Tính thời điểm Sóc.

Jean Meeus
Astronomical Algorithms
Chapter 49
"""

from math import sin, radians


SYNODIC_MONTH = 29.530588853


BASE_NEW_MOON = 2451550.09765


def mean_new_moon(k: float) -> float:
    """
    Sóc trung bình.
    """

    T = k / 1236.85

    jd = (
        BASE_NEW_MOON
        + SYNODIC_MONTH * k
        + 0.0001337 * T ** 2
        - 0.000000150 * T ** 3
        + 0.00000000073 * T ** 4
    )

    return jd


def true_new_moon(k: float) -> float:
    """
    Sóc thật.

    Bản rút gọn.
    """

    jd = mean_new_moon(k)

    T = k / 1236.85

    M = radians(
        2.5534
        + 29.10535669 * k
        - 0.0000218 * T * T
    )

    MPR = radians(
        201.5643
        + 385.81693528 * k
    )

    correction = (
        -0.40720 * sin(MPR)
        + 0.17241 * sin(M)
    )

    return jd + correction


def nearest_new_moon(jd: float) -> float:
    """
    Sóc gần nhất trước JD.
    """

    k = int((jd - BASE_NEW_MOON) / SYNODIC_MONTH)

    nm = true_new_moon(k)

    if nm > jd:
        nm = true_new_moon(k - 1)

    return nm
