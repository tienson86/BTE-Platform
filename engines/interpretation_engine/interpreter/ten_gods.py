"""
interpretation_engine/interpreter/ten_gods.py

Interpreter diễn giải Thập Thần.

Nhiệm vụ:
- Nhận kết quả Thập Thần từ Bazi Engine.
- Tra dữ liệu template.
- Sinh InterpretationResult.

Không tính quan hệ Thập Thần.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class TenGodsInterpreter(BaseInterpreter):
    """
    Diễn giải hệ thống Thập Thần.
    """

    name = "TenGodsInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "ten_gods"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        ten_gods = analysis.get(
            "ten_gods"
        )


        if not ten_gods:

            result.warnings.append(
                "Không tìm thấy dữ liệu Thập Thần."
            )

            return result



        for god in ten_gods:


            template = self.loader.lookup(
                "ten_gods.json",
                god
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="personality",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    70
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
