"""
report_engine/conflict_resolver.py

Conflict Resolver.

Nhiệm vụ:
- Phát hiện xung đột giữa các kết quả diễn giải.
- Điều chỉnh score.
- Thêm ghi chú cân bằng.

Không tính toán Bát Tự.
"""


from __future__ import annotations



class ConflictResolver:
    """
    Bộ xử lý xung đột diễn giải.
    """

    name = "ConflictResolver"



    CONFLICT_RULES = [

        {

            "positive":
                "TAI_TINH_HIEN",

            "negative":
                "THAN_NHUOC_KY_TAI",

            "adjust":
                -10,

            "message":
                "Tài vận có tiềm năng nhưng cần tăng cường năng lực quản lý trước khi mở rộng."

        },


        {

            "positive":
                "DAO_HOA",

            "negative":
                "CO_THAN",

            "adjust":
                -5,

            "message":
                "Có sức hút trong giao tiếp nhưng xu hướng nội tâm có thể tạo khoảng cách tình cảm."

        },


        {

            "positive":
                "HONG_LOAN",

            "negative":
                "QUA_TU",

            "adjust":
                -5,

            "message":
                "Có duyên tình cảm nhưng cần chú trọng sự chia sẻ và kết nối."

        },


        {

            "positive":
                "DUNG_THAN_GAP_VAN",

            "negative":
                "KY_THAN_GAP_VAN",

            "adjust":
                -15,

            "message":
                "Vận trình có cơ hội nhưng vẫn tồn tại yếu tố thử thách cần cân bằng."

        },


        {

            "positive":
                "THIEN_TAI_MANH",

            "negative":
                "TY_KIEP_DOAT_TAI",

            "adjust":
                -10,

            "message":
                "Có khả năng tạo cơ hội tài chính nhưng cần chú ý hợp tác và quản lý nguồn lực."

        }

    ]



    def resolve(
        self,
        interpretation_result
    ):
        """
        Xử lý toàn bộ danh sách kết quả.
        """


        items = [

            item.copy()

            for item in interpretation_result

        ]



        codes = {

            item.get(
                "code"
            )

            for item in items

        }



        warnings = []



        for rule in self.CONFLICT_RULES:


            if (

                rule["positive"]
                in
                codes

                and

                rule["negative"]
                in
                codes

            ):


                self.adjust_score(

                    items,

                    rule

                )


                warnings.append(

                    rule["message"]

                )



        return items + self.create_warning_items(
            warnings
        )



    def adjust_score(
        self,
        items,
        rule
    ):
        """
        Điều chỉnh điểm khi có xung đột.
        """


        for item in items:


            if item.get(
                "code"
            ) == rule["positive"]:


                old_score = item.get(
                    "score",
                    0
                )


                item["score"] = (

                    old_score
                    +
                    rule["adjust"]

                )



    def create_warning_items(
        self,
        warnings
    ):
        """
        Tạo mục cảnh báo cân bằng.
        """


        result = []



        for index, text in enumerate(
            warnings,
            start=1
        ):


            result.append(

                {

                    "section":
                        "summary",


                    "code":
                        f"WARNING_{index}",


                    "title":
                        "Lưu ý cân bằng",


                    "content":
                        text,


                    "score":
                        0,


                    "priority":
                        100

                }

            )



        return result
