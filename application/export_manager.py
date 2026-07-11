"""
application/export_manager.py

Export Manager.

Quản lý toàn bộ đầu ra báo cáo.

Nhiệm vụ:
- Tạo thư mục lưu trữ.
- Xuất nhiều định dạng.
- Chuẩn hóa file.

Không tính toán và không luận đoán.
"""


from __future__ import annotations


from pathlib import Path

import json

from datetime import datetime



class ExportManager:
    """
    Bộ quản lý xuất báo cáo.
    """

    name = "ExportManager"



    def __init__(
        self,
        markdown_renderer=None,
        pdf_renderer=None,
        word_renderer=None
    ):


        self.markdown_renderer = (
            markdown_renderer
        )


        self.pdf_renderer = (
            pdf_renderer
        )


        self.word_renderer = (
            word_renderer
        )



    def create_folder(
        self,
        customer_id: str,
        base_dir="reports"
    ):
        """
        Tạo thư mục lưu báo cáo.
        """


        folder = (

            Path(base_dir)

            /
            customer_id

            /
            datetime.now()
            .strftime("%Y%m%d")

        )


        folder.mkdir(

            parents=True,

            exist_ok=True

        )


        return folder




    def export_all(
        self,
        report: dict,
        customer_id: str,
        base_dir="reports"
    ):
        """
        Xuất toàn bộ định dạng.
        """


        folder = self.create_folder(

            customer_id,

            base_dir

        )



        result = {}



        # =====================
        # JSON
        # =====================


        json_file = (

            folder
            /
            "report.json"

        )


        json_file.write_text(

            json.dumps(

                report,

                ensure_ascii=False,

                indent=4

            ),

            encoding="utf-8"

        )


        result["json"] = str(
            json_file
        )



        # =====================
        # Markdown
        # =====================


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



        # =====================
        # PDF
        # =====================


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



        # =====================
        # WORD
        # =====================


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




    def export_single(
        self,
        content,
        filename,
        folder
    ):
        """
        Xuất file đơn giản.
        """


        path = (

            Path(folder)

            /
            filename

        )


        path.write_text(

            content,

            encoding="utf-8"

        )


        return str(path)
