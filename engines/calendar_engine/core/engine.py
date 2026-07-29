"""
engine.py
==============================

Moon Engine

API dùng cho toàn bộ hệ thống.
"""

from dataclasses import dataclass

from .newmoon import nearest_new_moon

from .phase import moon_phase


@dataclass(slots=True)
class MoonInfo:

    jd_new_moon: float

    age: float

    angle: float

    illumination: float

    phase: str


class MoonEngine:

    @staticmethod
    def calculate(jd: float) -> MoonInfo:

        nm = nearest_new_moon(jd)

        p = moon_phase(jd, nm)

        return MoonInfo(

            jd_new_moon=nm,

            age=p.age,

            angle=p.angle,

            illumination=p.illumination,

            phase=p.phase_name,

        )
