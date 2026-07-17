"""
Rule Loader
===========

Nạp dữ liệu Rule Database cho Interpretation Engine.

Flow:

Rule Database
      ↓
Rule Loader
      ↓
Rule Matcher
      ↓
Rule Scoring
      ↓
Interpretation Builder


Chức năng:

- Đọc dữ liệu rule.
- Chuẩn hóa rule.
- Lọc rule theo module.
- Cache dữ liệu rule.

Không chứa:
- Logic luận giải.
- Điều kiện Bát Tự.
- Chấm điểm.
"""


import os

import csv

import json

from typing import List, Dict, Any, Optional





# =====================================================
# CONSTANT
# =====================================================


SUPPORTED_FORMAT = [

    "csv",

    "json"

]





# =====================================================
# CLASS
# =====================================================


class RuleLoader:



    def __init__(
        self,
        rule_path: Optional[str] = None
    ):


        self.rule_path = rule_path


        self.cache = []





    # =================================================
    # MAIN LOAD
    # =================================================


    def load(
        self,
        path=None
    ) -> List[Dict[str, Any]]:


        file_path = path or self.rule_path



        if not file_path:


            return []



        if self.cache:


            return self.cache




        extension = (

            os.path.splitext(

                file_path

            )[1]

            .replace(
                ".",
                ""
            )

            .lower()

        )



        if extension == "csv":


            rules = self.load_csv(

                file_path

            )



        elif extension == "json":


            rules = self.load_json(

                file_path

            )



        else:


            raise ValueError(

                "Unsupported rule format"

            )



        self.cache = self.normalize_rules(

            rules

        )



        return self.cache





    # =================================================
    # LOAD CSV
    # =================================================


    def load_csv(
        self,
        file_path
    ):


        rules = []



        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:



            reader = csv.DictReader(
                file
            )



            for row in reader:


                rules.append(

                    dict(row)

                )



        return rules





    # =================================================
    # LOAD JSON
    # =================================================


    def load_json(
        self,
        file_path
    ):


        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)





    # =================================================
    # NORMALIZE
    # =================================================


    def normalize_rules(
        self,
        rules
    ):


        result = []



        for rule in rules:


            item = {



                "rule_id":

                    rule.get(

                        "rule_id",

                        ""

                    ),



                "rule_name":

                    rule.get(

                        "rule_name",

                        ""

                    ),



                "category":

                    rule.get(

                        "category",

                        ""

                    ),



                "layer":

                    rule.get(

                        "layer",

                        "mac_dinh"

                    ),



                "section":

                    rule.get(

                        "section",

                        "tong_quan"

                    ),



                "condition":

                    rule.get(

                        "condition",

                        {}

                    ),



                "description":

                    rule.get(

                        "description",

                        ""

                    ),



                "polarity":

                    rule.get(

                        "polarity",

                        "neutral"

                    ),



                "priority":

                    self.convert_number(

                        rule.get(

                            "priority",

                            99

                        )

                    ),



                "score":

                    self.convert_number(

                        rule.get(

                            "score",

                            0

                        )

                    )

            }



            result.append(
                item
            )



        return result





    # =================================================
    # FILTER
    # =================================================


    def filter_by_category(
        self,
        rules,
        category
    ):


        return [

            r

            for r in rules

            if r.get(

                "category"

            ) == category

        ]





    def filter_by_layer(
        self,
        rules,
        layer
    ):


        return [

            r

            for r in rules

            if r.get(

                "layer"

            ) == layer

        ]





    # =================================================
    # CLEAR CACHE
    # =================================================


    def clear_cache(
        self
    ):


        self.cache = []





    # =================================================
    # NUMBER CONVERT
    # =================================================


    def convert_number(
        self,
        value
    ):


        try:

            return int(value)


        except:


            try:

                return float(value)


            except:


                return 0





# =====================================================
# SERVICE FUNCTION
# =====================================================


def load_rules(
    rule_path
):


    loader = RuleLoader(

        rule_path

    )


    return loader.load()
