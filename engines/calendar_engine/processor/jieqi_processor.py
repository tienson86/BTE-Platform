"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    jieqi_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Solar Term (Tiết Khí)

=========================================================
"""


class JieQiProcessor:
    """
    JieQi Processor

    Chức năng:

    - Xác định Tiết Khí
    - Xác định Nguyệt Lệnh
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        julian_day = context["julian_day"]

        formula = context["formula"]

        result = self.find_jieqi(

            julian_day,

            formula

        )

        context["jieqi"] = result["jieqi"]

        context["month_commander"] = result["month_commander"]

        context["solar_longitude"] = result["solar_longitude"]

        context["jieqi_index"] = result["jieqi_index"]

        return context


    # =====================================================
    # FIND JIEQI
    # =====================================================

    def find_jieqi(

        self,

        julian_day,

        formula

    ):

        """
        Tra cứu Tiết Khí.

        Thuật toán sẽ được hoàn thiện
        trong Lunar Calendar Library.
        """

        result = {

            "jieqi": None,

            "month_commander": None,

            "solar_longitude": None,

            "jieqi_index": None

        }

        return result


    # =====================================================
    # GET JIEQI
    # =====================================================

    def get_jieqi(self, context):

        return context["jieqi"]


    # =====================================================
    # GET MONTH COMMANDER
    # =====================================================

    def get_month_commander(self, context):

        return context["month_commander"]


    # =====================================================
    # GET SOLAR LONGITUDE
    # =====================================================

    def get_solar_longitude(self, context):

        return context["solar_longitude"]


    # =====================================================
    # GET JIEQI INDEX
    # =====================================================

    def get_jieqi_index(self, context):

        return context["jieqi_index"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "JieQiProcessor",

            "version": "1.0",

            "status": "READY"

        }
