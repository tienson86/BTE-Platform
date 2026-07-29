"""
report_engine/markdown_renderer.py

Markdown Renderer.

Nhiệm vụ:
- Chuyển Report Object thành Markdown.
- Chuẩn hóa bố cục báo cáo.

Không luận đoán.
"""


from __future__ import annotations

from datetime import datetime



class MarkdownRenderer:
    """
    Xuất báo cáo dạng Markdown.
    """

    name = "MarkdownRenderer"



    def render(
        self,
        report: dict
    ) -> str:
        """
        Tạo nội dung Markdown.
        """


        output = []



        output.append(

            "# BÁO CÁO PHÂN TÍCH BÁT TỰ\n"

        )



        output.append(

            self.render_meta(
                report
            )

        )



        output.append(

            self.render_person(
                report
            )

        )



        output.append(

            self.render_score(
                report
            )

        )



        output.append(

            self.render_summary(
                report
            )

        )



        output.append(

            self.render_sections(
                report
            )

        )



        return "\n\n".join(
            output
        )




    def render_meta(
        self,
        report
    ) -> str:


        meta = report.get(
            "meta",
            {}
        )


        return f"""
## Thông tin hệ thống

- Engine:
  {meta.get('engine','')}

- Ngày tạo:
  {meta.get('created_at','')}
"""




    def render_person(
        self,
        report
    ) -> str:


        person = report.get(
            "person",
            {}
        )


        return f"""
# Thông Tin Khách Hàng

- Họ tên:
  {person.get('name','')}

- Giới tính:
  {person.get('gender','')}

- Ngày sinh:
  {person.get('birth_date','')}

- Giờ sinh:
  {person.get('birth_time','')}

"""




    def render_score(
        self,
        report
    ) -> str:


        score = report.get(
            "score",
            {}
        )


        return f"""
# Đánh Giá Tổng Quan

Điểm tổng:
**{score.get('overall',0)}**

Xếp loại:
**{score.get('rating','')}**

"""




    def render_summary(
        self,
        report
    ) -> str:


        summary = report.get(
            "summary",
            {}
        )


        text = []

        text.append(
            "# Tổng Kết Mệnh Cục"
        )



        text.append(
            "## Điểm mạnh"
        )


        for item in summary.get(
            "strengths",
            []
        ):


            text.append(

                f"- {item.get('title')}"

            )



        text.append(
            "## Điểm cần lưu ý"
        )


        for item in summary.get(
            "weaknesses",
            []
        ):


            text.append(

                f"- {item.get('title')}"

            )



        text.append(
            "## Khuyến nghị"
        )


        for item in summary.get(
            "recommendations",
            []
        ):


            text.append(

                f"- {item.get('title')}"

            )


        return "\n".join(
            text
        )




    def render_sections(
        self,
        report
    ) -> str:


        output = []


        output.append(
            "# Phân Tích Chi Tiết"
        )



        for section in report.get(
            "sections",
            []
        ):


            output.append(

                self.render_section(
                    section
                )

            )



        return "\n\n".join(
            output
        )




    def render_section(
        self,
        section
    ) -> str:


        lines = []



        lines.append(

            f"## {section.get('title')}"

        )



        for item in section.get(
            "items",
            []
        ):


            lines.append(

                f"""
### {item.get('title')}

**Điểm đánh giá:**
{item.get('score',0)}

{item.get('content')}
"""

            )


        return "\n".join(
            lines
        )
