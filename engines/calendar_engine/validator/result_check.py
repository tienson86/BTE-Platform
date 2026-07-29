"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    result_validator.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Validate Calendar Engine Result

=========================================================
"""


class ResultValidator:
    """
    Kiểm tra kết quả sau khi Calendar Engine xử lý.
    """

    REQUIRED_FIELDS = [

        "julian_day",

        "lunar_day",
        "lunar_month",
        "lunar_year",

        "year_can",
        "year_chi",

        "month_can",
        "month_chi",

        "day_can",
        "day_chi",

        "hour_can",
        "hour_chi"

    ]


    # =====================================================

    # MAIN

    # =====================================================

    def execute(self, context):

        self.validate_required(context)

        self.validate_calendar(context)

        self.validate_ganzhi(context)

        self.validate_julian(context)

        context["result_checked"] = True

        return context


    # =====================================================

    # REQUIRED

    # =====================================================

    def validate_required(self, context):

        for field in self.REQUIRED_FIELDS:

            if field not in context:

                raise ValueError(

                    f"Missing result field : {field}"

                )


    # =====================================================

    # CALENDAR

    # =====================================================

    def validate_calendar(self, context):

        lunar_day = context["lunar_day"]

        lunar_month = context["lunar_month"]

        lunar_year = context["lunar_year"]


        if lunar_day < 1 or lunar_day > 30:

            raise ValueError(

                "Invalid lunar day."

            )


        if lunar_month < 1 or lunar_month > 12:

            raise ValueError(

                "Invalid lunar month."

            )


        if lunar_year < 1900 or lunar_year > 2100:

            raise ValueError(

                "Invalid lunar year."

            )


    # =====================================================

    # GANZHI

    # =====================================================

    def validate_ganzhi(self, context):

        ganzhi_fields = [

            "year_can",
            "year_chi",

            "month_can",
            "month_chi",

            "day_can",
            "day_chi",

            "hour_can",
            "hour_chi"

        ]


        for field in ganzhi_fields:

            value = context[field]

            if value is None:

                raise ValueError(

                    f"{field} is None"

                )


            if str(value).strip() == "":

                raise ValueError(

                    f"{field} is empty"

                )


    # =====================================================

    # JULIAN DAY

    # =====================================================

    def validate_julian(self, context):

        julian = context["julian_day"]

        if julian <= 0:

            raise ValueError(

                "Invalid Julian Day."

            )


    # =====================================================

    # OPTIONAL CHECK

    # =====================================================

    def validate_optional(self, context):

        optional_fields = [

            "jieqi",

            "nap_am",

            "huang_dao",

            "day_officer"

        ]


        for field in optional_fields:

            if field not in context:

                context[field] = None


    # =====================================================

    # SUMMARY

    # =====================================================

    def summary(self):

        return {

            "validator": "ResultValidator",

            "version": "1.0",

            "status": "READY"

        }
