"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    huangdao.py

Version:
    1.0

Description:
    Huang Dao Algorithm

=========================================================
"""


class HuangDaoAlgorithm:
    """
    Thuật toán xác định
    Hoàng Đạo / Hắc Đạo.
    """

    @staticmethod
    def calculate(

        month_commander,

        day_branch,

        mapping

    ):

        result = mapping[

            (mapping["mapping_type"] == "HUANGDAO")

            &

            (mapping["month_commander"] == month_commander)

            &

            (mapping["day_chi"] == day_branch)

        ]

        if result.empty:

            raise ValueError(

                f"Huang Dao not found : "

                f"{month_commander} - {day_branch}"

            )

        row = result.iloc[0]

        return {

            "name": row["huang_dao"],

            "type": row["huangdao_type"],

            "star": row["huangdao_star"],

            "description": row["description"]

        }


    @staticmethod
    def is_huangdao(result):

        return result["type"] == "HOANG_DAO"


    @staticmethod
    def is_hacdao(result):

        return result["type"] == "HAC_DAO"
