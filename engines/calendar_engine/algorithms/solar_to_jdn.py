"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    solar_to_jdn.py

Version:
    1.0

Description:
    Convert Gregorian Date to Julian Day Number

=========================================================
"""

import math


class SolarToJDN:
    """
    Chuyển Dương lịch sang Julian Day Number
    """

    @staticmethod
    def convert(day, month, year):

        if month <= 2:

            year -= 1

            month += 12

        A = math.floor(year / 100)

        B = 2 - A + math.floor(A / 4)

        jd = (

            math.floor(365.25 * (year + 4716))

            + math.floor(30.6001 * (month + 1))

            + day
            + B
            - 1524

        )

        return jd


    @staticmethod
    def convert_datetime(

        day,

        month,

        year,

        hour,

        minute,

        second,

        timezone

    ):

        jd = SolarToJDN.convert(

            day,

            month,

            year

        )

        fraction = (

            hour

            - timezone

            + minute / 60

            + second / 3600

        ) / 24

        return jd + fraction - 0.5
