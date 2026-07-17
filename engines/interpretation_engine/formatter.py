"""
Formatter
=========

Chuẩn hóa kết quả luận giải.

Flow:

Interpretation Builder
        ↓
Sentence Generator
        ↓
Formatter
        ↓
Report Engine


Chức năng:

- Chuyển dữ liệu luận giải thành các định dạng đầu ra.
- Chuẩn bị cho:
    + API
    + Web
    + PDF Report
    + Markdown
"""


from typing import Dict, List, Any

import json



# =====================================================
# FORMAT TYPE
# =====================================================


FORMAT_TYPES = [

    "dict",

    "json",

    "text",

    "markdown"

]





# =====================================================
# CLASS FORMATTER
# =====================================================


class Formatter:



    def __init__(self):

        pass




    # =================================================
    # MAIN FORMAT
    # =================================================


    def format(
        self,
        data,
        output_type="dict"
    ):


        if output_type == "dict":

            return self.to_dict(data)



        elif output_type == "json":

            return self.to_json(data)



        elif output_type == "text":

            return self.to_text(data)



        elif output_type == "markdown":

            return self.to_markdown(data)



        else:

            raise ValueError(

                "Unsupported format type"

            )





    # =================================================
    # TO DICT
    # =================================================


    def to_dict(
        self,
        data
    ):


        if isinstance(
            data,
            dict
        ):

            return data



        result = {



            "summary":

                getattr(

                    data,

                    "summary",

                    ""

                ),



            "confidence":

                getattr(

                    data,

                    "confidence",

                    0

                ),



            "sections":{},



            "strengths":

                getattr(

                    data,

                    "strengths",

                    []

                ),



            "weaknesses":

                getattr(

                    data,

                    "weaknesses",

                    []

                ),



            "warnings":

                getattr(

                    data,

                    "warnings",

                    []

                )

        }



        sections = getattr(

            data,

            "sections",

            {}

        )



        for name, section in sections.items():


            result["sections"][name] = {


                "score":

                    section.score,



                "rules":

                    section.rules,



                "positive":

                    section.positive_rules,



                "negative":

                    section.negative_rules


            }



        return result





    # =================================================
    # TO JSON
    # =================================================


    def to_json(
        self,
        data
    ):


        dictionary = self.to_dict(
            data
        )


        return json.dumps(

            dictionary,

            ensure_ascii=False,

            indent=4

        )





    # =================================================
    # TO TEXT
    # =================================================


    def to_text(
        self,
        data
    ):


        obj = self.to_dict(
            data
        )


        lines=[]



        lines.append(

            "KET QUA LUAN GIAI"

        )


        lines.append(

            ""

        )


        lines.append(

            obj.get(

                "summary",

                ""

            )

        )



        lines.append(

            ""

        )


        for name, section in obj["sections"].items():


            lines.append(

                "== "

                +

                name

                +

                " =="

            )



            for rule in section["rules"]:


                description = rule.get(

                    "description",

                    ""

                )


                if description:


                    lines.append(

                        "- "

                        +

                        description

                    )



            lines.append("")



        return "\n".join(lines)





    # =================================================
    # MARKDOWN
    # =================================================


    def to_markdown(
        self,
        data
    ):


        obj = self.to_dict(
            data
        )


        lines=[]



        lines.append(

            "# Kết quả luận giải"

        )


        lines.append("")



        lines.append(

            obj.get(

                "summary",

                ""

            )

        )



        lines.append("")



        for name, section in obj["sections"].items():


            lines.append(

                "## "

                +

                name

            )



            lines.append("")



            for rule in section["rules"]:


                desc = rule.get(

                    "description",

                    ""

                )


                if desc:


                    lines.append(

                        "- "

                        +

                        desc

                    )



            lines.append("")



        return "\n".join(lines)






# =====================================================
# SERVICE FUNCTION
# =====================================================


def format_result(

    data,

    output_type="dict"

):


    formatter = Formatter()



    return formatter.format(

        data,

        output_type

    )
