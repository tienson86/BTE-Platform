"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    ganzhi.py

Version:
    1.0

Description:
    Heavenly Stem Earthly Branch Algorithm

=========================================================
"""


class GanzhiAlgorithm:

    STEM = [

        "Giáp",
        "Ất",
        "Bính",
        "Đinh",
        "Mậu",

        "Kỷ",
        "Canh",
        "Tân",
        "Nhâm",
        "Quý"

    ]


    BRANCH = [

        "Tý",
        "Sửu",
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",

        "Ngọ",
        "Mùi",
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi"

    ]


    @staticmethod
    def year(year):

        stem = (year + 6) % 10

        branch = (year + 8) % 12

        return {

            "can": GanzhiAlgorithm.STEM[stem],

            "chi": GanzhiAlgorithm.BRANCH[branch]

        }


    @staticmethod
    def day(jdn):

        stem = int(jdn + 9) % 10

        branch = int(jdn + 1) % 12

        return {

            "can": GanzhiAlgorithm.STEM[stem],

            "chi": GanzhiAlgorithm.BRANCH[branch]

        }


    @staticmethod
    def month(

        year_can_index,

        month_commander_index

    ):

        stem = (

            year_can_index * 2

            + month_commander_index

        ) % 10

        branch = (

            month_commander_index + 2

        ) % 12

        return {

            "can": GanzhiAlgorithm.STEM[stem],

            "chi": GanzhiAlgorithm.BRANCH[branch]

        }
