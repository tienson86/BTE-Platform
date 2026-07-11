"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    jieqi.py

Version:
    1.0

Description:
    Calculate 24 Solar Terms

=========================================================
"""

from algorithms.solar_longitude import SolarLongitude


class JieQiAlgorithm:
    """
    Thuật toán xác định Tiết Khí.
    """

    JIEQI = [

        "Xuân Phân",
        "Thanh Minh",
        "Cốc Vũ",
        "Lập Hạ",
        "Tiểu Mãn",
        "Mang Chủng",

        "Hạ Chí",
        "Tiểu Thử",
        "Đại Thử",
        "Lập Thu",
        "Xử Thử",
        "Bạch Lộ",

        "Thu Phân",
        "Hàn Lộ",
        "Sương Giáng",
        "Lập Đông",
        "Tiểu Tuyết",
        "Đại Tuyết",

        "Đông Chí",
        "Tiểu Hàn",
        "Đại Hàn",
        "Lập Xuân",
        "Vũ Thủy",
        "Kinh Trập"

    ]


    MONTH_COMMANDER = [

        "Mão",
        "Thìn",
        "Thìn",
        "Tỵ",
        "Tỵ",
        "Ngọ",

        "Ngọ",
        "Mùi",
        "Mùi",
        "Thân",
        "Thân",
        "Dậu",

        "Dậu",
        "Tuất",
        "Tuất",
        "Hợi",
        "Hợi",
        "Tý",

        "Tý",
        "Sửu",
        "Sửu",
        "Dần",
        "Dần",
        "Mão"

    ]


    @staticmethod
    def calculate(jdn):

        longitude = SolarLongitude.calculate(jdn)

        index = SolarLongitude.get_term_index(longitude)

        return {

            "index": index,

            "solar_longitude": longitude,

            "jieqi": JieQiAlgorithm.JIEQI[index],

            "month_commander":

                JieQiAlgorithm.MONTH_COMMANDER[index]

        }
