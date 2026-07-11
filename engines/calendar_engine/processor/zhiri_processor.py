"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    zhiri_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Trực Nhật

=========================================================
"""


class ZhiRiProcessor:
    """
    Trực Nhật Processor
    """

    def execute(self, context):

        day_chi = context["day_chi"]

        month_commander = context["month_commander"]

        mapping = context["mapping"]

        result = self.find_day_officer(

            month_commander,

            day_chi,

            mapping

        )

        context["day_officer"] = result["day_officer"]

        context["day_officer_code"] = result["day_officer_code"]

        return context


    # =====================================================
    # FIND DAY OFFICER
    # =====================================================

    def find_day_officer(

        self,

        month_commander,

        day_chi,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "DAY_OFFICER")

            &

            (mapping["month_commander"] == month_commander)

            &

            (mapping["day_chi"] == day_chi)

        ]

        if result.empty:

            raise ValueError(

                f"Day Officer not found : "

                f"{month_commander} - {day_chi}"

            )

        return result.iloc[0]


    # =====================================================
    # GET DAY OFFICER
    # =====================================================

    def get_day_officer(self, context):

        return context["day_officer"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "ZhiRiProcessor",

            "version": "1.0",

            "status": "READY"

        }
