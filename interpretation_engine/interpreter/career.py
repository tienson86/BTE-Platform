"""
interpretation_engine/interpreter/career.py

Interpreter diễn giải Công Danh - Nghề Nghiệp.

Nhiệm vụ:
- Đọc kết quả nghề nghiệp từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tự phân tích nghề nghiệp.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class CareerInterpreter(BaseInterpreter):
    """
    Diễn giải công danh sự nghiệp.
    """

    name = "CareerInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "career"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        career_data = analysis.get(
            "career"
        )


        if not career_data:

            result.warnings.append(
                "Không có dữ liệu công danh."
            )

            return result



        factors = career_data.get(
            "factors",
            []
        )



        for factor in factors:


            template = self.loader.lookup(
                "career.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="career",

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
                    factor
                ]
            )


            result.add(item)



        return result
