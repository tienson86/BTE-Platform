"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    zhiri.py

Version:
    1.0

Description:
    Day Officer Algorithm

=========================================================
"""


class ZhiRiAlgorithm:
    """
    Thuật toán xác định Trực Nhật.
    """

    @staticmethod
    def calculate(

        month_commander,

        day_branch,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "DAY_OFFICER")

            &

            (mapping["month_commander"] == month_commander)

            &

            (mapping["day_chi"] == day_branch)

        ]

        if result.empty:

            raise ValueError(

                f"Day Officer not found : "

                f"{month_commander} - {day_branch}"

            )

        row = result.iloc[0]

        return {

            "code": row["day_officer_code"],

            "name": row["day_officer"],

            "description": row["description"]

        }


    @staticmethod
    def is_good(result):

        return result["name"] in [

            "Kiến",

            "Mãn",

            "Thành",

            "Khai"

        ]


    @staticmethod
    def is_bad(result):

        return result["name"] in [

            "Phá",

            "Nguy",

            "Bế"

        ]
