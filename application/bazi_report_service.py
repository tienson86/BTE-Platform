"""
application/bazi_report_service.py

Bazi Report Service.

Đây là tầng điều phối chính.

Luồng:

Input
 |
 v
Bazi Engine
 |
 v
Interpretation Engine
 |
 v
Report Engine
 |
 v
Export

Không tự tính toán luận đoán.
"""


from __future__ import annotations


from pathlib import Path



class BaziReportService:
    """
    Dịch vụ tạo báo cáo Bát Tự.
    """

    name = "BaziReportService"



    def __init__(
        self,
        bazi_engine,
        interpretation_engine,
        report_builder,
        markdown_renderer=None,
        pdf_renderer=None,
        word_renderer=None,
    ):


        self.bazi_engine = bazi_engine


        self.interpretation_engine = (
            interpretation_engine
        )


        self.report_builder = (
            report_builder
        )


        self.markdown_renderer = (
            markdown_renderer
        )


        self.pdf_renderer = (
            pdf_renderer
        )


        self.word_renderer = (
            word_renderer
        )



    def generate_report(
        self,
        birth_data: dict,
        person_info: dict | None = None,
        output_dir: str = "reports"
    ):
        """
        Tạo báo cáo hoàn chỉnh.

        Parameters
        ----------
        birth_data:
            ngày giờ sinh

        person_info:
            thông tin khách hàng

        output_dir:
            thư mục lưu báo cáo

        """


        # ======================
        # 1. Chạy Bazi Engine
        # ======================


        bazi_result = (
            self.bazi_engine.calculate(
                birth_data
            )
        )



        # ======================
        # 2. Chạy Interpretation
        # ======================


        interpretation_result = (

            self.interpretation_engine.run(

                bazi_result

            )

        )



        # ======================
        # 3. Build Report Object
        # ======================


        report = (

            self.report_builder.build(

                interpretation_result,

                person_info

            )

        )



        # ======================
        # 4. Export
        # ======================


        return self.export(

            report,

            output_dir

        )




    def export(
        self,
        report: dict,
        output_dir: str
    ) -> dict:
        """
        Xuất các định dạng báo cáo.
        """


        folder = Path(
            output_dir
        )


        folder.mkdir(
            parents=True,
            exist_ok=True
        )


        result = {}



        # Markdown

        if self.markdown_renderer:


            md_file = (

                folder
                /
                "bao_cao_bat_tu.md"

            )


            content = (

                self.markdown_renderer.render(

                    report

                )

            )


            md_file.write_text(

                content,

                encoding="utf-8"

            )


            result["markdown"] = str(
                md_file
            )



        # PDF

        if self.pdf_renderer:


            pdf_file = (

                folder
                /
                "bao_cao_bat_tu.pdf"

            )


            self.pdf_renderer.render(

                report,

                str(pdf_file)

            )


            result["pdf"] = str(
                pdf_file
            )



        # Word

        if self.word_renderer:


            docx_file = (

                folder
                /
                "bao_cao_bat_tu.docx"

            )


            self.word_renderer.render(

                report,

                str(docx_file)

            )


            result["docx"] = str(
                docx_file
            )



        return result
