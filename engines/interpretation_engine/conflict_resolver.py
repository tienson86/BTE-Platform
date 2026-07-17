"""
Conflict Resolver
=================

Xử lý các Rule mâu thuẫn.

Ví dụ:

- Rule tốt + Rule xấu cùng xuất hiện.
- Dụng thần có lợi nhưng bị phá.
- Đại vận tốt nhưng lưu niên xấu.

Không tự kết luận.
Chỉ phát hiện xung đột.
"""


from typing import List, Dict





class ConflictResolver:



    def __init__(self):

        pass





    def analyze(
        self,
        rules: List[Dict]
    ):


        result = {


            "rules": rules,


            "positive": [],


            "negative": [],


            "conflicts": []

        }



        sections = {}



        for rule in rules:


            polarity = rule.get(

                "polarity",

                "neutral"

            )



            if polarity == "positive":

                result["positive"].append(
                    rule
                )


            elif polarity == "negative":

                result["negative"].append(
                    rule
                )



            section = rule.get(

                "section",

                "tong_quan"

            )


            sections.setdefault(

                section,

                []

            ).append(rule)





        for section, items in sections.items():


            positive = any(

                r.get(

                    "polarity"

                ) == "positive"

                for r in items

            )


            negative = any(

                r.get(

                    "polarity"

                ) == "negative"

                for r in items

            )



            if positive and negative:


                result["conflicts"].append({

                    "section": section,


                    "type": "polarity_conflict",


                    "message":

                    "Có đồng thời yếu tố thuận lợi và bất lợi"

                })



        return result





    def resolve(
        self,
        rules
    ):


        data = self.analyze(
            rules
        )


        return data





def resolve_conflict(
    rules
):


    resolver = ConflictResolver()


    return resolver.resolve(

        rules

    )
