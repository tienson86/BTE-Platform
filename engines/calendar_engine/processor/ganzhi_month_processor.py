"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    ganzhi_month_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Heavenly Stem and Earthly Branch of Month

=========================================================
"""


class GanzhiMonthProcessor:
    """
    Ganzhi Month Processor

    Chức năng:

    - Xác định Can Chi tháng
    - Căn cứ theo Tiết Khí (Nguyệt Lệnh)
    - Tra Mapping
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        year_can = context["year_can"]

        month_commander = context["month_commander"]

        mapping = context["mapping"]

        result = self.find_month_ganzhi(

            year_can,

            month_commander,

            mapping

        )

        context["month_can"] = result["can"]

        context["month_chi"] = result["chi"]

        context["month_ganzhi"] = (

            f"{result['can']} {result['chi']}"

        )

        return context


    # =====================================================
    # FIND MONTH GANZHI
    # =====================================================

    def find_month_ganzhi(

        self,

        year_can,

        month_commander,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "MONTH_GANZHI")

            &

            (mapping["year_can"] == year_can)

            &

            (mapping["month_commander"] == month_commander)

        ]

        if result.empty:

            raise ValueError(

                f"Month Ganzhi not found : "

                f"{year_can} - {month_commander}"

            )

        return result.iloc[0]


    # =====================================================
    # GET MONTH CAN
    # =====================================================

    def get_month_can(self, context):

        return context["month_can"]


    # =====================================================
    # GET MONTH CHI
    # =====================================================

    def get_month_chi(self, context):

        return context["month_chi"]


    # =====================================================
    # GET MONTH GANZHI
    # =====================================================

    def get_month_ganzhi(self, context):

        return context["month_ganzhi"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "GanzhiMonthProcessor",

            "version": "1.0",

            "status": "READY"

        }
