"""
Rule Matcher
============

Kiểm tra điều kiện Rule với dữ liệu lá số.

Flow:

Context
    ↓
Rule Database
    ↓
Rule Matcher
    ↓
Matched Rules
    ↓
Rule Scoring


Chức năng:

- Đọc điều kiện của Rule.
- So sánh với Context.
- Trả về Rule được kích hoạt.

Không chứa:
- Chấm điểm.
- Sinh câu luận giải.
- Kiến thức Bát Tự trực tiếp.
"""


from typing import Dict, List, Any





# =====================================================
# OPERATOR DATABASE
# =====================================================


SUPPORTED_OPERATORS = [

    "eq",

    "neq",

    "in",

    "not_in",

    "contains",

    "exists",

    "gt",

    "lt"

]





# =====================================================
# CLASS
# =====================================================


class RuleMatcher:



    def __init__(self):

        pass




    # =================================================
    # MAIN MATCH
    # =================================================


    def match(
        self,
        context: Dict[str, Any],
        rules: List[Dict[str, Any]]
    ):


        matched = []



        for rule in rules:


            condition = rule.get(

                "condition",

                {}

            )



            if self.check_condition(

                context,

                condition

            ):


                matched_rule = rule.copy()



                matched_rule["matched"] = True



                matched.append(

                    matched_rule

                )



        return matched





    # =================================================
    # CHECK CONDITION
    # =================================================


    def check_condition(
        self,
        context,
        condition
    ):


        if not condition:


            return False



        for key, requirement in condition.items():


            value = self.get_context_value(

                context,

                key

            )



            if not self.compare(

                value,

                requirement

            ):


                return False



        return True





    # =================================================
    # GET VALUE
    # =================================================


    def get_context_value(
        self,
        context,
        key
    ):


        parts = key.split(".")

        value = context



        for part in parts:


            if isinstance(

                value,

                dict

            ):


                value = value.get(

                    part

                )



            else:


                return None



        return value





    # =================================================
    # COMPARE
    # =================================================


    def compare(
        self,
        value,
        requirement
    ):


        if isinstance(
            requirement,
            dict
        ):


            operator = requirement.get(

                "operator",

                "eq"

            )


            target = requirement.get(

                "value"

            )


            return self.compare_operator(

                value,

                operator,

                target

            )



        else:


            return value == requirement





    # =================================================
    # OPERATOR PROCESS
    # =================================================


    def compare_operator(
        self,
        value,
        operator,
        target
    ):



        if operator == "eq":


            return value == target




        elif operator == "neq":


            return value != target




        elif operator == "in":


            if isinstance(

                target,

                list

            ):


                return value in target



            return False





        elif operator == "not_in":


            if isinstance(

                target,

                list

            ):


                return value not in target



            return False





        elif operator == "contains":


            if isinstance(

                value,

                list

            ):


                return target in value



            if isinstance(

                value,

                str

            ):


                return target in value



            return False





        elif operator == "exists":


            return value is not None




        elif operator == "gt":


            return value > target




        elif operator == "lt":


            return value < target





        return False





    # =================================================
    # DEBUG MATCH
    # =================================================


    def explain_match(
        self,
        context,
        rule
    ):


        condition = rule.get(

            "condition",

            {}

        )


        result = {}



        for key, requirement in condition.items():


            value = self.get_context_value(

                context,

                key

            )


            result[key] = {


                "actual": value,


                "required": requirement,


                "matched":

                    self.compare(

                        value,

                        requirement

                    )

            }



        return result





# =====================================================
# SERVICE FUNCTION
# =====================================================


def match_rules(

    context,

    rules

):


    matcher = RuleMatcher()



    return matcher.match(

        context,

        rules

    )
