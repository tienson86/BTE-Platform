"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    lunar_converter.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Convert Solar Date to Lunar Date

=========================================================
"""

from datetime import datetime


class LunarConverter:
    """
    Lunar Converter

    Chức năng:

    - Chuyển ngày dương sang ngày âm
    - Xác định tháng nhuận
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        input_data = context["input"]

        julian_day = context["julian_day"]

        timezone = context["utc_offset"]

        solar_date = datetime.strptime(

            input_data["solar_date"],

            "%d/%m/%Y"

        )

        lunar = self.convert(

            solar_date,

            julian_day,

            timezone

        )

        context["lunar_day"] = lunar["day"]

        context["lunar_month"] = lunar["month"]

        context["lunar_year"] = lunar["year"]

        context["leap_month"] = lunar["leap"]

        return context


    # =====================================================
    # CONVERT
    # =====================================================

    def convert(

        self,

        solar_date,

        julian_day,

        timezone

    ):

        """
        Hàm chuyển đổi Âm Dương.

        Phiên bản 1.0:
        Là khung chuẩn.

        Thuật toán chuyển đổi sẽ hoàn thiện
        khi xây dựng Lunar Calendar Library.
        """

        lunar = {

            "day": None,

            "month": None,

            "year": None,

            "leap": False

        }

        return lunar


    # =====================================================
    # GET LUNAR DATE
    # =====================================================

    def get_lunar_date(self, context):

        return {

            "day": context["lunar_day"],

            "month": context["lunar_month"],

            "year": context["lunar_year"],

            "leap": context["leap_month"]

        }


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "LunarConverter",

            "version": "1.0",

            "status": "READY"

        }
