"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    nap_am_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Nap Am

=========================================================
"""


class NapAmProcessor:
    """
    Nap Âm Processor

    Chức năng:

    - Xác định Nạp Âm của trụ năm
    - Tra Mapping
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        year_can = context["year_can"]

        year_chi = context["year_chi"]

        mapping = context["mapping"]

        result = self.find_nap_am(

            year_can,

            year_chi,

            mapping

        )

        context["nap_am"] = result["nap_am"]

        context["nap_am_code"] = result["nap_am_code"]

        return context


    # =====================================================
    # FIND NAP AM
    # =====================================================

    def find_nap_am(

        self,

        year_can,

        year_chi,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "NAP_AM")

            &

            (mapping["can"] == year_can)

            &

            (mapping["chi"] == year_chi)

        ]

        if result.empty:

            raise ValueError(

                f"Nap Am not found : "

                f"{year_can} {year_chi}"

            )

        return result.iloc[0]


    # =====================================================
    # GET NAP AM
    # =====================================================

    def get_nap_am(self, context):

        return context["nap_am"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "NapAmProcessor",

            "version": "1.0",

            "status": "READY"

        }
