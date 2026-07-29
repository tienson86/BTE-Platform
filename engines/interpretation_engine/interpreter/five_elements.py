"""
interpretation_engine/interpreter/five_elements.py

Interpreter diễn giải Ngũ Hành.

Nhiệm vụ:
- Nhận kết quả phân tích ngũ hành từ Bazi Engine.
- Tra template diễn giải.
- Tạo InterpretationResult.

Không thực hiện tính toán ngũ hành.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class FiveElementsInterpreter(BaseInterpreter):
    """
    Diễn giải cân bằng Ngũ Hành.
    """

    name = "FiveElementsInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "five_elements"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        elements = analysis.get(
            "five_elements"
        )


        if not elements:

            result.warnings.append(
                "Không tìm thấy dữ liệu Ngũ Hành."
            )

            return result



        conditions = []


        if elements.get("strong"):

            conditions.append(
                elements["strong"]
            )


        if elements.get("weak"):

            conditions.append(
                elements["weak"]
            )


        if elements.get("missing"):

            conditions.append(
                elements["missing"]
            )



        for condition in conditions:


            template = self.loader.lookup(
                "five_elements.json",
                condition
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="five_elements",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    80
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
                    condition
                ]
            )


            result.add(item)



        return result
