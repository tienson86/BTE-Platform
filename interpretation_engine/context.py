"""
interpretation_engine/context.py

Định nghĩa các cấu trúc dữ liệu dùng chung cho
Interpretation Engine.

Tất cả Interpreter đều phải trả về InterpretationItem.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InterpretationItem:
    """
    Một đoạn diễn giải độc lập.
    """

    section: str
    code: str

    title: str

    content: str

    priority: int = 50

    score: float = 0.0

    tags: list[str] = field(default_factory=list)

    references: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class InterpretationResult:
    """
    Kết quả của một Interpreter.
    """

    interpreter: str

    items: list[InterpretationItem] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def add(self, item: InterpretationItem) -> None:
        self.items.append(item)

    def extend(self, items: list[InterpretationItem]) -> None:
        self.items.extend(items)
