"""
interpretation_engine/interpreter/combination.py

Interpreter diễn giải quan hệ Can Chi.

Bao gồm:
- Hợp
- Xung
- Hình
- Hại
- Phá
- Tam hợp
- Tam hội

Không tính toán quan hệ.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class CombinationInterpreter(BaseInterpreter):
    """
    Diễn giải các quan hệ trong Bát Tự.
    """

    name = "CombinationInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "combination"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        relations = analysis.get(
            "relations"
        )


        if not relations:

            result.warnings.append(
                "Không có dữ liệu quan hệ Can Chi."
            )

            return result



        for relation in relations:


            template = self.loader.lookup(
                "combination.json",
                relation
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
                    relation
                ]
            )


            result.add(item)



        return result
