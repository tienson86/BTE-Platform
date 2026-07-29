"""
interpretation_engine/interpreter/summary.py

Interpreter tổng hợp báo cáo.

Nhiệm vụ:
- Tổng hợp các kết quả diễn giải.
- Sinh phần kết luận.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class SummaryInterpreter(BaseInterpreter):
    """
    Tổng hợp toàn bộ báo cáo.
    """

    name = "SummaryInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "summary"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        summary_data = analysis.get(
            "summary"
        )


        if not summary_data:

            result.warnings.append(
                "Không có dữ liệu tổng hợp."
            )

            return result



        factors = summary_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "summary.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="summary",

                code=template["code"],

                title=template["title"],

                content=template["content"],

                priority=template.get(
                    "priority",
                    100
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
