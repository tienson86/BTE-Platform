"""
Interpretation Builder
======================

Part 3

Chức năng:

- Nhận kết quả Rule Engine
- Chuẩn hóa Rule
- Tính trọng số
- Sắp xếp ưu tiên
- Gộp Rule
- Phân tích xung đột
- Tạo cấu trúc luận giải


Flow:

Rule Engine
      ↓
Interpretation Builder
      ↓
Sentence Generator
      ↓
Report Engine
"""


from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional




# =====================================================
# SECTION DATABASE
# =====================================================


INTERPRETATION_SECTIONS = [

    "tong_quan",

    "nguyen_cuc",

    "dung_than",

    "hy_than_ky_than",

    "tinh_cach",

    "suc_khoe",

    "tai_van",

    "su_nghiep",

    "hon_nhan",

    "tu_tuc",

    "dai_van",

    "luu_nien",

]




# =====================================================
# RULE WEIGHT DATABASE
# =====================================================


RULE_LAYER_WEIGHT = {


    "cach_cuc": 1.50,

    "dung_than": 1.45,

    "hy_than_ky_than": 1.35,


    "dai_van": 1.30,

    "luu_nien": 1.25,


    "su_nghiep": 1.15,

    "tai_van": 1.15,

    "hon_nhan": 1.10,

    "tu_tuc": 1.10,


    "suc_khoe": 1.05,


    "than_sat": 0.90,


    "mac_dinh": 1.00

}





RULE_DEFAULT_STRUCTURE = {


    "rule_id": "",

    "rule_name": "",

    "category": "",

    "layer": "mac_dinh",

    "section": "tong_quan",

    "score": 0,

    "polarity": "neutral",

    "description": "",

    "priority": 99

}





# =====================================================
# DATA MODEL
# =====================================================


@dataclass
class InterpretationSection:


    name: str


    rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    positive_rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    negative_rules: List[Dict[str, Any]] = field(
        default_factory=list
    )


    warnings: List[Dict[str, Any]] = field(
        default_factory=list
    )


    score: float = 0




@dataclass
class InterpretationResult:


    summary: str = ""


    sections: Dict[str, InterpretationSection] = field(
        default_factory=dict
    )


    rules_used: List[str] = field(
        default_factory=list
    )


    strengths: List[Dict] = field(
        default_factory=list
    )


    weaknesses: List[Dict] = field(
        default_factory=list
    )


    warnings: List[Dict] = field(
        default_factory=list
    )


    confidence: float = 0





# =====================================================
# BUILDER
# =====================================================


class InterpretationBuilder:



    def __init__(self):

        self.sections = INTERPRETATION_SECTIONS




    # =================================================
    # MAIN BUILD
    # =================================================


    def build(
        self,
        matched_rules,
        context=None
    ):


        rules = [

            self.normalize_rule(rule)

            for rule in matched_rules

        ]



        rules = self.apply_rule_weight(
            rules
        )



        rules = self.priority_sort(
            rules
        )



        conflict_result = self.resolve_conflict(
            rules
        )



        grouped = self.group_rules(
            conflict_result["rules"]
        )



        sections = {}



        for name, items in grouped.items():


            sections[name] = self.build_section(

                name,

                items

            )



        return InterpretationResult(


            summary=self.create_summary(
                sections
            ),


            sections=sections,


            rules_used=[

                r.get("rule_id")

                for r in rules

            ],


            strengths=conflict_result["positive"],


            weaknesses=conflict_result["negative"],


            warnings=conflict_result["warnings"],


            confidence=self.calculate_confidence(
                rules
            )

        )




    # =================================================
    # NORMALIZE
    # =================================================


    def normalize_rule(
        self,
        rule
    ):


        data = RULE_DEFAULT_STRUCTURE.copy()

        data.update(rule)

        return data




    # =================================================
    # WEIGHT
    # =================================================


    def apply_rule_weight(
        self,
        rules
    ):


        result=[]



        for rule in rules:


            weight = RULE_LAYER_WEIGHT.get(

                rule.get(

                    "layer",

                    "mac_dinh"

                ),

                1

            )



            new = rule.copy()



            new["layer_weight"] = weight


            new["final_score"] = (

                new["score"]

                *

                weight

            )



            result.append(new)



        return result




    # =================================================
    # SORT
    # =================================================


    def priority_sort(
        self,
        rules
    ):


        return sorted(

            rules,

            key=lambda x:

            x.get(

                "final_score",

                0

            ),

            reverse=True

        )




    # =================================================
    # CONFLICT RESOLVER
    # =================================================


    def resolve_conflict(
        self,
        rules
    ):


        positive=[]

        negative=[]

        warnings=[]



        for rule in rules:


            if rule.get(
                "polarity"
            ) == "positive":


                positive.append(rule)



            elif rule.get(
                "polarity"
            ) == "negative":


                negative.append(rule)



            else:

                warnings.append(rule)




        # Rule cùng section trái chiều

        section_map={}



        for rule in rules:


            sec = rule.get(
                "section"
            )


            section_map.setdefault(
                sec,
                []
            ).append(rule)



        for sec, items in section_map.items():


            has_good = any(

                x.get("polarity")=="positive"

                for x in items

            )


            has_bad = any(

                x.get("polarity")=="negative"

                for x in items

            )


            if has_good and has_bad:


                warnings.append({

                    "section":sec,

                    "type":
                    "conflict",

                    "message":
                    "Co ca yeu to thuan loi va bat loi"

                })



        return {


            "rules": rules,


            "positive": positive,


            "negative": negative,


            "warnings": warnings

        }




    # =================================================
    # GROUP
    # =================================================


    def group_rules(
        self,
        rules
    ):


        grouped={}



        for rule in rules:


            section = rule.get(

                "section",

                "tong_quan"

            )


            grouped.setdefault(

                section,

                []

            ).append(rule)



        return grouped




    # =================================================
    # BUILD SECTION
    # =================================================


    def build_section(
        self,
        name,
        rules
    ):


        section = InterpretationSection(

            name=name,

            rules=rules

        )


        for rule in rules:


            if rule.get(
                "polarity"
            )=="positive":

                section.positive_rules.append(rule)


            elif rule.get(
                "polarity"
            )=="negative":

                section.negative_rules.append(rule)



        section.score=sum(

            r.get(

                "final_score",

                0

            )

            for r in rules

        )



        return section




    # =================================================
    # SUMMARY
    # =================================================


    def create_summary(
        self,
        sections
    ):


        names=list(
            sections.keys()
        )


        return (

            "Da kich hoat cac nhom luan giai: "

            +

            ", ".join(names)

        )




    # =================================================
    # CONFIDENCE
    # =================================================


    def calculate_confidence(
        self,
        rules
    ):


        if not rules:

            return 0



        avg = sum(

            r.get(

                "final_score",

                0

            )

            for r in rules

        ) / len(rules)



        return round(

            min(avg/100,1),

            2

        )





# =====================================================
# SERVICE
# =====================================================


def build_interpretation(

    matched_rules,

    context=None

):


    builder = InterpretationBuilder()


    return builder.build(

        matched_rules,

        context

    )
