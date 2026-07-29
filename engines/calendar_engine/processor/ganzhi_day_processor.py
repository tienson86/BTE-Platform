"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    ganzhi_day_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Heavenly Stem and Earthly Branch of Day

=========================================================
"""


class GanzhiDayProcessor:
    """
    Ganzhi Day Processor

    Chức năng:

    - Xác định Can Chi ngày
    - Căn cứ theo Julian Day Number
    - Tra Mapping
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        julian_day = context["julian_day"]

        mapping = context["mapping"]

        result = self.find_day_ganzhi(

            julian_day,

            mapping

        )

        context["day_can"] = result["can"]

        context["day_chi"] = result["chi"]

        context["day_ganzhi"] = (

            f"{result['can']} {result['chi']}"

        )

        return context


    # =====================================================
    # FIND DAY GANZHI
    # =====================================================

    def find_day_ganzhi(

        self,

        julian_day,

        mapping

    ):

        """
        Tra cứu Can Chi ngày.

        Phiên bản 1.0:
        Tra bảng Mapping hoặc bảng Day Cycle.
        """

        result = mapping[

            (mapping["mapping_type"] == "DAY_GANZHI")

            &

            (mapping["julian_day"] == int(julian_day))

        ]

        if result.empty:

            raise ValueError(

                f"Day Ganzhi not found : {julian_day}"

            )

        return result.iloc[0]


    # =====================================================
    # GET DAY CAN
    # =====================================================

    def get_day_can(self, context):

        return context["day_can"]


    # =====================================================
    # GET DAY CHI
    # =====================================================

    def get_day_chi(self, context):

        return context["day_chi"]


    # =====================================================
    # GET DAY GANZHI
    # =====================================================

    def get_day_ganzhi(self, context):

        return context["day_ganzhi"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "GanzhiDayProcessor",

            "version": "1.0",

            "status": "READY"

        }
