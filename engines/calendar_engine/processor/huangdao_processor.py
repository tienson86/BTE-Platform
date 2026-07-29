"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    huangdao_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Hoàng Đạo / Hắc Đạo

=========================================================
"""


class HuangDaoProcessor:
    """
    Hoàng Đạo Processor
    """

    def execute(self, context):

        day_chi = context["day_chi"]

        month_commander = context["month_commander"]

        mapping = context["mapping"]

        result = self.find_huangdao(

            month_commander,

            day_chi,

            mapping

        )

        context["huang_dao"] = result["huang_dao"]

        context["huangdao_type"] = result["huangdao_type"]

        context["huangdao_star"] = result["huangdao_star"]

        return context


    # =====================================================
    # FIND HUANG DAO
    # =====================================================

    def find_huangdao(

        self,

        month_commander,

        day_chi,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "HUANGDAO")

            &

            (mapping["month_commander"] == month_commander)

            &

            (mapping["day_chi"] == day_chi)

        ]

        if result.empty:

            raise ValueError(

                f"Huang Dao not found : "

                f"{month_commander} - {day_chi}"

            )

        return result.iloc[0]


    # =====================================================
    # GET HUANG DAO
    # =====================================================

    def get_huang_dao(self, context):

        return context["huang_dao"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "HuangDaoProcessor",

            "version": "1.0",

            "status": "READY"

        }
