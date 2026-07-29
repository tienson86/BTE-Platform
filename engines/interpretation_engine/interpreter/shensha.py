"""
interpretation_engine/interpreter/shensha.py

Interpreter diễn giải Thần Sát.

Nhiệm vụ:
- Nhận kết quả Thần Sát từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tính toán Thần Sát.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class ShenShaInterpreter(BaseInterpreter):
    """
    Diễn giải hệ thống Thần Sát.
    """

    name = "ShenShaInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "shensha"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        shensha_list = analysis.get(
            "shensha"
        )


        if not shensha_list:

            result.warnings.append(
                "Không có dữ liệu Thần Sát."
            )

            return result



        for sha in shensha_list:


            template = self.loader.lookup(
                "shensha.json",
                sha
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
                    sha
                ]
            )


            result.add(item)



        return result
