"""
============================================================
BTE - Calendar Engine
------------------------------------------------------------
File        : periodic_terms.py
Module      : calendar_engine.moon
Version     : 1.0.0
Author      : BTE Project
Encoding    : UTF-8
Python      : >=3.11
------------------------------------------------------------

Periodic Lunar Terms Loader

Đọc các bảng hệ số tuần hoàn của Mặt Trăng.

Nguồn dữ liệu:

    data/
        periodic_longitude.csv
        periodic_latitude.csv
        periodic_distance.csv

Thuật toán sử dụng:

Jean Meeus
Astronomical Algorithms
Chapter 47

============================================================
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

# ==========================================================
# PATH
# ==========================================================

DATA_DIR = Path(__file__).parent / "data"

LONGITUDE_FILE = DATA_DIR / "periodic_longitude.csv"

LATITUDE_FILE = DATA_DIR / "periodic_latitude.csv"

DISTANCE_FILE = DATA_DIR / "periodic_distance.csv"


# ==========================================================
# DATA CLASS
# ==========================================================

@dataclass(slots=True)
class PeriodicTerm:

    D: int

    M: int

    M_prime: int

    F: int

    coefficient: float

    coefficient_t: float = 0.0


# ==========================================================
# LOADER
# ==========================================================

class PeriodicTermsLoader:

    """
    Đọc các bảng hệ số tuần hoàn.
    """

    @staticmethod
    def load_csv(path: Path) -> List[PeriodicTerm]:

        terms: List[PeriodicTerm] = []

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                terms.append(

                    PeriodicTerm(

                        D=int(row["D"]),

                        M=int(row["M"]),

                        M_prime=int(row["M_prime"]),

                        F=int(row["F"]),

                        coefficient=float(row["coefficient"]),

                        coefficient_t=float(
                            row.get(
                                "coefficient_t",
                                0,
                            )
                        ),

                    )

                )

        return terms

    # ------------------------------------------------------

    @classmethod
    def longitude_terms(cls):

        return cls.load_csv(LONGITUDE_FILE)

    # ------------------------------------------------------

    @classmethod
    def latitude_terms(cls):

        return cls.load_csv(LATITUDE_FILE)

    # ------------------------------------------------------

    @classmethod
    def distance_terms(cls):

        return cls.load_csv(DISTANCE_FILE)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Longitude")

    print(len(PeriodicTermsLoader.longitude_terms()))

    print()

    print("Latitude")

    print(len(PeriodicTermsLoader.latitude_terms()))

    print()

    print("Distance")

    print(len(PeriodicTermsLoader.distance_terms()))
