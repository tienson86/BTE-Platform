"""
report_engine/scoring.py

Hệ thống chấm điểm báo cáo Bát Tự.

Nhiệm vụ:
- Tổng hợp điểm từ Interpretation Engine.
- Sinh bảng đánh giá tổng quan.

Không tự tính Bát Tự.
"""


from __future__ import annotations



class ReportScoring:
    """
    Bộ chấm điểm báo cáo.
    """

    name = "ReportScoring"



    # Trọng số từng lĩnh vực

    SECTION_WEIGHT = {


        "summary":
            20,


        "day_master":
            10,


        "five_elements":
            10,


        "useful_god":
            15,


        "career":
            20,


        "wealth":
            20,


        "marriage":
            10,


        "children":
            5,


        "health":
            5,


        "luck":
            10,


        "fengshui":
            5

    }



    def calculate(
        self,
        interpretation_result
    ) -> dict:
        """
        Tính điểm tổng hợp.
        """


        section_scores = {}



        for section, weight in self.SECTION_WEIGHT.items():


            scores = []



            for item in interpretation_result:


                if item.get(
                    "section"
                ) == section:


                    scores.append(

                        item.get(
                            "score",
                            0
                        )

                    )



            if scores:


                avg = (
                    sum(scores)
                    /
                    len(scores)
                )


                section_scores[section] = {

                    "raw_score":
                        round(
                            avg,
                            2
                        ),


                    "weight":
                        weight,


                    "weighted_score":
                        round(
                            avg
                            *
                            weight
                            /
                            100,
                            2
                        )

                }



        return {

            "sections":
                section_scores,


            "overall":
                self.calculate_overall(
                    section_scores
                ),


            "rating":
                self.rating(
                    self.calculate_overall(
                        section_scores
                    )
                )

        }



    def calculate_overall(
        self,
        section_scores: dict
    ) -> float:
        """
        Tính điểm tổng.
        """


        total = 0



        for data in section_scores.values():


            total += data[
                "weighted_score"
            ]



        return round(
            total,
            2
        )



    def rating(
        self,
        score: float
    ) -> str:
        """
        Xếp loại tổng quan.
        """


        if score >= 85:

            return "Rất tốt"



        elif score >= 70:

            return "Tốt"



        elif score >= 55:

            return "Trung bình"



        elif score >= 40:

            return "Cần cải thiện"



        else:

            return "Nhiều thử thách"
