"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    ganzhi_year_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Heavenly Stem and Earthly Branch of Year

=========================================================
"""


class GanzhiYearProcessor:
    """
    Ganzhi Year Processor

    Chức năng:

    - Xác định Can Chi năm
    - Tra bảng Mapping
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        lunar_year = context["lunar_year"]

        mapping = context["mapping"]

        result = self.find_year_ganzhi(

            lunar_year,

            mapping

        )

        context["year_can"] = result["can"]

        context["year_chi"] = result["chi"]

        context["year_ganzhi"] = (

            f"{result['can']} {result['chi']}"

        )

        return context


    # =====================================================
    # FIND YEAR GANZHI
    # =====================================================

    def find_year_ganzhi(

        self,

        lunar_year,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "YEAR_GANZHI")

            &

            (mapping["year"] == lunar_year)

        ]

        if result.empty:

            raise ValueError(

                f"Year Ganzhi not found : {lunar_year}"

            )

        return result.iloc[0]


    # =====================================================
    # GET YEAR CAN
    # =====================================================

    def get_year_can(self, context):

        return context["year_can"]


    # =====================================================
    # GET YEAR CHI
    # =====================================================

    def get_year_chi(self, context):

        return context["year_chi"]


    # =====================================================
    # GET YEAR GANZHI
    # =====================================================

    def get_year_ganzhi(self, context):

        return context["year_ganzhi"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "GanzhiYearProcessor",

            "version": "1.0",

            "status": "READY"

        }
