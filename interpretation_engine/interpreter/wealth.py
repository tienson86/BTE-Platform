"""
interpretation_engine/interpreter/wealth.py

Interpreter diễn giải Tài Vận.

Nhiệm vụ:
- Đọc kết quả tài vận từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không thực hiện tính toán tài tinh.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class WealthInterpreter(BaseInterpreter):
    """
    Diễn giải tài vận.
    """

    name = "WealthInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "wealth"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        wealth_data = analysis.get(
            "wealth"
        )


        if not wealth_data:

            result.warnings.append(
                "Không có dữ liệu tài vận."
            )

            return result



        factors = wealth_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "wealth.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="wealth",

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
