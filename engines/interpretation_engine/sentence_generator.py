"""
Sentence Generator
==================

Sinh câu luận giải từ Interpretation Result.

Flow:

Interpretation Builder
        ↓
Sentence Generator
        ↓
Formatter
        ↓
Report Engine


Nguyên tắc:

- Không tự luận Bát Tự.
- Không chứa rule.
- Không tính toán.
- Chỉ chuyển dữ liệu phân tích thành câu văn.
"""


from typing import Dict, List, Any



# =====================================================
# SENTENCE TEMPLATE DATABASE
# =====================================================


DEFAULT_SENTENCE_TEMPLATE = {


    "positive":

        "Có {description}, tạo điều kiện thuận lợi cho {section}.",



    "negative":

        "Có {description}, cần chú ý trong vấn đề {section}.",



    "neutral":

        "{description}."

}




# =====================================================
# SECTION NAME
# =====================================================


SECTION_LABEL = {


    "tong_quan":
        "tổng quan lá số",


    "nguyen_cuc":
        "nguyên cục",


    "dung_than":
        "dụng thần",


    "hy_than_ky_than":
        "hỷ thần và kỵ thần",


    "tinh_cach":
        "tính cách",


    "suc_khoe":
        "sức khỏe",


    "tai_van":
        "tài vận",


    "su_nghiep":
        "sự nghiệp",


    "hon_nhan":
        "hôn nhân",


    "tu_tuc":
        "tử tức",


    "dai_van":
        "đại vận",


    "luu_nien":
        "lưu niên"

}




# =====================================================
# CLASS
# =====================================================


class SentenceGenerator:



    def __init__(self):

        self.templates = DEFAULT_SENTENCE_TEMPLATE



    # =================================================
    # MAIN GENERATE
    # =================================================


    def generate(
        self,
        interpretation_result
    ):


        result = {


            "summary":

                interpretation_result.summary,


            "sentences":[],



            "sections":{}

        }



        for name, section in interpretation_result.sections.items():


            sentences = self.generate_section(

                section

            )


            result["sections"][name] = sentences



            result["sentences"].extend(

                sentences

            )



        return result




    # =================================================
    # GENERATE SECTION
    # =================================================


    def generate_section(
        self,
        section
    ):


        sentences=[]



        label = SECTION_LABEL.get(

            section.name,

            section.name

        )



        for rule in section.rules:


            sentence = self.generate_rule_sentence(

                rule,

                label

            )


            if sentence:

                sentences.append(

                    sentence

                )



        return sentences




    # =================================================
    # GENERATE RULE SENTENCE
    # =================================================


    def generate_rule_sentence(
        self,
        rule,
        section
    ):



        polarity = rule.get(

            "polarity",

            "neutral"

        )



        description = rule.get(

            "description",

            ""

        )



        if not description:


            return ""



        template = self.templates.get(

            polarity,

            self.templates["neutral"]

        )



        return template.format(

            description=description,


            section=section

        )




    # =================================================
    # GENERATE SUMMARY
    # =================================================


    def generate_summary(
        self,
        interpretation_result
    ):


        strengths = len(

            interpretation_result.strengths

        )


        weaknesses = len(

            interpretation_result.weaknesses

        )


        warnings = len(

            interpretation_result.warnings

        )



        return {


            "strengths":

                strengths,


            "weaknesses":

                weaknesses,


            "warnings":

                warnings

        }





# =====================================================
# SERVICE FUNCTION
# =====================================================


def generate_sentences(

    interpretation_result

):


    generator = SentenceGenerator()


    return generator.generate(

        interpretation_result

    )
