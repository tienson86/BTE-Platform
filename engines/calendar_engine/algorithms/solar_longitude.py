"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    solar_longitude.py

Version:
    1.0

Description:
    Calculate Solar Longitude

=========================================================
"""

import math


class SolarLongitude:
    """
    Tính Kinh độ Mặt Trời.
    """

    @staticmethod
    def calculate(jdn):

        T = (jdn - 2451545.0) / 36525

        M = (

            357.52910

            + 35999.05030 * T

            - 0.0001559 * T * T

            - 0.00000048 * T * T * T

        )

        M = math.radians(M)

        L0 = (

            280.46645

            + 36000.76983 * T

            + 0.0003032 * T * T

        )

        DL = (

            (1.914600 - 0.004817 * T - 0.000014 * T * T)

            * math.sin(M)

            +

            (0.019993 - 0.000101 * T)

            * math.sin(2 * M)

            +

            0.000290 * math.sin(3 * M)

        )

        longitude = L0 + DL

        longitude = longitude % 360

        return longitude


    # ====================================================

    # SOLAR TERM INDEX

    # ====================================================

    @staticmethod
    def get_term_index(longitude):

        return int(longitude / 15)


    # ====================================================

    # SOLAR TERM DEGREE

    # ====================================================

    @staticmethod
    def get_degree(longitude):

        return longitude
