"""
Priority Resolver
=================

Xử lý thứ tự ưu tiên của Rule.

Nguyên tắc:

Cách cục
    ↓
Dụng thần
    ↓
Hỷ Kỵ
    ↓
Đại vận
    ↓
Lưu niên
    ↓
Thần sát
"""


from typing import List, Dict





PRIORITY_LEVEL = {


    "cach_cuc": 1,


    "dung_than": 2,


    "hy_than_ky_than": 3,


    "dai_van": 4,


    "luu_nien": 5,


    "su_nghiep": 6,


    "tai_van": 7,


    "hon_nhan": 8,


    "suc_khoe": 9,


    "than_sat": 10,


    "mac_dinh": 99

}





class PriorityResolver:



    def __init__(self):

        self.priority = PRIORITY_LEVEL




    def get_priority(
        self,
        rule
    ):


        layer = rule.get(

            "layer",

            "mac_dinh"

        )


        return self.priority.get(

            layer,

            99

        )





    def sort(
        self,
        rules: List[Dict]
    ):


        return sorted(

            rules,

            key=lambda r:(

                self.get_priority(r),

                -

                r.get(

                    "score",

                    0

                )

            )

        )





    def top_rules(
        self,
        rules,
        limit=10
    ):


        return self.sort(

            rules

        )[:limit]




def sort_rules(
    rules
):


    resolver = PriorityResolver()


    return resolver.sort(

        rules

    )
