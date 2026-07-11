"""
phase.py
=================================

Tính pha Mặt Trăng.

Thuật toán:
Jean Meeus
Astronomical Algorithms

Trả về:

- tuổi trăng
- pha
- góc pha
- illumination
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi


SYNODIC_MONTH = 29.530588853


@dataclass(slots=True)
class MoonPhase:

    age: float

    angle: float

    illumination: float

    phase_name: str


PHASES = [

    (1.84566, "New Moon"),

    (5.53699, "Waxing Crescent"),

    (9.22831, "First Quarter"),

    (12.91963, "Waxing Gibbous"),

    (16.61096, "Full Moon"),

    (20.30228, "Waning Gibbous"),

    (23.99361, "Last Quarter"),

    (27.68493, "Waning Crescent"),

]


def phase_name(age: float) -> str:

    for limit, name in PHASES:

        if age < limit:

            return name

    return "New Moon"


def moon_phase(jd: float, jd_new_moon: float) -> MoonPhase:

    age = (jd - jd_new_moon) % SYNODIC_MONTH

    angle = age / SYNODIC_MONTH * 360.0

    illumination = (1 - cos(angle * pi / 180)) / 2

    return MoonPhase(

        age=age,

        angle=angle,

        illumination=illumination,

        phase_name=phase_name(age),

    )
