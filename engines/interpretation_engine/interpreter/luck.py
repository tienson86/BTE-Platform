"""
interpretation_engine/interpreter/luck.py

Interpreter diễn giải Đại Vận - Lưu Niên.

Nhiệm vụ:
- Nhận dữ liệu vận khí từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tính toán Đại Vận.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class LuckInterpreter(BaseInterpreter):
    """
    Diễn giải vận trình.
    """

    name = "LuckInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "luck"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        luck_data = analysis.get(
            "luck"
        )


        if not luck_data:

            result.warnings.append(
                "Không có dữ liệu vận trình."
            )

            return result



        factors = luck_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "luck.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="luck",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    85
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
