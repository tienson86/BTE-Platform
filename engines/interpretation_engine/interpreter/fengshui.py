"""
interpretation_engine/interpreter/fengshui.py

Interpreter diễn giải ứng dụng phong thủy.

Nhiệm vụ:
- Nhận dữ liệu phong thủy từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tự tính phong thủy.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class FengShuiInterpreter(BaseInterpreter):
    """
    Diễn giải phong thủy theo Bát Tự.
    """

    name = "FengShuiInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "fengshui"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        feng_data = analysis.get(
            "fengshui"
        )


        if not feng_data:

            result.warnings.append(
                "Không có dữ liệu phong thủy."
            )

            return result



        factors = feng_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "fengshui.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="fengshui",

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
