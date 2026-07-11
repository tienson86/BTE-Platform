"""
interpretation_engine/interpreter/useful_god.py

Interpreter diễn giải Dụng Thần - Hỷ Thần - Kỵ Thần.

Nhiệm vụ:
- Đọc kết quả Dụng Thần từ Bazi Engine.
- Tra dữ liệu diễn giải.
- Tạo InterpretationResult.

Không thực hiện tính toán chọn Dụng Thần.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class UsefulGodInterpreter(BaseInterpreter):
    """
    Diễn giải hệ thống Dụng Thần.
    """

    name = "UsefulGodInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "useful_god"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        useful_data = analysis.get(
            "useful_god"
        )


        if not useful_data:

            result.warnings.append(
                "Không tìm thấy dữ liệu Dụng Thần."
            )

            return result



        gods = [

            useful_data.get("dung_than"),

            useful_data.get("hy_than"),

            useful_data.get("ky_than"),

            useful_data.get("nhan_than")

        ]



        for god in gods:


            if not god:

                continue



            template = self.loader.lookup(
                "useful_god.json",
                god
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="overview",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    90
                ),

                score=template.get(
                    "score",
                    0
                ),

                tags=template.get(
                    "tags",
                    []
                ),

                references=[
                    god
                ]
            )


            result.add(item)



        return result
