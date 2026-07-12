"""
report_engine/pdf_renderer.py

PDF Renderer.

Nhiệm vụ:
- Xuất báo cáo Bát Tự dạng PDF.
- Tạo bố cục A4.
- Hiển thị nội dung từ Report Object.

Sử dụng thư viện:
reportlab
"""


from __future__ import annotations


from pathlib import Path


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)


from reportlab.lib.styles import getSampleStyleSheet




class PDFRenderer:
    """
    Bộ xuất PDF báo cáo.
    """

    name = "PDFRenderer"



    def __init__(self):

        self.styles = (
            getSampleStyleSheet()
        )



    def render(
        self,
        report: dict,
        output_file: str
    ):
        """
        Tạo file PDF.

        Parameters
        ----------
        report:
            Report Object

        output_file:
            đường dẫn PDF
        """



        document = SimpleDocTemplate(

            output_file,

            pagesize="A4"

        )



        story = []



        # Tiêu đề

        story.append(

            Paragraph(

                "BÁO CÁO PHÂN TÍCH BÁT TỰ",

                self.styles["Title"]

            )

        )


        story.append(
            Spacer(1,20)
        )



        # Thông tin khách hàng

        person = report.get(
            "person",
            {}
        )


        story.append(

            Paragraph(

                f"""
                Họ tên:
                {person.get('name','')}
                <br/>
                Ngày sinh:
                {person.get('birth_date','')}
                <br/>
                Giờ sinh:
                {person.get('birth_time','')}
                """,

                self.styles["Normal"]

            )

        )



        story.append(
            PageBreak()
        )



        # Điểm tổng quan

        score = report.get(
            "score",
            {}
        )


        story.append(

            Paragraph(

                "ĐÁNH GIÁ TỔNG QUAN",

                self.styles["Heading2"]

            )

        )



        story.append(

            Paragraph(

                f"""
                Tổng điểm:
                {score.get('overall',0)}
                <br/>
                Xếp loại:
                {score.get('rating','')}
                """,

                self.styles["Normal"]

            )

        )



        story.append(
            Spacer(1,20)
        )



        # Nội dung từng chương

        for section in report.get(
            "sections",
            []
        ):


            story.append(

                Paragraph(

                    section.get(
                        "title",
                        ""
                    ),

                    self.styles["Heading2"]

                )

            )



            for item in section.get(
                "items",
                []
            ):


                story.append(

                    Paragraph(

                        f"""
                        <b>
                        {item.get('title','')}
                        </b>

                        <br/>

                        Điểm:
                        {item.get('score',0)}

                        <br/>

                        {item.get('content','')}
                        """,

                        self.styles["Normal"]

                    )

                )


                story.append(

                    Spacer(
                        1,
                        12
                    )

                )



        document.build(
            story
        )
