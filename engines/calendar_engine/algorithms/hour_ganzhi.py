"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    hour_ganzhi.py

Version:
    1.0

Description:
    Heavenly Stem Earthly Branch of Hour

=========================================================
"""


from algorithms.ganzhi import GanzhiAlgorithm


class HourGanzhiAlgorithm:


    HOUR_BRANCH = [

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
    def hour_branch(hour):

        if hour >= 23 or hour < 1:
            return 0

        return ((hour + 1) // 2) % 12


    @staticmethod
    def calculate(

        day_can_index,

        hour

    ):

        branch = HourGanzhiAlgorithm.hour_branch(hour)

        stem = (

            day_can_index * 2

            + branch

        ) % 10

        return {

            "can":

                GanzhiAlgorithm.STEM[stem],

            "chi":

                GanzhiAlgorithm.BRANCH[branch]

        }
