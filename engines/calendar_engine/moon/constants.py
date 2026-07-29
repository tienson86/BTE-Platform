"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : constants.py
Module      : calendar_engine.moon
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Moon Constants

Module này chứa toàn bộ hằng số thiên văn sử dụng
cho Moon Engine.

Không chứa thuật toán.

Được sử dụng bởi:

    arguments.py
    phase.py
    newmoon.py
    engine.py

Nguồn tham khảo

- Jean Meeus - Astronomical Algorithms (2nd Edition)
- IAU Astronomical Constants
- NASA JPL

============================================================
"""

from __future__ import annotations

from math import pi

# ==========================================================
# ENGINE
# ==========================================================

MODULE_NAME = "Moon Engine"

MODULE_VERSION = "1.0.0"

# ==========================================================
# MATHEMATICAL CONSTANTS
# ==========================================================

PI = pi

TWO_PI = 2.0 * pi

HALF_PI = pi / 2.0

RAD = PI / 180.0

DEG = 180.0 / PI

ARCSEC_TO_DEG = 1.0 / 3600.0

# ==========================================================
# JULIAN CONSTANTS
# ==========================================================

J2000 = 2451545.0

J1900 = 2415020.0

J1950 = 2433282.5

J2100 = 2488070.0

DAYS_PER_CENTURY = 36525.0

# ==========================================================
# MOON ORBIT
# ==========================================================

MEAN_SYNODIC_MONTH = 29.530588853

SIDEREAL_MONTH = 27.321661547

DRACONIC_MONTH = 27.212220817

ANOMALISTIC_MONTH = 27.554549878

TROPICAL_MONTH = 27.321582241

# ==========================================================
# EARTH
# ==========================================================

EARTH_RADIUS_KM = 6378.137

EARTH_FLATTENING = 1.0 / 298.257223563

EARTH_ECCENTRICITY = 0.016708634

EARTH_AXIAL_TILT = 23.439291111

# ==========================================================
# MOON
# ==========================================================

MOON_RADIUS_KM = 1737.4

MOON_DIAMETER_KM = 3474.8

MEAN_DISTANCE_KM = 384400.0

PERIGEE_DISTANCE_KM = 363300.0

APOGEE_DISTANCE_KM = 405500.0

MOON_ORBIT_INCLINATION = 5.145396

MOON_ECCENTRICITY = 0.0549

# ==========================================================
# SUN
# ==========================================================

SUN_MEAN_LONGITUDE = 280.46646

SUN_MEAN_ANOMALY = 357.52911

SUN_ECCENTRICITY = 0.016708634

# ==========================================================
# PHASE ANGLES
# ==========================================================

NEW_MOON = 0.0

FIRST_QUARTER = 90.0

FULL_MOON = 180.0

LAST_QUARTER = 270.0

# ==========================================================
# ILLUMINATION
# ==========================================================

FULL_ILLUMINATION = 100.0

NEW_ILLUMINATION = 0.0

# ==========================================================
# PRECISION
# ==========================================================

EPSILON = 1e-12

ANGLE_TOLERANCE = 1e-8

TIME_TOLERANCE = 1e-8

# ==========================================================
# ITERATION
# ==========================================================

MAX_ITERATION = 100

DEFAULT_ITERATION = 50

# ==========================================================
# EXPORT
# ==========================================================

__all__ = [

    "MODULE_NAME",
    "MODULE_VERSION",

    "PI",
    "TWO_PI",
    "HALF_PI",

    "RAD",
    "DEG",

    "ARCSEC_TO_DEG",

    "J1900",
    "J1950",
    "J2000",
    "J2100",

    "DAYS_PER_CENTURY",

    "MEAN_SYNODIC_MONTH",
    "SIDEREAL_MONTH",
    "DRACONIC_MONTH",
    "ANOMALISTIC_MONTH",
    "TROPICAL_MONTH",

    "EARTH_RADIUS_KM",
    "EARTH_FLATTENING",
    "EARTH_ECCENTRICITY",
    "EARTH_AXIAL_TILT",

    "MOON_RADIUS_KM",
    "MOON_DIAMETER_KM",
    "MEAN_DISTANCE_KM",
    "PERIGEE_DISTANCE_KM",
    "APOGEE_DISTANCE_KM",
    "MOON_ORBIT_INCLINATION",
    "MOON_ECCENTRICITY",

    "SUN_MEAN_LONGITUDE",
    "SUN_MEAN_ANOMALY",
    "SUN_ECCENTRICITY",

    "NEW_MOON",
    "FIRST_QUARTER",
    "FULL_MOON",
    "LAST_QUARTER",

    "FULL_ILLUMINATION",
    "NEW_ILLUMINATION",

    "EPSILON",
    "ANGLE_TOLERANCE",
    "TIME_TOLERANCE",

    "MAX_ITERATION",
    "DEFAULT_ITERATION",
]

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print(MODULE_NAME)
    print("Version :", MODULE_VERSION)
    print("=" * 60)

    print("J2000               :", J2000)
    print("Synodic Month       :", MEAN_SYNODIC_MONTH)
    print("Moon Distance (km)  :", MEAN_DISTANCE_KM)
    print("Moon Radius (km)    :", MOON_RADIUS_KM)
    print("Earth Radius (km)   :", EARTH_RADIUS_KM)
    print("Earth Axial Tilt    :", EARTH_AXIAL_TILT)
    print("RAD                 :", RAD)
    print("DEG                 :", DEG)
