"""
interpretation_engine/interpreter/marriage.py

Interpreter diễn giải Hôn Nhân.

Nhiệm vụ:
- Đọc các yếu tố hôn nhân từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tự tính duyên số.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class MarriageInterpreter(BaseInterpreter):
    """
    Diễn giải tình cảm và hôn nhân.
    """

    name = "MarriageInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "marriage"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        marriage_data = analysis.get(
            "marriage"
        )


        if not marriage_data:

            result.warnings.append(
                "Không có dữ liệu hôn nhân."
            )

            return result



        factors = marriage_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "marriage.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="marriage",

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
