"""
Rule Scoring
============

Chấm điểm Rule sau khi đã được Rule Matcher kích hoạt.

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

- Tính điểm Rule.
- Điều chỉnh điểm theo mức ảnh hưởng.
- Phân loại mức độ.
- Chuẩn hóa kết quả.

Không chứa:
- Điều kiện Bát Tự.
- Sinh câu luận giải.
"""



from typing import List, Dict, Any





# =====================================================
# SCORE CONFIG
# =====================================================


SCORE_LEVEL = {


    "very_high": 90,


    "high": 75,


    "medium": 50,


    "low": 25,


    "very_low": 0

}





# =====================================================
# SCORE WEIGHT
# =====================================================


CATEGORY_WEIGHT = {


    "cach_cuc": 1.5,


    "dung_than": 1.45,


    "hy_than_ky_than": 1.35,


    "dai_van": 1.30,


    "luu_nien": 1.25,


    "su_nghiep": 1.15,


    "tai_van": 1.15,


    "hon_nhan": 1.10,


    "suc_khoe": 1.05,


    "than_sat": 0.90,


    "default": 1.00

}






# =====================================================
# CLASS
# =====================================================


class RuleScoring:




    def __init__(self):

        self.category_weight = CATEGORY_WEIGHT





    # =================================================
    # MAIN SCORE
    # =================================================


    def score(
        self,
        rules: List[Dict[str,Any]],
        context=None
    ):
        return self.calculate_total(
            self.score_rules(
                rules,
                context
            )
        )


    def score_rules(
        self,
        rules: List[Dict[str,Any]],
        context=None
    ):


        result = []



        for rule in rules:


            scored_rule = self.score_rule(

                rule,

                context

            )


            result.append(

                scored_rule

            )



        return result






    # =================================================
    # SCORE SINGLE RULE
    # =================================================


    def score_rule(
        self,
        rule,
        context=None
    ):



        new_rule = rule.copy()



        base_score = self.get_base_score(

            rule

        )



        category = rule.get(

            "layer",

            rule.get(

                "category",

                "default"

            )

        )



        weight = self.category_weight.get(

            category,

            self.category_weight["default"]

        )



        final_score = (

            base_score

            *

            weight

        )



        polarity = rule.get(

            "polarity",

            "neutral"

        )



        if polarity == "negative":


            final_score = final_score * (-1)





        new_rule["base_score"] = base_score



        new_rule["weight"] = weight



        new_rule["score"] = round(

            final_score,

            2

        )



        new_rule["level"] = self.get_score_level(

            abs(final_score)

        )



        return new_rule






    # =================================================
    # BASE SCORE
    # =================================================


    def get_base_score(
        self,
        rule
    ):


        score = rule.get(

            "score",

            0

        )



        try:


            return float(score)



        except:


            return 0






    # =================================================
    # SCORE LEVEL
    # =================================================


    def get_score_level(
        self,
        score
    ):



        if score >= 90:


            return "very_high"



        elif score >= 75:


            return "high"



        elif score >= 50:


            return "medium"



        elif score >= 25:


            return "low"



        else:


            return "very_low"







    # =================================================
    # TOTAL SCORE
    # =================================================


    def calculate_total(
        self,
        rules
    ):


        total = 0



        for rule in rules:


            total += rule.get(

                "score",

                0

            )



        return round(

            total,

            2

        )






    # =================================================
    # FILTER SCORE
    # =================================================


    def filter_positive(
        self,
        rules
    ):


        return [

            r

            for r in rules

            if r.get(

                "score",

                0

            ) > 0

        ]





    def filter_negative(
        self,
        rules
    ):


        return [

            r

            for r in rules

            if r.get(

                "score",

                0

            ) < 0

        ]






# =====================================================
# SERVICE FUNCTION
# =====================================================


def score_rules(
    rules,
    context=None
):


    scorer = RuleScoring()



    return scorer.score_rules(

        rules,

        context

    )
