"""
Interpretation Builder
======================

Module xây dựng cấu trúc luận giải từ kết quả Rule Engine.

Luồng:

Rule Matcher
      ↓
Rule Scoring
      ↓
Priority Resolver
      ↓
Interpretation Builder
      ↓
Sentence Generator
      ↓
Report Engine


Lưu ý:
- Không chứa kiến thức Bát Tự.
- Không tự luận đoán.
- Không chứa điều kiện Ngũ Hành.
- Chỉ xử lý dữ liệu rule đã được tính toán.
"""


from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


# =====================================================
# CONSTANT
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
# DATA MODEL
# =====================================================


@dataclass
class InterpretationSection:
    """
    Một nhóm luận giải.
    """

    name: str

    rules: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contents: List[str] = field(
        default_factory=list
    )

    score: float = 0



@dataclass
class InterpretationResult:
    """
    Kết quả cuối của Builder.
    """

    summary: str = ""

    sections: Dict[str, InterpretationSection] = field(
        default_factory=dict
    )

    rules_used: List[str] = field(
        default_factory=list
    )

    confidence: float = 0



# =====================================================
# BUILDER CLASS
# =====================================================


class InterpretationBuilder:


    def __init__(self):

        self.sections = (
            INTERPRETATION_SECTIONS
        )


    # -------------------------------------------------
    # MAIN BUILD FUNCTION
    # -------------------------------------------------

    def build(
        self,
        matched_rules: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> InterpretationResult:
        """
        Xây dựng kết quả luận giải.

        Input:
            matched_rules:
                danh sách rule đã scoring

            context:
                thông tin lá số


        Output:
            InterpretationResult
        """


        grouped_rules = (
            self._group_rules(
                matched_rules
            )
        )


        sections = {}


        for section_name, rules in grouped_rules.items():

            sections[section_name] = (
                self.build_section(
                    section_name,
                    rules
                )
            )


        summary = (
            self.create_summary(
                sections
            )
        )


        rules_used = [

            rule.get(
                "rule_id"
            )

            for rule in matched_rules

        ]


        confidence = (
            self.calculate_confidence(
                matched_rules
            )
        )


        return InterpretationResult(

            summary=summary,

            sections=sections,

            rules_used=rules_used,

            confidence=confidence

        )


    # -------------------------------------------------
    # GROUP RULE
    # -------------------------------------------------

    def _group_rules(
        self,
        rules: List[Dict[str, Any]]
    ) -> Dict[str, List]:

        grouped = {}


        for rule in rules:

            section = rule.get(
                "section",
                "tong_quan"
            )


            if section not in grouped:

                grouped[section] = []


            grouped[section].append(
                rule
            )


        return grouped



    # -------------------------------------------------
    # BUILD SECTION
    # -------------------------------------------------

    def build_section(
        self,
        section_name: str,
        rules: List[Dict[str, Any]]
    ) -> InterpretationSection:
        """
        Tạo một nhóm luận giải.
        """

        section = InterpretationSection(

            name=section_name,

            rules=rules

        )


        total_score = 0


        for rule in rules:

            score = rule.get(
                "score",
                0
            )


            total_score += score


        section.score = total_score


        return section



    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    def create_summary(
        self,
        sections: Dict[str, InterpretationSection]
    ) -> str:
        """
        Tạo phần tổng quan.

        Chưa sinh câu chữ.
        Sentence Generator đảm nhiệm.
        """

        active_sections = [

            name

            for name, section in sections.items()

            if section.score > 0

        ]


        return (
            "Các nhóm luận giải được kích hoạt: "
            +
            ", ".join(active_sections)
        )



    # -------------------------------------------------
    # CONFIDENCE
    # -------------------------------------------------

    def calculate_confidence(
        self,
        rules: List[Dict[str, Any]]
    ) -> float:


        if not rules:

            return 0



        scores = [

            rule.get(
                "score",
                0
            )

            for rule in rules

        ]


        avg = sum(scores) / len(scores)


        return round(
            avg / 100,
            2
        )



# =====================================================
# SERVICE FUNCTION
# =====================================================


def build_interpretation(
    matched_rules: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None
):

    builder = InterpretationBuilder()


    return builder.build(
        matched_rules,
        context
    )
