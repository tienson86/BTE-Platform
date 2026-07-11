"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    ganzhi_hour_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Calculate Heavenly Stem and Earthly Branch of Hour

=========================================================
"""


class GanzhiHourProcessor:
    """
    Ganzhi Hour Processor

    Chức năng:

    - Xác định Can Chi giờ
    - Căn cứ theo Can ngày và giờ sinh
    - Tra Mapping
    - Ghi kết quả vào Context
    """

    def execute(self, context):

        day_can = context["day_can"]

        input_data = context["input"]

        mapping = context["mapping"]

        solar_time = input_data["solar_time"]

        hour_branch = self.find_hour_branch(solar_time)

        result = self.find_hour_ganzhi(

            day_can,

            hour_branch,

            mapping

        )

        context["hour_branch"] = hour_branch

        context["hour_can"] = result["can"]

        context["hour_chi"] = result["chi"]

        context["hour_ganzhi"] = (

            f"{result['can']} {result['chi']}"

        )

        return context


    # =====================================================
    # FIND HOUR BRANCH
    # =====================================================

    def find_hour_branch(self, solar_time):

        hour = int(solar_time.split(":")[0])

        if hour >= 23 or hour < 1:
            return "Tý"

        elif hour < 3:
            return "Sửu"

        elif hour < 5:
            return "Dần"

        elif hour < 7:
            return "Mão"

        elif hour < 9:
            return "Thìn"

        elif hour < 11:
            return "Tỵ"

        elif hour < 13:
            return "Ngọ"

        elif hour < 15:
            return "Mùi"

        elif hour < 17:
            return "Thân"

        elif hour < 19:
            return "Dậu"

        elif hour < 21:
            return "Tuất"

        else:
            return "Hợi"


    # =====================================================
    # FIND HOUR GANZHI
    # =====================================================

    def find_hour_ganzhi(

        self,

        day_can,

        hour_branch,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "HOUR_GANZHI")

            &

            (mapping["day_can"] == day_can)

            &

            (mapping["hour_branch"] == hour_branch)

        ]

        if result.empty:

            raise ValueError(

                f"Hour Ganzhi not found : "

                f"{day_can} - {hour_branch}"

            )

        return result.iloc[0]


    # =====================================================
    # GET HOUR CAN
    # =====================================================

    def get_hour_can(self, context):

        return context["hour_can"]


    # =====================================================
    # GET HOUR CHI
    # =====================================================

    def get_hour_chi(self, context):

        return context["hour_chi"]


    # =====================================================
    # GET HOUR GANZHI
    # =====================================================

    def get_hour_ganzhi(self, context):

        return context["hour_ganzhi"]


    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "processor": "GanzhiHourProcessor",

            "version": "1.0",

            "status": "READY"

        }
