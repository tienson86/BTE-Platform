"""
=========================================================
BTE PLATFORM
Calendar Engine

File:
    timezone_processor.py

Version:
    1.0

Author:
    BTE Platform

Description:
    Normalize timezone information.

=========================================================
"""

from datetime import timedelta


class TimezoneProcessor:
    """
    Timezone Processor

    Chức năng:

    - Đọc timezone từ input
    - Tra cứu bảng timezone
    - Chuẩn hóa UTC Offset
    - Đưa kết quả vào Context
    """

    def execute(self, context):

        input_data = context["input"]

        timezone_table = context["timezone"]

        timezone_name = input_data["timezone"]

        timezone = self.find_timezone(
            timezone_name,
            timezone_table
        )

        context["timezone_name"] = timezone["timezone_name"]

        context["utc_offset"] = timezone["utc_offset"]

        context["dst_supported"] = timezone["dst_supported"]

        context["dst_offset"] = timezone["dst_offset"]

        context["timezone_delta"] = timedelta(
            hours=timezone["utc_offset"]
        )

        return context


    # =====================================================

    # FIND TIMEZONE

    # =====================================================

    def find_timezone(
        self,
        timezone_name,
        timezone_table
    ):

        result = timezone_table[

            timezone_table["timezone_name"] == timezone_name

        ]

        if result.empty:

            raise ValueError(

                f"Timezone not found : {timezone_name}"

            )

        return result.iloc[0]


    # =====================================================

    # GET UTC OFFSET

    # =====================================================

    def get_utc_offset(self, context):

        return context["utc_offset"]


    # =====================================================

    # GET TIMEZONE NAME

    # =====================================================

    def get_timezone_name(self, context):

        return context["timezone_name"]
