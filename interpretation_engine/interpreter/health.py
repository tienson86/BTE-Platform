"""
interpretation_engine/interpreter/health.py

Interpreter diễn giải sức khỏe.

Nhiệm vụ:
- Nhận dữ liệu cân bằng ngũ hành từ Bazi Engine.
- Tra template sức khỏe.
- Sinh InterpretationResult.

Không chẩn đoán bệnh.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader

from .base import BaseInterpreter


class HealthInterpreter(BaseInterpreter):
    """
    Diễn giải xu hướng sức khỏe theo ngũ hành.
    """

    name = "HealthInterpreter"


    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "health"
        )


    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:


        result = InterpretationResult(
            interpreter=self.name
        )


        health_data = analysis.get(
            "health"
        )


        if not health_data:

            result.warnings.append(
                "Không có dữ liệu sức khỏe."
            )

            return result



        factors = health_data.get(
            "factors",
            []
        )


        for factor in factors:


            template = self.loader.lookup(
                "health.json",
                factor
            )


            if template is None:

                continue



            item = InterpretationItem(

                section="health",

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
                    factor
                ]
            )


            result.add(item)



        return result
