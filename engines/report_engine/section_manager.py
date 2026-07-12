"""
report_engine/section_manager.py

Section Manager.

Nhiệm vụ:
- Gom nhóm các InterpretationItem.
- Sắp xếp thứ tự các chương báo cáo.
- Chuẩn hóa cấu trúc Report Section.

Không luận đoán.
"""


from __future__ import annotations



class SectionManager:
    """
    Quản lý các section trong báo cáo Bát Tự.
    """

    name = "SectionManager"



    # Thứ tự chuẩn của báo cáo

    SECTION_ORDER = [

        "summary",

        "day_master",

        "five_elements",

        "ten_gods",

        "useful_god",

        "combination",

        "shensha",

        "career",

        "wealth",

        "marriage",

        "children",

        "health",

        "luck",

        "fengshui"

    ]



    SECTION_TITLE = {


        "summary":
            "Tổng Quan Mệnh Cục",


        "day_master":
            "Phân Tích Nhật Chủ",


        "five_elements":
            "Cân Bằng Ngũ Hành",


        "ten_gods":
            "Phân Tích Thập Thần",


        "useful_god":
            "Dụng Thần - Hỷ Thần - Kỵ Thần",


        "combination":
            "Quan Hệ Hợp Xung Hình Hại",


        "shensha":
            "Hệ Thống Thần Sát",


        "career":
            "Sự Nghiệp Và Nghề Nghiệp",


        "wealth":
            "Tài Vận",


        "marriage":
            "Hôn Nhân Và Tình Cảm",


        "children":
            "Tử Tức - Con Cái",


        "health":
            "Xu Hướng Sức Khỏe",


        "luck":
            "Đại Vận - Lưu Niên",


        "fengshui":
            "Ứng Dụng Phong Thủy"

    }



    def organize(
        self,
        interpretation_result
    ) -> list:
        """
        Chuyển danh sách InterpretationItem
        thành các chương báo cáo.
        """


        sections = {}



        for item in interpretation_result:


            section_name = (
                item.get(
                    "section",
                    "summary"
                )
            )


            if section_name not in sections:


                sections[section_name] = {

                    "id":
                        section_name,


                    "title":
                        self.SECTION_TITLE.get(
                            section_name,
                            section_name
                        ),


                    "items":[]

                }



            sections[section_name]["items"].append(

                self.normalize_item(
                    item
                )

            )



        return self.sort_sections(
            sections
        )



    def normalize_item(
        self,
        item: dict
    ) -> dict:
        """
        Chuẩn hóa một mục diễn giải.
        """


        return {


            "code":
                item.get(
                    "code"
                ),


            "title":
                item.get(
                    "title"
                ),


            "content":
                item.get(
                    "content"
                ),


            "score":
                item.get(
                    "score",
                    0
                ),


            "priority":
                item.get(
                    "priority",
                    0
                ),


            "tags":
                item.get(
                    "tags",
                    []
                ),


            "references":
                item.get(
                    "references",
                    []
                )

        }



    def sort_sections(
        self,
        sections: dict
    ) -> list:
        """
        Sắp xếp chương báo cáo.
        """


        result = []



        for section_id in self.SECTION_ORDER:


            if section_id in sections:

                result.append(
                    sections[section_id]
                )



        # Những phần mở rộng chưa có trong cấu trúc

        for key, value in sections.items():


            if key not in self.SECTION_ORDER:

                result.append(
                    value
                )



        return result
