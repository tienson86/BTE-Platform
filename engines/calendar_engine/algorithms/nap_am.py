"""
=========================================================
BTE PLATFORM

Calendar Algorithm

File:
    nap_am.py

Version:
    1.0

Description:
    Nap Am Algorithm

=========================================================
"""


class NapAmAlgorithm:
    """
    Thuật toán tra cứu Nạp Âm.
    """

    @staticmethod
    def calculate(can, chi, mapping):

        result = mapping[

            (mapping["mapping_type"] == "NAP_AM")

            &

            (mapping["can"] == can)

            &

            (mapping["chi"] == chi)

        ]

        if result.empty:

            raise ValueError(

                f"Nap Am not found : {can} {chi}"

            )

        row = result.iloc[0]

        return {

            "code": row["nap_am_code"],

            "name": row["nap_am"],

            "element": row["ngu_hanh"]

        }


    @staticmethod
    def get_name(result):

        return result["name"]


    @staticmethod
    def get_element(result):

        return result["element"]
