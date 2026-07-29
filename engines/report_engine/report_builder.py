"""
report_engine/report_builder.py

Report Builder trung tâm.

Nhiệm vụ:
- Nhận kết quả Interpretation Engine.
- Tổ chức thành báo cáo hoàn chỉnh.
- Chuẩn bị dữ liệu cho Renderer.

Không thực hiện luận đoán.
"""

from __future__ import annotations

from datetime import datetime

from .section_manager import SectionManager
from .scoring import ReportScoring
from .conflict_resolver import ConflictResolver



class ReportBuilder:
    """
    Bộ xây dựng báo cáo Bát Tự.
    """


    name = "ReportBuilder"



    def __init__(self):

        self.section_manager = SectionManager()

        self.scoring = ReportScoring()

        self.conflict_resolver = ConflictResolver()



    def build(
        self,
        interpretation_result,
        person_info: dict | None = None,
    ) -> dict:
        """
        Tạo cấu trúc báo cáo hoàn chỉnh.

        Parameters
        ----------
        interpretation_result:
            Kết quả từ Interpretation Engine

        person_info:
            Thông tin khách hàng

        Returns
        -------
        dict
            Report Object
        """


        report = {

            "meta": {

                "created_at":
                    datetime.now().isoformat(),

                "engine":
                    self.name

            },


            "person":

                person_info or {},


            "sections": [],


            "summary": {},


            "score": {},


            "warnings": []

        }



        # 1. Xử lý xung đột diễn giải

        clean_result = (
            self.conflict_resolver.resolve(
                interpretation_result
            )
        )



        # 2. Chia nhóm nội dung

        sections = (
            self.section_manager.organize(
                clean_result
            )
        )



        report["sections"] = sections



        # 3. Chấm điểm tổng quan

        report["score"] = (
            self.scoring.calculate(
                clean_result
            )
        )



        # 4. Sinh phần tóm tắt

        report["summary"] = (
            self.create_summary(
                sections
            )
        )



        return report




    def create_summary(
        self,
        sections: list
    ) -> dict:
        """
        Tạo phần mở đầu báo cáo.
        """


        summary = {

            "strengths": [],

            "weaknesses": [],

            "recommendations": []

        }



        for section in sections:


            for item in section.get(
                "items",
                []
            ):


                score = item.get(
                    "score",
                    0
                )



                if score >= 80:

                    summary[
                        "strengths"
                    ].append(
                        item
                    )


                elif score <= -40:

                    summary[
                        "weaknesses"
                    ].append(
                        item
                    )


                else:

                    summary[
                        "recommendations"
                    ].append(
                        item
                    )



        return summary
