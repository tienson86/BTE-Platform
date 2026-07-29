"""
interpretation_engine/interpreter/children.py

Interpreter diễn giải Tử Tức.

Nhiệm vụ:
- Đọc dữ liệu con cái từ Bazi Engine.
- Tra template.
- Sinh InterpretationResult.

Không tự tính sao con cái.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class ChildrenInterpreter(BaseInterpreter):
    """
    Diễn giải con cái.
    """

    name = "ChildrenInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "children"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        children_data = analysis.get(
            "children"
        )


        if not children_data:

            result.warnings.append(
                "Không có dữ liệu Tử Tức."
            )

            return result



        factors = children_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "children.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="children",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    75
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
