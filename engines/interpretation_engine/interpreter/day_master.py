"""
interpretation_engine/interpreter/day_master.py

Interpreter diễn giải Nhật Chủ (Day Master).

Nhiệm vụ:
- Đọc kết quả phân tích Bát Tự.
- Xác định Nhật Chủ.
- Đọc template tương ứng.
- Sinh InterpretationResult.

Không thực hiện bất kỳ phép tính Bát Tự nào.
"""

from __future__ import annotations

from pathlib import Path

from ..context import InterpretationItem
from ..context import InterpretationResult
from ..template_loader import TemplateLoader
from .base import BaseInterpreter


class DayMasterInterpreter(BaseInterpreter):
    """
    Diễn giải Nhật Chủ.
    """

    name = "DayMasterInterpreter"

    def __init__(
        self,
        template_root: Path,
        language: str = "vi",
    ) -> None:

        self.loader = TemplateLoader(
            template_root / language / "day_master"
        )

    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:

        result = InterpretationResult(
            interpreter=self.name
        )

        day_master = analysis.get("day_master")

        if not day_master:
            result.warnings.append(
                "Không tìm thấy Nhật Chủ."
            )
            return result

        template = self.loader.lookup(
            "day_master.json",
            day_master,
        )

        if template is None:
            result.warnings.append(
                f"Không có template cho {day_master}"
            )
            return result

        item = InterpretationItem(

            section="personality",

            code=template["code"],

            title=template["title"],

            content=template["content"],

            priority=template.get(
                "priority",
                90,
            ),

            score=template.get(
                "score",
                0,
            ),

            tags=template.get(
                "tags",
                [],
            ),

            references=[
                day_master
            ],
        )

        result.add(item)

        return result
