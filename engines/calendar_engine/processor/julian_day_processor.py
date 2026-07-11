"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    julian_day_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Julian Day Number (JDN)

=========================================================
"""

from datetime import datetime
import math


class JulianDayProcessor:
    """
    Julian Day Processor

    Chức năng:

    - Chuyển ngày giờ dương lịch sang Julian Day Number
    - Lưu kết quả vào Context
    """

    def execute(self, context):

        input_data = context["input"]

        solar_date = input_data["solar_date"]

        solar_time = input_data["solar_time"]

        utc_offset = context["utc_offset"]

        julian_day = self.calculate_julian_day(

            solar_date,

            solar_time,

            utc_offset

        )

        context["julian_day"] = julian_day

        return context


    # =====================================================
    # CALCULATE JULIAN DAY
    # =====================================================

    def calculate_julian_day(

        self,

        solar_date,

        solar_time,

        utc_offset

    ):

        dt = datetime.strptime(

            f"{solar_date} {solar_time}",

            "%d/%m/%Y %H:%M"

        )

        year = dt.year

        month = dt.month

        day = dt.day

        hour = dt.hour

        minute = dt.minute

        second = dt.second


        if month <= 2:

            year -= 1

            month += 12


        A = math.floor(year / 100)

        B = 2 - A + math.floor(A / 4)


        day_fraction = (

            (hour - utc_offset)

            + minute / 60

            + second / 3600

        ) / 24


        jdn = (

            math.floor(365.25 * (year + 4716))

            + math.floor(30.6001 * (month + 1))

            + day

            + B

            - 1524.5

            + day_fraction

        )

        return jdn


    # =====================================================
    # GET JULIAN DAY
    # =====================================================

    def get_julian_day(self, context):

        return context["julian_day"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "JulianDayProcessor",

            "version": "1.0",

            "status": "READY"

        }
